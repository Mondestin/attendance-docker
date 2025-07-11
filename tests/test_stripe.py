from fastapi.testclient import TestClient
from main import app
from database.firebase import db
from firebase_admin import auth
from dotenv import load_dotenv
import os
import stripe

load_dotenv()
# Create a TestClient instance for making HTTP requests
client = TestClient(app)

# Set up the Stripe test secret API key
#config = dotenv_values(".env")
config={
    "STRIPE_SK": os.getenv("STRIPE_SK")
}
stripe.api_key = config['STRIPE_SK']

# Test case to check if stripe_checkout endpoint redirects successfully
def test_stripe_checkout_redirect():
    response = client.get("/stripe/checkout")
    assert response.status_code == 200  # Redirect status code

# Test case for the success endpoint
def test_stripe_success():
    response = client.get("/stripe/success")
    assert response.status_code == 200
    assert response.json() == {"message": "You have successfully subscribed to Attendance Track"}

# Test case to check if webhook endpoint returns success for a sample event
def test_stripe_webhook_received_success():
    event_data = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "cust_id": "test@gmail.com"
            }
        }
    }
    response = client.post("/stripe/webhook", json=event_data, headers={"Stripe-Signature": "sample_signature"})
    assert response.status_code == 200




