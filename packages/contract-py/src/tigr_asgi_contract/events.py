from ._enum_compat import StrEnum
from pydantic import BaseModel, Field


class TransportEventType(StrEnum):
    HTTP_REQUEST = 'http.request'
    HTTP_DISCONNECT = 'http.disconnect'
    HTTP_RESPONSE_START = 'http.response.start'
    HTTP_RESPONSE_BODY = 'http.response.body'
    HTTP_RESPONSE_PATHSEND = 'http.response.pathsend'
    WEBSOCKET_CONNECT = 'websocket.connect'
    WEBSOCKET_RECEIVE = 'websocket.receive'
    WEBSOCKET_DISCONNECT = 'websocket.disconnect'
    WEBSOCKET_ACCEPT = 'websocket.accept'
    WEBSOCKET_SEND = 'websocket.send'
    WEBSOCKET_CLOSE = 'websocket.close'
    WEBTRANSPORT_CONNECT = 'webtransport.connect'
    WEBTRANSPORT_ACCEPT = 'webtransport.accept'
    WEBTRANSPORT_STREAM_RECEIVE = 'webtransport.stream.receive'
    WEBTRANSPORT_STREAM_SEND = 'webtransport.stream.send'
    WEBTRANSPORT_STREAM_CLOSE = 'webtransport.stream.close'
    WEBTRANSPORT_STREAM_RESET = 'webtransport.stream.reset'
    WEBTRANSPORT_STREAM_STOP_SENDING = 'webtransport.stream.stop_sending'
    WEBTRANSPORT_DATAGRAM_RECEIVE = 'webtransport.datagram.receive'
    WEBTRANSPORT_DATAGRAM_SEND = 'webtransport.datagram.send'
    WEBTRANSPORT_DISCONNECT = 'webtransport.disconnect'
    WEBTRANSPORT_CLOSE = 'webtransport.close'
    STREAM_RESUME_REQUEST = 'stream.resume.request'
    STREAM_RESUME_ACCEPT = 'stream.resume.accept'
    STREAM_RESUME_REJECT = 'stream.resume.reject'
    LIFESPAN_STARTUP = 'lifespan.startup'
    LIFESPAN_STARTUP_COMPLETE = 'lifespan.startup.complete'
    LIFESPAN_STARTUP_FAILED = 'lifespan.startup.failed'
    LIFESPAN_SHUTDOWN = 'lifespan.shutdown'
    LIFESPAN_SHUTDOWN_COMPLETE = 'lifespan.shutdown.complete'
    LIFESPAN_SHUTDOWN_FAILED = 'lifespan.shutdown.failed'
    TRANSPORT_EMIT_COMPLETE = 'transport.emit.complete'
    TRANSPORT_EMIT_FAILED = 'transport.emit.failed'


class ContractEvent(BaseModel):
    type: TransportEventType
    message: str | None = None
    payload: dict = Field(default_factory=dict)
