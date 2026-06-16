export enum EmitCompletionLevel {
  ACCEPTED_BY_RUNTIME = "accepted_by_runtime",
  QUEUED_FOR_TRANSPORT = "queued_for_transport",
  FLUSHED_TO_TRANSPORT = "flushed_to_transport",
  PEER_ACKNOWLEDGED = "peer_acknowledged",
  FAILED_DURING_EMIT = "failed_during_emit",
  ABORTED_BY_PEER = "aborted_by_peer",
}
