pub const CHANNELS: &[&str] = &["receive", "send"];

pub const DIRECTIONS: &[&str] = &["client_to_server", "server_to_client", "app_to_server", "server_to_app", "system"];

pub const FRAMINGS: &[&str] = &["json", "jsonrpc", "ndjson", "sse", "text", "bytes", "binary"];

pub const EVENT_CLASSIFICATIONS_JSON: &str = r#"[
  {
    "event": "http.request",
    "channel": "receive",
    "scope_type": "http",
    "binding": "rest",
    "family": "request",
    "exchange": "unary",
    "direction": "client_to_server",
    "allowed_framings": [
      "json",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": []
  },
  {
    "event": "http.request",
    "channel": "receive",
    "scope_type": "http",
    "binding": "jsonrpc",
    "family": "request",
    "exchange": "unary",
    "direction": "client_to_server",
    "allowed_framings": [
      "jsonrpc"
    ],
    "required_payload_fields": []
  },
  {
    "event": "http.request",
    "channel": "receive",
    "scope_type": "http",
    "binding": "http.stream",
    "family": "stream",
    "exchange": "client_stream",
    "direction": "client_to_server",
    "allowed_framings": [
      "json",
      "ndjson",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": []
  },
  {
    "event": "http.disconnect",
    "channel": "receive",
    "scope_type": "http",
    "binding": "rest",
    "family": "request",
    "exchange": "unary",
    "direction": "client_to_server",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "http.response.start",
    "channel": "send",
    "scope_type": "http",
    "binding": "rest",
    "family": "request",
    "exchange": "unary",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "http.response.start",
    "channel": "send",
    "scope_type": "http",
    "binding": "jsonrpc",
    "family": "request",
    "exchange": "unary",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "http.response.body",
    "channel": "send",
    "scope_type": "http",
    "binding": "rest",
    "family": "request",
    "exchange": "unary",
    "direction": "server_to_client",
    "allowed_framings": [
      "json",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": []
  },
  {
    "event": "http.response.body",
    "channel": "send",
    "scope_type": "http",
    "binding": "jsonrpc",
    "family": "request",
    "exchange": "unary",
    "direction": "server_to_client",
    "allowed_framings": [
      "jsonrpc"
    ],
    "required_payload_fields": []
  },
  {
    "event": "http.response.body",
    "channel": "send",
    "scope_type": "http",
    "binding": "http.stream",
    "family": "stream",
    "exchange": "server_stream",
    "direction": "server_to_client",
    "allowed_framings": [
      "json",
      "ndjson",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": []
  },
  {
    "event": "http.response.body",
    "channel": "send",
    "scope_type": "http",
    "binding": "sse",
    "family": "stream",
    "exchange": "server_stream",
    "direction": "server_to_client",
    "allowed_framings": [
      "sse"
    ],
    "required_payload_fields": []
  },
  {
    "event": "http.response.pathsend",
    "channel": "send",
    "scope_type": "http",
    "binding": "http.stream",
    "family": "request",
    "exchange": "unary",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": [
      "path"
    ]
  },
  {
    "event": "websocket.connect",
    "channel": "receive",
    "scope_type": "websocket",
    "binding": "websocket",
    "family": "session",
    "exchange": "unary",
    "direction": "client_to_server",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "websocket.receive",
    "channel": "receive",
    "scope_type": "websocket",
    "binding": "websocket",
    "family": "message",
    "exchange": "duplex",
    "direction": "client_to_server",
    "allowed_framings": [
      "json",
      "jsonrpc",
      "ndjson",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": []
  },
  {
    "event": "websocket.disconnect",
    "channel": "receive",
    "scope_type": "websocket",
    "binding": "websocket",
    "family": "session",
    "exchange": "unary",
    "direction": "client_to_server",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "websocket.accept",
    "channel": "send",
    "scope_type": "websocket",
    "binding": "websocket",
    "family": "session",
    "exchange": "unary",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "websocket.send",
    "channel": "send",
    "scope_type": "websocket",
    "binding": "websocket",
    "family": "message",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [
      "json",
      "jsonrpc",
      "ndjson",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": []
  },
  {
    "event": "websocket.close",
    "channel": "send",
    "scope_type": "websocket",
    "binding": "websocket",
    "family": "session",
    "exchange": "unary",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "webtransport.connect",
    "channel": "receive",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "session",
    "exchange": "unary",
    "direction": "client_to_server",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "webtransport.accept",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "session",
    "exchange": "unary",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "webtransport.stream.receive",
    "channel": "receive",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "duplex",
    "direction": "client_to_server",
    "allowed_framings": [
      "json",
      "jsonrpc",
      "ndjson",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": [
      "stream_id",
      "stream_direction"
    ],
    "capability_gates": [
      "supports_bidi_streams"
    ],
    "stream_direction": "bidi"
  },
  {
    "event": "webtransport.stream.receive",
    "channel": "receive",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "client_stream",
    "direction": "client_to_server",
    "allowed_framings": [
      "json",
      "jsonrpc",
      "ndjson",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": [
      "stream_id",
      "stream_direction"
    ],
    "capability_gates": [
      "supports_uni_streams"
    ],
    "stream_direction": "client_to_server"
  },
  {
    "event": "webtransport.stream.send",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [
      "json",
      "jsonrpc",
      "ndjson",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": [
      "stream_id",
      "stream_direction"
    ],
    "capability_gates": [
      "supports_bidi_streams"
    ],
    "stream_direction": "bidi"
  },
  {
    "event": "webtransport.stream.send",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "server_stream",
    "direction": "server_to_client",
    "allowed_framings": [
      "json",
      "ndjson",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": [
      "stream_id",
      "stream_direction"
    ],
    "capability_gates": [
      "supports_uni_streams"
    ],
    "stream_direction": "server_to_client"
  },
  {
    "event": "webtransport.stream.close",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": [
      "stream_id"
    ]
  },
  {
    "event": "webtransport.stream.reset",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": [
      "stream_id"
    ]
  },
  {
    "event": "webtransport.stream.stop_sending",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": [
      "stream_id"
    ]
  },
  {
    "event": "stream.resume.request",
    "channel": "receive",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "duplex",
    "direction": "client_to_server",
    "allowed_framings": [],
    "required_payload_fields": [
      "resume_token",
      "client_id",
      "session_id",
      "stream_id",
      "binding"
    ]
  },
  {
    "event": "stream.resume.accept",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": [
      "resume_token",
      "client_id",
      "session_id",
      "stream_id",
      "binding",
      "accepted_offset"
    ]
  },
  {
    "event": "stream.resume.reject",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "stream",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": [
      "resume_token",
      "client_id",
      "session_id",
      "stream_id",
      "binding",
      "reason"
    ]
  },
  {
    "event": "webtransport.datagram.receive",
    "channel": "receive",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "datagram",
    "exchange": "duplex",
    "direction": "client_to_server",
    "allowed_framings": [
      "json",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": [
      "datagram_id"
    ],
    "capability_gates": [
      "supports_datagrams"
    ]
  },
  {
    "event": "webtransport.datagram.send",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "datagram",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [
      "json",
      "text",
      "bytes",
      "binary"
    ],
    "required_payload_fields": [
      "datagram_id"
    ],
    "capability_gates": [
      "supports_datagrams"
    ]
  },
  {
    "event": "webtransport.disconnect",
    "channel": "receive",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "session",
    "exchange": "unary",
    "direction": "client_to_server",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "webtransport.close",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "session",
    "exchange": "unary",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "lifespan.startup",
    "channel": "receive",
    "scope_type": "lifespan",
    "binding": "lifespan",
    "family": "lifespan",
    "exchange": "unary",
    "direction": "system",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "lifespan.shutdown",
    "channel": "receive",
    "scope_type": "lifespan",
    "binding": "lifespan",
    "family": "lifespan",
    "exchange": "unary",
    "direction": "system",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "lifespan.startup.complete",
    "channel": "send",
    "scope_type": "lifespan",
    "binding": "lifespan",
    "family": "lifespan",
    "exchange": "unary",
    "direction": "system",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "lifespan.startup.failed",
    "channel": "send",
    "scope_type": "lifespan",
    "binding": "lifespan",
    "family": "lifespan",
    "exchange": "unary",
    "direction": "system",
    "allowed_framings": [],
    "required_payload_fields": [
      "message"
    ]
  },
  {
    "event": "lifespan.shutdown.complete",
    "channel": "send",
    "scope_type": "lifespan",
    "binding": "lifespan",
    "family": "lifespan",
    "exchange": "unary",
    "direction": "system",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "lifespan.shutdown.failed",
    "channel": "send",
    "scope_type": "lifespan",
    "binding": "lifespan",
    "family": "lifespan",
    "exchange": "unary",
    "direction": "system",
    "allowed_framings": [],
    "required_payload_fields": [
      "message"
    ]
  },
  {
    "event": "transport.emit.complete",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "datagram",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": []
  },
  {
    "event": "transport.emit.failed",
    "channel": "send",
    "scope_type": "webtransport",
    "binding": "webtransport",
    "family": "datagram",
    "exchange": "duplex",
    "direction": "server_to_client",
    "allowed_framings": [],
    "required_payload_fields": [
      "message"
    ]
  }
]"#;

pub const REQUEST_SUBEVENTS: &[&str] = &["request.open", "request.body_in", "request.chunk_in", "request.dispatch", "request.close", "request.disconnect", "response.open", "response.body_out", "response.chunk_out", "response.finalize", "response.emit_complete"];

pub const PROTOCOLS: &[(&str, &str, &str, bool, &str)] = &[
    ("http.rest", "rest", "http", false, "http"),
    ("https.rest", "rest", "http", true, "http"),
    ("http.jsonrpc", "jsonrpc", "http", false, "http"),
    ("https.jsonrpc", "jsonrpc", "http", true, "http"),
    ("http.stream", "http.stream", "http", false, "http"),
    ("https.stream", "http.stream", "http", true, "http"),
    ("http.sse", "sse", "http", false, "http"),
    ("https.sse", "sse", "http", true, "http"),
    ("ws", "websocket", "websocket", false, "websocket"),
    ("wss", "websocket", "websocket", true, "websocket"),
    ("webtransport", "webtransport", "webtransport", true, "webtransport"),
    ("asgi.pathsend", "http.stream", "http", false, "http"),
    ("lifespan", "lifespan", "lifespan", false, "lifespan"),
];

pub const AUTOMATA_TRANSITIONS: &[(&str, &str, &str, &str)] = &[
    ("request", "idle", "request.open", "open"),
    ("request", "open", "request.body_in", "open"),
    ("request", "open", "request.chunk_in", "open"),
    ("request", "open", "request.close", "body_closed"),
    ("request", "open", "request.dispatch", "dispatched"),
    ("request", "body_closed", "request.dispatch", "dispatched"),
    ("request", "dispatched", "response.open", "responding"),
    ("request", "responding", "response.body_out", "responding"),
    ("request", "responding", "response.chunk_out", "responding"),
    ("request", "responding", "response.emit_complete", "completing"),
    ("request", "completing", "response.finalize", "closed"),
    ("request", "open", "request.disconnect", "disconnected"),
    ("request", "body_closed", "request.disconnect", "disconnected"),
    ("session", "idle", "session.open", "open"),
    ("session", "open", "session.accept", "accepted"),
    ("session", "open", "session.reject", "rejected"),
    ("session", "open", "session.disconnect", "disconnected"),
    ("session", "accepted", "session.ready", "ready"),
    ("session", "accepted", "session.disconnect", "disconnected"),
    ("session", "ready", "session.heartbeat", "ready"),
    ("session", "ready", "session.sync", "ready"),
    ("session", "ready", "session.emit_complete", "ready"),
    ("session", "ready", "session.close", "closed"),
    ("session", "ready", "session.disconnect", "disconnected"),
    ("message", "idle", "message.in", "received"),
    ("message", "received", "message.decode", "decoded"),
    ("message", "received", "message.decode_failed", "failed"),
    ("message", "decoded", "message.handle", "handled"),
    ("message", "decoded", "message.handle_failed", "failed"),
    ("message", "handled", "message.out", "emitted"),
    ("message", "emitted", "message.emit_complete", "complete"),
    ("message", "emitted", "message.emit_failed", "failed"),
    ("message", "complete", "message.replay", "emitted"),
    ("message", "complete", "message.snapshot", "complete"),
    ("stream", "idle", "stream.open", "open"),
    ("stream", "open", "stream.chunk_in", "open"),
    ("stream", "open", "stream.chunk_out", "open"),
    ("stream", "open", "stream.flush", "open"),
    ("stream", "open", "stream.finalize", "finalizing"),
    ("stream", "finalizing", "stream.emit_complete", "closed"),
    ("stream", "open", "stream.close", "closed"),
    ("stream", "open", "stream.reset", "reset"),
    ("stream", "open", "stream.stop_sending", "stopped"),
    ("stream", "finalizing", "stream.reset", "reset"),
    ("stream", "finalizing", "stream.stop_sending", "stopped"),
    ("datagram", "idle", "datagram.in", "received"),
    ("datagram", "received", "datagram.handle", "handled"),
    ("datagram", "handled", "datagram.out", "emitted"),
    ("datagram", "emitted", "datagram.emit_complete", "complete"),
    ("datagram", "emitted", "datagram.emit_failed", "failed"),
    ("lifespan", "idle", "lifespan.startup", "starting"),
    ("lifespan", "starting", "lifespan.startup_complete", "startup_complete"),
    ("lifespan", "starting", "lifespan.startup_failed", "startup_failed"),
    ("lifespan", "startup_complete", "lifespan.shutdown", "shutting_down"),
    ("lifespan", "idle", "lifespan.shutdown", "shutting_down"),
    ("lifespan", "shutting_down", "lifespan.shutdown_complete", "shutdown_complete"),
    ("lifespan", "shutting_down", "lifespan.shutdown_failed", "shutdown_failed"),
];
