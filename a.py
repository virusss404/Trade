import telebot
import time
import random
from threading import Timer
from quotexapi.stable_api import Quotex
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram bot token
API_TOKEN = '7727434430:AAHLxdCSrm9w49QbT8vqojTo-tycfiX2UNo'
bot = telebot.TeleBot(API_TOKEN)

# Quotex API credentials
QUOTEX_EMAIL = 'virusssssss404@gmail.com'
QUOTEX_PASSWORD = 'virusssssss404@gmail.com'

# Initialize Quotex API session
client = Quotex(QUOTEX_EMAIL, QUOTEX_PASSWORD)

# Trade counters
total_signals = 0
up_signals = 0
put_signals = 0

def update_signal_percentages():
    global total_signals, up_signals, put_signals
    if total_signals == 0:
        return "No signals received yet."
    up_percentage = (up_signals / total_signals) * 100
    put_percentage = (put_signals / total_signals) * 100
    return f"UP🔼: {up_percentage:.2f}% | PUT🔻: {put_percentage:.2f}%"

def analyze_market():
    # Here you can implement your market analysis logic
    # This is a simple placeholder returning random signals
    return "UP🔼" if random.random() > 0.5 else "PUT🔻"

def send_auto_signal():
    global total_signals, up_signals, put_signals

    # Get signal from market analysis
    signal = analyze_market()
    total_signals += 1
    if signal == "UP🔼":
        up_signals += 1
    elif signal == "PUT🔻":
        put_signals += 1

    # Send the signal to Telegram chat
    bot.send_message(chat_id='8174678650', text=f"🚨AUTO-SIGNAL╰┈➤👀: {signal}🔥\n\n\n{update_signal_percentages()}")

    # Schedule the next auto-signal
    Timer(60, send_auto_signal).start()  # Repeat every 60 seconds

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🎯💰💸Welcome to the Quotex Auto Signal Bot.")

@bot.message_handler(commands=['stats'])
def send_stats(message):
    bot.reply_to(message, update_signal_percentages())

@bot.message_handler(commands=['up_trade', 'put_trade'])
def manual_trade(message):
    signal = 'up' if message.text.lower() == '/up_trade' else 'put'
    try:
        trade_result = client.buy(signal, amount=1, asset="EURCAD")  # Adjust asset and amount
        if trade_result['status']:
            bot.reply_to(message, f"Manual trade executed: {signal.upper()}")
            logging.info(f"Executed {signal.upper()} trade successfully.")
        else:
            bot.reply_to(message, f"Trade failed: {trade_result.get('message', 'Unknown error')}")
            logging.error(f"Trade failed: {trade_result.get('message', 'Unknown error')}")
    except Exception as e:
        bot.reply_to(message, f"Error executing trade: {str(e)}")
        logging.error(f"Error executing trade: {str(e)}")

# Start the bot and auto-signal
if __name__ == "__main__":
    print("Bot is running...")
    Timer(54, send_auto_signal).start()  # Start auto-signal after 30 seconds
    bot.polling()
