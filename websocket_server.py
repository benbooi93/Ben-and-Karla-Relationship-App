import asyncio
import websockets
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class AudioHandler:
    def __init__(self):
        self.openai_ws = None
        self.api_key = os.getenv('OPENAI_API_KEY')
        print(f"[DEBUG] OpenAI API Key present: {bool(self.api_key)}")

    async def connect_to_openai(self):
        """Connect to OpenAI's Realtime API"""
        url = "wss://api.openai.com/v1/realtime?model=gpt-4o-mini-realtime-preview"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "realtime=v1"
        }
        print(f"[DEBUG] Attempting to connect to OpenAI at: {url}")
        
        try:
            self.openai_ws = await websockets.connect(url, extra_headers=headers)
            print("[DEBUG] Successfully connected to OpenAI WebSocket")
            
            # Initialize the conversation
            init_message = {
                "type": "response.create",
                "response": {
                    "modalities": ["audio", "text"]
                }
            }
            print("[DEBUG] Sending init message:", init_message)
            await self.openai_ws.send(json.dumps(init_message))
            
        except Exception as e:
            print(f"[ERROR] Failed to connect to OpenAI: {e}")
            raise

    async def handle_audio(self, websocket):
        """Handle audio from Twilio and relay to OpenAI"""
        try:
            if not self.openai_ws:
                await self.connect_to_openai()

            async for message in websocket:
                data = json.loads(message)
                
                if data["event"] == "media":
                    # Forward audio to OpenAI
                    await self.openai_ws.send(json.dumps({
                        "type": "audio.data",
                        "audio": {
                            "data": data["media"]["payload"]
                        }
                    }))
                    
                    # Get response from OpenAI
                    response = await self.openai_ws.recv()
                    response_data = json.loads(response)
                    
                    if response_data["type"] == "text.response":
                        # Send text response back to Twilio
                        await websocket.send(json.dumps({
                            "event": "media",
                            "streamSid": data["streamSid"],
                            "media": {
                                "payload": base64.b64encode(
                                    response_data["text"]["content"].encode()
                                ).decode()
                            }
                        }))

        except Exception as e:
            print(f"Error in WebSocket handler: {e}")
            if self.openai_ws:
                await self.openai_ws.close()

async def start_server():
    handler = AudioHandler()
    async with websockets.serve(handler.handle_audio, "localhost", 8080):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(start_server()) 