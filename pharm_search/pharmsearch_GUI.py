import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QBrush,QColor
import json
from urllib.parse import urljoin
import unicodedata
import requests
from bs4 import BeautifulSoup
import datetime as dt
from urllib import parse
import os
date=dt.datetime.now()
DATE=date.strftime("%Y-%m-%d")
USER="2021091"
PASS="2021091"
PAEKJAE_PWD="yoon2736"
class MyTableWidget(QTableWidget) :
        def table_insert(self,item):
            currentRowCount = self.rowCount() #necessary even when there are no rows in the table
            self.insertRow(currentRowCount)
            self.setItem(currentRowCount,0,QTableWidgetItem(item[0]))
            self.setItem(currentRowCount,1,QTableWidgetItem(item[1]))
            self.setItem(currentRowCount,2,QTableWidgetItem(item[2]))
            self.setItem(currentRowCount,3,QTableWidgetItem(item[3]))
            if item[3]=="품절":
                self.item(currentRowCount, 3).setForeground(QBrush(QColor(255,0,0)))
            else:
                self.item(currentRowCount, 3).setForeground(QBrush(QColor(0,0,255)))
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid=QGridLayout()
        container=QHBoxLayout()
        container.addStretch(1)
        self.setLayout(grid)
        self.search_bar=QLineEdit(self)
        self.search_btn=QPushButton("검색")
        self.search_bar.returnPressed.connect(self.search_clicked)
        self.search_btn.clicked.connect(self.search_clicked)
        container.addWidget(self.search_bar)
        container.addWidget(self.search_btn)
        container.addStretch(1)

        self.boksan_label=QLabel()
        self.boksan_label.setText('<a href="http://wos.nicepharm.com/Contents/Main/Main9.asp">복산나이스팜</a>')
        self.incheon_label=QLabel()
        self.incheon_label.setText('<a href="http://inchunpharm.com/homepage/contents/login/login.asp">인천약품</a>')
        self.TJ_label=QLabel()
        self.TJ_label.setText('<a href="http://tjp.co.kr/login.php?login_p=2">티제이약품</a>')
        self.baekjae_label=QLabel()
        self.baekjae_label.setText('<a href="https://www.ibjp.co.kr/ord/comOrd.act">백제약품</a>')
        self.boksan_label.setOpenExternalLinks(True)
        self.incheon_label.setOpenExternalLinks(True)
        self.TJ_label.setOpenExternalLinks(True)
        self.baekjae_label.setOpenExternalLinks(True)
        table_labels=["이름","용량","가격","재고"]
        self.boksan_table=MyTableWidget()
        self.boksan_table.setColumnCount(4)
        self.boksan_table.setRowCount(0)
        
        self.incheon_table=MyTableWidget()
        self.incheon_table.setColumnCount(4)
        self.incheon_table.setRowCount(0)

        self.TJ_table=MyTableWidget()
        self.TJ_table.setColumnCount(4)
        self.TJ_table.setRowCount(0)

        self.baekjae_table=MyTableWidget()
        self.baekjae_table.setColumnCount(4)
        self.baekjae_table.setRowCount(0)

        self.boksan_table.setHorizontalHeaderLabels(table_labels)
        self.incheon_table.setHorizontalHeaderLabels(table_labels)
        self.TJ_table.setHorizontalHeaderLabels(table_labels)
        self.baekjae_table.setHorizontalHeaderLabels(table_labels)

        self.boksan_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.baekjae_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.TJ_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.incheon_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        grid.addLayout(container,0,0,1,4)
        grid.addWidget(self.boksan_label,1,0)
        grid.addWidget(self.incheon_label,1,1)
        grid.addWidget(self.TJ_label,1,2)
        grid.addWidget(self.baekjae_label,1,3)
        grid.addWidget(self.boksan_table,2,0)
        grid.addWidget(self.incheon_table,2,1)
        grid.addWidget(self.TJ_table,2,2)
        grid.addWidget(self.baekjae_table,2,3)
        self.setWindowTitle('Pharm Search')
        self.setGeometry(30, 100, 2500, 1200)
        self.show()
    
    def search_clicked(self):
        MED_NAME=self.search_bar.text()
        self.search_bar.clear()
        self.boksan_table.setRowCount(0)
        self.TJ_table.setRowCount(0)
        self.incheon_table.setRowCount(0)
        self.baekjae_table.setRowCount(0)
        self.baekjae_session(MED_NAME)
        self.incheon_session(MED_NAME)
        self.TJ_session(MED_NAME)
        self.boksan_session(MED_NAME)
        
        self.baekjae_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.incheon_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.TJ_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.boksan_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
    def incheon_session(self,MED_NAME):
        
        with requests.session() as session:
            login_header={
            "Referer":"http://inchunpharm.com/homepage/contents/login/login.asp",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            login_info={  
                "tx_id":USER,
                "tx_pw":PASS
            }
            login_url="http://inchunpharm.com/common/certify/login.asp"
            res=session.post(login_url,headers=login_header,data=login_info)
            res.raise_for_status()
            tmp=MED_NAME.encode('utf-8').hex().upper()
            encoded_MEDNAME=""
            for i in range(len(tmp)):
                if i%2==0:
                    encoded_MEDNAME=encoded_MEDNAME+"%"+tmp[i:i+2]
            order_url=f'http://inchunpharm.com/Service/Order/Order.asp?saveNumOrders=&so=0&so2=0&currMkind=U&tx_insucd=&df=t&sDate={DATE}&eDate={DATE}&tx_maker=&tx_physic={encoded_MEDNAME}&x=23&y=25'
            order_header={
                "Referer":"http://inchunpharm.com/Service/Order/Order.asp?l=login",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            order_info={
                "sDate":DATE,
                "eDate":DATE,
                "tx_physic":MED_NAME
            }
            response=session.post(order_url,headers=order_header,data=order_info)
            soup=BeautifulSoup(response.text,"html.parser")
            list=soup.select(".tbl_list .ln_physic")
            if (len(list)==0):
                print(f'검색결과 "{MED_NAME}"이 존재 하지 않습니다.')
            else:
               
                for idx,item in enumerate(list):
                    #id=item.select_one(".ln_physic on")["data-kims-searchcd"]
                    name=item.select_one(".physic_nm").get_text().split(' ',1)[1].strip()
                    price=item.select(".td_num")[0].get_text().strip().replace(',',"")
                    stock=item.select(".td_num")[1].get_text().strip().replace(',',"")
                    size=item.select(".td_nm")[2].get_text().strip()
                    if stock =="0":
                        stock="품절"
                    #print(f"name: {name},  size: {size},  price: {price},  stock: {stock}")
                    
                    self.incheon_table.table_insert([name,size,price,stock])
                pages=soup.select("#paging > a")
                max=len(pages)
                if max>=1:
                    in_str=str(pages[max-1]).replace("amp;","")
                    back="&so=0&so2=0"
                    front="Order.asp?Page="
                    s=in_str.find("href=")
                    e=in_str.find('">')
                    href=in_str[s+6:e]

                    f=href.find(front)
                    b=href.find(back)
                    max_page=int(href[f+15:b])
                    if(max_page>1):
                        new_header={
                            "Referer":"http://inchunpharm.com/service/order/Order.asp",
                            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
                        }
                        format="{0}"
                        new_href="http://inchunpharm.com/service/order/"+href[:f+15]+format+href[b:]
                        for i in range(2,max_page+1):
                            response=session.get(new_href.format(i),headers=new_header)
                            soup=BeautifulSoup(response.text,"html.parser")
                            list=soup.select(".tbl_list .ln_physic")
                            for idx,item in enumerate(list):
                                #id=item.select_one(".ln_physic on")["data-kims-searchcd"]
                                name=item.select_one(".physic_nm").get_text().strip()
                                price=item.select(".td_num")[0].get_text().strip().replace(',',"")
                                stock=item.select(".td_num")[1].get_text().strip().replace(',',"")
                                size=item.select(".td_nm")[2].get_text().strip()
                                if stock =="0":
                                    stock="품절"
                                
                                self.incheon_table.table_insert([name,size,price,stock])

    def TJ_session(self,MED_NAME):
        with requests.session() as session:
            login_header={
            "Referer":"http://tjp.co.kr/login.php?login_p=2",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            login_info={
                "service_gubun":"2",
                "userid":USER,
                "userpwd":PASS
            }
            order_header={
                "Referer":"http://tjp.co.kr/Order/",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            url_login="http://tjp.co.kr/login_proc.php"
            res=session.post(url_login,headers=login_header,data=login_info)
            res.raise_for_status()
            order_url="http://tjp.co.kr/Order/item_api.php?b86a3dd3=1675672547"
            order_info={
                "name":MED_NAME,
            }
            response=session.post(order_url, headers=order_header, data=order_info)

            j_res=json.loads(response.text)
            if(len(j_res["ResultSet"])==0):
                print(f'검색결과 "{MED_NAME}"이 존재 하지 않습니다.')
            else:
                
                for idx,item in enumerate(j_res["ResultSet"]):
                    name=item["ItemName"]
                    stock=str(item["InvQty"])
                    size=item["ItemSize"]
                    price=str(item["Cst2"])
                    if stock =="0":
                        stock="품절"
                    self.TJ_table.table_insert([name,size,price,stock])
    def boksan_session(self,MED_NAME):
        with requests.session() as session:
            login_header={
            "Referer":"http://wos.nicepharm.com/Contents/Main/Main9.asp",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            login_info={
                "tx_id":USER,
                "tx_pw":PASS
            }
            login_url="http://wos.nicepharm.com/Common/Certify/Login.asp"
            res=session.post(login_url,headers=login_header,data=login_info)
            res.raise_for_status()

            order_url="http://wos.nicepharm.com/Service/Order/Order.asp"
            order_header={
                "Referer":"http://wos.nicepharm.com/Service/Order/Order.asp?l=login",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            order_info={
                "UserDef001":"02",
                "so":"0",
                "so2":"0",
                "tx_ven":"5080233",
                "currVenNum":"512004-이수약국",
                "currMkind":"U",
                "sv":"5080233",
                "currStockCd":"59003",
                "currSndStockCd":"50003",
                "df":"t",
                "sDate":DATE,
                "eDate":DATE,
                "tx_physic":MED_NAME
            }
            response=session.post(order_url,headers=order_header,data=order_info)
            soup=BeautifulSoup(response.text,"html.parser")
            list=soup.select(".tbl_list .ln_physic")
            if(len(list)==0):
                print(f'검색결과 "{MED_NAME}"이 존재 하지 않습니다.')
            else:
                for idx,item in enumerate(list):
                    #id=item.select_one(".ln_physic on")["data-kims-searchcd"]
                    
                    name=item.select_one(".physic_nm").get_text().strip()
                    price=item.select(".td_num")[0].get_text().strip().replace(',',"")
                    stock=item.select(".td_num")[2].get_text().strip().replace(',',"")
                    size=item.select(".td_nm")[2].get_text().strip()
                    if stock =="0":
                        stock="품절"
                    self.boksan_table.table_insert([name,size,price,stock])
                pages=soup.select("#paging > a")
                max=len(pages)
                if max>=1:
                    in_str=str(pages[max-1]).replace("amp;","")
                    back="&so=0&so2=0"
                    front="Order.asp?Page="
                    s=in_str.find("href=")
                    e=in_str.find('">')
                    href=in_str[s+6:e]

                    f=href.find(front)
                    b=href.find(back)
                    max_page=int(href[f+15:b])
                    if(max_page>1):
                        new_header={
                            "Referer":"http://wos.nicepharm.com/Service/Order/Order.asp",
                            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
                        }
                        format="{0}"
                        new_href="http://wos.nicepharm.com/Service/Order/"+href[:f+15]+format+href[b:]
                        for i in range(2,max_page+1):
                            response=session.get(new_href.format(i),headers=new_header)
                            soup=BeautifulSoup(response.text,"html.parser")
                            list=soup.select(".tbl_list .ln_physic")
                            for idx,item in enumerate(list):
                                #id=item.select_one(".ln_physic on")["data-kims-searchcd"]
                                name=item.select_one(".physic_nm").get_text().strip()
                                price=item.select(".td_num")[0].get_text().strip().replace(',',"")
                                stock=item.select(".td_num")[2].get_text().strip().replace(',',"")
                                size=item.select(".td_nm")[2].get_text().strip()
                                if stock =="0":
                                    stock="품절"
                                
                                self.boksan_table.table_insert([name,size,price,stock])
                                
    def baekjae_session(self,MED_NAME):
         with requests.session() as session:

            page_header={
                "Connection":"keep-alive",
                "Referer":"https://www.ibjp.co.kr/ord/comOrd.act",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            page_url="https://www.ibjp.co.kr/logout.act"
            res=session.get(page_url,headers=page_header)
            soup=BeautifulSoup(res.text,"html.parser")
            WEB_TOKEN=soup.select_one("input[id=WEB_TOKEN]")["value"]
            
            login_header={
                "Connection":"keep-alive",
                "Referer":"https://www.ibjp.co.kr/logout.act",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            login_info={
                "WEB_TOKEN":WEB_TOKEN,
                "loginId":USER,
                "pwd":PAEKJAE_PWD
            }
            login_url="https://www.ibjp.co.kr/loginChk.ajx"
            res=session.post(login_url,headers=login_header,data=login_info)
            res.raise_for_status()
            order_url="https://www.ibjp.co.kr/ord/itemSearch.ajx"
            order_header={
                "Referer":"https://www.ibjp.co.kr/ord/comOrd.act",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
            }
            order_info={
                "H_SORT_GB":"AVAIL_STOCK",
                "H_SEARCH_GB":"ITEM_NM",
                "H_SEARCH_NM":MED_NAME,
                "H_SEARCH_ING":"N",
                "H_SEARCh_EFF":"N",
                "SEL_MONTH":"-3",
                "PAGE_ITEM":"1",
                "PAGE_HISTORY":"1",
                "PAGE_PER_CNT":"100",
                "PAGE_OFFSET_CNT":"0",
                "TOTAL_CNT":"0",
                "BASKET_GB_CD":"01",
                "SEARCH_GB":"ITEM_NM",
                "SEARCH_NM":MED_NAME,
                "SORT_GB":"AVAIL_STOCK"
            }
            response=session.post(order_url,headers=order_header,data=order_info)
            j_res=json.loads(response.text)
            try:
                for idx,item in enumerate(j_res["itemSearchList"]):
                    price=str(item["ORD_WP2_AMT"])
                    name=item["ITEM_NM"]
                    stock=str(item["AVAIL_STOCK"])
                    size=item["ITEM_NM_UNIT"].split()[1]
                    if stock =="0":
                        stock="품절"
                    self.baekjae_table.table_insert([name,size,price,stock])
            except:
                print(f'검색결과 "{MED_NAME}"이 존재 하지 않습니다.')
if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=MyApp()
    sys.exit(app.exec_())

