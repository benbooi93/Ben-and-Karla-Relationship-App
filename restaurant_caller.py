import os
from twilio.rest import Client
from dotenv import load_dotenv
import openai
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime

# Load environment variables
load_dotenv()

class RestaurantCaller:
    def __init__(self):
        # Initialize Twilio client
        self.twilio_client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        
        # Initialize OpenAI client
        self.openai_client = openai.Client(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')

    def scrape_menu(self, website_url):
        """Scrape restaurant menu from website"""
        try:
            response = requests.get(website_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # This is a basic implementation - you'll need to adjust based on the specific website structure
            menu_items = soup.find_all(['h2', 'h3', 'p'])
            return ' '.join([item.text for item in menu_items])
        except Exception as e:
            print(f"Error scraping menu: {str(e)}")
            return None

    def make_call(self, to_number, restaurant_name, objective, menu_data=None):
        """Make a call to restaurant with specific objective"""
        try:
            # Create TwiML for the call
            callback_url = f"https://your-ngrok-url/handle-call?restaurant={restaurant_name}&objective={objective}"
            if menu_data:
                callback_url += f"&menu={menu_data}"

            call = self.twilio_client.calls.create(
                url=callback_url,
                to=to_number,
                from_=self.from_number,
                record=True,  # Enable call recording
                status_callback="https://your-ngrok-url/call-status",
                status_callback_event=["completed"]
            )
            
            print(f"Call initiated! SID: {call.sid}")
            return call.sid
            
        except Exception as e:
            print(f"Error making call: {str(e)}")
            return None

    def get_call_transcript(self, call_sid):
        """Get transcript of the recorded call"""
        try:
            recordings = self.twilio_client.recordings.list(call_sid=call_sid)
            if recordings:
                # Get the latest recording
                recording = recordings[0]
                # Here you would implement the transcription using OpenAI's Whisper API
                # This is a placeholder for the actual implementation
                return f"Recording URL: {recording.uri}"
            return None
        except Exception as e:
            print(f"Error getting transcript: {str(e)}")
            return None

def main():
    caller = RestaurantCaller()
    
    # Example usage
    restaurant_info = {
        "name": "Example Restaurant",
        "phone": "+1234567890",
        "website": "https://example-restaurant.com",
        "objective": "Reserve a table for 2 people tonight at 7pm"
    }
    
    # Scrape menu if website is provided
    menu_data = caller.scrape_menu(restaurant_info["website"]) if restaurant_info["website"] else None
    
    # Make the call
    call_sid = caller.make_call(
        restaurant_info["phone"],
        restaurant_info["name"],
        restaurant_info["objective"],
        menu_data
    )
    
    if call_sid:
        # Get transcript after call is completed
        transcript = caller.get_call_transcript(call_sid)
        if transcript:
            print("Call transcript:", transcript)

if __name__ == "__main__":
    main() 