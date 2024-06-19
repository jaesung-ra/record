import pymysql
import requests
from bs4 import BeautifulSoup
import json
from p_tqdm import p_map
from  tqdm.auto import tqdm
import random
import multiprocessing
import time
from nordvpn_switcher import initialize_VPN,rotate_VPN,terminate_VPN
from collections import defaultdict
import os
change_flag=False
pf=open("prob_done.txt","r")
done=pf.readlines()
done=list(map(lambda s: s.strip(),done))
pf.close()
conn = pymysql.connect(host='127.0.0.1', user='root',
                       password='0000', db='recodb', charset='utf8')
cur = conn.cursor()
cur.execute("select code from tmp group by code")
datas = list(list(zip(*cur.fetchall()))[0])
conn.close()


for d in done:
    if d in datas: datas.remove(d)
ef=open("prob_error.txt","r")
done=ef.readlines()
done=list(map(lambda s: s.strip(),done))
ef.close()
for d in done:
    if d in datas: datas.remove(d)

def crawler(params):
    code=params[0]
    flag=params[1]
    lock=params[2]
    print(f"\nPID: {os.getpid()}, {code}     START")
    rand=random.randint(0,201)
    dict=defaultdict(int)
    with requests.session() as session:
        res = session.get(f"https://www.codechef.com/status/{code}?page=0")
        bs = BeautifulSoup(res.text, 'html.parser')
        csrf = bs.findAll("script")[4].text[74:138]
        res=session.post("https://www.codechef.com/api/codechef/login",data={"name":"jsr123","pass":"Dhwltla18~","csrfToken":csrf,"form_id":"ajax_login_form"})
        url = f"https://www.codechef.com/api/submissions/PRACTICE/{code}?limit=20&page=0&usernames=&language=&status="
        header = {
            "authority": "www.codechef.com",
            "path": f"https://www.codechef.com/api/submissions/PRACTICE/{code}?limit=20&page=0&usernames=&language=&status=",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Referer": f"https://www.codechef.com/status/{code}?page=0",
            "X-Csrf-Token": csrf
        }
        payload = {
            "page": 0,
            "limit": 20
        }
        res = session.get(url, headers=header, data=payload)
        if res.status_code==403:
            if flag.value==1:
                while True:
                    print(f"\nPID: {os.getpid()}, SLEEPING..")
                    time.sleep(60)
                    if flag.value==0:
                        time.sleep(60)
                        print(f"\nPID: {os.getpid()}, WAKING..") 
                        break
            else:
                with lock:
                    flag.value=1
                rotate_VPN()
                with lock:
                    flag.value=0
            time.sleep(4)
            res = session.get(f"https://www.codechef.com/status/{code}?page=0")
            bs = BeautifulSoup(res.text, 'html.parser')
            csrf = bs.findAll("script")[4].text[74:138]
            res=session.post("https://www.codechef.com/api/codechef/login",data={"name":"jsr123","pass":"Dhwltla18~","csrfToken":csrf,"form_id":"ajax_login_form"})
            header = {
                "authority": "www.codechef.com",
                "path": f"https://www.codechef.com/api/submissions/PRACTICE/{code}?limit=20&page=0&usernames=&language=&status=",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Referer": f"https://www.codechef.com/status/{code}?page=0",
                "X-Csrf-Token": csrf
            }
            res = session.get(url, headers=header, data=payload)
        try:
            json_res = json.loads(res.text)
            max = int(json_res['count'])
            max_page = max//100
        except:
            print(f"\nPID: {os.getpid()}, ERROR")
            time.sleep(60)
            res=session.get(url,headers=header,data=payload)
            try:
                json_res = json.loads(res.text)
                max = int(json_res['count'])
                max_page = max//100
            except:
                print(f"\nPID: {os.getpid()}, ERROR AGAIN")
                return
            '''
            error_prob_file=open("prob_error.txt","a")
            error_prob_file.write(f"{code}\n")
            error_prob_file.close()
            '''
            return
        if (max % 100 == 0):
            max_page -= 1
        for p in range(0, max_page+1):
            url = f"https://www.codechef.com/api/submissions/PRACTICE/{code}?limit=100&page={p}&usernames=&language=&status="
            header = {
                "authority": "www.codechef.com",
                "path": f"https://www.codechef.com/api/submissions/PRACTICE/{code}?limit=100&page={p}&usernames=&language=&status=",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Referer": f"https://www.codechef.com/status/{code}?page={p}",
                "X-Csrf-Token": csrf
            }
            payload = {
                "page": p,
                "limit": 100
            }
            time.sleep(rand/100)
            res = session.get(url, headers=header, data=payload)
            if res.status_code==403:
                if flag.value==1:
                    while True:
                        print(f"\nPID: {os.getpid()}, SLEEPING..")
                        time.sleep(60)
                        if flag.value==0: 
                            time.sleep(60)
                            print(f"\nPID: {os.getpid()}, RESUMING..")
                            break
                else:
                    with lock:
                        flag.value=1
                    rotate_VPN()
                    with lock:
                        flag.value=0
                    print(f"\nPID: {os.getpid()}, VPN ROATATION FINISHED SLEEPING..")
                    time.sleep(60)
                res = session.get(f"https://www.codechef.com/status/{code}?page=0")
                bs = BeautifulSoup(res.text, 'html.parser')
                csrf = bs.findAll("script")[4].text[74:138]
                res=session.post("https://www.codechef.com/api/codechef/login",data={"name":"jsr123","pass":"Dhwltla18~","csrfToken":csrf,"form_id":"ajax_login_form"})
                header = {
                    "authority": "www.codechef.com",
                    "path": f"https://www.codechef.com/api/submissions/PRACTICE/{code}?limit=20&page=0&usernames=&language=&status=",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                    "Referer": f"https://www.codechef.com/status/{code}?page=0",
                    "X-Csrf-Token": csrf
                }
                res = session.get(url, headers=header, data=payload)
            try:
                jres = json.loads(res.text)
                list = jres['data']
            except:
                print(f"{code} error at page: {p}")
                res=session.get(url,headers=header,data=payload)
                time.sleep(10)
                try:
                    jres=json.laods(res.text)
                    list=jres['data']
                except:
                    print(f"{code} at page: {p} error again")
                    if(p>0):
                        try:
                            conn = pymysql.connect(host='127.0.0.1', user='root',
                                        password='0000', db='recodb', charset='utf8')
                            cur = conn.cursor()
                            for key, value in dict.items():
                                query = "insert into test (username,code,tooltip) values (%s,%s,%s)"
                                if value == 1:
                                    data = (key, code, 'r')
                                else:
                                    data = (key, code, 'w')
                                cur.execute(query, data)
                                conn.commit()
                        finally:
                            conn.close()
                        del dict
                        print(f"{code}     FINISH")
                    error_prob_file=open("prob_done.txt","a")
                    error_prob_file.write(f"{code}\n")
                    error_prob_file.close()
                    return
            for d in list:
                username = d['username']
                tool = d['tooltip']
                if tool == "accepted":
                    dict[username] = 1
                else:
                    dict[username] = 0
    try:
        conn = pymysql.connect(host='127.0.0.1', user='root',
                                            password='0000', db='recodb', charset='utf8')
        cur = conn.cursor()
        for key, value in dict.items():
            query = "insert into test (username,code,tooltip) values (%s,%s,%s)"
            if value == 1:
                data = (key, code, 'r')
            else:
                data = (key, code, 'w')
            cur.execute(query, data)
            conn.commit()
    finally:
        conn.close()
    del dict
    done_prob_file=open("prob_done.txt","a")
    done_prob_file.write(f"{code}\n")
    done_prob_file.close()
    print(f"\nPID: {os.getpid()}, {code}     FINISH")

if __name__ == "__main__":
    initialize_VPN(save=1,area_input=['south korea, japan, germany,united states,united kingdom,canada,singapore,dallas,chicago,atlanta,miami,los angeles,new york,san francisco,seattle,buffalo,saint louis,denver,salt lake city,phoenix'])
    manager=multiprocessing.Manager()
    lock=manager.Lock()
    flag=manager.Value(int,0)
    pool=multiprocessing.Pool(processes=6)
    pool.map(crawler,[(code,flag,lock)for code in done])
    pool.close()
    pool.join()




