---
name: Voice AI
description: Build phone bots with Twilio, ElevenLabs, and AI
---

# Voice AI Skill

## Stack Overview

```
User calls → Twilio → Your server → AI (GPT/Claude) → TTS → Twilio → User hears
```

## Twilio Setup

### Webhook Handler (Flask)
```python
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route('/incoming', methods=['POST'])
def incoming():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/process', timeout=3)
    gather.say('Hello! How can I help you today?')
    response.append(gather)
    return str(response)

@app.route('/process', methods=['POST'])
def process():
    speech = request.form.get('SpeechResult')
    # Send to AI, get response
    ai_response = get_ai_response(speech)
    
    response = VoiceResponse()
    response.say(ai_response)
    return str(response)
```

## Text-to-Speech Options

| Service | Quality | Cost |
|---------|---------|------|
| Twilio built-in | Basic | Free |
| ElevenLabs | Excellent | $5+/mo |
| Google TTS | Good | $0.000004/char |
| Amazon Polly | Good | $0.004/char |

### ElevenLabs Integration
```python
import requests

def text_to_speech(text):
    response = requests.post(
        'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}',
        headers={'xi-api-key': 'YOUR_KEY'},
        json={'text': text}
    )
    return response.content  # Audio bytes
```

## Speech-to-Text

```python
# Twilio does this automatically
speech_result = request.form.get('SpeechResult')

# Or use Whisper for better accuracy
import openai
transcript = openai.Audio.transcribe('whisper-1', audio_file)
```

## Use Cases

- Customer service IVR
- Appointment booking
- Lead qualification
- Outbound calling campaigns
- Voice assistants

## When to Apply
Use when building phone bots, IVR systems, or voice-enabled applications.
