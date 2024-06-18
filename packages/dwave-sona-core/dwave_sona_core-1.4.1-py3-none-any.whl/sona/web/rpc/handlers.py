import asyncio
import json

from loguru import logger
from sona.core.stream.inferencer import StreamInferencerBase
from sona.core.stream.messages.context import EvtType, StreamContext
from sona.settings import settings
from sona.web.rpc.tracks import AudioInferencerTrack

try:
    from aiortc import (
        MediaStreamTrack,
        RTCDataChannel,
        RTCPeerConnection,
        RTCSctpTransport,
    )
    from aiortc.mediastreams import MediaStreamError
except ImportError:
    pass

DEBUG = settings.SONA_DEBUG
STREAM_INFERENCER_CLASS = settings.SONA_STREAM_INFERENCER_CLASS


class MediaInferencerHandler:
    def __init__(self, inferencer_cls=STREAM_INFERENCER_CLASS) -> None:
        self.inferencer_cls = StreamInferencerBase.load_class(inferencer_cls)
        self.inferencers = {}
        self.tracks = []
        self.queue = asyncio.Queue()

    def addTrack(
        self, track: MediaStreamTrack, peer: RTCPeerConnection, options: dict = None
    ):
        options = options or {}
        inferencer: StreamInferencerBase = self.inferencer_cls(**options)
        inferencer.setup()
        inferencer.on_load()
        inferencer.on_reply = lambda ctx: self.queue.put_nowait((inferencer, ctx))
        inferencer.reply_channel = peer.createDataChannel(f"reply_{track.id}")
        inferencer.audio_track = AudioInferencerTrack()
        inferencer.session_param = options
        peer.addTrack(inferencer.audio_track)

        self.tracks += [track]
        self.inferencers[track.id] = inferencer

    async def start(self):
        self.task = asyncio.create_task(self.on_reply())
        for track in self.tracks:
            inferencer = self.inferencers[track.id]
            inferencer.task = asyncio.create_task(self.run_track(track, inferencer))

    async def run_track(
        self, track: MediaStreamTrack, inferencer: StreamInferencerBase
    ):
        while True:
            try:
                headers = inferencer.session_param
                frame = await track.recv()
                if DEBUG:
                    logger.info(f"{headers}, {frame}")
                ctx = StreamContext(
                    event_type=EvtType.AV_AUDIO, payload=frame, header=headers
                )
                inferencer.on_context(ctx)
            except MediaStreamError:
                logger.warning("MediaStreamError")
                return
            except Exception as e:
                logger.exception(e)
                raise

    async def stop(self, track_id):
        inferencer = self.inferencers[track_id]
        inferencer.on_stop()

    async def stop_all(self):
        for track_id in self.inferencers:
            self.stop(track_id)

    async def on_reply(self):
        while True:
            inferencer, ctx = await self.queue.get()
            _type = ctx.event_type
            if _type == EvtType.AV_AUDIO.value:
                inferencer.audio_track.reply(ctx.payload)
            elif _type == EvtType.DICT.value:
                datachannel: RTCDataChannel = inferencer.reply_channel
                if datachannel.readyState not in ["closing", "closed"]:
                    datachannel.send(json.dumps(ctx.payload))
                    transport: RTCSctpTransport = datachannel.transport
                    await transport._data_channel_flush()
                    await transport._transmit()
            else:
                raise Exception(
                    "Only support AVAudioStreamData / DictStreamData for now"
                )
