# PyMonitor

Monitor the status of your servers.

# PyMonitor Protocol
This defines the PyMonitor protocol

[Sequence Diagrams](https://bramp.github.io/js-sequence-diagrams/)

#### Connection Sequence
```sequence
Client->Server: connection_request
Note over Server: Update or Create new server
Server-->Client: connection_response
Note over Client,Server: ... session ...
Client->Server: disconnect_request
Server-->Client: disconnect_reponse
```
#### State update
```sequence
Client->Server: monitor_state_update
Note over Server: Set monitors state
Server-->Client: monitor_state_response
```

#### Monitor update
```sequence
Client->Server: monitor_update
Note over Server: Add monitor record
```