import asyncio
import contextlib
import os

import aiohttp
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from loguru import logger
from sona.core.inferencer import InferencerBase
from sona.core.messages import Context
from sona.core.messages.result import Result
from sona.settings import settings

from .messages import RPCOfferRequest, SonaResponse
from .rpc.handlers import MediaInferencerHandler

try:
    from aiortc import (
        RTCConfiguration,
        RTCIceServer,
        RTCPeerConnection,
        RTCSessionDescription,
    )
    from fastapi import FastAPI, Request
    from fastapi.exceptions import RequestValidationError
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
except ImportError:
    pass


INFERENCER_CLASS = settings.SONA_INFERENCER_CLASS
STREAM_INFERENCER_CLASS = settings.SONA_STREAM_INFERENCER_CLASS
INFERENCER_PROCESS_LIMIT = settings.SONA_INFERENCER_PROCESS_LIMIT
STATIC_ROOT = os.path.dirname(__file__)

RTC_TURN_FDQN = settings.SONA_STREAM_RTC_TURN_FDQN
RTC_USER = settings.SONA_STREAM_RTC_USER
RTC_PASS = settings.SONA_STREAM_RTC_PASS

RTC_AUTH_URL = settings.SONA_STREAM_RTC_TURN_AUTH_URL


@contextlib.asynccontextmanager
async def lifespan(app):
    app.peers = set()
    app.handlers = set()
    if INFERENCER_CLASS:
        app.inferencer = InferencerBase.load_class(INFERENCER_CLASS)()
        app.inferencer.setup()
        app.inferencer.on_load()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, err: RequestValidationError):
    logger.warning(f"Client Error: {request}, {err.errors()}")
    resp = SonaResponse(code="400", message=str(err.errors()))
    return JSONResponse(status_code=400, content=resp.model_dump())


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, err: Exception):
    logger.exception(f"Server Error: {request}")
    resp = SonaResponse(code="500", message=str(err))
    return JSONResponse(status_code=500, content=resp.model_dump())


@app.get("/ping")
async def ping():
    return SonaResponse(message="pong")


if INFERENCER_CLASS:

    @app.post("/inference")
    async def inference(ctx: Context):
        inferencer: InferencerBase = app.inferencer
        loop = asyncio.get_running_loop()
        next_ctx: Context = await loop.run_in_executor(None, inferencer.on_context, ctx)
        if next_ctx.is_failed:
            raise Exception("Internal Server Error")
        return SonaResponse(result=list(next_ctx.results.values())[0])


if STREAM_INFERENCER_CLASS:
    app.mount("/static", StaticFiles(directory=f"{STATIC_ROOT}/static"), name="static")

    @app.post("/offer")
    async def offer(req: RPCOfferRequest):
        logger.info(f"Recive offer: {req}")
        if len(app.handlers) > INFERENCER_PROCESS_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=f"Too many inference sessions (sessions: {len(app.handlers)}, limit: {INFERENCER_PROCESS_LIMIT})",
            )

        offer = RTCSessionDescription(sdp=req.sdp, type=req.type)
        servers = [RTCIceServer("stun:stun.l.google:19302")]
        if RTC_AUTH_URL:
            async with aiohttp.request("GET", RTC_AUTH_URL) as resp:
                assert resp.status == 200
                result = await resp.json()
                servers += [
                    RTCIceServer(**ice_server) for ice_server in result["iceServers"]
                ]
        if RTC_TURN_FDQN:
            servers += [RTCIceServer(RTC_TURN_FDQN, RTC_USER, RTC_PASS)]
        peer = RTCPeerConnection(configuration=RTCConfiguration(servers))
        handler = MediaInferencerHandler()

        app.handlers.add(handler)
        app.peers.add(peer)

        @peer.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                if isinstance(message, str) and message.startswith("ping"):
                    channel.send("pong" + message[4:])

        @peer.on("connectionstatechange")
        async def on_connectionstatechange():
            logger.info(f"Connection state is {peer.connectionState}")
            if peer.connectionState in ["failed", "closed"]:
                await peer.close()
                app.peers.discard(peer)

        @peer.on("track")
        def on_track(track):
            logger.info(f"Track {track.kind} received")
            if track.kind == "audio":
                handler.addTrack(track, peer, req.options)
            elif track.kind == "video":
                peer.addTrack(track)

            @track.on("ended")
            async def on_ended():
                logger.info(f"Track {track.kind} ended")
                await handler.stop(track.id)
                app.handlers.discard(handler)

        await peer.setRemoteDescription(offer)
        answer = await peer.createAnswer()
        await peer.setLocalDescription(answer)
        await handler.start()

        return SonaResponse(
            result=Result(
                data={
                    "sdp": peer.localDescription.sdp,
                    "type": peer.localDescription.type,
                }
            )
        )
