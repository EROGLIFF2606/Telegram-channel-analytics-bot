from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from datetime import datetime, timedelta
import pytz
from settings import API_ID, API_HASH
from language import get_text
import logging
from db import store_user_data, get_user_data, update_user_data

logger = logging.getLogger(__name__)

client = TelegramClient('session', API_ID, API_HASH)

CHOOSING, CHANNEL, TIME, LANGUAGE = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    language = user_data.get('language', 'en')
    
    reply_keyboard = [[get_text('set_channel', language), get_text('set_time', language)],
                      [get_text('set_language', language)]]
    
    await update.message.reply_text(
        get_text('start_message', language),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return CHOOSING

async def set_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    language = user_data.get('language', 'en')
    
    if update.message.text in [get_text('set_channel', 'en'), get_text('set_channel', 'ru')]:
        await update.message.reply_text(get_text('ask_channel', language))
        return CHANNEL
    
    channel_link = update.message.text
    
    async with client:
        try:
            channel = await client.get_entity(channel_link)
            admin = await client(JoinChannelRequest(channel))
            if admin.chats[0].admin_rights or admin.chats[0].creator:
                update_user_data(user_id, {'channel': channel.id})
                await update.message.reply_text(get_text('channel_set', language))
                return CHOOSING
            else:
                await update.message.reply_text(get_text('not_admin', language))
                return CHOOSING
        except Exception as e:
            await update.message.reply_text(get_text('channel_error', language))
            return CHOOSING

async def set_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    language = user_data.get('language', 'en')
    
    if update.message.text in [get_text('set_time', 'en'), get_text('set_time', 'ru')]:
        await update.message.reply_text(get_text('ask_time', language))
        return TIME
    
    time_str = update.message.text
    
    try:
        time = datetime.strptime(time_str, "%H:%M").time()
        update_user_data(user_id, {'time': time.strftime("%H:%M")})
        await update.message.reply_text(get_text('time_set', language).format(time=time_str))
        await schedule_daily_job(update, context)
        return CHOOSING
    except ValueError:
        await update.message.reply_text(get_text('time_error', language))
        return TIME

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    current_language = user_data.get('language', 'en')
    
    if update.message.text in [get_text('set_language', 'en'), get_text('set_language', 'ru')]:
        reply_keyboard = [['English', 'Русский']]
        await update.message.reply_text(
            get_text('ask_language', current_language),
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
        return LANGUAGE
    
    new_language = 'en' if update.message.text == 'English' else 'ru'
    update_user_data(user_id, {'language': new_language})
    await update.message.reply_text(
        get_text('language_set', new_language),
        reply_markup=ReplyKeyboardRemove(),
    )
    return CHOOSING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    language = user_data.get('language', 'en')
    
    await update.message.reply_text(
        get_text('cancel', language),
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def schedule_daily_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    time_str = user_data.get('time')
    
    if not time_str:
        return
    
    time = datetime.strptime(time_str, "%H:%M").time()
    now = datetime.now(pytz.utc)
    target_time = datetime.now(pytz.utc).replace(hour=time.hour, minute=time.minute, second=0, microsecond=0)
    
    if target_time <= now:
        target_time += timedelta(days=1)
    
    delay = (target_time - now).total_seconds()
    context.job_queue.run_repeating(send_analytics, interval=timedelta(days=1), first=delay, data=user_id)

async def send_analytics(context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = context.job.data
    user_data = get_user_data(user_id)
    channel_id = user_data.get('channel')
    language = user_data.get('language', 'en')
    
    if not channel_id:
        return
    
    async with client:
        
        new_subscribers = 15  # Placeholder 
        new_views = 30  # Placeholder
        new_reactions = 5  # Placeholder
        
        message = get_text('analytics', language).format(
            new_subscribers=new_subscribers,
            new_views=new_views,
            new_reactions=new_reactions
        )
        
        await context.bot.send_message(chat_id=user_id, text=message)

def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)