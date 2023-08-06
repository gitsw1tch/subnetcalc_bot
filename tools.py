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
	if len(ip) != 4:
		return False
	else:
		for i in ip:
			if i < 0 or i > 255:
				continue
	return True
	
def check_mask(mask):
	if mask in all_mask:
		return True
	return False
	
def get_mask_markup():
	mask_markup = ReplyKeyboardMarkup(row_width = 1)
	i = 0
	while i < len(all_mask):
		button_content = all_mask[i] + ' /' + str(i)
		mask_markup.add(button_content)
		i += 1
	return mask_markup	

def get_str_from(any_list):
	string = '.'.join(str(x) for x in any_list)
	return string 

def make_content(ip, mask, network_addr, broadcast_addr, ip_range):
	content = ('IP address: {}' + 
			   '\nSubnet Mask: {}' +
			   '\nNetwork address: {}' +
		       '\nBroadcast address: {}' + 
			   '\nUsable IP range: {}').format(get_str_from(ip),
											   get_str_from(mask),
											   get_str_from(network_addr),
											   get_str_from(broadcast_addr),
											   ip_range)
	return content							  
	
def get_info(ip, mask):
		network_addr = [x & y for x, y in zip(ip, mask)]
		inversed_mask = [255 - x for x in mask]		
		broadcast_addr = [x + y for x, y in zip(network_addr, inversed_mask)]	
		if mask[3] == 255 or mask[3] == 254:
			ip_range = 'N/A'		
		else:
			first_addr = network_addr.copy()
			first_addr[3] = str(int(first_addr[3]) + 1)
			last_addr = broadcast_addr.copy()
			last_addr[3] = str(int(last_addr[3]) - 1)
			ip_range = get_str_from(first_addr) + ' - ' + get_str_from(last_addr)
		content = make_content(ip, mask, network_addr, broadcast_addr, ip_range)
		return content