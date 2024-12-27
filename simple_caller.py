import os
from twilio.rest import Client
from dotenv import load_dotenv
import openai
import json

load_dotenv()

class SimpleCaller:
    def __init__(self):
        # Initialize clients using API Key authentication
        api_key = os.getenv('TWILIO_API_KEY')
        api_secret = os.getenv('TWILIO_API_SECRET')
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')  # This should be your Account SID (AC...)
        
        # Debug print to verify credentials
        print("[DEBUG] Twilio Credentials:")
        print(f"  • API Key exists: {bool(api_key)}")
        print(f"  • API Secret exists: {bool(api_secret)}")
        print(f"  • Phone number exists: {bool(os.getenv('TWILIO_PHONE_NUMBER'))}")
        
        if not all([api_key, api_secret]):
            raise ValueError("Missing Twilio API credentials in .env file")
            
        # Use API Key authentication
        self.twilio_client = Client(api_key, api_secret, account_sid)
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.openai_client = openai.Client(api_key=os.getenv('OPENAI_API_KEY'))
        
    def make_call(self, to_number, objective):
        """Make a call with AI-driven conversation"""
        try:
            # Create TwiML for Media Streams
            twiml = f"""
            <Response>
                <Start>
                    <Stream name="openai_stream" url="wss://api.openai.com/v1/realtime">
                        <Parameter name="model" value="gpt-4o-mini-realtime-preview"/>
                        <Parameter name="Authorization" value="Bearer {os.getenv('OPENAI_API_KEY')}"/>
                        <Parameter name="OpenAI-Beta" value="realtime=v1"/>
                        <Parameter name="objective" value="{objective}"/>
                    </Stream>
                </Start>
                <Connect>
                    <Stream name="openai_stream"/>
                </Connect>
            </Response>
            """
            
            call = self.twilio_client.calls.create(
                twiml=twiml,
                to=to_number,
                from_=self.from_number,
                record=True
            )
            
            print(f"Call initiated! SID: {call.sid}")
            return call.sid
            
        except Exception as e:
            print(f"Error making call: {str(e)}")
            return None

    def check_call_status(self, call_sid):
        """Check the status of a call"""
        try:
            call = self.twilio_client.calls(call_sid).fetch()
            return call.status
        except Exception as e:
            print(f"Error checking call status: {str(e)}")
            return None 