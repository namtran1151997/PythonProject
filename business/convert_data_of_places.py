import pymysql
import pymongo

# convert data of places from mysql to mongodb
if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["webDoanhNghiep"]
    mycol = mydb["places"]

    db = pymysql.connect("localhost", "nam", "namtran115", "thongtincongty", charset='utf8', use_unicode=True)
    cursor = db.cursor()

    sql = "select * from places"

    cursor.execute(sql)

    data = cursor.fetchall()

    for row in data:
        m_dict = {
            'NID': row[1],
            'parent': row[2],
            'place': row[3],
            'permalink': row[4]}
        x = mycol.insert_one(m_dict)
        print(x.inserted_id)
    db.close()
    myclient.close()
