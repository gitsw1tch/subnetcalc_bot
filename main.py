import telebot
from telebot.types import ReplyKeyboardRemove
import tools
from configs import TOKEN


bot = telebot.TeleBot(TOKEN)

text_get_ip = 'Enter IPv4 address (e.g. 192.168.0.1)'
text_get_mask = 'Choose subnet mask'

temp = {} #{message.from_user.id: {'ip': [1, 1, 1, 1]} -> save requested ip for next handler 

@bot.message_handler(commands = ['start'])
def start(message):
	bot.send_message(message.chat.id, text_get_ip, reply_markup = ReplyKeyboardRemove())
	
@bot.message_handler(content_types = ['text'])
def get_ip(message):
	try:
		ip = list(map(int, message.text.split('.')))				#'1.1.1.1' -> [1, 1, 1, 1]
		if tools.check_ip(ip):
			#save ip for next handler
			request_ip = {message.from_user.id: {'ip': ip}}
			temp.update(request_ip)
			msg = bot.send_message(message.chat.id, text_get_mask, reply_markup = tools.get_mask_markup())
			bot.register_next_step_handler(msg, get_mask)	
		else:
			bot.reply_to(message, 'Error! ' + text_get_ip)
	except Exception:
		bot.reply_to(message, 'Error! ' + text_get_ip)
	
def get_mask(message):
	try:
		mask = message.text.partition('/')[0].strip()	#'255.255.255.255 /32' -> ['255.255.255.255']
		if tools.check_mask(mask):
			mask = list(map(int, mask.split('.')))		#['255.255.255.255'] -> [255, 255, 255, 255]			
			ip = temp[message.from_user.id]['ip']
			temp.pop(message.from_user.id) #clear temp
			bot.send_message(message.chat.id, tools.get_info(ip, mask), reply_markup = ReplyKeyboardRemove())
			bot.send_message(message.chat.id, text_get_ip)
		else:
			msg = bot.reply_to(message, 'Error! ' + text_get_mask, reply_markup = tools.get_mask_markup())
			bot.register_next_step_handler(msg, get_mask)
	except Exception:
		msg = bot.reply_to(message, 'Error! ' + text_get_mask, reply_markup = tools.get_mask_markup())
		bot.register_next_step_handler(msg, get_mask)
		
bot.infinity_polling()