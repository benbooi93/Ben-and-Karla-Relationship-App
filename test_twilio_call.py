import os
from twilio.rest import Client
from dotenv import load_dotenv

def test_twilio_auth():
    """Test Twilio authentication"""
    load_dotenv()
    
    api_key = os.getenv('TWILIO_API_KEY')
    api_secret = os.getenv('TWILIO_API_SECRET')
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    
    try:
        client = Client(api_key, api_secret, account_sid)
        # Try to list calls (this will verify auth)
        calls = client.calls.list(limit=1)
        print("✅ Twilio authentication successful!")
        return True
    except Exception as e:
        print(f"❌ Twilio authentication failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_twilio_auth() 