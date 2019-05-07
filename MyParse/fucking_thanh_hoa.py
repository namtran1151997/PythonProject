
def replace_thanh_hoa(dn_collection):
    business_th = dn_collection.find({'dia_chi': {'$regex': 'Hoá'}})
    for dn in business_th:
        dia_chi = dn['dia_chi']
        dia_chi = dia_chi.replace("Hoá", "Hóa")
        dn_collection.update_one({'_id': dn['_id']}, {"$set": {"dia_chi": dia_chi}}, upsert=False)
