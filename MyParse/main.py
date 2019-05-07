import json
from bs4 import BeautifulSoup
import os
import no_accent_vietnamese as nav
import pymongo
import fucking_thanh_hoa
import modify_doanhnghiep


# cap truyen tham so path vao day
def parse_doanh_nghiep(path, dn_collection):
    for file_name in os.listdir(path):
        if os.stat(path + "/" + file_name).st_size == 0:
            continue
        file = open(path + "/" + file_name, 'r')
        json_data = json.loads(file.read())
        m_dict = {}
        m_list = []
        a = json_data['title'].split(' ')
        a.pop(0)
        tdn = ' '.join(a)
        m_dict['ten_doanh_nghiep'] = tdn

        soup = BeautifulSoup(json_data['content'], "lxml")
        for paragraph in soup.find_all('li'):
            if paragraph.text[0] != ' ':
                break
            if ':' in paragraph.text and '[' in paragraph.text and "Ngày hoạt động" not in paragraph.text:
                l1 = (paragraph.text.split('['))
                m_list.append(l1[0])
            elif ':' in paragraph.text and '[' not in paragraph.text and "Ngày hoạt động" not in paragraph.text:
                m_list.append(paragraph.text)
            elif ':' in paragraph.text and "Ngày hoạt động" in paragraph.text:
                l1 = (paragraph.text.split('('))
                m_list.append(l1[0])

        for e in m_list:
            elm = e.split(': ')
            nav_elm = nav.remove_accents(elm[0]).lower()
            l_elm = nav_elm.split(' ')
            l_elm.pop(0)
            key = '_'.join(l_elm)
            m_dict[key] = elm[1]
        x = dn_collection.insert_one(m_dict)

        print(x.inserted_id)


if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["webDoanhNghiep"]
    dn_collection = db["business"]
    path = '/home/nam/Downloads/info'
    parse_doanh_nghiep(path, dn_collection)
    fucking_thanh_hoa.replace_thanh_hoa(dn_collection)
    modify_doanhnghiep.modify_dn(client)
