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

## Running Dev build

```
docker run --rm -it -p 3000:3000 \
   --name=grafana \
   -e "GF_SERVER_ROOT_URL=http://grafana.server.name" \
   -e "GF_SECURITY_ADMIN_PASSWORD=secret" \
   grafana/grafana
docker run --name some-postgres -e POSTGRES_PASSWORD=secret --rm -it postgres
docker run -it --rm postgres psql -h 172.17.0.3 -U postgres
```
grafana user is admin
