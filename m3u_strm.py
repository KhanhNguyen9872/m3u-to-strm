# KhanhNguyen9872
import os, random, datetime, threading, time

try:
	import requests
except:
	os.system("{} -m pip install requests".format(__import__('sys').executable))
	import requests

def random_str(length = 8):
	return ''.join([random.choice('qwertyuiopasdfghjklzxcvbnm') for i in range(length)])

def mkdir(folder):
	try:os.mkdir(folder)
	except:pass

def replace_name(name):
	return str(name.replace(":", "-").replace("|", "_").replace("?", "_").replace("<", "(").replace(">",")").replace("/", "_").replace("\\", "_").replace("*", "_").replace("\"", "'"))

def download_logo(link, path, name, timeout):
	if globals()["is_thread_download"]:
		time.sleep(timeout)
	open(path, 'wb').write(requests.get(link).content)
	print(">> Downloaded Logo [{}]".format(name))

file_name = input('m3u file: ')
data_m3u = open(file_name, 'rb').read().decode('utf8').split('\n')
is_download_logo = (True if input("Add with logo? [Y/n]: ").lower() == "y" else False)
if is_download_logo:
	is_thread_download = (True if input("Download logo with multi thread? (Recommend: Y) [Y/n]: ").lower() == "y" else False)

working_dir = replace_name("/".join(file_name.split('\\')).split("/")[-1].split(".")[0]) + "_" + replace_name(str(datetime.datetime.now()).split('.')[0]).replace(" ", "_")
default_group = 'tvshows'

switch_name_value = 0
lock_str = 0
name = ''
value = ''
single_data = []
group = {}

for line in data_m3u:
	if line.replace('\r', '') == '':
		continue
	if line[0] == '#':
		name = ''
		value = ''
		tv_name = ''
		if '#EXTINF:' in line.split(' ')[0]:
			single_data = {}
			switch_name_value = 0
			lock_str = 0
			line = ' '.join(line.split(' ')[1:])
		else:
			continue

		for char in line:
			if switch_name_value:
				if char == '"' or char == "'":
					lock_str = not lock_str
					continue
				if lock_str:
					value += char
				elif char == ' ':
					single_data[name] = value
					switch_name_value = 0
					name = ''
					value = ''
				elif char == ',':
					single_data[name] = value
					single_data['tvg-name'] = line.split(',')[-1].strip()
					break
			else:
				if char != '=':
					name += char
				else:
					switch_name_value = 1
	else:
		if "http://" == line[:7] or "https://" == line[:8] or "mms://" == line[:6] or "rtsp://" == line[:7] or r"\\" == line[:2] or ":/" == line[1:3] or ":\\" == line[1:3]:
			single_data['tvg-url'] = line.replace('\r', '')
			try:
				single_data['group-title']
			except KeyError:
				single_data['group-title'] = default_group
			try:
				single_data['tvg-name']
			except KeyError:
				single_data['tvg-name'] = random_str()
			try:
				group[single_data['tvg-name']] = single_data
			except KeyError:
				try:
					group[single_data['tvg-id']] = single_data
				except KeyError:
					group[random_str()] = single_data
			
			print(">> Added: {} [Group: {}]".format(single_data['tvg-name'], single_data['group-title']))
			single_data = {}

multi_group = {}
for target in group:
	if group[target]['group-title'] in multi_group:
		multi_group[group[target]['group-title']].append(group[target])
	else:
		multi_group[group[target]['group-title']] = [group[target]]

mkdir(working_dir)
os.chdir(working_dir)

for group in multi_group:
	mkdir(replace_name(group))
	for each in multi_group[group]:
		mkdir(replace_name(group) + "/" + replace_name(each['tvg-name']))
		open(replace_name(group) + "/" + replace_name(each['tvg-name']) + "/" + replace_name(each['tvg-name']) + '.strm', 'w').write(each['tvg-url'])
		if is_download_logo:
			try:
				if is_thread_download:
					threading.Thread(target=download_logo, args=(each['tvg-logo'], replace_name(group) + "/" + replace_name(each['tvg-name']) + "/" + replace_name(each['tvg-name']) + '.tbn', each['tvg-name'], random.randint(0, 3), )).start()
				else:
					download_logo(each['tvg-logo'], replace_name(group) + "/" + replace_name(each['tvg-name']) + "/" + replace_name(each['tvg-name']) + '.tbn', each['tvg-name'], 0)
			except KeyError:
				pass

while 1:
	if threading.active_count() == 1:
		input(">> Done! ({})".format(working_dir))
		break
	time.sleep(1)