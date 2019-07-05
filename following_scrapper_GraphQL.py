import http.clientimport json
import random
import time
from datetime import datetime, timedelta
import time
import requests
import requests.utils

def do_sleep():
    time.sleep(min(random.expovariate(0.7), 5.0))
    
def authorization(user, passwd):
    http.client._MAXHEADERS = 200
    session = requests.Session()
    session.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                            'ig_vw': '1920', 'ig_cb': '1', 'csrftoken': '',
                            's_network': '', 'ds_user_id': ''})
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"})
    session.get('https://www.instagram.com/web/__mid/')
    csrf_token = session.cookies.get_dict()['csrftoken']
    session.headers.update({'X-CSRFToken': csrf_token})
    do_sleep()
    login = session.post('https://www.instagram.com/accounts/login/ajax/',
                         data={'password': passwd, 'username': user}, allow_redirects=True)
    try:
        resp_json = login.json()
    except json.decoder.JSONDecodeError:
        raise Exception()
    if resp_json.get('two_factor_required'):
        two_factor_session = copy_session(session)
        two_factor_session.headers.update({'X-CSRFToken': csrf_token})
        two_factor_session.cookies.update({'csrftoken': csrf_token})
        self.two_factor_auth_pending = (two_factor_session,
                                        user,
                                        resp_json['two_factor_info']['two_factor_identifier'])
        raise Exception()
    if resp_json.get('checkpoint_url'):
        raise Exception()
    if resp_json['status'] != 'ok':
        if 'message' in resp_json:
            raise Exception(resp_json['message'])
    if resp_json['authenticated'] == False:
            raise Exception('not authenticated')
    session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
    return session

def followParser(userID, session):
    hasNext = True
    isFirstRequest = True
    after = ""
    users = []
    request_number = 0
    start_time = time.time()
    query_hash = "d04b0a864b4b54837c0d870b0e77e076"
    while hasNext:
        if isFirstRequest:
            url = 'https://www.instagram.com/graphql/query/?query_hash='+query_hash+'&variables={"id":"'+userID+'","include_reel":true,"fetch_mutual":false, "first":100 }' 
            isFirstRequest = False
        else:
            url = 'https://www.instagram.com/graphql/query/?query_hash='+query_hash+'&variables={"id":"'+userID+'","include_reel":true,"fetch_mutual":false,"first":100,"after":"'+after+'" }'

        r = session.get(url)
        json_format = json.loads(r.text)
        after = json_format['data']['user']['edge_follow']['page_info']['end_cursor']
        users = users + json_format['data']['user']['edge_follow']['edges']
        hasNext = json_format['data']['user']['edge_follow']['page_info']['has_next_page']
        request_number += 1
        time.sleep(2)
        if request_number == 20:
            time.sleep(60*10)
    elapsed_time = time.time() - start_time
    print(elapsed_time)
    return users

def main():
    passwd = "12345abc"
    user = "eero.tamm"
    session = authorization(user, passwd)
    r = session.get("https://www.instagram.com/promoty.eu/?__a=1")
    json_format = json.loads(r.text)
    userID = json_format['graphql']['user']['id']
    users = followParser(userID, session)
    with open('csvfile2.csv','w') as file:
        for user in users:
            file.write(user['node']['username'])
            file.write('\n')
if __name__ == '__main__':
    main()


# In[ ]:




