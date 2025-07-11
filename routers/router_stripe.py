from fastapi import APIRouter, Body, Depends, Header, Request
from fastapi.responses import RedirectResponse
import stripe
from firebase_admin import auth
from database.firebase import db
from routers.router_auth import get_current_user
router = APIRouter(
      tags=["Stripe"],
      prefix='/stripe'
)
  
# This is your test secret API key.
from dotenv import dotenv_values
config = dotenv_values(".env")
stripe.api_key = config['STRIPE_SK']

DOMAIN = 'http://localhost:8000'

@router.get('/checkout')
async def stripe_checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Price ID  of the product 
                    'price': 'price_1O9vKMGWUEsr87M0a1Bmhkzx',
                    'quantity': 1
                },
            ],
            mode='subscription',
            payment_method_types=['card'],
            success_url=DOMAIN + '/stripe/success',
            cancel_url=DOMAIN + '/docs',
            client_reference_id= "cus_Oy2dykAqu4nHqk"
        )
        # return checkout_session
        response = RedirectResponse(url=checkout_session['url'])
        return response
    except Exception as e:
        return str(e)
    
# response after successfull subscription
@router.get('/success')   
async def stripe_success():
    return {
        "message": f"You have successfully subscribed to Attendance Track"
        }


# webhook to get event from stripe
@router.post('/webhook')
async def webhook_received(request: Request, stripe_signature: str = Header(None)):
    webhook_secret = config['STRIPE_WEBHOOK_SECRET']
    data = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
        event_data = event['data']
    except Exception as e:
        return {"error": str(e)}
    print(event_data)
    event_type = event['type']
    if event_type == 'checkout.session.completed':
        print('checkout session completed')
    elif event_type == 'invoice.paid':
        print('invoice paid')
        cust_email = event_data['object']['customer_email'] 
        fireBase_user = auth.get_user_by_email(cust_email) 
        cust_id =event_data['object']['customer'] 
        item_id= event_data['object']['lines']['data'][0]['subscription_item']
        db.child("users").child(fireBase_user.uid).child("stripe").set({"item_id":item_id, "cust_id":cust_id}) # écriture dans la DB firebase      

    elif event_type == 'invoice.payment_failed':
        print('invoice payment failed')
    return {"status": "success"}


@router.get('/usage')
async def stripe_usage(userData: int = Depends(get_current_user)):
    fireBase_user = auth.get_user(userData['uid']) 
    stripe_data= db.child("users").child(fireBase_user.uid).child("stripe").get().val()
    cust_id =stripe_data['cust_id']
    return stripe.Invoice.upcoming(customer=cust_id)

def increment_stripe(userId:str):
   # Retrieve user information from Firebase using the provided 'userId'
    fireBase_user = auth.get_user(userId)  
    # Query data from Firebase's Realtime Database under the 'stripe' child node for the user's UID
    stripe_data = db.child("users").child(fireBase_user.uid).child("stripe").get().val()
    # Extract the 'item_id' from the retrieved 'stripe_data' 
    item_id = stripe_data['item_id']
    # Create a usage record for the specific Stripe subscription item identified by 'item_id'
    stripe.SubscriptionItem.create_usage_record(item_id, quantity=1)
    return
