import pymongo


def ignore_blank(temp):
    while "" in temp:
        temp.remove("")
    while "TP" in temp:
        temp.remove("TP")
    li = []
    for w in temp:
        li.append(w.capitalize())
    return ' '.join(temp)


def modify_dn(myclient):
    mydb = myclient["webDoanhNghiep"]
    places = mydb['places']
    mycol = mydb["business"]

    for dn in mycol.find():
        print('-----------------------------------------------------------------------------------------------------')
        dia_chi = dn['dia_chi']
        print(dn['_id'])
        # lay dia chi
        if '(' in dia_chi:
            dia_chi = dia_chi.replace('(', '')
            if ')' in dia_chi:
                dia_chi = dia_chi.replace(')', '')
            if '-' in dia_chi:
                dia_chi = dia_chi.split('-')
            elif ',' in dia_chi:
                dia_chi = dia_chi.split(',')
        else:
            if '-' in dia_chi:
                dia_chi = dia_chi.split('-')
            elif ',' in dia_chi:
                dia_chi = dia_chi.split(',')

        # tach lay vi tri cuoi
        t1 = dia_chi[len(dia_chi) - 1]
        t1 = ignore_blank(t1.split(' '))
        place1 = places.find_one({'place': {"$regex": t1}, 'parent': '0'})
        if place1 is not None:
            mycol.update_one({'_id': dn['_id']}, {"$set": {"NID1": place1['NID']}}, upsert=False)
            t2 = dia_chi[len(dia_chi) - 2]
            t2 = ignore_blank(t2.split(' '))
            place2 = places.find_one({'place': {"$regex": t2}, 'parent': place1['NID']})
            if place2 is not None:
                mycol.update_one({'_id': dn['_id']}, {"$set": {"NID2": place2['NID']}}, upsert=False)
                t3 = dia_chi[len(dia_chi) - 3]
                t3 = ignore_blank(t3.split(' '))
                place3 = places.find_one({'place': {"$regex": t3}, 'parent': place2['NID']})
                if place3 is not None:
                    mycol.update_one({'_id': dn['_id']}, {"$set": {"NID3": place3['NID']}}, upsert=False)

