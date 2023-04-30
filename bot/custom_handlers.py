from telegram import (
    Update
)
from telegram.ext import (
    CallbackContext,
    filters
)
import yaml, sys, os


# def update_user_filter():
#     with open('config/config.yml', 'r') as file:
#         config = yaml.load(file, Loader=yaml.SafeLoader)
#     value = config['allowed_telegram_usernames']
#     user_filter = filters.ALL
#     user_filter = filters.User(username=value)
#     return user_filter


async def allow_user(update: Update, context: CallbackContext)->None:
    username: str = ((update.message.text).split(' '))[1]
    if '@' in username: username = username.replace('@','')
    with open('config/config.yml', 'r') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    
    value = config['allowed_telegram_usernames']
    if len(value) == 0: 
        value = [username]
        config["allowed_telegram_usernames"] = value
    else:
        for user in value:
            if user == username:
                await update.message.reply_text(f'✔️ @{username} уже есть в списке!')
                return
        value.append(username)
        config["allowed_telegram_usernames"] = value
    
    with open('config/config.yml', 'w') as file:
        yaml.dump(config, file, default_flow_style=None, sort_keys=False)
   
    await update.message.reply_text(f'✅ @{username} добавлен! Перезапускаю бота.')
    # Получаем полный путь к текущему скрипту
    script_path = os.path.abspath(sys.argv[0])
    # Вызываем новый экземпляр текущего скрипта
    os.execl(sys.executable, sys.executable, script_path, *sys.argv[1:])