import ptbot

import os 

from pytimeparse import parse

from dotenv import load_dotenv


load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")


bot = ptbot.Bot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, chat_id, message_id, total):
	remained = total - secs_left
	progress = render_progressbar(total, remained)
	if secs_left > 0:
		bot.update_message(chat_id, message_id,
			"{0}\nОсталось {1} секунд".format(progress, secs_left))
	else:
		bot.update_message(chat_id, message_id,
			"{0}\nВремя вышло!".format(progress))


def timer(chat_id, message):
	delay = parse(message)
	if delay is None or delay <= 0:
		return
	message_id = bot.send_message(chat_id, 
		"Запускаю таймер на {0} секунд".format(delay))

	
	for sec in range(delay, 0, -1):
		notify_progress(sec, chat_id, message_id, delay)
		time.sleep(1)
	notify_progress(0, chat_id, message_id, delay)


def main():
	bot.reply_on_message(timer)
	bot.run_bot()


if __name__ == '__main__':
    main()