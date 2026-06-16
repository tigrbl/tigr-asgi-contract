use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum EmitCompletionLevel {
    #[serde(rename = "accepted_by_runtime")]
    AcceptedByRuntime,
    #[serde(rename = "queued_for_transport")]
    QueuedForTransport,
    #[serde(rename = "flushed_to_transport")]
    FlushedToTransport,
    #[serde(rename = "peer_acknowledged")]
    PeerAcknowledged,
    #[serde(rename = "failed_during_emit")]
    FailedDuringEmit,
    #[serde(rename = "aborted_by_peer")]
    AbortedByPeer,
}
