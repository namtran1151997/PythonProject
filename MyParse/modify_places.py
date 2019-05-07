import pymysql

if __name__ == '__main__':
    db = pymysql.connect("localhost", "nam", "namtran115", "thongtincongty", charset='utf8', use_unicode=True)
    cursor = db.cursor()

    sql = "SELECT * FROM `places`"

    cursor.execute(sql)

    data = cursor.fetchall()
    i = 0
    for row in data:
        list_word = row[3].split(' ')
        for i in range(len(list_word)):
            if list_word[i] == "Hóa":
                list_word[i] = "Hoá"
            if list_word[i] == "Hòa":
                list_word[i] = "Hoà"
        place = ' '.join(list_word)

        sql = "UPDATE `places` SET `place` = '" + place + "' WHERE `places`.`ID` = " + str(row[0])
        cursor.execute(sql)
        db.commit()
        i += 1
        print(i)

    db.close()
