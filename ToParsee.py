import requests
import asyncio
import pandas as pd
import numpy as np
import xgboost as xgb
from concurrent.futures import ProcessPoolExecutor
from bs4 import BeautifulSoup
from selenium import webdriver
import logging
# from selenium.webdriver.remote.remote_connection import LOGGER
# LOGGER.setLevel(logging.WARNING)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import csv
import pickle
def url_find(query,count):
    print('url_find')
    site_links = []
    sites = []
    agreg = ('tiu',
    'baza.drom','pulscen',
    'krsk.au','avito',
    'youtube','garage-cts',
    'coppertubes',
    'youla','wuerthmarket',
    'alibaba','ovkgrupp',
    'blog','farpost'
    'agro-klimat','doski.ru',
    'transcool','prom.',
    'flagma.','rowen.',
     '/search?','aliexpress',
    'el-vent','market.yandex',
    'mvideo','eldorado','leroymerlin',
    'citilink','dns','xolodnoeleto',
    'e-katalog','ozon','onlinetrade',
    'kcentr','rbt','farpost',
    'voltmart','vent33','ulmart','05.',
    'luxclimat','mitsubishi','haieronline',
    'vk')

    prefix = 'https://'
    for i in range(count+1):
        time.sleep(0.0001)
        r = requests.get('https://www.google.ru/search?q='+ query+"&start=" + str(i) + "0", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.106"})
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup.find_all('div',class_="g"):
            check = False
            link = element.a['href']
            for i in agreg:
                if i in link:
                    check = True
            if not check:
                site_links.append(link)
    return site_links

def ultra_findP(soup,tag,charct,length = 3):
    max_ = -1
    res = ''
#     for i in range(len(charct)):
#         if 'class=' in charct[i]:
#             charct[i] = charct[i].split('class=')[1]
#             if len(charct[i].split('=')) != 1:
#                 charct[i] = charct[i].split('=',1)[0].rsplit(' ',1)[0]
#             charct[i] = 'class='+charct[i]
#         else:
#             charct[i] = ''
#     print(tag,charct)
    char = []
    # print(charct)
    for i in range(length,0,-1):
        # print(charct[-i].split('='))
        char.append({charct[-i].split('=')[0]:charct[-i].split('=')[-1].strip()})
    # print([i.keys() for i in char])
    for elem in soup.findAll(tag[-1], char[-1] if char[-1] != {'',''} else ''):
        for elem1 in elem.findAll(tag[-2],char[-2] if char[-2] != {'',''} else ''):
            for elem2 in elem1.findAll(tag[-3],char[-3] if char[-3] != {'',''} else ''):
                try:
                    if int(''.join(x for x in elem2['href'] if x.isdigit() and x!='')) > max_:
                        max_ = int(''.join(x for x in elem2['href'] if x.isdigit() and x!=''))
                        res = elem2['href']
                except:
                    pass       
    return res
        
                        
                        
def U_find(soup,tag,charct,url,length = 3):
    res = []
    # try:
#         for i in range(len(charct)):
#             if 'class=' in charct[i]:
#                 charct[i] = charct[i].split('class=')[1]
#                 if len(charct[i].split('=')) != 1:
#                     charct[i] = charct[i].split('=',1)[0].rsplit(' ',1)[0]
#                 charct[i] = 'class='+charct[i]
#             else:
#                 charct[i] = ''
#         print(tag,charct)
    char = []
        
    for i in range(length,0,-1):
        char.append({charct[-i].split('=')[0]:charct[-i].split('=')[-1].strip()})
    try:
        for elem in soup.findAll(tag[-1], char[-1] if char[-1] != {'',''} else ''):
            for elem1 in elem.findAll(tag[-2],char[-2] if char[-2] != {'',''} else ''):
                for elem2 in elem1.findAll(tag[-3],char[-3] if char[-3] != {'',''} else ''):
                    try:
                        if url.split('//')[1].split('/')[0] not in elem2['href']:
                            res.append(''.join(['https://',url.split('//')[1].split('/')[0],elem2['href']]))
                        else:
                            res.append(elem2['href'])
                    except:
                        pass
    except:
        return res
    return res

def N_find(soup,tag,charct,length = 3):
    res = []
    # try:
#         for i in range(len(charct)):
#             if 'class=' in charct[i]:
#                 charct[i] = charct[i].split('class=')[1]
#                 if len(charct[i].split('=')) != 1:
#                     charct[i] = charct[i].split('=',1)[0].rsplit(' ',1)[0]
#                 charct[i] = 'class='+charct[i]
#             else:
#                 charct[i] = ''
#         print(tag,charct)
    char = []
    for i in range(length,0,-1):
        char.append({charct[-i].split('=')[0]:charct[-i].split('=')[-1].strip()})
    try:
        for elem in soup.findAll(tag[-1], char[-1] if char[-1] != {'',''} else ''):
            for elem1 in elem.findAll(tag[-2],char[-2] if char[-2] != {'',''} else ''):
                for elem2 in elem1.findAll(tag[-3],char[-3] if char[-3] != {'',''} else ''):
                    if elem2.text == '':
                        res.append(elem2['title'].replace('\n','').strip())
                    else:
                        res.append(elem2.text.replace('\n','').strip())
    except:
        return res
    return res

def C_find(soup,tag,charct,length = 3):
    res = []
    # try:
#         for i in range(len(charct)):
#             if 'class=' in charct[i]:
#                 charct[i] = charct[i].split('class=')[1]
#                 if len(charct[i].split('=')) != 1:
#                     charct[i] = charct[i].split('=',1)[0].rsplit(' ',1)[0]
#                 charct[i] = 'class='+charct[i]
#             else:
#                 charct[i] = ''
#         print(tag,charct)
    char = []
    for i in range(length,0,-1):
        char.append({charct[-i].split('=')[0]:charct[-i].split('=')[-1].strip()})
    try:
        for elem in soup.findAll(tag[-1], char[-1] if char[-1] != {'',''} else ''):
            for elem1 in elem.findAll(tag[-2],char[-2] if char[-2] != {'',''} else ''):
                for elem2 in elem1.findAll(tag[-3],char[-3] if char[-3] != {'',''} else ''):
                    price = ''.join(x for x in elem2.text if x.isdigit() and x!='')
                    res.append(price if price!='' else '0')
    except:
        return res
    return res


# def parseOnePage(session,url_page,Tnames,Tprices):
# #     positions = []
#     try:
#         with session.get(url_page) as r:
#     #         print(url_page)
#             #r = p.apply_async(requests.get({'url':url_page,'headers':headers,'verify':False}))
#             #print(r)
#             #print(r.get(timeout=1))
#             soup = BeautifulSoup(r.text, 'html5lib')
#             links,names,prices = [],[],[]
#             for i in Tprices:
#                 elem_ = [i['tag'],i['ptag'],i['pptag']]
#                 into = [i['class'],i['pclass'],i['ppclass']]
#                 pr = C_find(soup,elem_,into)
#                 if pr != []:
#                     prices.append(pr)
#             for i in Tnames:
#                 elem_ = [i['tag'],i['ptag'],i['pptag']]
#                 into = [i['class'],i['pclass'],i['ppclass']]
#                 nm,ln = N_find(soup,elem_,into),U_find(soup,elem_,into,url_page)
#                 if nm!=[]:
#                     names.append(nm)
#                 if ln!=[]:
#                     links.append(ln)
#             links,prices,names = [list(i) for i in list(set(map(tuple, links)))],[list(i) for i in list(set(map(tuple, prices)))],[list(i) for i in list(set(map(tuple, names)))]
#         #                     print(links,names,prices)
#     #         if len(names) == len(prices) == len(links):
#     #             for i in range(len(names)):
#     #         positions.append([names[i],prices[i],links[i]])
#     #         print(prices,'price')
#             if [names,prices,links] == [[],[],[]]:
#                 return url_page
#             return [names,prices,links]
#     except:
#         return url_page

def parseOnePageP(session,url_page,Dtags):
#     positions = []
    try:
        with session.get(url_page) as r:
            # print(url_page)
            #r = p.apply_async(requests.get({'url':url_page,'headers':headers,'verify':False}))
            #print(r)
            #print(r.get(timeout=1))
            soup = BeautifulSoup(r.text, 'lxml')
            res = []
            for i in Dtags:
                # elem_ = [i['tag'],i['ptag'],i['pptag']]
                # into = [i['class'],i['pclass'],i['ppclass']]
                pr,nm,ln = C_find(soup,[i['tag'],i['ptag'],i['pptag']],[i['Cclass'],i['pclass'],i['ppclass']]),N_find(soup,[i['tag'],i['ptag'],i['pptag']],[i['Cclass'],i['pclass'],i['ppclass']]),U_find(soup,[i['tag'],i['ptag'],i['pptag']],[i['Cclass'],i['pclass'],i['ppclass']],url_page)
                if pr != [] or nm!=[] or ln !=[]:
                    # print('add',len(pr),len(nm),len(ln))
                    res.append([pr,nm,ln])
            # for i in Tnames:
            #     elem_ = [i['tag'],i['ptag'],i['pptag']]
            #     into = [i['class'],i['pclass'],i['ppclass']]
            #     nm,ln = N_find(soup,elem_,into),U_find(soup,elem_,into,url_page)
            #     if nm!=[]:
            #         names.append(nm)
            #     if ln!=[]:
            #         links.append(ln)
            # links,prices,names = [list(i) for i in list(set(map(tuple, links)))],[list(i) for i in list(set(map(tuple, prices)))],[list(i) for i in list(set(map(tuple, names)))]

        #                     print(links,names,prices)
    #         if len(names) == len(prices) == len(links):
    #             for i in range(len(names)):
    #         positions.append([names[i],prices[i],links[i]])
    #         print(prices,'price')
            # if [names,prices,links] == [[],[],[]]:
            #     return url_page
            return res
    except:
        return url_page













# async def parse_pages(site_links,urls,datas):
#     headers ={
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.106",
#     }
#     positions = []
#     for url in site_links:
#         try:
#             url = url.split('&')[0]
#         except:
#             continue
#         requests.packages.urllib3.disable_warnings()
#         r = requests.get(url, headers=headers, verify = False)
#         soup = BeautifulSoup(r.text, 'html5lib')

#         for fileName in urls:
#             urlCheck = ''
#             try:
#                 urlCheck = url.split('https://')[1]
#             except:
#                 urlCheck = url.split('http://')[1]
#             urlCheck = urlCheck.split('/')[0]
#         #     print(''.join(url_.split('.')[1:-1]),''.join(url_.split('.')[0:-1]))
#             if urlCheck.split('.')[0] == 'www':
#                 urlCheck = ''.join(urlCheck.split('.')[1:-1])
#             else:
#                 urlCheck = ''.join(urlCheck.split('.')[0:-1])
#             if fileName in urlCheck:
# #                 print(fileName,urlCheck,url)
# #                 data = datas[datas['site'] == fileName].reset_index()
#                 #params = data.to_dict('records')
# #                 Tpaginates = data[data['type']==3].to_dict('records')
# #                 Tprices = data[data['type']==1].to_dict('records')
# #                 TnamesUrls = data[data['type']==2].to_dict('records')
#                 lengs = [0]
#                 Tpaginstors,Tnames,Tprices = datas['paginate'][datas['paginate']['site'] == fileName].to_dict('records'),\
#                                                 datas['name'][datas['name']['site'] == fileName].to_dict('records'),\
#                                                     datas['price'][datas['price']['site'] == fileName].to_dict('records')
#                 for i in Tpaginstors:
#                     elem_ = [i['tag'],i['ptag'],i['pptag']]
#                     into = [i['class'],i['pclass'],i['ppclass']]
# #                     print(elem_,'|',into)
#                     res = ultra_findP(soup,elem_,into)
# #                     print(res)
#                     if res == '':
#                         leng = 1
#                     elif '=' in res:
#                         try:
#                             leng = int(res.rsplit('=')[-1])
#                             lengs = [leng]
#                             break
#                         except:
#                             pass
#                     else:
#                         leng = int(''.join(x for x in res if x.isdigit()))
#                     lengs.append(leng)
#                 leng = max(lengs)
# #                 print(lengs)
                
#                 url_pages = [url]
# #                 print(leng,'1',url_pages)
#                 for lk in range(leng):
#                     if leng != 1:
#                         if url.split('//')[1].split('/')[0] not in res.rsplit('/',1)[0]:
# #                         print(res.rsplit('/',1)[0],res.rsplit('/',1)[1])
#                             a = ''.join(['https://',url.split('//')[1].split('/')[0],res.rsplit('/',1)[0],'/',res.rsplit('/',1)[1].replace(str(leng),str(lk+1))])
#                             if a.count('https://')>1:
# #                     print(url_pages[-1].split('https://')[2])
#                                 a = 'https://'+a.split('https://')[-1]
#                                 url_pages.append(a)
#                         else:
#                             url_pages.append(''.join([res.rsplit('/',1)[0],'/',res.rsplit('/',1)[1].replace(str(leng),str(lk+1))]))
# #                 if url_pages[-1].count('https://')>1:
# # #                     print(url_pages[-1].split('https://')[2])
# #                     url_pages[-1] = 'https://'+url_pages[-1].split('https://')[-1]
# #                 print(url_pages)
#                 url_pages = url_pages[1:] if len(url_pages) > 1 else url_pages
# #                 print(url_pages)
#                 with ProcessPoolExecutor(15) as executor:
#                     with requests.Session() as session:
#                         # Set any session parameters here before calling `fetch`
#                         session.headers=headers
#                         session.verify=False
#                         loop = asyncio.get_event_loop()
#                         tasks = [
#                             loop.run_in_executor(
#                                 executor,
#                                 parseOnePage,
#                                 *(session, url_page,Tnames,Tprices) # Allows us to pass in multiple arguments to `fetch`
#                             )
#                             for url_page in url_pages
#                         ]
#                         for response in await asyncio.gather(*tasks):
#                             positions.append(response)
# #                     r = requests.get(url_page,headers=headers,verify=False)
# #                     #r = p.apply_async(requests.get({'url':url_page,'headers':headers,'verify':False}))
# #                     #print(r)
# #                     #print(r.get(timeout=1))
# #                     soup = BeautifulSoup(r.text, 'html5')
# #                     links,names,prices = [],[],[]
# #                     for i in datas['price'][datas['price']['site'] == fileName].to_dict('records'):
# #                         elem_ = [i['tag'],i['ptag'],i['pptag']]
# #                         into = [i['class'],i['pclass'],i['ppclass']]
# #                         pr = C_find(soup,elem_,into)
# #                         if pr != []:
# #                             prices.append(pr)
# #                     for i in datas['name'][datas['name']['site'] == fileName].to_dict('records'):
# #                         elem_ = [i['tag'],i['ptag'],i['pptag']]
# #                         into = [i['class'],i['pclass'],i['ppclass']]
# #                         nm,ln = N_find(soup,elem_,into),U_find(soup,elem_,into,url)
# #                         if nm!=[]:
# #                             names.append(nm)
# #                         if ln!=[]:
# #                             links.append(ln)
# #                     links,prices,names = [list(i) for i in list(set(map(tuple, links)))],[list(i) for i in list(set(map(tuple, prices)))],[list(i) for i in list(set(map(tuple, names)))]
# #                 #                     print(links,names,prices)
# # #                     if len(names) == len(prices) == len(links):
# #                     for i in range(min(len(names),len(prices),len(links))):
# #                         positions.append([names[i],prices[i],links[i]])
# #                     p = Pool(2)
# #                     records = p.starmap(parse_pages2, (url_page,datas))
# #                     positions.append([records])
#     return positions
async def parse_pagesP(site_links,urls,datas):
    headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 OPR/57.0.3098.106",
    }
    # urls,site_links,datas = await urls,await site_links,await datas
    positions = []
    for url in site_links:
        try:
            url = url.split('&')[0]
        except:
            continue
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url, headers=headers, verify = False)
        soup = BeautifulSoup(r.text, 'lxml')
        # for i in datas:
        #     print(i)
        for fileName in urls:
            # print(fileName)
            fileName = fileName['site']
            urlCheck = ''
            try:
                urlCheck = url.split('https://')[1]
            except:
                urlCheck = url.split('http://')[1]
            urlCheck = urlCheck.split('/')[0]
        #     print(''.join(url_.split('.')[1:-1]),''.join(url_.split('.')[0:-1]))
            if urlCheck.split('.')[0] == 'www':
                urlCheck = ''.join(urlCheck.split('.')[1:-1])
            else:
                urlCheck = ''.join(urlCheck.split('.')[0:-1])

            if fileName in urlCheck:
#                 print(fileName,urlCheck,url)
#                 data = datas[datas['site'] == fileName].reset_index()
                #params = data.to_dict('records')
#                 Tpaginates = data[data['type']==3].to_dict('records')
#                 Tprices = data[data['type']==1].to_dict('records')
#                 TnamesUrls = data[data['type']==2].to_dict('records')
                # print([sub if sub['site'] == fileName else None for sub in datas])
                # [sub['site'] == fileName for sub in datas]
                lengs = [0]
                DataTags = []
                #superbDUMB
                for sub in datas:
                    if sub['site'] == fileName:
                        DataTags.append(sub)
                # DataTags = [sub['site'] == fileName and DataTags.append([sub]) for sub in datas]
                for i in DataTags:
                    elem_ = [i['tag'],i['ptag'],i['pptag']]
                    into = [i['Cclass'],i['pclass'],i['ppclass']]
#                     print(elem_,'|',into)
                    res = ultra_findP(soup,elem_,into)
                    # print(res,'dsadas')
                    if res == '':
                        leng = 1
                    elif '=' in res:
                        try:
                            leng = int(res.rsplit('=')[-1])
                            lengs = [leng]
                            break
                        except:
                            pass
                    else:
                        leng = int(''.join(x for x in res if x.isdigit()))
                    lengs.append(leng)
                leng = max(lengs)
                # print(lengs)
                
                url_pages = [url]
#                 print(leng,'1',url_pages)
                for lk in range(leng):
                    if leng != 1:
                        if url.split('//')[1].split('/')[0] not in res.rsplit('/',1)[0]:
#                         print(res.rsplit('/',1)[0],res.rsplit('/',1)[1])
                            a = ''.join(['https://',url.split('//')[1].split('/')[0],res.rsplit('/',1)[0],'/',res.rsplit('/',1)[1].replace(str(leng),str(lk+1))])
                            if a.count('https://')>1:
#                     print(url_pages[-1].split('https://')[2])
                                a = 'https://'+a.split('https://')[-1]
                                url_pages.append(a)
                        else:
                            url_pages.append(''.join([res.rsplit('/',1)[0],'/',res.rsplit('/',1)[1].replace(str(leng),str(lk+1))]))
#                 if url_pages[-1].count('https://')>1:
# #                     print(url_pages[-1].split('https://')[2])
#                     url_pages[-1] = 'https://'+url_pages[-1].split('https://')[-1]
#                 print(url_pages)
                url_pages = url_pages[1:] if len(url_pages) > 1 else url_pages
#                 print(url_pages)
                with ProcessPoolExecutor(15) as executor:
                    with requests.Session() as session:
                        # Set any session parameters here before calling `fetch`
                        session.headers=headers
                        session.verify=False
                        loop = asyncio.get_event_loop()
                        tasks = [
                            loop.run_in_executor(
                                executor,
                                parseOnePageP,
                                *(session, url_page,DataTags) # Allows us to pass in multiple arguments to `fetch`
                            )
                            for url_page in url_pages
                        ]
                        for response in await asyncio.gather(*tasks):
                            positions.append(response)
#                     r = requests.get(url_page,headers=headers,verify=False)
#                     #r = p.apply_async(requests.get({'url':url_page,'headers':headers,'verify':False}))
#                     #print(r)
#                     #print(r.get(timeout=1))
#                     soup = BeautifulSoup(r.text, 'html5')
#                     links,names,prices = [],[],[]
#                     for i in datas['price'][datas['price']['site'] == fileName].to_dict('records'):
#                         elem_ = [i['tag'],i['ptag'],i['pptag']]
#                         into = [i['class'],i['pclass'],i['ppclass']]
#                         pr = C_find(soup,elem_,into)
#                         if pr != []:
#                             prices.append(pr)
#                     for i in datas['name'][datas['name']['site'] == fileName].to_dict('records'):
#                         elem_ = [i['tag'],i['ptag'],i['pptag']]
#                         into = [i['class'],i['pclass'],i['ppclass']]
#                         nm,ln = N_find(soup,elem_,into),U_find(soup,elem_,into,url)
#                         if nm!=[]:
#                             names.append(nm)
#                         if ln!=[]:
#                             links.append(ln)
#                     links,prices,names = [list(i) for i in list(set(map(tuple, links)))],[list(i) for i in list(set(map(tuple, prices)))],[list(i) for i in list(set(map(tuple, names)))]
#                 #                     print(links,names,prices)
# #                     if len(names) == len(prices) == len(links):
#                     for i in range(min(len(names),len(prices),len(links))):
#                         positions.append([names[i],prices[i],links[i]])
#                     p = Pool(2)
#                     records = p.starmap(parse_pages2, (url_page,datas))
#                     positions.append([records])
    return positions
# def generate(url,model,sites):
# #     if not model:
# #         df = pd.read_csv('data8.csv',encoding = "cp1251")
# #         df['zero'] = df.apply(lambda row: 0 if row.label == 0 else 1, axis = 1)
# #         label0 = df[df['zero']==0]#1500
# #         label1 = df[df['label']==1]
# #         label2 = df[df['label']==2]
# #         label3 = df[df['label']==3]#int(len_[1])
# #         ww = (len(label1)+len(label2)+len(label3))/len(label0)
# #         w0 = [0.1 for i in label0.values]
# #         w1 = [1 for i in label1.values]
# #         w2 = [2 for i in label2.values]
# #         w3 = [1 for i in label3.values]
# # #         print((len(label0)+len(label2)+len(label3))/len(label1),(len(label0)+len(label1)+len(label3))/len(label2),(len(label0)+len(label2)+len(label1))/len(label3),ww)
# #         ws = w0+w1+w2+w3
# #         df = label0.append(label1).append(label2).append(label3)
# #         df = df.replace('NaN','0')
# #         df = df.fillna(0)
# #         df = df.replace('Infinity','1')
# #         label_train = df['label']
# #         df = df.drop(columns=['label','zero'])
# #         df = df.drop(columns=['Y','X'])
# #         df = df.drop(columns=['height'])
# #         df = df.drop(columns=['width'])
# #         df = df.drop(columns=['par_height'])
# #         df = df.drop(columns=['par_width'])
# #         dtrain = xgb.DMatrix(df.astype('float64'), label_train,weight = ws)
# #         xgb_params = {
# #             # 'subsample': 0.99,
# #         #     'eval_metric': 'mlogloss',
# #         #     'tree_method':'gpu_hist',
# #         #     'gpu_id':0,
# #             'silent': 0,
# #            #'min_child_weight' : 2,
# #         'objective':'multi:softmax', #multi:softmax multi:softprob
# #         #     'scale_pos_weight' : 0.0000001,
# #         #     'scale_pos_weight':(len(label1)+len(label2)+len(label3))/len(label0),
# #             'eta':0.01,
# #             'max_depth': 1,
# #             'num_class':4,
# #         }
# #         model = xgb.train(dict(xgb_params, silent=0), dtrain, num_boost_round=1500)
# #         print('trainColmplete')
#     url_ = ''
#     try:
#         url_ = url.split('https://')[1]
#     except:
#         url_ = url.split('http://')[1]
#     url_ = url_.split('/')[0]
# #     print(''.join(url_.split('.')[1:-1]),''.join(url_.split('.')[0:-1]))
#     if url_.split('.')[0] == 'www':
#         url_ = ''.join(url_.split('.')[1:-1])
#     else:
#         url_ = ''.join(url_.split('.')[0:-1])
#     check = False
#     for i in sites:
#         if url_ == i:
#             check = True
#     if not check:
#         columns = ['height','width','par_height','par_width','is_link','is_parent_link','is_like_price','is_par_like_price','is_like_name',
#                'is_like_paginate','word_count','tag_DIV','tag_P','tag_A','tag_LI','tag_H','tag_SPAN','ptag_DIV','ptag_P','ptag_A','ptag_LI','ptag_H','tag_FONT','ptag_FONT','ptag_SPAN','ChLen','X','Y','digLen','phone','meanLng','cl','tg','parcl','partg','parparcl','parpartg','text']
#         arr = []
#         options = webdriver.ChromeOptions()
#         options.add_argument('headless') 
#         d = DesiredCapabilities.CHROME
#         d['loggingPrefs'] = {'browser':'ALL'}
#         driver = webdriver.Chrome("CHRM/chromedriver.exe",options=options,desired_capabilities=d)
#         driver.get(url) #https://rbb-holod.ru/catalog/freony-xladony https://morena.ru/catalog/teploobmennoe-oborudovanie/ http://www.aholod.ru/catalog/42/ https://www.eldorado.ru/c/stiralnye-mashiny/
#         js = """
#                     console.clear();
#                     document.querySelectorAll('body *').forEach(function(node) {
#                     try {
#                         href = node.href ? 1 :0;
#                         parenthref = node.parentNode.href ? 1:0;
#                         islikeprice = node.className.toLowerCase().indexOf('price') != -1 || node.className.toLowerCase().indexOf('cost') != -1 ? 1:0;
#                         isplikeprice = node.parentNode.className.toLowerCase().indexOf('price') != -1 || node.parentNode.className.toLowerCase().indexOf('cost') != -1 ? 1:0; 
#                         islikename = node.innerText.length>=20 && node.innerText.length<=70 ? 1:0;
#                         islikepaginate = node.search != "" && node.search ? 1:0;
#                         tag_DIV = node.localName == 'div' ? 1:0;
#                         tag_P = node.localName == 'p' ? 1:0;
#                         tag_A = node.localName == 'a' ? 1:0;
#                         tag_LI = node.localName == 'li' ? 1:0;
#                         tag_H = node.localName.indexOf('h') != -1 ? 1:0;
#                         tag_FONT = node.localName == 'font' ? 1:0;
#                         tag_SPAN = node.localName == 'span' ? 1:0;
#                         ptag_DIV = node.parentNode.localName == 'div' ? 1:0;
#                         ptag_P = node.parentNode.localName == 'p' ? 1:0;
#                         ptag_A = node.parentNode.localName == 'a' ? 1:0;
#                         ptag_LI = node.parentNode.localName == 'li' ? 1:0;
#                         ptag_H = node.parentNode.localName.indexOf('h') != -1 ? 1:0;
#                         ptag_FONT = node.parentNode.localName == 'font' ? 1:0;
#                         ptag_SPAN = node.parentNode.localName == 'span' ? 1:0;

#                         var text =  node.innerText;
#                         lens = 0;
#                         words = text.split(" ");
#                         word_count = words.length;

#                         for (let i =0;i<word_count;i++)
#                         {
#                             lens += words[i].length;
#                         }

#                         meanLng = lens/word_count;

#                         chLen = node.childElementCount;


#                         var box = node.getBoundingClientRect();
#                         Y = box.top + window.pageYOffset;
#                         X = box.left + window.pageXOffset;
#                         a = text.replace(/[\s]/g,'').replace(/[0-9]/g, '').length;
#                         b = text.replace(/[\s]/g,'').replace(/[^0-9]/g, '').length;
#                         inLen = b/a;
#                         phoneCheck = /^[0-9\s+]*[(\s]{1}[0-9]{1,4}[)\s]{1}[-\s\./0-9]+/g.test(text) ? 1 : 0; 

#                         width = node.offsetWidth/window.innerWidth;
#                         heigth = node.offsetHeight/window.innerHeight;
#                         widthP = node.parentNode.offsetWidth/window.innerWidth;
#                         heigthP = node.parentNode.offsetHeight /window.innerHeight;
#                         var teext = (node.innerText.length <= 100) ? node.innerText.replace(/,/g,"").replace(/\|/g, ''): " ";

#                         var out_='|'+heigth+','+width+','+heigthP+','+
#                         widthP+','+href+','+parenthref+','+islikeprice+','+isplikeprice+','+
#                         islikename+','+islikepaginate+','+word_count+','+tag_DIV+','+tag_P
#                         +','+tag_A+','+tag_LI+','+tag_H+','+tag_SPAN+','+ptag_DIV+','+ptag_P+','+ptag_A+
#                         ','+ptag_LI+','+ptag_H+','+tag_FONT+','+ptag_FONT+','+ptag_SPAN+','+chLen+','+X+','+Y+','+inLen+','+phoneCheck+','+meanLng+','+node.className+','+                   node.localName+','+node.parentNode.className+','+node.parentNode.localName+','+node.parentNode.parentNode.className+','+node.parentNode.parentNode.localName+','+ teext + ','
#                         if (width > 0 && heigth > 0 && (widthP > 0 || heigthP > 0))
#                         { 
#                             console.log(out_);
#                         }
#                     } catch (e) {}
#                     });

#                     """
#         driver.execute_script(js)#/^[0-9\s+]*[(]{1,2}[0-9]{1,4}[)]{1,2}[-\s\./0-9]*/g
#         #print(driver.get_log('browser'))

#         kk = 0
#         for entry in driver.get_log('browser'):

#             if entry['level']=='INFO' and '|' in entry['message']:
#                 # msg = str(entry['message'].split('|')[-1]).replace('\\u003C','').replace('\\','').replace('"','').split(',')[:-1]
#                 # if len(msg) != 31:
#                 #     print(entry['message']+'|'+str(len(msg))+'|'+str(kk))
#                 # kk+=1
#                 arr.append(str(entry['message'].split('|')[-1]).replace('\\u003C','').replace('\\','').replace('"','').split(',')[:-1])
#         dft = pd.DataFrame(data=arr,columns = columns)
#         # dft = dft.drop(columns=['height'])
#         # dft = dft.drop(columns=['width'])
#         # dft = dft.drop(columns=['par_height'])
#         # dft = dft.drop(columns=['par_width'])
#         driver.close()
#         dft = dft.replace('NaN','0')
#         dft = dft.fillna(0)
#         dft = dft.replace('Infinity','1')
#         dft = dft.drop(columns=['X','Y'])
#         dft = dft.drop(columns=['height'])
#         dft = dft.drop(columns=['width'])
#         dft = dft.drop(columns=['par_height'])
#         dft = dft.drop(columns=['par_width'])
#         dtest = xgb.DMatrix(dft.drop(columns=['cl','tg','parcl','partg','parparcl','parpartg','text']).astype('float64'))
#         # pred = model.predict(dtest,ntree_limit=num_boost_rounds)
#         pred = model.predict(dtest)
#         pred = pred.tolist()
#         # print(pred)
#         for i in range(len(pred)):
#         #     pred[i] = pred[i].index(max(pred[i]))
#             pred[i] = int(round(pred[i]))
#         pred = np.array(pred)
#         fSearch = ['site','type','tag','ptag','pptag','class','pclass','ppclass']
#         elems = []
#     #     print(columns)
#         for k in range(1,4):
#             indexs = np.where(pred == k)[0]
#             indexed = dft.iloc[indexs]

#             for i in indexed.values:
#                 elems.append({'site':url_,
#                               'type':k,
#                               'tag':str(i[-6]) if str(i[-6])!='' else '',
#                               'class':'class='+str(i[-7]) if str(i[-7])!='' else '=',
#                               'ptag':str(i[-4]) if str(i[-4])!='' else '',
#                               'pptag':str(i[-2]) if str(i[-2])!='' else '',
#                               'pclass':'class='+str(i[-5]) if str(i[-5])!='' else '=',
#                               'ppclass':'class='+str(i[-3]) if str(i[-3])!='' else '='
#                              })
#     #             print(i,k)
#         print(len(elems))
#         elems = [dict(s) for s in set(frozenset(d.items()) for d in elems)]
#         print(len(elems))
#         print(url)
#         with open('datas.csv', 'a', newline='') as csvfile:
#             writer = csv.DictWriter(csvfile,fieldnames = fSearch)
#             for i in elems:
#                 writer.writerow(i)

def APtrainM(train,xgb_params,nbr=1500,prev_model = False):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # print(site_links,datas,sites)
    future = asyncio.ensure_future(PtrainM(train,xgb_params,nbr,prev_model))
    res = loop.run_until_complete(future)
    return res
async def PtrainM(train,xgb_params,nbr,prev_model):
    columns = ['height','width','par_height','par_width','is_link','is_parent_link','is_like_price','is_par_like_price','is_like_name',
               'is_like_paginate','word_count','tag_DIV','tag_P',
               'tag_A','tag_LI','tag_H','tag_SPAN','ptag_DIV',
               'ptag_P','ptag_A','ptag_LI','ptag_H','tag_FONT','ptag_FONT',
               'ptag_SPAN','ChLen','X','Y','digLen','phone','meanLng','label']
    features = ['is_link','is_parent_link','is_like_price','is_par_like_price','is_like_name',
               'is_like_paginate','word_count','tag_DIV','tag_P',
               'tag_A','tag_LI','tag_H','tag_SPAN','ptag_DIV',
               'ptag_P','ptag_A','ptag_LI','ptag_H','tag_FONT','ptag_FONT',
               'ptag_SPAN','ChLen','digLen','phone','meanLng']
    # print(columns)
    df = pd.DataFrame(columns = columns)
    for i in train[0]:
        df = df.append(pd.Series(i[0]+[1], columns), ignore_index=True)
    for i in train[1][:100]: #!!!!!!!!!!!!!!
        df = df.append(pd.Series(i[0]+[0], columns), ignore_index=True)
    df = df.fillna(0)
    # print(df)
    label_train = df['label']
    df = df.drop(columns=['label'])
    df = df.drop(columns=['Y','X']) #!!!! data
    df = df.drop(columns=['height'])
    df = df.drop(columns=['width'])
    df = df.drop(columns=['par_height'])
    df = df.drop(columns=['par_width'])
    # print(df)
    dtrain = xgb.DMatrix(df.astype('float64'), label_train, feature_names=features)
    if xgb_params == {}:
        xgb_params = {
        'objective':'binary:logitraw',
        'eta':0.01,
        'max_depth': 3}
    if prev_model:
        res = pickle.loads(prev_model)
        # res = xgb.Booster({'nthread': 4})
        model = xgb.train(xgb_params,dtrain,num_boost_round=nbr,xgb_model=res)
        # print(model)
        return pickle.dumps(model)
    return pickle.dumps(xgb.train(xgb_params, dtrain, num_boost_round=nbr))
    # return xgb.train(xgb_params, dtrain, num_boost_round=nbr).save_model()




# def trainM(uniqLabels):
#     df = pd.read_csv('data8.csv',encoding = "cp1251")
#     df['zero'] = df.apply(lambda row: 0 if row.label == 0 else 1, axis = 1)
#     label0 = df[df['zero']==0]#1500
#     label1 = df[df['label']==1]
#     label2 = df[df['label']==2]
#     label3 = df[df['label']==3]#int(len_[1])
#     ww = (len(label1)+len(label2)+len(label3))/(len(label0))
#     w0 = [ww*100 for i in label0.values]
#     w1 = [12 for i in label1.values]
#     w2 = [15 for i in label2.values]
#     w3 = [21 for i in label3.values]
# #         print((len(label0)+len(label2)+len(label3))/len(label1),(len(label0)+len(label1)+len(label3))/len(label2),(len(label0)+len(label2)+len(label1))/len(label3),ww)
#     ws = w0+w1+w2+w3
#     df = label0.append(label1).append(label2).append(label3)
#     df = df.replace('NaN','0')
#     df = df.fillna(0)
#     df = df.replace('Infinity','1')
#     label_train = df['label']
#     df = df.drop(columns=['label','zero'])
#     df = df.drop(columns=['Y','X'])
#     df = df.drop(columns=['height'])
#     df = df.drop(columns=['width'])
#     df = df.drop(columns=['par_height'])
#     df = df.drop(columns=['par_width'])
#     dtrain = xgb.DMatrix(df.astype('float64'), label_train,weight = ws)
#     xgb_params = {
#         # 'subsample': 0.99,
#     #     'eval_metric': 'mlogloss',
#     #     'tree_method':'gpu_hist',
#     #     'gpu_id':0,
#         'silent': 0,
#        #'min_child_weight' : 2,
#     'objective':'multi:softmax', #multi:softmax multi:softprob
#     #     'scale_pos_weight' : 0.0000001,
#     #     'scale_pos_weight':(len(label1)+len(label2)+len(label3))/len(label0),
#         'eta':0.01,
#         'max_depth': 1,
#         'num_class':4,
#     }
#     model = xgb.train(dict(xgb_params, silent=0), dtrain, num_boost_round=1500)
#     return model
# def loadDataset():
#     data = pd.read_csv('datas.csv',encoding = "cp1251")
#     data = data.fillna('')
#     Tpaginates = data[data['type']==3]
#     Tprices = data[data['type']==1]
#     TnamesUrls = data[data['type']==2]
    # return set(data['site'].values),{'paginate':Tpaginates,'price':Tprices,'name':TnamesUrls}
def AgenerateP(url,models,url_):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # print(site_links,datas,sites)
    future = asyncio.ensure_future(generateP(url,models,url_))
    res = loop.run_until_complete(future)
    return res
async def generateP(url,models,url_):
    # url_ = ''
    # try:
    #     url_ = url.split('https://')[1]
    # except:
    #     url_ = url.split('http://')[1]
    # url_ = url_.split('/')[0]
    # if url_.split('.')[0] == 'www':
    #     url_ = ''.join(url_.split('.')[1:-1])
    # else:
    #     url_ = ''.join(url_.split('.')[0:-1])
    # check = False
    # for i in sites:
    #     if url_ == i['site']:
    #         check = True
    # if not check:
    columns = ['height','width','par_height','par_width','is_link','is_parent_link','is_like_price','is_par_like_price','is_like_name',
            'is_like_paginate','word_count','tag_DIV','tag_P',
            'tag_A','tag_LI','tag_H','tag_SPAN','ptag_DIV',
            'ptag_P','ptag_A','ptag_LI','ptag_H','tag_FONT','ptag_FONT',
            'ptag_SPAN','ChLen','X','Y','digLen','phone','meanLng','cl','tg','parcl','partg','parparcl','parpartg','text']
    # print(columns)
    arr = []
    elems = []
    options = webdriver.ChromeOptions()
    options.add_argument('headless') 
    d = "{
  "a": {
    "applicationCacheEnabled": false,
    "rotatable": false,
    "mobileEmulationEnabled": false,
    "networkConnectionEnabled": false,
    "chrome": {
      "chromedriverVersion": "2.35 (0)",
      "userDataDir": "/tmp/.org.chromium.Chromium.2EhY8R"
    },
    "takesHeapSnapshot": true,
    "pageLoadStrategy": "normal",
    "databaseEnabled": false,
    "handlesAlerts": true,
    "hasTouchScreen": false,
    "version": "66.0.3359.181",
    "platform": "Linux",
    "browserConnectionEnabled": false,
    "nativeEvents": true,
    "acceptSslCerts": false,
    "acceptInsecureCerts": false,
    "locationContextEnabled": true,
    "webStorageEnabled": true,
    "browserName": "chrome",
    "takesScreenshot": true,
    "javascriptEnabled": true,
    "cssSelectorsEnabled": true,
    "setWindowRect": true,
    "unexpectedAlertBehaviour": ""
  }
}"
    # d['loggingPrefs'] = {'browser':'ALL'}resolve_ip
    #driver = webdriver.PhantomJS()#.Chrome("/opt/app-root/src/chromedriver.exe",options=options)
    print('beforeDriver')
    driver = webdriver.Remote(command_executor='http://selenium-openshift-ai-parser.apps.us-east-1.starter.openshift-online.com:5555/wd/hub',desired_capabilities=d,options=options)
    driver.get(url) #https://rbb-holod.ru/catalog/freony-xladony https://morena.ru/catalog/teploobmennoe-oborudovanie/ http://www.aholod.ru/catalog/42/ https://www.eldorado.ru/c/stiralnye-mashiny/
    js = """
                var res = [];
                document.querySelectorAll('body *').forEach(function(node) {
                try {
                    href = node.href ? 1 :0;
                    parenthref = node.parentNode.href ? 1:0;
                    islikeprice = node.className.toLowerCase().indexOf('price') != -1 || node.className.toLowerCase().indexOf('cost') != -1 ? 1:0;
                    isplikeprice = node.parentNode.className.toLowerCase().indexOf('price') != -1 || node.parentNode.className.toLowerCase().indexOf('cost') != -1 ? 1:0; 
                    islikename = node.innerText.length>=20 && node.innerText.length<=70 ? 1:0;
                    islikepaginate = node.search != "" && node.search ? 1:0;
                    tag_DIV = node.localName == 'div' ? 1:0;
                    tag_P = node.localName == 'p' ? 1:0;
                    tag_A = node.localName == 'a' ? 1:0;
                    tag_LI = node.localName == 'li' ? 1:0;
                    tag_H = node.localName.indexOf('h') != -1 ? 1:0;
                    tag_FONT = node.localName == 'font' ? 1:0;
                    tag_SPAN = node.localName == 'span' ? 1:0;
                    ptag_DIV = node.parentNode.localName == 'div' ? 1:0;
                    ptag_P = node.parentNode.localName == 'p' ? 1:0;
                    ptag_A = node.parentNode.localName == 'a' ? 1:0;
                    ptag_LI = node.parentNode.localName == 'li' ? 1:0;
                    ptag_H = node.parentNode.localName.indexOf('h') != -1 ? 1:0;
                    ptag_FONT = node.parentNode.localName == 'font' ? 1:0;
                    ptag_SPAN = node.parentNode.localName == 'span' ? 1:0;

                    var text =  node.innerText;
                    lens = 0;
                    words = text.split(" ");
                    word_count = words.length;

                    for (let i =0;i<word_count;i++)
                    {
                        lens += words[i].length;
                    }

                    meanLng = lens/word_count;

                    chLen = node.childElementCount;


                    var box = node.getBoundingClientRect();
                    Y = box.top + window.pageYOffset;
                    X = box.left + window.pageXOffset;
                    a = text.replace(/[\s]/g,'').length;
                    b = text.replace(/[\s]/g,'').replace(/[^0-9]/g, '').length;
                    inLen = b/a;
                    phoneCheck = /^[0-9\s+]*[(\s]{1}[0-9]{1,4}[)\s]{1}[-\s\./0-9]+/g.test(text) ? 1 : 0; 

                    width = node.offsetWidth/window.innerWidth;
                    heigth = node.offsetHeight/window.innerHeight;
                    widthP = node.parentNode.offsetWidth/window.innerWidth;
                    heigthP = node.parentNode.offsetHeight /window.innerHeight;
                    var teext = (node.innerText.length <= 100) ? node.innerText.replace(/,/g,"").replace(/\|/g, ''): " ";

                    var out_=[heigth,width,heigthP,
                    widthP,href,parenthref,islikeprice,isplikeprice,
                    islikename,islikepaginate,word_count,tag_DIV,tag_P
                    ,tag_A,tag_LI,tag_H,tag_SPAN,ptag_DIV,ptag_P,ptag_A
                    ,ptag_LI,ptag_H,tag_FONT,ptag_FONT,ptag_SPAN,chLen,X,Y,inLen,phoneCheck,meanLng,node.className,node.localName,
                    node.parentNode.className,node.parentNode.localName,node.parentNode.parentNode.className,node.parentNode.parentNode.localName,teext]
                    if (width > 0 && heigth > 0 && (widthP > 0 || heigthP > 0))
                    { 
                        res.push(out_);
                    }
                } catch (e) {}
                });
                return res
                """
    arr = driver.execute_script(js)#/^[0-9\s+]*[(]{1,2}[0-9]{1,4}[)]{1,2}[-\s\./0-9]*/g
    # print(arr)
    # for entry in driver.get_log('browser'):
    #     if entry['level']=='INFO' and '|' in entry['message']:
    #         arr.append(str(entry['message'].split('|')[-1]).replace('\\u003C','').replace('\\','').replace('"','').split(',')[:-1])
    dft = pd.DataFrame(data=arr,columns = columns)
    # print(dft)
    driver.close()
    print('closedDriver')
    dft = dft.replace('NaN','0')
    dft = dft.fillna(0)
    dft = dft.replace('Infinity','1')
    dft = dft.drop(columns=['X','Y'])
    dft = dft.drop(columns=['height'])
    dft = dft.drop(columns=['width'])
    dft = dft.drop(columns=['par_height'])
    dft = dft.drop(columns=['par_width'])
    dtest = xgb.DMatrix(dft.drop(columns=['cl','tg','parcl','partg','parparcl','parpartg','text']).astype('float64'))
    # print(dft.drop(columns=['cl','tg','parcl','partg','parparcl','parpartg','text']))
    for model in models:
        # print(model)
        model = pickle.loads(model[0])
        pred = model.predict(dtest)
        pred = pred.tolist()
        for i in range(len(pred)):
            pred[i] = 1 if pred[i] > 0.5 else 0
        pred = np.array(pred)
        # print(pred)
        fSearch = ['site','tag','ptag','pptag','class','pclass','ppclass']
        siteelems = []
        good = pred[pred == 1]
        # for k in range(1,lbl_count):
        indexed = dft.iloc[np.where(pred == 1)[0]]
        for i in indexed.values:
            siteelems.append({'site':url_,
                        #'type':k, текст/ссылка/число - не нужно
                        'tag':str(i[-6]) if str(i[-6])!='' else '',
                        'class':'class='+str(i[-7]) if str(i[-7])!='' else '=',
                        'ptag':str(i[-4]) if str(i[-4])!='' else '',
                        'pptag':str(i[-2]) if str(i[-2])!='' else '',
                        'pclass':'class='+str(i[-5]) if str(i[-5])!='' else '=',
                        'ppclass':'class='+str(i[-3]) if str(i[-3])!='' else '='
                        })
    #             print(i,k)
        # print(len(elems))
        elems.append([dict(s) for s in set(frozenset(d.items()) for d in siteelems)])
    return elems




# def sec_search(sites,datas,query,count):
#     site_links = url_find(query,count)  
#     model = trainM()
#     res = []
#     for i in site_links:
#         generate(i,model,sites)
#     # urls,datas = loadDataset()
#     print(site_links)
#     loop = asyncio.get_event_loop()
#     future = asyncio.ensure_future(parse_pages(site_links,sites,datas))
#     res = loop.run_until_complete(future)
#     return res   
def asyncParse(site_links,sites,datas):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(site_links)
    # loop.run_until_complete(site_links)


    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # print(site_links,datas,sites)
    future = asyncio.ensure_future(parse_pagesP(site_links,sites,datas))
    res = loop.run_until_complete(future)
    return res   
#     print(site_links)
#     with Pool() as p:
#         records = p.starmap(defs.parse_pages,[(site_links,urls,datas)])
#         records = p.map(partial(defs.parse_pages, urls = urls,datas = datas), site_links)
#     return list(records)
#     datas = pd.read_csv('datas.csv',encoding = "cp1251")
#     datas = datas.fillna('')
#     urls = set(datas['site'])
