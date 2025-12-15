# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # فعال کردن CORS

@app.route('/send', methods=['POST'])
def send_message():
    """دریافت پیام از فرم و ارسال به تلگرام"""
    
    # دریافت داده‌های JSON
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "داده‌ای دریافت نشد"}), 400
    
    name = data.get('name', 'ناشناس')
    message = data.get('message', '')
    email = data.get('email')
    
    # دریافت توکن و چت آیدی
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    CHAT_ID = os.environ.get('CHAT_ID')
    
    if not BOT_TOKEN or not CHAT_ID:
        return jsonify({"success": False, "message": "تنظیمات سرور ناقص است"}), 500
    
    # ساخت پیام
    telegram_text = f"📨 پیام جدید\n👤 نام: {name}\n📝 پیام: {message}"
    if email:
        telegram_text += f"\n📧 ایمیل: {email}"
    
    # ارسال به تلگرام
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": telegram_text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return jsonify({"success": True, "message": "پیام ارسال شد"})
        else:
            return jsonify({"success": False, "message": "تلگرام خطا داد"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/')
def health_check():
    return jsonify({"status": "active"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
