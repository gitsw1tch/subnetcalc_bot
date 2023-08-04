import telebot
import tools
from tools import get_str_from as gsf
from configs import TOKEN


bot = telebot.TeleBot(TOKEN)

text_get_ip = 'Enter IP address (i.e. 192.168.0.1)'
text_get_mask = 'Choose subnet mask'

temp = {} #{message.from_user.id: {'ip': iplist} -> to save ip for next handler

@bot.message_handler(commands = ['start'])
def start(message):
	bot.send_message(message.chat.id, text_get_ip)

@bot.message_handler(content_types = ['text'])
def get_ip(message):
	try:
		ip = message.text.split('.')    #'1.1.1.1' -> ['1', '1', '1', '1']
		ip = list(map(int, ip))         #['1', '1', '1', '1'] -> [1, 1, 1, 1]
		if tools.check_ip(ip):
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
		mask = message.text.partition('/')[0].strip()     #'255.255.255.255 /32' -> '255.255.255.255'
		if tools.check_mask(mask):
			mask = list(map(int, mask.split('.')))        #'255.255.255.255' -> [255, 255, 255, 255]               
			ip = temp[message.from_user.id]['ip']
			network_addr = [x & y for x, y in zip(ip, mask)]			
			inversed_mask = [255 - x for x in mask]
			broadcast_addr = [x + y for x, y in zip(network_addr, inversed_mask)]
			content = ('IP: {}\n'
						'Subnet Mask: {}\n'
						'Network Address: {}\n'
						'Broadcast Address: {}\n').format(gsf(ip), gsf(mask), gsf(network_addr), gsf(broadcast_addr))
			bot.send_message(message.chat.id, content)
			temp.pop(message.from_user.id) #clear temp
		else:
			msg = bot.reply_to(message, 'Error! ' + text_get_mask, reply_markup = tools.get_mask_markup())
			bot.register_next_step_handler(msg, get_mask)
	except Exception:
		msg = bot.reply_to(message, 'Error! ' + text_get_mask, reply_markup = tools.get_mask_markup())
		bot.register_next_step_handler(msg, get_mask)
		
bot.infinity_polling()