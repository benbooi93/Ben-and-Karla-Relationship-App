from flask import Flask, request, Response
import os
from dotenv import load_dotenv
from simple_caller import SimpleCaller

load_dotenv()
app = Flask(__name__)
caller = SimpleCaller()

@app.route("/recording-status", methods=['POST'])
def recording_status():
    """Handle recording status updates"""
    recording_url = request.values.get('RecordingUrl')
    call_sid = request.values.get('CallSid')
    
    if recording_url and call_sid:
        # Download the recording locally
        local_file = caller.download_recording(recording_url, call_sid)
        
        if local_file:
            print(f"\nRecording saved to: {local_file}")
    
    return Response(status=200)

if __name__ == "__main__":
    app.run(debug=True, port=5000) 