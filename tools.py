from telebot.types import ReplyKeyboardMarkup, KeyboardButton

all_mask = ['0.0.0.0', '128.0.0.0', '192.0.0.0',
			'224.0.0.0', '240.0.0.0', '248.0.0.0', 
			'252.0.0.0', '254.0.0.0', '255.0.0.0',
			'255.128.0.0', '255.192.0.0', '255.224.0.0',
			'255.240.0.0', '255.248.0.0', '255.252.0.0',
			'255.254.0.0', '255.255.0.0', '255.255.128.0',
			'255.255.192.0', '255.255.224.0', '255.255.240.0',
			'255.255.248.0', '255.255.252.0', '255.255.254.0',
			'255.255.255.0', '255.255.255.128', '255.255.255.192',
			'255.255.255.224', '255.255.255.240', '255.255.255.248',
			'255.255.255.252', '255.255.255.254', '255.255.255.255']

def check_ip(ip):
	if len(ip) == 4:
		for i in ip:
			if i < 0 or i > 255:
				return False
	else:
		return False
	return True
	
def check_mask(mask):
	if mask in all_mask:
		return True
	return False

def get_str_from(src_list):
	string = '.'.join(str(x) for x in src_list)
	return string
	
def get_mask_markup():
	mask_markup = ReplyKeyboardMarkup(row_width = 1)
	i = 0
	while i < len(all_mask):
		button_content = all_mask[i] + ' /' + str(i)
		mask_markup.add(button_content)
		i += 1
	return mask_markup


	