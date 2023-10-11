from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, Update


# Constants for conversation states
START, PRODUCT_SELECTED, PAYMENT, ORDER_PLACED, BROWSE_IN_BOT = range(5)

# Initialize the Telegram Bot (replace with your bot token)
# updater = Updater(token="6383839015:AAHKBfwagRiN3HrmnzLg8ka1HmyG4ubAK0s")

bot = Bot(token="6383839015:AAHKBfwagRiN3HrmnzLg8ka1HmyG4ubAK0s")


# Example product data (you can replace this with your actual product data)
products = [
    {
        "name": "Fancy Shirt",
        "price": "$20.00",
        "description": "A stylish shirt for any occasion",
    },
    {
        "name": "Elegant Dress",
        "price": "$30.00",
        "description": "Perfect for formal events",
    },
    # Add more products as needed
]
def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        f"Hi {user.first_name}! Welcome to our store. You can browse products in the channel or search for products here in the bot."
    )
    return START

def product_selected(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    product_name = query.data.split("_")[1]
    query.answer()
    query.edit_message_text(f"You selected: {product_name}. Please proceed with the payment.")
    return PAYMENT

def payment(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        f"Great choice, {user.first_name}! Your order has been placed successfully."
    )
    return ORDER_PLACED

def browse_in_bot(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(
        f"You can search for products here in the bot. Please enter a search query or use /cancel to go back."
    )
    return BROWSE_IN_BOT

def search_products(update: Update, context: CallbackContext) -> int:
    query = update.message.text
    matching_products = [product for product in products if query.lower() in product["name"].lower()]
    
    if matching_products:
        update.message.reply_text("Here are the matching products:")
        for product in matching_products:
            product_message = (
                f"Product Name: {product['name']}\n"
                f"Price: {product['price']}\n"
                f"Description: {product['description']}"
            )
            update.message.reply_text(product_message)
    else:
        update.message.reply_text("No matching products found.")
    
    return BROWSE_IN_BOT

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Order/search cancelled.")
    return ConversationHandler.END

# Define conversation handlers
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        START: [CallbackQueryHandler(product_selected, pattern=r'^select_product_')],
        PAYMENT: [MessageHandler(lambda update: update.message.text and not update.message.text.startswith('/'), 
    payment
)],
        BROWSE_IN_BOT: [CommandHandler('browse', browse_in_bot)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

search_handler = ConversationHandler(
    entry_points=[CommandHandler('search', browse_in_bot)],
    states={
        BROWSE_IN_BOT: [MessageHandler(lambda update: update.message.text and not update.message.text.startswith('/'), 
    search_products)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

# Register the conversation handlers
bot.add_handler(conv_handler)
bot.add_handler(search_handler)

# Run the bot
bot.polling()
