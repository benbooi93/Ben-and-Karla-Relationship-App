import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def make_test_call(to_number):
    """
    Make a test call using Twilio
    
    Args:
        to_number (str): The phone number to call (E.164 format)
    """
    try:
        # Get credentials from environment variables
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Make the call
        call = client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",
            to=to_number,
            from_=from_number
        )
        
        print(f"Call initiated! SID: {call.sid}")
        return call.sid
        
    except Exception as e:
        print(f"Error making call: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    test_number = "+16133168831"  # Replace with the number you want to test
    make_test_call(test_number) 