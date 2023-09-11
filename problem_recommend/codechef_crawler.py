import requests
from bs4 import BeautifulSoup
import json
import csv
from collections import defaultdict
from p_tqdm import p_map
from tqdm.auto import tqdm
import time
from datetime import datetime
def crawler(username):
    # dictionary that holds user,code, and submission data
    csv_file=open('record.csv','a',newline="")
    writer=csv.writer(csv_file)
    code_dict=defaultdict(str)  
    PAGE=0
    user=username.strip()
    url=f"https://www.codechef.com/recent/user?page={PAGE}&user_handle={user}"
    header={
            "authority": "www.codechef.com",
            "path": f"/recent/user?page={PAGE}&user_handle={user}",
            "referer": f"https://www.codechef.com/users/{user}"
        }
    payload={
            "page":PAGE,
            "user_handle":user
        }
    with requests.session() as session:
            
            while True:
                try:
                    res=session.get(url,headers=header,data=payload)
                    json_res=json.loads(res.text)
                except:
                    log_file=open("log.txt","a")
                    date=datetime.today().strftime("%Y/%m/%d %H:%M:%S")  
                    log_file.write(f"{date}: {user}, first exception\n")
                    log_file.close()
                    time.sleep(1800)
                break
            max_page=json_res["max_page"]
            for i in range(max_page):
                PAGE=i
                url=f"https://www.codechef.com/recent/user?page={PAGE}&user_handle={user}"
                header={
                    "authority": "www.codechef.com",
                    "path": f"/recent/user?page={PAGE}&user_handle={user}",
                    "referer": f"https://www.codechef.com/users/{user}"
                }
                payload={
                    "page":PAGE,
                    "user_handle":user
                }
                while True:
                    try:
                        res=session.get(url,headers=header,data=payload)
                        json_res=json.loads(res.text)
                    except:
                        log_file=open("log.txt","a")
                        date=datetime.today().strftime("%Y/%m/%d %H:%M:%S") 
                        log_file.write(f"{date}: {user}, {PAGE}, second exception\n")
                        log_file.close()
                        time.sleep(1800)
                    break
                soup=BeautifulSoup(json_res["content"],"html.parser")
                tr=soup.find_all("a",class_=False)
                for item in tr:
                    code=item.get_text()
                    if item.get("target") is None:
                        break
                    if code not in probs:
                        continue
                    img=item.parent.parent.select_one("img")["src"]
                    if img=="https://cdn.codechef.com/misc/tick-icon.gif":
                        code_dict[code]="1"+code_dict[code]
                    else:
                        code_dict[code]="0"+code_dict[code]
            for code,score in code_dict.items():
                data=[user,code,score]
                writer.writerow(data)
            user_done_file=open("user_done.txt","a")
            user_done_file.write(f"{user}\n")
            user_done_file.close()
            csv_file.close()
    del code_dict
                
# opening and loading data and storing them in global variables #

prob_file=open("probs.txt","r")
probs=prob_file.readlines()
probs = list(map(lambda s: s.strip(), probs))
prob_file.close()
user_file=open("left_users4.txt","r")
users=user_file.readlines()
user_number=len(users)
user_file.close()

if __name__=="__main__":
    # using multiprocess with 8 cpus, and showing progress bar #
    # only shows the progress bar of the total process #
    # future adjustments: show the progress bar for each 8 multi-processes #
    num_cpus=8
    p_map(crawler,users,**{"num_cpus": num_cpus})