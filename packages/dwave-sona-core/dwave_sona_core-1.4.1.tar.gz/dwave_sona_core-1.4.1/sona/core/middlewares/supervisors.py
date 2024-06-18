import datetime
from pathlib import Path
import threading
import boto3
from loguru import logger
from sona.core.messages.context import Context
from sona.core.messages.file import File
from sona.core.messages.job import Job
from sona.core.messages.result import Result
from sona.core.messages.state import State
from sona.core.stream.messages.context import EvtType, StreamContext
from sona.settings import settings
import smart_open
import av
import queue

from .base import MiddlewareBase

try:
    from confluent_kafka import Producer
except ImportError:
    Producer = None


MIN_PART_SIZE = 5 * 1024**2
SUPERVISOR_TOPICS = settings.SONA_MIDDLEWARE_SUPERVISOR_TOPICS
KAFKA_SETTING = settings.SONA_MIDDLEWARE_SUPERVISOR_KAFKA_SETTING
SQS_SETTING = settings.SONA_MIDDLEWARE_SUPERVISOR_SQS_SETTING
S3_SETTING = settings.SONA_MIDDLEWARE_SUPERVISOR_S3_SETTING
S3_BUCKET = settings.SONA_MIDDLEWARE_SUPERVISOR_S3_BUCKET


class KafkaSupervisor(MiddlewareBase):
    def __init__(self, configs=KAFKA_SETTING):
        if Producer:
            self.producer = Producer(configs)
        else:
            logger.warning(
                "Missing SONA_MIDDLEWARE_SUPERVISOR_KAFKA_SETTING, KafkaSupervisor will be ignored."
            )
            self.producer = None

    def on_context(self, ctx: Context, on_context):
        for topic in ctx.supervisors:
            self._emit(topic, ctx.to_message())
        next_ctx: Context = on_context(ctx)
        for topic in next_ctx.supervisors:
            self._emit(topic, next_ctx.to_message())
        return next_ctx

    def _emit(self, topic, message):
        try:
            if self.producer:
                self.producer.poll(0)
                self.producer.produce(
                    topic, message.encode("utf-8"), callback=self.__delivery_report
                )
                self.producer.flush()
        except Exception as e:
            logger.warning(f"Supervisor emit error occur {e}, ignore message {message}")

    def __delivery_report(self, err, msg):
        if err:
            raise Exception(msg.error())


class SQSSupervisor(MiddlewareBase):
    def __init__(self, setting=SQS_SETTING):
        self.sqs = boto3.resource("sqs", **setting)

    def on_context(self, ctx: Context, on_context):
        for topic in ctx.supervisors:
            self._emit(topic, ctx.to_message())
        next_ctx: Context = on_context(ctx)
        for topic in next_ctx.supervisors:
            self._emit(topic, next_ctx.to_message())
        return next_ctx

    def _emit(self, topic, message):
        try:
            queue = self.sqs.get_queue_by_name(QueueName=topic)
            queue.send_message(MessageBody=message)
        except Exception as e:
            logger.warning(f"Supervisor emit error occur {e}, ignore message {message}")


class SQSStreamSupervisor(MiddlewareBase):
    def __init__(self):
        self.sqs = boto3.resource("sqs", **SQS_SETTING)
        self.s3 = boto3.client("s3", **S3_SETTING)
        self.queue = queue.Queue()

    def on_load(self, on_load):
        self.worker = threading.Thread(target=self.load_worker, daemon=True)
        self.worker.start()
        return on_load()

    def on_context(self, stream_ctx: StreamContext, on_context):
        self.queue.put_nowait(stream_ctx)
        return on_context(stream_ctx)

    def on_stop(self, on_stop):
        self.queue.put_nowait(None)
        return on_stop()

    def load_worker(self):
        # Init
        today = datetime.date.today().strftime("%Y%m%d")
        self.ctx = None

        # Recv frames
        while True:
            stream_ctx = self.queue.get()
            if stream_ctx is None:
                break

            if not self.ctx:
                logger.info(f"create context: {stream_ctx}")
                self.ctx = Context(
                    application=stream_ctx.header.get("application", "common")
                    or "common",  # Avoid pass `None` value from gateway
                    supervisors=SUPERVISOR_TOPICS,
                    jobs=[Job(name="stream_job", params=stream_ctx.header)],
                )
                self.ctx_state = State.start("stream_job")

                self.total_parts = 0
                self.filepath = f"s3://{S3_BUCKET}/storage/{self.ctx.application}/{today}/{self.ctx.id}.flac"
                self.s3file = smart_open.open(
                    self.filepath,
                    "wb",
                    transport_params={
                        "client": self.s3,
                        "min_part_size": MIN_PART_SIZE,
                    },
                )

                self.out_container = av.open(self.s3file, "w")
                self.out_stream = self.out_container.add_stream(
                    codec_name="flac", rate=48000
                )

            self._process_context(stream_ctx)
            self.queue.task_done()

        # End of work
        for packet in self.out_stream.encode():
            self.out_container.mux(packet)
        self.s3file.close()
        self.ctx_state.complete()
        self.ctx = self.ctx.mutate(
            results={
                "stream_job": Result(files=[File(label="result", path=self.filepath)])
            },
            states=[self.ctx_state],
        )
        for topic in self.ctx.supervisors:
            self._emit(topic, self.ctx.to_message())

    def _process_context(self, stream_ctx: StreamContext):
        if stream_ctx.event_type == EvtType.AV_AUDIO.value:
            self._process_audio(stream_ctx)

    def _process_audio(self, stream_ctx: StreamContext):
        frame = stream_ctx.payload
        frame.pts = None
        for packet in self.out_stream.encode(frame):
            self.out_container.mux(packet)

        if self.s3file._total_parts > self.total_parts:
            self.ctx = self.ctx.mutate(
                results={
                    "stream_job": Result(
                        data={
                            "Bucket": self.s3file._bucket,
                            "Key": self.s3file._key,
                            "UploadId": self.s3file._upload_id,
                            "MultipartUpload": {"Parts": self.s3file._parts},
                        }
                    )
                }
            )
            for topic in self.ctx.supervisors:
                self._emit(topic, self.ctx.to_message())
            self.total_parts = self.s3file._total_parts

    def _emit(self, topic, message):
        try:
            queue = self.sqs.get_queue_by_name(QueueName=topic)
            queue.send_message(MessageBody=message)
        except Exception as e:
            logger.warning(f"Supervisor emit error occur {e}, ignore message {message}")
