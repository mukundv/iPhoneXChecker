import codecs
import datetime
import json
import sys
import time
from urllib.error import URLError, HTTPError
from urllib.request import urlopen, Request

from pushbullet import Pushbullet, InvalidKeyError

avail_url = "https://reserve-prime.apple.com/AU/en_AU/reserve/iPhoneX/availability.json"
interested_stores = ['R504', 'R180', 'R342', 'R530', 'R343']  # Melbourne stores only
store_names = {'R504': 'Highpoint', 'R180': 'Chadstone', 'R342': 'Doncaster', 'R530': 'Fountain Gate',
               'R343': 'Southland'}
model_names = {'MQA92X/A': 'Silver 256GB', 'MQA82X/A': 'Space Grey 256GB'}
interested_models = ['MQA92X/A', 'MQA82X/A']  # 256 Silver, 256 Grey
pushbullet_apiKey = 'API_KEY'
reader = codecs.getreader("utf-8")
headers = {'User-Agent': 'Mozilla/5.0'}
store = ''
model = ''
arg1 = sys.argv[1]

while True:
    count = 0
    try:
        res = urlopen(Request(avail_url, headers=headers))
    except HTTPError as e:
        print('Error calling url. Error code: ', e.code)
    except URLError as e:
        print('Error calling url. Error reason: ', e.reason)
    else:
        dat = json.load(reader(res))
        updated = datetime.datetime.fromtimestamp(float(str(dat['updated'])[0:-3]))

        print('Checking for availability at {1}. Last updated: {0}'.format(str(updated), str(datetime.datetime.now(

        ).strftime('%Y-%m-%d %H:%M:%S'))))
        for k, v in dat['stores'].items():
            if k in interested_stores:  # If store is in list
                for i, s in v.items():
                    if i in interested_models:  # if model is in list
                        for x, y in s['availability'].items():
                            if y:  # Either the contract or unlocked = True
                                count += 1
                                store = store_names[k]  # Name of store
                                model = model_names[i]  # Name of model

    if count > 0:  # If available, send push
        push_text = '{1} is available in {0} available. Go to {2}?channel=1'.format(store, model, avail_url[:-5])
        print(push_text)
        try:
            pb = Pushbullet(pushbullet_apiKey)
        except InvalidKeyError as e:
            print("Invalid Push Bullet API Key: {0}".format(pushbullet_apiKey))
        else:
            push = pb.push_note('iPhoneX available', push_text)

    time.sleep(int(arg1))  # time to sleep
