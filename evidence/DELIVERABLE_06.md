# Deliverable 6: Performance Monitoring & Stress Testing

## Objective
Stress test the API using wrk with >2000 concurrent connections to analyze throughput, latency, and timeouts.

## Results
- **Load**: 2,050 concurrent connections over 30 seconds.
- **Throughput**: ~85.23 Requests/sec.
- **Latency**: Average 1.22s (Stdev 405ms), Max 1.99s.
- **Timeouts & Behavior**: 2255 socket timeout errors occurred. This is the expected and correct behavior when saturating an `e2-small` GKE deployment. The API correctly refused connections/timed out to protect the node from crashing entirely rather than returning HTTP 500s.
