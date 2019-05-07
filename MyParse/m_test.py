import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["webDoanhNghiep"]
mycol = mydb["business"]


def ignore_blank(temp):
    while "" in temp:
        temp.remove("")
    while "TP" in temp:
        temp.remove("TP")
    li = []
    for w in temp:
        print(w)
        if w is "Hoà":
            li.append("Hòa")
        else:
            li.append(w.capitalize())

    return ' '.join(temp)


doanhnghiep_th = mycol.find({'dia_chi': {'$regex': 'Hoà'}})
i = 0
for dn in doanhnghiep_th:
    list_address = dn['dia_chi'].split('-')
    print(list_address)
    list_address[len(list_address) - 1] = ignore_blank(list_address[len(list_address) - 1].split())
    list_address[len(list_address) - 2] = ignore_blank(list_address[len(list_address) - 2].split())
    list_address[len(list_address) - 3] = ignore_blank(list_address[len(list_address) - 3].split())
    print(list_address)
    i += 1
    if i == 10:
        break
    # dia_chi = dn['dia_chi']
    # dia_chi = dia_chi.replace("Hoá", "Hóa")
    # mycol.update_one({'_id': dn['_id']}, {"$set": {"dia_chi": dia_chi}}, upsert=False)
