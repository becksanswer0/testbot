from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from coinbase_commerce.client import Client
from coinbase_commerce.api_resources import Charge

API_TOKEN = '7488509768:AAHCRKkm7FdqzRTxGP1njBq_nEaEzoTmpTw'
COINBASE_API_KEY = 'YOUR_COINBASE_API_KEY'

client = Client(api_key=COINBASE_API_KEY)
abonelikler = ['Silver', 'Gold', 'Platinum']
abonelik_fiyatları = {
    'Silver': '10.00',
    'Gold': '20.00',
    'Platinum': '30.00'
}

def start(update, context):
    reply_keyboard = [abonelikler]
    update.message.reply_text(
        'Merhaba! Hangi aboneliği almak istersiniz?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

def handle_subscription_choice(update, context):
    choice = update.message.text
    if choice in abonelikler:
        update.message.reply_text(f'{choice} aboneliğini seçtiniz. Ödeme işlemi için devam edin.')
        create_charge(update, choice)
    else:
        update.message.reply_text('Geçersiz seçim. Lütfen geçerli bir abonelik seçin.')

def create_charge(update, subscription_type):
    price = abonelik_fiyatları[subscription_type]
    charge_data = {
        'name': f'{subscription_type} Aboneliği',
        'description': f'{subscription_type} aboneliği için ödeme.',
        'local_price': {
            'amount': price,
            'currency': 'USD'
        },
        'pricing_type': 'fixed_price'
    }
    charge = Charge.create(**charge_data)
    update.message.reply_text(f'Lütfen ödemeyi şu bağlantı üzerinden yapın: {charge.hosted_url}')

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_subscription_choice))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
