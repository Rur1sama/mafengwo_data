# builder:wstki
# 开发时间11:55,2024/2/2
# name:function_05_getPOIID
import re
import logging
from bs4 import BeautifulSoup
import time
import requests
from functions.function_02_md5_getCityPOIList import _md5
REQ = requests.session()
# 获取一个城市的POI和对应的编号
def _get_route( mdd_id):
    '''
    获取景点信息
    '''
    results = []
    # 获取景点有多少页，防止少于20页
    post_data = _md5({
        'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
        'iMddid': mdd_id,
        'iTagId': 0,
        'iPage': 1
    })
    url = 'http://www.mafengwo.cn/ajax/router.php' + '?' + '&'.join(
        [f'{key}={value}' for key, value in post_data.items()])
    r = REQ.post(url, data=post_data)
    if r.status_code == 403:
        exit('访问被拒绝')
    response = r.json()
    list_data = response['data']['list']
    page_data = response['data']['page']
    soup_page = BeautifulSoup(page_data, "html.parser")
    page = int(soup_page.find('span', class_='count').find('span').text)
    # 没法突破20页的限制，每个城市最多只能获取300个POI
    for page in range(1,page):
        post_data = _md5({
            'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
            'iMddid': mdd_id,
            'iTagId': 0,
            'iPage': page
        })
        url = 'http://www.mafengwo.cn/ajax/router.php' + '?' + '&'.join([f'{key}={value}' for key, value in post_data.items()])
        r = REQ.post(url, data=post_data)
        if r.status_code == 403:
            exit('访问被拒绝')
        response = r.json()
        list_data = response['data']['list']
        print(list_data)
        page_data = response['data']['page']
        # 解析景点列表数据
        soup = BeautifulSoup(list_data, "html.parser")
        route_list = soup.find_all('a')

        for route in route_list:
            link = route['href']
            route_id = re.findall(r'/poi/(.*?).html', link)
            name = route['title']
            image = route.find('img')['src'].split('?')[0]
            results.append({
                'poi_id': int(route_id[0]),
                'name': name,
                'image': image,
                'link': 'http://www.mafengwo.cn' + link,
            })



        # 返回当前页列表数据和总页数
    return results
