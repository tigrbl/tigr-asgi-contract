export const BINDING_FAMILY_MATRIX = {
  "rest": {
    "request": "R",
    "session": "F",
    "message": "F",
    "stream": "O",
    "datagram": "F",
    "lifespan": "F"
  },
  "jsonrpc": {
    "request": "R",
    "session": "F",
    "message": "F",
    "stream": "O",
    "datagram": "F",
    "lifespan": "F"
  },
  "http.stream": {
    "request": "R",
    "session": "F",
    "message": "F",
    "stream": "R",
    "datagram": "F",
    "lifespan": "F"
  },
  "sse": {
    "request": "R",
    "session": "R",
    "message": "R",
    "stream": "R",
    "datagram": "F",
    "lifespan": "F"
  },
  "websocket": {
    "request": "F",
    "session": "R",
    "message": "R",
    "stream": "F",
    "datagram": "F",
    "lifespan": "F"
  },
  "webtransport": {
    "request": "F",
    "session": "R",
    "message": "F",
    "stream": "R",
    "datagram": "R",
    "lifespan": "F"
  },
  "lifespan": {
    "request": "F",
    "session": "F",
    "message": "F",
    "stream": "F",
    "datagram": "F",
    "lifespan": "R"
  }
} as const;

export const FAMILY_SUBEVENT_MATRIX = {
  "request": {
    "request.open": "R",
    "request.body_in": "R",
    "request.chunk_in": "R",
    "request.dispatch": "R",
    "request.close": "R",
    "request.disconnect": "R",
    "response.open": "R",
    "response.body_out": "R",
    "response.chunk_out": "R",
    "response.finalize": "R",
    "response.emit_complete": "R"
  },
  "session": {
    "session.open": "R",
    "session.accept": "R",
    "session.reject": "R",
    "session.ready": "R",
    "session.heartbeat": "R",
    "session.sync": "R",
    "session.close": "R",
    "session.disconnect": "R",
    "session.emit_complete": "R"
  },
  "message": {
    "message.in": "R",
    "message.decode": "R",
    "message.decode_failed": "R",
    "message.handle": "R",
    "message.handle_failed": "R",
    "message.out": "R",
    "message.replay": "R",
    "message.snapshot": "R",
    "message.emit_complete": "R",
    "message.emit_failed": "R"
  },
  "stream": {
    "stream.open": "R",
    "stream.chunk_in": "R",
    "stream.chunk_out": "R",
    "stream.flush": "R",
    "stream.finalize": "R",
    "stream.reset": "R",
    "stream.stop_sending": "R",
    "stream.close": "R",
    "stream.emit_complete": "R"
  },
  "datagram": {
    "datagram.in": "R",
    "datagram.handle": "R",
    "datagram.out": "R",
    "datagram.emit_complete": "R",
    "datagram.emit_failed": "R"
  },
  "lifespan": {
    "lifespan.startup": "R",
    "lifespan.startup_complete": "R",
    "lifespan.startup_failed": "R",
    "lifespan.shutdown": "R",
    "lifespan.shutdown_complete": "R",
    "lifespan.shutdown_failed": "R"
  }
} as const;

export const BINDING_SUBEVENT_MATRIX = {
  "rest": {
    "request.open": "R",
    "request.body_in": "R",
    "request.chunk_in": "F",
    "request.dispatch": "D",
    "request.close": "R",
    "request.disconnect": "O",
    "response.open": "R",
    "response.body_out": "R",
    "response.chunk_out": "F",
    "response.finalize": "O",
    "response.emit_complete": "R",
    "session.open": "F",
    "session.accept": "F",
    "session.reject": "F",
    "session.ready": "F",
    "session.heartbeat": "F",
    "session.sync": "F",
    "session.close": "F",
    "session.disconnect": "F",
    "session.emit_complete": "F",
    "message.in": "F",
    "message.decode": "F",
    "message.decode_failed": "F",
    "message.handle": "F",
    "message.handle_failed": "F",
    "message.out": "F",
    "message.replay": "F",
    "message.snapshot": "F",
    "message.emit_complete": "F",
    "message.emit_failed": "F",
    "stream.open": "O",
    "stream.chunk_in": "O",
    "stream.chunk_out": "O",
    "stream.flush": "F",
    "stream.finalize": "O",
    "stream.reset": "F",
    "stream.stop_sending": "F",
    "stream.close": "O",
    "stream.emit_complete": "O",
    "datagram.in": "F",
    "datagram.handle": "F",
    "datagram.out": "F",
    "datagram.emit_complete": "F",
    "datagram.emit_failed": "F",
    "lifespan.startup": "F",
    "lifespan.startup_complete": "F",
    "lifespan.startup_failed": "F",
    "lifespan.shutdown": "F",
    "lifespan.shutdown_complete": "F",
    "lifespan.shutdown_failed": "F"
  },
  "jsonrpc": {
    "request.open": "R",
    "request.body_in": "R",
    "request.chunk_in": "F",
    "request.dispatch": "D",
    "request.close": "R",
    "request.disconnect": "O",
    "response.open": "R",
    "response.body_out": "R",
    "response.chunk_out": "F",
    "response.finalize": "O",
    "response.emit_complete": "R",
    "session.open": "F",
    "session.accept": "F",
    "session.reject": "F",
    "session.ready": "F",
    "session.heartbeat": "F",
    "session.sync": "F",
    "session.close": "F",
    "session.disconnect": "F",
    "session.emit_complete": "F",
    "message.in": "F",
    "message.decode": "D",
    "message.decode_failed": "D",
    "message.handle": "F",
    "message.handle_failed": "F",
    "message.out": "F",
    "message.replay": "F",
    "message.snapshot": "F",
    "message.emit_complete": "F",
    "message.emit_failed": "F",
    "stream.open": "O",
    "stream.chunk_in": "O",
    "stream.chunk_out": "O",
    "stream.flush": "F",
    "stream.finalize": "O",
    "stream.reset": "F",
    "stream.stop_sending": "F",
    "stream.close": "O",
    "stream.emit_complete": "O",
    "datagram.in": "F",
    "datagram.handle": "F",
    "datagram.out": "F",
    "datagram.emit_complete": "F",
    "datagram.emit_failed": "F",
    "lifespan.startup": "F",
    "lifespan.startup_complete": "F",
    "lifespan.startup_failed": "F",
    "lifespan.shutdown": "F",
    "lifespan.shutdown_complete": "F",
    "lifespan.shutdown_failed": "F"
  },
  "http.stream": {
    "request.open": "R",
    "request.body_in": "O",
    "request.chunk_in": "D",
    "request.dispatch": "D",
    "request.close": "R",
    "request.disconnect": "O",
    "response.open": "R",
    "response.body_out": "O",
    "response.chunk_out": "D",
    "response.finalize": "O",
    "response.emit_complete": "R",
    "session.open": "F",
    "session.accept": "F",
    "session.reject": "F",
    "session.ready": "F",
    "session.heartbeat": "F",
    "session.sync": "F",
    "session.close": "F",
    "session.disconnect": "F",
    "session.emit_complete": "F",
    "message.in": "F",
    "message.decode": "F",
    "message.decode_failed": "F",
    "message.handle": "F",
    "message.handle_failed": "F",
    "message.out": "F",
    "message.replay": "F",
    "message.snapshot": "F",
    "message.emit_complete": "F",
    "message.emit_failed": "F",
    "stream.open": "R",
    "stream.chunk_in": "R",
    "stream.chunk_out": "R",
    "stream.flush": "O",
    "stream.finalize": "R",
    "stream.reset": "O",
    "stream.stop_sending": "F",
    "stream.close": "R",
    "stream.emit_complete": "R",
    "datagram.in": "F",
    "datagram.handle": "F",
    "datagram.out": "F",
    "datagram.emit_complete": "F",
    "datagram.emit_failed": "F",
    "lifespan.startup": "F",
    "lifespan.startup_complete": "F",
    "lifespan.startup_failed": "F",
    "lifespan.shutdown": "F",
    "lifespan.shutdown_complete": "F",
    "lifespan.shutdown_failed": "F"
  },
  "sse": {
    "request.open": "R",
    "request.body_in": "O",
    "request.chunk_in": "F",
    "request.dispatch": "D",
    "request.close": "R",
    "request.disconnect": "O",
    "response.open": "O",
    "response.body_out": "F",
    "response.chunk_out": "D",
    "response.finalize": "O",
    "response.emit_complete": "R",
    "session.open": "R",
    "session.accept": "R",
    "session.reject": "F",
    "session.ready": "R",
    "session.heartbeat": "O",
    "session.sync": "O",
    "session.close": "R",
    "session.disconnect": "O",
    "session.emit_complete": "O",
    "message.in": "F",
    "message.decode": "F",
    "message.decode_failed": "F",
    "message.handle": "F",
    "message.handle_failed": "F",
    "message.out": "R",
    "message.replay": "O",
    "message.snapshot": "O",
    "message.emit_complete": "R",
    "message.emit_failed": "O",
    "stream.open": "R",
    "stream.chunk_in": "F",
    "stream.chunk_out": "R",
    "stream.flush": "O",
    "stream.finalize": "O",
    "stream.reset": "O",
    "stream.stop_sending": "F",
    "stream.close": "R",
    "stream.emit_complete": "R",
    "datagram.in": "F",
    "datagram.handle": "F",
    "datagram.out": "F",
    "datagram.emit_complete": "F",
    "datagram.emit_failed": "F",
    "lifespan.startup": "F",
    "lifespan.startup_complete": "F",
    "lifespan.startup_failed": "F",
    "lifespan.shutdown": "F",
    "lifespan.shutdown_complete": "F",
    "lifespan.shutdown_failed": "F"
  },
  "websocket": {
    "request.open": "F",
    "request.body_in": "F",
    "request.chunk_in": "F",
    "request.dispatch": "F",
    "request.close": "F",
    "request.disconnect": "F",
    "response.open": "F",
    "response.body_out": "F",
    "response.chunk_out": "F",
    "response.finalize": "F",
    "response.emit_complete": "F",
    "session.open": "R",
    "session.accept": "R",
    "session.reject": "O",
    "session.ready": "R",
    "session.heartbeat": "O",
    "session.sync": "O",
    "session.close": "R",
    "session.disconnect": "O",
    "session.emit_complete": "O",
    "message.in": "R",
    "message.decode": "O",
    "message.decode_failed": "O",
    "message.handle": "R",
    "message.handle_failed": "O",
    "message.out": "R",
    "message.replay": "O",
    "message.snapshot": "O",
    "message.emit_complete": "R",
    "message.emit_failed": "O",
    "stream.open": "F",
    "stream.chunk_in": "F",
    "stream.chunk_out": "F",
    "stream.flush": "F",
    "stream.finalize": "F",
    "stream.reset": "F",
    "stream.stop_sending": "F",
    "stream.close": "F",
    "stream.emit_complete": "F",
    "datagram.in": "F",
    "datagram.handle": "F",
    "datagram.out": "F",
    "datagram.emit_complete": "F",
    "datagram.emit_failed": "F",
    "lifespan.startup": "F",
    "lifespan.startup_complete": "F",
    "lifespan.startup_failed": "F",
    "lifespan.shutdown": "F",
    "lifespan.shutdown_complete": "F",
    "lifespan.shutdown_failed": "F"
  },
  "webtransport": {
    "request.open": "F",
    "request.body_in": "F",
    "request.chunk_in": "F",
    "request.dispatch": "F",
    "request.close": "F",
    "request.disconnect": "F",
    "response.open": "F",
    "response.body_out": "F",
    "response.chunk_out": "F",
    "response.finalize": "F",
    "response.emit_complete": "F",
    "session.open": "R",
    "session.accept": "R",
    "session.reject": "O",
    "session.ready": "R",
    "session.heartbeat": "O",
    "session.sync": "O",
    "session.close": "R",
    "session.disconnect": "O",
    "session.emit_complete": "O",
    "message.in": "F",
    "message.decode": "F",
    "message.decode_failed": "F",
    "message.handle": "F",
    "message.handle_failed": "F",
    "message.out": "F",
    "message.replay": "F",
    "message.snapshot": "F",
    "message.emit_complete": "F",
    "message.emit_failed": "F",
    "stream.open": "R",
    "stream.chunk_in": "R",
    "stream.chunk_out": "R",
    "stream.flush": "O",
    "stream.finalize": "R",
    "stream.reset": "O",
    "stream.stop_sending": "O",
    "stream.close": "R",
    "stream.emit_complete": "R",
    "datagram.in": "R",
    "datagram.handle": "R",
    "datagram.out": "R",
    "datagram.emit_complete": "R",
    "datagram.emit_failed": "O",
    "lifespan.startup": "F",
    "lifespan.startup_complete": "F",
    "lifespan.startup_failed": "F",
    "lifespan.shutdown": "F",
    "lifespan.shutdown_complete": "F",
    "lifespan.shutdown_failed": "F"
  },
  "lifespan": {
    "request.open": "F",
    "request.body_in": "F",
    "request.chunk_in": "F",
    "request.dispatch": "F",
    "request.close": "F",
    "request.disconnect": "F",
    "response.open": "F",
    "response.body_out": "F",
    "response.chunk_out": "F",
    "response.finalize": "F",
    "response.emit_complete": "F",
    "session.open": "F",
    "session.accept": "F",
    "session.reject": "F",
    "session.ready": "F",
    "session.heartbeat": "F",
    "session.sync": "F",
    "session.close": "F",
    "session.disconnect": "F",
    "session.emit_complete": "F",
    "message.in": "F",
    "message.decode": "F",
    "message.decode_failed": "F",
    "message.handle": "F",
    "message.handle_failed": "F",
    "message.out": "F",
    "message.replay": "F",
    "message.snapshot": "F",
    "message.emit_complete": "F",
    "message.emit_failed": "F",
    "stream.open": "F",
    "stream.chunk_in": "F",
    "stream.chunk_out": "F",
    "stream.flush": "F",
    "stream.finalize": "F",
    "stream.reset": "F",
    "stream.stop_sending": "F",
    "stream.close": "F",
    "stream.emit_complete": "F",
    "datagram.in": "F",
    "datagram.handle": "F",
    "datagram.out": "F",
    "datagram.emit_complete": "F",
    "datagram.emit_failed": "F",
    "lifespan.startup": "R",
    "lifespan.startup_complete": "R",
    "lifespan.startup_failed": "O",
    "lifespan.shutdown": "R",
    "lifespan.shutdown_complete": "R",
    "lifespan.shutdown_failed": "O"
  }
} as const;

export const PROTOCOLS = {
  "http.rest": {
    "binding": "rest",
    "transport": "http",
    "secure": false,
    "scope_type": "http"
  },
  "https.rest": {
    "binding": "rest",
    "transport": "http",
    "secure": true,
    "scope_type": "http"
  },
  "http.jsonrpc": {
    "binding": "jsonrpc",
    "transport": "http",
    "secure": false,
    "scope_type": "http"
  },
  "https.jsonrpc": {
    "binding": "jsonrpc",
    "transport": "http",
    "secure": true,
    "scope_type": "http"
  },
  "http.stream": {
    "binding": "http.stream",
    "transport": "http",
    "secure": false,
    "scope_type": "http"
  },
  "https.stream": {
    "binding": "http.stream",
    "transport": "http",
    "secure": true,
    "scope_type": "http"
  },
  "http.sse": {
    "binding": "sse",
    "transport": "http",
    "secure": false,
    "scope_type": "http"
  },
  "https.sse": {
    "binding": "sse",
    "transport": "http",
    "secure": true,
    "scope_type": "http"
  },
  "ws": {
    "binding": "websocket",
    "transport": "websocket",
    "secure": false,
    "scope_type": "websocket"
  },
  "wss": {
    "binding": "websocket",
    "transport": "websocket",
    "secure": true,
    "scope_type": "websocket"
  },
  "webtransport": {
    "binding": "webtransport",
    "transport": "webtransport",
    "secure": true,
    "scope_type": "webtransport"
  },
  "asgi.pathsend": {
    "binding": "http.stream",
    "transport": "http",
    "secure": false,
    "scope_type": "http"
  },
  "lifespan": {
    "binding": "lifespan",
    "transport": "lifespan",
    "secure": false,
    "scope_type": "lifespan"
  }
} as const;

export const AUTOMATA = {
  "request": {
    "initial": "idle",
    "terminal": [
      "closed",
      "disconnected"
    ],
    "transitions": [
      {
        "from": "idle",
        "event": "request.open",
        "to": "open"
      },
      {
        "from": "open",
        "event": "request.body_in",
        "to": "open"
      },
      {
        "from": "open",
        "event": "request.chunk_in",
        "to": "open"
      },
      {
        "from": "open",
        "event": "request.close",
        "to": "body_closed"
      },
      {
        "from": "open",
        "event": "request.dispatch",
        "to": "dispatched"
      },
      {
        "from": "body_closed",
        "event": "request.dispatch",
        "to": "dispatched"
      },
      {
        "from": "dispatched",
        "event": "response.open",
        "to": "responding"
      },
      {
        "from": "responding",
        "event": "response.body_out",
        "to": "responding"
      },
      {
        "from": "responding",
        "event": "response.chunk_out",
        "to": "responding"
      },
      {
        "from": "responding",
        "event": "response.emit_complete",
        "to": "completing"
      },
      {
        "from": "completing",
        "event": "response.finalize",
        "to": "closed"
      },
      {
        "from": "open",
        "event": "request.disconnect",
        "to": "disconnected"
      },
      {
        "from": "body_closed",
        "event": "request.disconnect",
        "to": "disconnected"
      }
    ]
  },
  "session": {
    "initial": "idle",
    "terminal": [
      "closed",
      "disconnected",
      "rejected"
    ],
    "transitions": [
      {
        "from": "idle",
        "event": "session.open",
        "to": "open"
      },
      {
        "from": "open",
        "event": "session.accept",
        "to": "accepted"
      },
      {
        "from": "open",
        "event": "session.reject",
        "to": "rejected"
      },
      {
        "from": "open",
        "event": "session.disconnect",
        "to": "disconnected"
      },
      {
        "from": "accepted",
        "event": "session.ready",
        "to": "ready"
      },
      {
        "from": "accepted",
        "event": "session.disconnect",
        "to": "disconnected"
      },
      {
        "from": "ready",
        "event": "session.heartbeat",
        "to": "ready"
      },
      {
        "from": "ready",
        "event": "session.sync",
        "to": "ready"
      },
      {
        "from": "ready",
        "event": "session.emit_complete",
        "to": "ready"
      },
      {
        "from": "ready",
        "event": "session.close",
        "to": "closed"
      },
      {
        "from": "ready",
        "event": "session.disconnect",
        "to": "disconnected"
      }
    ]
  },
  "message": {
    "initial": "idle",
    "terminal": [
      "complete",
      "failed"
    ],
    "transitions": [
      {
        "from": "idle",
        "event": "message.in",
        "to": "received"
      },
      {
        "from": "received",
        "event": "message.decode",
        "to": "decoded"
      },
      {
        "from": "received",
        "event": "message.decode_failed",
        "to": "failed"
      },
      {
        "from": "decoded",
        "event": "message.handle",
        "to": "handled"
      },
      {
        "from": "decoded",
        "event": "message.handle_failed",
        "to": "failed"
      },
      {
        "from": "handled",
        "event": "message.out",
        "to": "emitted"
      },
      {
        "from": "emitted",
        "event": "message.emit_complete",
        "to": "complete"
      },
      {
        "from": "emitted",
        "event": "message.emit_failed",
        "to": "failed"
      },
      {
        "from": "complete",
        "event": "message.replay",
        "to": "emitted"
      },
      {
        "from": "complete",
        "event": "message.snapshot",
        "to": "complete"
      }
    ]
  },
  "stream": {
    "initial": "idle",
    "terminal": [
      "closed",
      "reset",
      "stopped"
    ],
    "transitions": [
      {
        "from": "idle",
        "event": "stream.open",
        "to": "open"
      },
      {
        "from": "open",
        "event": "stream.chunk_in",
        "to": "open"
      },
      {
        "from": "open",
        "event": "stream.chunk_out",
        "to": "open"
      },
      {
        "from": "open",
        "event": "stream.flush",
        "to": "open"
      },
      {
        "from": "open",
        "event": "stream.finalize",
        "to": "finalizing"
      },
      {
        "from": "finalizing",
        "event": "stream.emit_complete",
        "to": "closed"
      },
      {
        "from": "open",
        "event": "stream.close",
        "to": "closed"
      },
      {
        "from": "open",
        "event": "stream.reset",
        "to": "reset"
      },
      {
        "from": "open",
        "event": "stream.stop_sending",
        "to": "stopped"
      },
      {
        "from": "finalizing",
        "event": "stream.reset",
        "to": "reset"
      },
      {
        "from": "finalizing",
        "event": "stream.stop_sending",
        "to": "stopped"
      }
    ]
  },
  "datagram": {
    "initial": "idle",
    "terminal": [
      "complete",
      "failed"
    ],
    "transitions": [
      {
        "from": "idle",
        "event": "datagram.in",
        "to": "received"
      },
      {
        "from": "received",
        "event": "datagram.handle",
        "to": "handled"
      },
      {
        "from": "handled",
        "event": "datagram.out",
        "to": "emitted"
      },
      {
        "from": "emitted",
        "event": "datagram.emit_complete",
        "to": "complete"
      },
      {
        "from": "emitted",
        "event": "datagram.emit_failed",
        "to": "failed"
      }
    ]
  },
  "lifespan": {
    "initial": "idle",
    "terminal": [
      "startup_complete",
      "startup_failed",
      "shutdown_complete",
      "shutdown_failed"
    ],
    "transitions": [
      {
        "from": "idle",
        "event": "lifespan.startup",
        "to": "starting"
      },
      {
        "from": "starting",
        "event": "lifespan.startup_complete",
        "to": "startup_complete"
      },
      {
        "from": "starting",
        "event": "lifespan.startup_failed",
        "to": "startup_failed"
      },
      {
        "from": "startup_complete",
        "event": "lifespan.shutdown",
        "to": "shutting_down"
      },
      {
        "from": "idle",
        "event": "lifespan.shutdown",
        "to": "shutting_down"
      },
      {
        "from": "shutting_down",
        "event": "lifespan.shutdown_complete",
        "to": "shutdown_complete"
      },
      {
        "from": "shutting_down",
        "event": "lifespan.shutdown_failed",
        "to": "shutdown_failed"
      }
    ]
  }
} as const;

export const FRAMES = {
  "app": {
    "kind": "contract-framing",
    "binding": "webtransport",
    "schema": "contract/schemas/frames/app.schema.json"
  },
  "asgi-tls-extension": {
    "kind": "extension-frame",
    "binding": "*",
    "schema": "contract/schemas/frames/asgi-tls-extension.schema.json"
  },
  "asgi-pathsend-extension": {
    "kind": "extension-frame",
    "binding": "http.stream",
    "schema": "contract/schemas/frames/asgi-pathsend-extension.schema.json"
  },
  "bytes": {
    "kind": "contract-framing",
    "binding": "http.stream",
    "schema": "contract/schemas/frames/bytes.schema.json"
  },
  "grpc": {
    "kind": "contract-framing",
    "binding": "http.stream",
    "schema": "contract/schemas/frames/grpc.schema.json"
  },
  "http-1-1-message": {
    "kind": "wire-frame",
    "binding": "rest",
    "schema": "contract/schemas/frames/http-1-1-message.schema.json"
  },
  "http-request-body-chunk": {
    "kind": "wire-frame",
    "binding": "http.stream",
    "schema": "contract/schemas/frames/http-request-body-chunk.schema.json"
  },
  "http-response-body-chunk": {
    "kind": "wire-frame",
    "binding": "http.stream",
    "schema": "contract/schemas/frames/http-response-body-chunk.schema.json"
  },
  "http-response-start-frame": {
    "kind": "wire-frame",
    "binding": "rest",
    "schema": "contract/schemas/frames/http-response-start-frame.schema.json"
  },
  "json": {
    "kind": "contract-framing",
    "binding": "rest",
    "schema": "contract/schemas/frames/json.schema.json"
  },
  "jsonrpc": {
    "kind": "contract-framing",
    "binding": "jsonrpc",
    "schema": "contract/schemas/frames/jsonrpc.schema.json"
  },
  "json-rpc-request-object": {
    "kind": "contract-framing",
    "binding": "jsonrpc",
    "schema": "contract/schemas/frames/json-rpc-request-object.schema.json"
  },
  "json-rpc-response-object": {
    "kind": "contract-framing",
    "binding": "jsonrpc",
    "schema": "contract/schemas/frames/json-rpc-response-object.schema.json"
  },
  "json-rpc-notification-object": {
    "kind": "contract-framing",
    "binding": "jsonrpc",
    "schema": "contract/schemas/frames/json-rpc-notification-object.schema.json"
  },
  "json-rpc-error-object": {
    "kind": "contract-framing",
    "binding": "jsonrpc",
    "schema": "contract/schemas/frames/json-rpc-error-object.schema.json"
  },
  "raw": {
    "kind": "contract-framing",
    "binding": "websocket",
    "schema": "contract/schemas/frames/raw.schema.json"
  },
  "sse": {
    "kind": "contract-framing",
    "binding": "sse",
    "schema": "contract/schemas/frames/sse.schema.json"
  },
  "sse-data-field": {
    "kind": "contract-framing",
    "binding": "sse",
    "schema": "contract/schemas/frames/sse-data-field.schema.json"
  },
  "sse-event-field": {
    "kind": "contract-framing",
    "binding": "sse",
    "schema": "contract/schemas/frames/sse-event-field.schema.json"
  },
  "sse-id-field": {
    "kind": "contract-framing",
    "binding": "sse",
    "schema": "contract/schemas/frames/sse-id-field.schema.json"
  },
  "sse-retry-field": {
    "kind": "contract-framing",
    "binding": "sse",
    "schema": "contract/schemas/frames/sse-retry-field.schema.json"
  },
  "websocket-frame": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-frame.schema.json"
  },
  "websocket-accept-frame": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-accept-frame.schema.json"
  },
  "websocket-close-frame": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-close-frame.schema.json"
  },
  "websocket-continuation-frame": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-continuation-frame.schema.json"
  },
  "websocket-disconnect-frame": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-disconnect-frame.schema.json"
  },
  "websocket-ping-frame": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-ping-frame.schema.json"
  },
  "websocket-pong-frame": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-pong-frame.schema.json"
  },
  "websocket-receive-bytes": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-receive-bytes.schema.json"
  },
  "websocket-receive-text": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-receive-text.schema.json"
  },
  "websocket-send-bytes": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-send-bytes.schema.json"
  },
  "websocket-send-text": {
    "kind": "wire-frame",
    "binding": "websocket",
    "schema": "contract/schemas/frames/websocket-send-text.schema.json"
  },
  "webtransport-datagram-frame": {
    "kind": "wire-frame",
    "binding": "webtransport",
    "schema": "contract/schemas/frames/webtransport-datagram-frame.schema.json"
  },
  "webtransport-stream-frame": {
    "kind": "wire-frame",
    "binding": "webtransport",
    "schema": "contract/schemas/frames/webtransport-stream-frame.schema.json"
  }
} as const;

export const EXTENSIONS = {
  "asgi.tls": {
    "scope_key": "tls",
    "fields": {
      "version": {
        "type": "string",
        "required": false
      },
      "cipher": {
        "type": "string",
        "required": false
      },
      "verified": {
        "type": "boolean",
        "required": false
      },
      "peer_identity": {
        "type": "string",
        "required": false
      },
      "peer_cert": {
        "type": "object",
        "required": false
      }
    }
  },
  "asgi.pathsend": {
    "event_type": "http.response.pathsend",
    "fields": {
      "path": {
        "type": "string",
        "required": true
      },
      "stat_result": {
        "type": "object",
        "required": false
      },
      "headers": {
        "type": "array",
        "required": false
      }
    }
  }
} as const;

export const CHANNELS = [
  "receive",
  "send"
] as const;

export const DIRECTIONS = [
  "client_to_server",
  "server_to_client",
  "app_to_server",
  "server_to_app",
  "system"
] as const;

export const FRAMINGS = [
  "json",
  "jsonrpc",
  "ndjson",
  "sse",
  "text",
  "bytes",
  "binary"
] as const;

export const EVENT_CLASSIFICATIONS = [
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
] as const;
