import requests
import json
import urllib
import re
from multiprocessing import Queue
from handelmongo import mongo_info
from concurrent.futures import ThreadPoolExecutor
#(.*?):(.*)  "$1":"$2",
quelist=Queue()
def handle_requets(url,data):
    header={
        "device": "OPPO R11",
        "sdk": "22,5.1.1",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "dpi": "2.0",
        "imei": "355757010580021",
        #"client": "4",
       # "mac": "58:00:E3:2E:FE:D6",
        "version": "602.2",
        #"resolution": "1920*1080",
        "Connection": "Keep-Alive",
        "channel": "baidu",
        "Accept-Encoding": "gzip, deflate",
        #"Cookie": "duid=61921715",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; OPPO R11 Build/NMF26X)",
        "Host": "api.douguo.net",
       # "Content-Length": "43",

    }

    response=requests.post(url=url,headers=header,data=data)
    return response
def  handle_index():
    url = 'http://api.douguo.net/recipe/flatcatalogs'
    # data = {"order":"0",
    #         "client":"4",
    #         "keyword":"%E7%82%92%E9%A5%AD",
    #         }
    data="client=4"
    response=handle_requets(url=url,data=data)
    index_dict=json.loads(response.text)
    for i in index_dict["result"]["catalogs"]:
        for k in i["tags"]:
            data_2=k["t"]
            quelist.put(data_2)

def handle_caipu_list(data):
    print('当前处理:%s'%data)
    caipu_list_url='http://api.douguo.net/recipe/s/0/15'
    datas="order=0&client=4&keyword=%s"%urllib.parse.quote(data)
    caipu_reponse=handle_requets(url=caipu_list_url,data=datas)
    caipu_list_dict=json.loads(caipu_reponse.text)
    for i in caipu_list_dict["result"]["list"]:
        caipu_info={}
        caipu_info["shicai"]=data
        if i["type"]==2:
            caipu_info["username"]=i["r"]["an"]
            caipu_info["cainame"]=i["r"]["n"]
            caipu_info["jianjie"] = i["r"]["cookstory"].replace("\n",'').replace(" ",'')
            caipu_info["id"] = i["r"]["id"]
            caipu_info["liulan"]= re.search("\d+",i["r"]["recommend_label"]).group(0)
            caipu_info["zuoguo"] = i["r"]["dc"]
            caipu_info["shoucang"] = i["r"]["fc"]
            detail="http://api.douguo.net/recipe/detail/%s"%i["r"]["id"]
            detail_data="author_id=0&client=4"
            detail_response=handle_requets(detail,detail_data)
            detail_response_dict=json.loads(detail_response.text)
            caipu_info["jieshao"] = detail_response_dict["result"]["recipe"]["tips"]
            caipu_info["zuofa"]=  detail_response_dict["result"]["recipe"]["cookstep"]
            print("当前入库:%s"%caipu_info["cainame"])
            # mongo_info.insert_item(caipu_info)



        else:
            continue








if __name__ == '__main__':
    # url='http://api.douguo.net/recipe/s/0/15'
    # data = "order=0&client=4&keyword=%E8%82%A5%E7%89%9B"
    # handle_requets(url,data)
    handle_index()
    pool=ThreadPoolExecutor(max_workers=20)
    while quelist.qsize()>0:
        pool.submit(handle_caipu_list,quelist.get())
