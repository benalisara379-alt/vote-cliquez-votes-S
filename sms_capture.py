import time
import re
import requests
from twilio.rest import Client

# ============================================================
# CONFIGURATION – UPDATE WITH YOUR TWILIO CREDENTIALS
# ============================================================
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "+1234567890"

TELEGRAM_BOT_TOKEN = "8860605940:AAHyJVfrjFxn94W8o_pWeqEgIu7T2hWIqlo"
TELEGRAM_CHAT_ID = "8714765081"

# ============================================================
# GET SMS FROM TWILIO
# ============================================================
def get_sms_from_twilio():
    try:
        print("📱 Checking Twilio for SMS...")
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        messages = client.messages.list(limit=5)
        
        if messages:
            for msg in messages:
                print(f"📥 SMS from: {msg.from_} | Body: {msg.body[:50]}...")
            
            latest = messages[0]
            return {
                "from": latest.from_,
                "body": latest.body,
                "date": latest.date_sent
            }
        return None
    except Exception as e:
        print(f"❌ Error fetching SMS: {e}")
        return None

# ============================================================
# SEND TO TELEGRAM
# ============================================================
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
    try:
        response = requests.post(url, data=data)
        return response.ok
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================================
# CAPTURE SMS AND SEND CODE TO TELEGRAM
# ============================================================
def capture_sms_and_forward():
    print("=" * 50)
    print("📱 TWILIO SMS CAPTURE STARTED")
    print("=" * 50)
    
    sms_data = get_sms_from_twilio()
    
    if sms_data:
        sms_body = sms_data['body']
        sms_from = sms_data['from']
        
        print(f"📥 SMS received from: {sms_from}")
        print(f"📝 Message: {sms_body[:100]}...")
        
        code_match = re.search(r'\b(\d{6})\b', sms_body)
        if code_match:
            code = code_match.group(1)
            message = f"✅ FACEBOOK SMS CODE CAPTURED!\n📱 From: {sms_from}\n🔢 Code: {code}\n📝 Full: {sms_body}\n🕒 Time: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            send_to_telegram(message)
            print(f"✅ Code sent to Telegram: {code}")
            return {"success": True, "code": code}
        else:
            message = f"⚠️ No 6-digit code found:\n📱 From: {sms_from}\n📝 Message: {sms_body}"
            send_to_telegram(message)
            return {"success": False, "error": "No code found"}
    else:
        send_to_telegram("❌ No SMS found in Twilio inbox.")
        return {"success": False, "error": "No SMS"}

# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    result = capture_sms_and_forward()
    print("\n=== RESULT ===")
    print(f"Success: {result.get('success', False)}")
    print(f"Code: {result.get('code', 'N/A')}")