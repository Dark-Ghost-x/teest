# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from typing import Optional

app = FastAPI(title="Telegram Bot API")

# فعال کردن CORS برای ارتباط با GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در پروژه واقعی دامنه دقیق رو بذارید
    allow_methods=["POST"],
    allow_headers=["*"],
)

# ساختار داده ورودی
class Message(BaseModel):
    name: str
    message: str
    email: Optional[str] = None

@app.post("/send")
async def send_message(msg: Message):
    """دریافت پیام از فرم و ارسال به تلگرام"""
    
    # دریافت توکن و چت آیدی از متغیرهای محیطی
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")
    
    if not BOT_TOKEN or not CHAT_ID:
        raise HTTPException(
            status_code=500,
            detail="سرور به درستی تنظیم نشده است."
        )
    
    # ساخت متن پیام
    telegram_text = f"""
📨 <b>پیام جدید از وبسایت</b>

👤 <b>نام:</b> {msg.name}
📝 <b>پیام:</b> {msg.message}
"""
    
    if msg.email:
        telegram_text += f"📧 <b>ایمیل:</b> {msg.email}\n"
    
    # ارسال به تلگرام
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": telegram_text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        return {"success": True, "message": "پیام با موفقیت ارسال شد"}
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"خطا در ارتباط با تلگرام: {str(e)}"
        )

@app.get("/")
async def health_check():
    """بررسی وضعیت سرور"""
    return {"status": "active", "service": "Telegram Bot API"}

# برای اجرای محلی
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
