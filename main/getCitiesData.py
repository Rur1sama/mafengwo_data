#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：mafengwo_data
@File    ：getCitiesData.py
@IDE     ：PyCharm 
@Author  ：lee_yukhang
@Date    ：2024/2/27 12:52 
'''

'''
将所有的城市ID、网址及其POI数量将会保存到数据库中
保存的数据库名称为：地途
保存城市数据的数据集合：cities_data
保存城市对应POI的数据集合：{城市ID}_POIs
'''
from functions.class_01_mongodb import MongoDB
from functions.function_04_getCitiesData_MongoDB import getCitiesData_DB
from functions.function_08_getPOIComment_MongoDB import get_POIcomment_DB
from functions.function_10_readcity_list import readcity_list

# 爬取城市信息：使用func04-数据库版
city_mongo = MongoDB(dataset='地途', collection='cities_data')  # 新建或连接一个数据库实例
getCitiesData_DB(city_mongo)  # 用于爬取所有城市列表到cities_data里面，若集合里面有数据，就会不爬了，重复爬取请删除数据

# 爬取目的地信息(城市的POI信息)： 使用func05-getPOIID

# todo 将上述爬取的对应城市信息用于爬取其前300个POI
cityID_list = readcity_list(city_mongo)  # cityID_list 是一个列表，存储着所有城市的id
for cityID in cityID_list:
    cities_POIs_mongo = MongoDB(dataset='地途', collection=f'{cityID}_POIs')  # 新建或连接一个数据库实例
    get_POIcomment_DB(cityID, cities_POIs_mongo)

