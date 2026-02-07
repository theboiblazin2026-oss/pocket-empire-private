---
name: IoT
description: MQTT, protocols, edge computing, sensor networks
---

# IoT Skill

## MQTT

```python
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f'{msg.topic}: {msg.payload.decode()}')

client = mqtt.Client()
client.on_message = on_message
client.connect('broker.hivemq.com', 1883)
client.subscribe('sensors/temperature')
client.loop_forever()

# Publish
client.publish('sensors/temperature', '72.5')
```

## Protocols Comparison

| Protocol | Best For |
|----------|----------|
| MQTT | Low bandwidth, pub/sub |
| HTTP/REST | Standard APIs |
| CoAP | Constrained devices |
| WebSocket | Real-time, bidirectional |
| LoRaWAN | Long range, low power |

## Sensor Data Format

```json
{
  "device_id": "sensor_001",
  "timestamp": "2024-01-15T10:30:00Z",
  "readings": {
    "temperature": 72.5,
    "humidity": 45
  }
}
```

## Edge vs Cloud

| Edge | Cloud |
|------|-------|
| Low latency | Unlimited compute |
| Works offline | Central storage |
| Data privacy | Easy scaling |
| Lower bandwidth | Complex analytics |

## Security Checklist

- [ ] Encrypted communication (TLS)
- [ ] Device authentication
- [ ] Secure firmware updates
- [ ] Network segmentation
- [ ] Access control

## When to Apply
Use when designing IoT systems, connecting devices, or building sensor networks.
