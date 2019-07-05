#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from instabot import Bot
import time
import requests
import json

start_time = time.time()
bot = Bot()
session = requests.Session()
//specify the username and password
passwd=""
user=""
bot.login(username=user, password=passwd)
//add the id of a profile that you want to scrap
followers = bot.get_user_following(***)
with open('csvfile3.csv','w') as file:
    for follower in followers:
        username_info = session.get('https://i.instagram.com/api/v1/users/'+follower+'/info')
        info_json_format = json.loads(username_info.text)
        if 'user' in info_json_format:
            username = json.dumps(info_json_format['user']['username'])
            file.write(username)
            file.write('\n')
            print(username)
elapsed_time = time.time() - start_time
print(elapsed_time)

