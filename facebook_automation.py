import time
import argparse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def send_facebook_sms(email, password, phone):
    """
    Automate Facebook to send SMS to the user's phone.
    """
    
    print(f"📱 Starting Facebook SMS automation...")
    print(f"📧 Email: {email}")
    print(f"📱 Phone: {phone}")
    print("-" * 50)
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = None
    
    try:
        # ============================================
        # USE THE LOCAL CHROMEDRIVER IN PROJECT ROOT
        # ============================================
        chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        print("✅ Chrome driver started")
        
        # ============================================
        # STEP 1: FACEBOOK LOGIN
        # ============================================
        print("⏳ Loading Facebook login...")
        driver.get("https://www.facebook.com/")
        time.sleep(3)
        
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(email)
        print("✅ Email entered")
        
        pass_field = driver.find_element(By.ID, "pass")
        pass_field.send_keys(password)
        print("✅ Password entered")
        
        driver.find_element(By.NAME, "login").click()
        time.sleep(5)
        print("✅ Login clicked")
        
        # ============================================
        # STEP 2: FORGOT PASSWORD
        # ============================================
        print("⏳ Navigating to Forgot Password...")
        driver.get("https://www.facebook.com/login/identify/?ctx=recover")
        time.sleep(3)
        
        phone_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identify_email"))
        )
        phone_field.send_keys(phone)
        print("✅ Phone entered")
        
        driver.find_element(By.NAME, "did_submit").click()
        time.sleep(3)
        print("✅ Search clicked")
        
        # ============================================
        # STEP 3: CLICK SEND SMS
        # ============================================
        print("⏳ Clicking SMS button...")
        
        try:
            sms_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Send Code via SMS')]"))
            )
            sms_btn.click()
            print("✅ SMS button clicked")
        except:
            try:
                driver.find_element(By.XPATH, "//button[contains(text(),'Send SMS')]").click()
                print("✅ SMS button clicked (alt)")
            except:
                driver.find_element(By.XPATH, "//span[contains(text(),'SMS')]").click()
                print("✅ SMS button clicked (span)")
        
        time.sleep(5)
        print("✅ SMS sent to user's phone")
        
        driver.quit()
        return {"success": True, "message": f"SMS sent to {phone}"}
        
    except Exception as e:
        if driver:
            driver.quit()
        print(f"❌ ERROR: {str(e)}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--phone", required=True)
    args = parser.parse_args()
    
    result = send_facebook_sms(args.email, args.password, args.phone)
    print("\n=== RESULT ===")
    print(f"Success: {result.get('success', False)}")
    print(f"Message: {result.get('message', result.get('error', 'Unknown'))}")