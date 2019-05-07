import json
import os
import re

import pymongo
import pymysql
import no_accent_vietnamese as nav
from bs4 import BeautifulSoup

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["webDoanhNghiep"]
business_collection = db["business"]
place_collection = db["places"]
path = '/home/nam/Downloads/info/'

sql_db = pymysql.connect("localhost", "nam", "namtran115", "thongtincongty", charset='utf8', use_unicode=True)
cursor = sql_db.cursor()


def str_to_permalink(no_accent_title):
    list_word = no_accent_title.split(' ')
    return '-'.join(list_word)


def get_business_name_and_permalink(my_dict):
    no_accent_name = nav.no_accent_vietnamese(my_dict['title'])
    business_permalink = str_to_permalink(no_accent_name.lower())
    list_word = list(my_dict['title'].split(' '))
    list_word.pop(0)
    business_name = ' '.join(list_word)
    return business_name, business_permalink


# lấy về dữ liệu của doanh nghiệp
def get_business_content(my_dict, content):
    soup = BeautifulSoup(my_dict['content'], 'html.parser')
    business_content = soup.findAll('li')

    for x in business_content:
        # print(x.text)
        if "Xem thêm" in x.text:
            break
        if ":" in x.text:
            temp = x.text.split(':')
            if '(' in temp[1]:
                start = temp[1].index('(')
                if ')' not in temp[1]:
                    end = len(temp[1])
                else:
                    end = temp[1].index(')') + 1
                temp[1] = temp[1].replace(temp[1][start:end], '')
            if '[' in temp[1]:
                temp[1] = temp[1].replace(temp[1][temp[1].index('['):temp[1].index(']') + 1], '')
            if "TP" in temp[1]:
                temp[1] = temp[1].replace("TP", '')
            if "." in temp[1]:
                temp[1] = temp[1].replace(".", '')
            if "'" in temp[1]:
                temp[1] = temp[1].replace("'", "&#039;")
            # if "Thành phố" in temp[1]:
            #     temp[1] = temp[1].replace("Thành phố", '')
            temp[0] = string_to_key(remove_excess_blank(temp[0]))
            temp[1] = remove_excess_blank(temp[1])
            content[temp[0]] = temp[1]
    return content


# loại bỏ khoảng trắng bị thừa
def remove_excess_blank(string):
    if string is '':
        return ''
    list_word = string.split(' ')
    if "" in list_word:
        list_word.remove("")
    if "" in list_word:
        list_word.remove("")
    return ' '.join(list_word)


# Chỉnh sửa chữ bị sai
def modify_wrong_word(business_address):
    temp = ""
    for i in range(len(business_address)):
        if business_address[i] == ',':
            temp += ' -'
        else:
            temp += business_address[i]
    list_address = temp.split('-')
    for i in range(len(list_address)):
        list_address[i] = remove_excess_blank(list_address[i])
        list_word = list_address[i].split(' ')
        for j in range(len(list_word)):
            if list_word[j] == "Hóa":
                list_word[j] = "Hoá"
            if list_word[j] == "Hòa":
                list_word[j] = "Hoà"
            if list_word[j] == "Cạn":
                list_word[j] = "Kạn"
            if list_word[j] == "Đắc":
                list_word[j] = "Đắk"
            if list_word[j] == "Lắc":
                list_word[j] = "Lắk"
        list_address[i] = ' '.join(list_word)
    return ' - '.join(list_address)


def string_to_key(string):
    key = nav.no_accent_vietnamese(string).lower().split(' ')
    return '_'.join(key)


if __name__ == '__main__':
    for file_name in os.listdir(path):
        file = open(path + file_name, 'r')
        if os.stat(path + "/" + file_name).st_size == 0:
            continue
        business_dict = json.loads(file.read())
        business_name, business_permalink = get_business_name_and_permalink(business_dict)
        content = {
            'name': business_name,
            'permalink': business_permalink,
        }
        business_content = get_business_content(business_dict, content)
        if 'dia_chi' in business_content:
            business_content['dia_chi'] = modify_wrong_word(business_content['dia_chi'])
            document = business_collection.insert_one(business_content)
            print(document.inserted_id)

    for business in business_collection.find():
        print(business['_id'])
        list_address = business['dia_chi'].split("-")
        address1 = remove_excess_blank(list_address[len(list_address) - 1])
        place1 = place_collection.find_one({'place': {"$regex": address1, "$options": "i"}, 'parent': '0'})
        # sql = "select * from places where place like '%" + address1 + "%' and parent = " + str(0)
        # cursor.execute(sql)
        # place1 = cursor.fetchone()
        if place1 is not None and len(list_address) > 2:
            business_collection.update_one({'_id': business['_id']}, {"$set": {"NID1": place1['NID']}}, upsert=False)
            address2 = remove_excess_blank(list_address[len(list_address) - 2])
            place2 = place_collection.find_one(
                {'place': {"$regex": address2, "$options": "i"}, 'parent': place1["NID"]})
            # sql = "select * from places where place like '%" + address2 + "%' and parent = " + place1[1]
            # cursor.execute(sql)
            # place2 = cursor.fetchone()
            if place2 is not None and len(list_address) > 3:
                business_collection.update_one({'_id': business['_id']}, {"$set": {"NID2": place2['NID']}},
                                               upsert=False)
                address3 = remove_excess_blank(list_address[len(list_address) - 3])
                place3 = place_collection.find_one(
                    {'place': {"$regex": address3, "$options": "i"}, 'parent': place2["NID"]})
                # sql = "select * from places where place like '%" + address3 + "%' and parent = " + place2[1]
                # cursor.execute(sql)
                # place3 = cursor.fetchone()
                if place3 is not None:
                    business_collection.update_one({'_id': business['_id']}, {"$set": {"NID3": place3['NID']}},
                                                   upsert=False)
    print("Done!")
