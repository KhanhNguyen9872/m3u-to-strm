# KhanhNguyen9872
import requests, os, random, datetime, threading

def random_str(length = 8):
	return ''.join([random.choice('qwertyuiopasdfghjklzxcvbnm') for i in range(length)])

def mkdir(folder):
	try:os.mkdir(folder)
	except:pass

data_m3u = open(input('m3u file: '), 'rb').read().decode('utf8').split('\n')
is_download_logo = (True if input("Add with Logo? [Y/n]: ").lower() == "y" else False)

working_dir = str(datetime.datetime.now()).split('.')[0]
mkdir(working_dir)
os.chdir(working_dir)

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
		
		print(">> Added: {}".format(single_data['tvg-name']))
		single_data = {}

def download_logo(link, path, name):
	open(path, 'wb').write(requests.get(link).content)
	print(">> Downloaded Logo [{}]".format(name))

multi_group = {}
for target in group:
	if group[target]['group-title'] in multi_group:
		multi_group[group[target]['group-title']].append(group[target])
	else:
		multi_group[group[target]['group-title']] = [group[target]]

for group in multi_group:
	mkdir(group)
	for each in multi_group[group]:
		mkdir(group + "/" + each['tvg-name'])
		open(group + "/" + each['tvg-name'] + "/" + each['tvg-name'] + '.strm', 'w').write(each['tvg-url'])
		if is_download_logo:
			try:
				threading.Thread(target=download_logo, args=(each['tvg-logo'], group + "/" + each['tvg-name'] + "/" + each['tvg-name'] + '.tbn', each['tvg-name'], )).start()
			except KeyError:
				pass
