# Aegis_bot
Telegram bot for the Aegis project, created using the aiogram library. The main function of the bot is to provide a convenient communication channel between users and developers, as well as the opportunity to support the project.

## Preliminary requirements:

* Python 3.8 or higher.
* Telegram account and bot token received from @BotFather.
* SMTP credentials (such as those from Gmail) for sending emails.

## Installation and launch (Linux).

### 1. Clone the repository:
```git clone https://github.com/Ind1ana/Aegis_bot.git```  
```cd Aegis_bot```

### 2. Install the dependencies:
```pip install -r requirements.txt```

### 3. Set up environment variables:
Copy the .env.example file to .env:  

```cp .env.example .env```

Open the .env file and fill it with your data:  
```
BOT_TOKEN=your_telegram_bot_token_here #Your token

SMTP_USER=your_email@gmail.com #Your email
SMTP_PASSWORD=your_app_specific_password #Done through Google
SMTP_HOST=smtp.gmail.com #Don't touch it if you use Google
SMTP_PORT=587
RECEIVER_EMAIL=developer@example.com #Where will the questions come from```



