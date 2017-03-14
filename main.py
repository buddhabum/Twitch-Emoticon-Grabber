import urllib.request
import os
import json
import multiprocessing.dummy as mp
import concurrent.futures
from collections import Counter
from collections import defaultdict
import time
import json
from multiprocessing.pool import ThreadPool as Pool

printme = True #Disable print statements if you'd like to save CPU time
dataFile = False #Enable this if you'd like to have the JSON the api returns
count = 0
pool_size = 300  # Lower this if you have a weak CPU or internet connection. Default downloads at ~1.6MB/s and 90% CPU usage on an i5 3570k
pool = Pool(pool_size)

#Calculate Runtime
start = time.time()


if not os.path.exists('./emotes'):
	os.makedirs('./emotes')

print('Saving emotes to folder: ' + os.path.abspath('./emotes') + '...')
print('Grabbing emote list...')

emotes = json.load(urllib.request.urlopen('https://api.twitch.tv/kraken/chat/emoticons/'))


#Pretty Print the JSON
if(dataFile):
	if not os.path.exists('data.txt'):
		with open('data.txt', 'w') as outfile:
			json.dump(emotes, outfile, sort_keys=True,indent=4, separators=(',',': '))

def my_op(emote):
	global count
	code = emote['regex']
	number = emote['images'][0]['emoticon_set']
	
	try:
		parentPath = './emotes/'+str(number)
		if not os.path.exists(parentPath):
			os.makedirs(parentPath)
		filePath = './emotes/'+str(number) +'/'+str(code)+'.png'
		if not os.path.exists(filePath):
			if(printme):
				print('Downloading: ' + str(code) + ' in ... ' + filePath)
			urllib.request.urlretrieve(emote['images'][0]['url'], filePath)
			count+=1
		else:
			if(printme):
				print('skipped')
		
		
	except Exception as e: 
			print(e)

			
for emote in emotes['emoticons']: 
	pool.apply_async(my_op, (emote,))
	
pool.close()
pool.join()


end = time.time()
print('Downloaded ' +str(count) +' new files')
print('Running time: ' + str(end - start))




