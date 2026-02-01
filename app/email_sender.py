# app/email_sender.py
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime

load_dotenv()

class EmailSender:
    def __init__(self):
        self.gmail_user = os.getenv('SMTP_USER', '').strip()
        self.gmail_password = os.getenv('SMTP_PASSWORD', '').strip()
    
    async def send_email(self, name: str, user_email: str, message: str):
        """Отправляет письмо через Gmail"""
        
        if not self.gmail_user or not self.gmail_password:
            return False, "❌ Не настроен Gmail"
        
        if not message or message == "Нет текста":
            return False, "❌ Текст письма пустой"
        
        try:
            # Формируем письмо с БОЛЬШЕ информацией
            email_text = f"""
            ===========================================
            📨 НОВОЕ СООБЩЕНИЕ ОТ ПОЛЬЗОВАТЕЛЯ
            ===========================================
            
            👤 ИМЯ ПОЛЬЗОВАТЕЛЯ: {name}
            📧 EMAIL ПОЛЬЗОВАТЕЛЯ: {user_email}
            🕐 ВРЕМЯ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            ===========================================
            💬 ТЕКСТ СООБЩЕНИЯ:
            ===========================================
            
            {message}
            
            ===========================================
            📝 ИНФОРМАЦИЯ ОТПРАВКИ:
            ===========================================
            
            • Отправлено через Telegram бота
            • Бот: @ваш_бот (укажите username)
            • Ответить пользователю: {user_email}
            • Дата отправки: {datetime.now().strftime('%d.%m.%Y')}
            
            ===========================================
            """
            
            # Создаем email
            msg = MIMEText(email_text, 'plain', 'utf-8')
            msg['From'] = f'Telegram Bot <{self.gmail_user}>'
            msg['To'] = 'shothed96@gmail.com'  # Ваш email
            msg['Reply-To'] = user_email  # Ответить пользователю
            msg['Subject'] = f'📨 Сообщение от {name} ({datetime.now().strftime("%H:%M")})'
            
            # Отправка
            def send():
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(self.gmail_user, self.gmail_password)
                    server.send_message(msg)
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, send)
            
            return True, "✅ Письмо отправлено!"
            
        except Exception as e:
            print(f"❌ Ошибка отправки: {str(e)}")
            return False, f"❌ Ошибка: {str(e)}"

email_sender = EmailSender()