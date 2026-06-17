use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum TransportEventType {
    #[serde(rename = "http.request")]
    HttpRequest,
    #[serde(rename = "http.disconnect")]
    HttpDisconnect,
    #[serde(rename = "http.response.start")]
    HttpResponseStart,
    #[serde(rename = "http.response.body")]
    HttpResponseBody,
    #[serde(rename = "http.response.pathsend")]
    HttpResponsePathsend,
    #[serde(rename = "websocket.connect")]
    WebsocketConnect,
    #[serde(rename = "websocket.receive")]
    WebsocketReceive,
    #[serde(rename = "websocket.disconnect")]
    WebsocketDisconnect,
    #[serde(rename = "websocket.accept")]
    WebsocketAccept,
    #[serde(rename = "websocket.send")]
    WebsocketSend,
    #[serde(rename = "websocket.close")]
    WebsocketClose,
    #[serde(rename = "webtransport.connect")]
    WebtransportConnect,
    #[serde(rename = "webtransport.accept")]
    WebtransportAccept,
    #[serde(rename = "webtransport.stream.receive")]
    WebtransportStreamReceive,
    #[serde(rename = "webtransport.stream.send")]
    WebtransportStreamSend,
    #[serde(rename = "webtransport.stream.close")]
    WebtransportStreamClose,
    #[serde(rename = "webtransport.stream.reset")]
    WebtransportStreamReset,
    #[serde(rename = "webtransport.stream.stop_sending")]
    WebtransportStreamStopSending,
    #[serde(rename = "webtransport.datagram.receive")]
    WebtransportDatagramReceive,
    #[serde(rename = "webtransport.datagram.send")]
    WebtransportDatagramSend,
    #[serde(rename = "webtransport.disconnect")]
    WebtransportDisconnect,
    #[serde(rename = "webtransport.close")]
    WebtransportClose,
    #[serde(rename = "stream.resume.request")]
    StreamResumeRequest,
    #[serde(rename = "stream.resume.accept")]
    StreamResumeAccept,
    #[serde(rename = "stream.resume.reject")]
    StreamResumeReject,
    #[serde(rename = "lifespan.startup")]
    LifespanStartup,
    #[serde(rename = "lifespan.startup.complete")]
    LifespanStartupComplete,
    #[serde(rename = "lifespan.startup.failed")]
    LifespanStartupFailed,
    #[serde(rename = "lifespan.shutdown")]
    LifespanShutdown,
    #[serde(rename = "lifespan.shutdown.complete")]
    LifespanShutdownComplete,
    #[serde(rename = "lifespan.shutdown.failed")]
    LifespanShutdownFailed,
    #[serde(rename = "transport.emit.complete")]
    TransportEmitComplete,
    #[serde(rename = "transport.emit.failed")]
    TransportEmitFailed,
}

impl Default for TransportEventType {
    fn default() -> Self {
        Self::HttpRequest
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContractEvent {
    pub r#type: TransportEventType,
    pub message: Option<String>,
    pub payload: serde_json::Map<String, serde_json::Value>,
}
