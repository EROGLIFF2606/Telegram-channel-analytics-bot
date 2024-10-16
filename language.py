TEXTS = {
    'en': {
        'start_message': "Welcome to the Channel Analytics Bot! What would you like to do?",
        'set_channel': "Set channel",
        'set_time': "Set time",
        'set_language': "Set language",
        'ask_channel': "Please send me the link to your Telegram channel.",
        'channel_set': "Great! I've verified that you're an admin of this channel.",
        'not_admin': "Sorry, you need to be an admin of the channel to use this bot.",
        'channel_error': "Sorry, I couldn't verify the channel or your admin status. Please try again.",
        'ask_time': "What time do you want to receive daily analytics? Use the format HH:MM in 24-hour time.",
        'time_set': "Perfect! I'll send you daily analytics at {time}.",
        'time_error': "Sorry, that's not a valid time format. Please use HH:MM in 24-hour time.",
        'ask_language': "Please choose your preferred language:",
        'language_set': "Language set to English.",
        'cancel': "Operation cancelled. You can start over with /start",
        'analytics': "Today's analytics:\n{new_subscribers} new subscribers\n{new_views} new views on your posts\n{new_reactions} new reactions on your posts",
    },
    'ru': {
        'start_message': "Добро пожаловать в бот аналитики канала! Что бы вы хотели сделать?",
        'set_channel': "Установить канал",
        'set_time': "Установить время",
        'set_language': "Установить язык",
        'ask_channel': "Пожалуйста, отправьте мне ссылку на ваш Telegram канал.",
        'channel_set': "Отлично! Я подтвердил, что вы администратор этого канала.",
        'not_admin': "Извините, вы должны быть администратором канала, чтобы использовать этого бота.",
        'channel_error': "Извините, я не смог проверить канал или ваш статус администратора. Пожалуйста, попробуйте снова.",
        'ask_time': "В какое время вы хотите получать ежедневную аналитику? Используйте формат ЧЧ:ММ в 24-часовом формате.",
        'time_set': "Отлично! Я буду отправлять вам ежедневную аналитику в {time}.",
        'time_error': "Извините, это неверный формат времени. Пожалуйста, используйте ЧЧ:ММ в 24-часовом формате.",
        'ask_language': "Пожалуйста, выберите предпочитаемый язык:",
        'language_set': "Язык установлен на русский.",
        'cancel': "Операция отменена. Вы можете начать заново с помощью /start",
        'analytics': "Аналитика за сегодня:\n{new_subscribers} новых подписчиков\n{new_views} новых просмотров ваших постов\n{new_reactions} новых реакций на ваши посты",
    }
}

def get_text(key: str, language: str) -> str:
    return TEXTS.get(language, TEXTS['en']).get(key, TEXTS['en'].get(key, "Text not found"))