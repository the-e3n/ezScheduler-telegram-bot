from bot.modules.scrapper import eztv_scrapper
from bot.modules.help import help
from config import *
from bot.modules.fs import *
from bot.modules.commands import BotCommand
from bot.modules.downloader import download
from bot.modules.show_filter import show_filter
from bot import OWNER_ID, BASE_DIR, url, updater, dispatcher, LOGGER
from telegram.ext import CommandHandler


def start(update, context):
    bot = context.bot
    user_id = update.effective_user.id
    user_config = fs_read(os.path.join(BASE_DIR, 'user_config.json'))
    user_config['id'] = user_id
    fs_create(os.path.join(BASE_DIR, f'users/{user_id}.json'), user_config)
    bot.send_message(chat_id=update.effective_chat.id, text=help.StartText)


def latest(update, context):
    bot = context.bot
    msg = ''
    result = eztv_scrapper(url)
    if not result:
        bot.send_message(update.effective_chat.id, text='Cannot connect to the server to get updates.')
        return
    checking = bot.send_message(chat_id=update.effective_chat.id, text='Checking')
    for k, v in enumerate(result, 1):
        msg += f'Episode_{k}: {v}\n'
    print(len(msg))
    last = bot.send_message(chat_id=update.effective_chat.id, text=msg)
    checking.delete()
    bot.send_message(chat_id=update.effective_chat.id, text='Thats all the new ones', reply_to_message_id=last.message_id)


def add_show(update, context):
    bot = context.bot
    show = ''
    config_dir = os.path.join(BASE_DIR, f'users/{update.effective_user.id}.json')
    user_config = fs_read(config_dir)
    if context.args:
        for arg in context.args:
            show += f' {arg}'
        if show.strip().lower() not in user_config['shows']:
            user_config['shows'].append(show.strip().lower())
            fs_update(config_dir, user_config)
            bot.send_message(chat_id=update.effective_chat.id, text=f"Added {show.strip()}")
        else:
            bot.send_message(chat_id=update.effective_chat.id, text=f"Already added {show.strip()}")
    else:
        bot.send_message(chat_id=update.effective_chat.id, text='\n'.join(user_config['shows']) or help.AddText)


def remove_show(update, context):
    bot = context.bot
    show = ''
    config_dir = os.path.join(BASE_DIR, f'users/{update.effective_user.id}.json')
    user_config = fs_read(config_dir)
    if context.args:
        for arg in context.args:
            show += f' {arg}'
        if show.strip().lower() in user_config['shows']:
            user_config['shows'].remove(show.strip().lower())
            fs_update(config_dir, user_config)
            bot.send_message(chat_id=update.effective_chat.id, text=f"Removed {show.strip()} from alarm list")
        else:
            bot.send_message(chat_id=update.effective_chat.id, text=f"{show.strip()} is not in alarm list")
    else:
        bot.send_message(chat_id=update.effective_chat.id, text=help.RemoveText)



def reset(update, context):
    config_dir = os.path.join(BASE_DIR, f'users/{update.effective_user.id}.json')
    fs_unlink(config_dir)
    user_config = fs_read(os.path.join(BASE_DIR, 'user_config.json'))
    user_config['id'] = update.effective_user.id
    fs_create(config_dir, user_config)
    job_removed = remove_job_if_exists(str(update.effective_user.id), context)
    if job_removed:
        update.message.reply_text('All of your settings have been reset')
    update.message.reply_text('All of your settings have been reset')


def hello(update, context):
    context.bot.send_message(update.effective_chat.id, text=f'Hello Human, {update.effective_user.first_name} {update.effective_user.last_name}\nI am ezScheduler')


def set_quality(update, context):
    bot = context.bot
    config_dir = os.path.join(BASE_DIR, f'users/{update.effective_user.id}.json')
    user_config = fs_read(config_dir)
    if context.args:
        user_config['quality'] = context.args[0]
        fs_update(config_dir, user_config)
        bot.send_message(chat_id=update.effective_chat.id, text=f"Quality Set to {user_config['quality']}")
    else:
        bot.send_message(chat_id=update.effective_chat.id, text=f'{help.SetQualityText}\nDefault quality is {user_config["quality"]}')


def list_match(update, context):
    config_dir = os.path.join(BASE_DIR, f'users/{update.effective_user.id}.json')
    user_config = fs_read(config_dir)
    result = eztv_scrapper(url)
    msg = '\n'.join(show_filter(user_config['shows'], result, user_config['quality']))
    if msg:
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Either No match Found or you haven\'t added show')
        context.bot.send_message(chat_id=update.effective_chat.id, text='Add Using /add [shows]')
        context.bot.send_message(chat_id=update.effective_chat.id, text=help.ListText)


def help_message(update, context):
    context.bot.send_message(update.effective_chat.id, text=help.HelpText)


def myshows(update, context):
    config_dir = os.path.join(BASE_DIR, f'users/{update.effective_user.id}.json')
    user_config = fs_read(config_dir)
    msg = '\n'.join(user_config['shows'])
    if msg:
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You haven\'t added show')
        context.bot.send_message(chat_id=update.effective_chat.id, text='Add Using /add [shows]\nUse /help to learn more')


def send_file_to_user(chat_id, context, file):
    bot = context.bot
    if file:
        with open(file, 'rb') as f:
            last = bot.send_document(document=f.read(), chat_id=chat_id, filename=file)
            bot.send_message(chat_id, f'New Episode of your show')


def refresh(context):
    job = context.job
    user_id = job.context
    config_dir = os.path.join(BASE_DIR, f'users/{user_id[0]}.json')
    user_config = fs_read(config_dir)
    result = eztv_scrapper(url)
    shows = user_config['shows']
    eps = show_filter(shows, result, quality=user_config['quality'])
    for ep in eps:
        if ep not in user_config['done']:
            ep = result[ep]
            context.bot.send_message(job.context[1], text=f'New Episode of show {ep["show"]} in {user_config["quality"]}')
            context.bot.send_message(job.context[1], text=f'Sending You the file')
            dest = download(ep)
            if dest:
                send_file_to_user(job.context[1], context, dest)
                user_config['done'].append(ep['name'])
                fs_update(config_dir, user_config)


def stop_daemon(update, context):
    current_jobs = context.job_queue.get_jobs_by_name(str(update.effective_user.id))
    if not current_jobs:
        context.bot.send_message(update.effective_chat.id, text=f'You have already stopped the service')
        return
    for job in current_jobs:
        job.schedule_removal()
    context.bot.send_message(update.effective_chat.id, text=f'You will not recieve any further update.\nUse /run to get updates')


def remove_job_if_exists(name: str, context) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def daemon(update, context):
    user_id = update.effective_user.id, update.message.chat_id
    print(user_id)
    job_removed = remove_job_if_exists(str(user_id[0]), context)
    context.job_queue.run_repeating(refresh, POLL_TIME, context=user_id, name=str(user_id[0]))
    text = 'Successfully Running'
    if job_removed:
        text += '\nOld one was removed.'
    update.message.reply_text(text)


def error_handler(update, context):
    print(context.error)
    LOGGER.info(context.error)
    raise context.error

def main():
    start_handler = CommandHandler(BotCommand.StartCommand, start)
    dispatcher.add_handler(start_handler)

    hello_handler = CommandHandler('hello', hello)
    dispatcher.add_handler(hello_handler)

    help_handler = CommandHandler(BotCommand.HelpCommand, help_message)
    dispatcher.add_handler(help_handler)

    latest_handler = CommandHandler(BotCommand.LatestCommand, latest)
    dispatcher.add_handler(latest_handler)

    add_show_handler = CommandHandler(BotCommand.AddCommand, add_show)
    dispatcher.add_handler(add_show_handler)

    add_show_handler = CommandHandler(BotCommand.MyShowsCommand, add_show)
    dispatcher.add_handler(add_show_handler)

    remove_show_handler = CommandHandler(BotCommand.RemoveCommand, remove_show)
    dispatcher.add_handler(remove_show_handler)

    list_match_handler = CommandHandler(BotCommand.ListCommand, list_match)
    dispatcher.add_handler(list_match_handler)

    quality_handler = CommandHandler(BotCommand.SetQualityCommand, set_quality)
    dispatcher.add_handler(quality_handler)

    reset_handler = CommandHandler(BotCommand.ResetCommand, reset)
    dispatcher.add_handler(reset_handler)

    daemon_handler = CommandHandler(BotCommand.RunCommand, daemon, pass_job_queue=True)
    dispatcher.add_handler(daemon_handler)

    stop_handler = CommandHandler(BotCommand.StopCommand, stop_daemon, pass_job_queue=True)
    dispatcher.add_handler(stop_handler)

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


main()