import csv
import pandas as pd
import mysql.connector as connector
from datetime import date
import os
import dotenv

dotenv.load_dotenv(".env")
print("Starting seeder")

dbconn = connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = dbconn.cursor()
df = pd.read_csv("./dataset.csv", encoding='windows-1252')

def get_sum_data(selector):
    result = 0
    select = "SELECT COUNT(*) FROM {}".format(selector)
    try:
        cursor.execute(select)
        data = cursor.fetchall()
        result = data[0][0]
    except Exception as e:
        print("Something went wrong", e)
        return "error"
    return result

query_db = get_sum_data("products")
if (query_db > 0):
    dbconn.close()
    print("Data already inserted")
    exit()

def get_data(selector):
    result = {}
    select = "SELECT * FROM {}".format(selector)
    try:
        cursor.execute(select)
        data = cursor.fetchall()
        for item in data:
            result[item[1]] = item[0]
    except:
        print("Something went wrong")
        return {}
    return result


def get_fk_id(fk, dict_data):
    arr = []
    for item in dict_data:
        idx = dict_data[item]
        idx = fk[idx]
        arr.append([item, idx])
    return arr

def insert_data(sql_script, data):
    cursor.executemany(sql_script, data)
    try:
        print(cursor.rowcount, "records inserted")
    except:
        print('Something went wrong')
    dbconn.commit()

def insert_id_name(df_key, tb_name):
    dt = df[df_key].unique().tolist()
    arrs = []
    for item in dt:
        arrs.append([item])

    sql = "INSERT INTO {}(name) VALUES(%s)".format(tb_name)
    insert_data(sql, arrs)

data_map = {
    "Country":"countries",
    "Region":"regions",
    "Segment":"segments",
    "Ship Mode":"ship_modes",
    "Category":"categories",
}

for item in data_map:
    insert_id_name(item,data_map[item])

def insert_name_idfk(tb_fk, df_fk, tb_name, df_key, fk_attrib):
    res = get_data(tb_fk)
    group = df[[df_key,df_fk]].groupby([df_key]).first().to_dict()
    group = get_fk_id(res, group[df_fk])
    sql = "INSERT INTO {}(name, {}) VALUES(%s,%s)".format(tb_name, fk_attrib)
    insert_data(sql,group)

data_map = [
    ["countries","Country","states","State","country_id"],
    ["states","State","cities","City","state_id"],
    ["categories","Category","sub_categories","Sub-Category","category_id"]
]

for item in data_map:
    insert_name_idfk(item[0],item[1],item[2],item[3],item[4])

def insert_customID_name_fk(tb_fk, df_fk, tb_name, df_key, df_id, fk_attrib):
    res = get_data(tb_fk)

    dt = df[[df_key,df_id,df_fk]].groupby([df_id]).first().to_dict()
    values = {}
    for item in dt:
        for j in dt[item]:
            if item == df_fk:
                dt[item][j] = res[dt[item][j]]
            if j not in values:
                values[j] = [dt[item][j]]
            else:
                values[j].append(dt[item][j])
    results = []
    for item in values:
        temp = values[item]
        item = [item]
        item+=temp
        results.append(item)
    sql = "INSERT INTO {}(id,name,{}) VALUES(%s,%s,%s)".format(tb_name,fk_attrib)
    insert_data(sql, results)

data_map = [
    ["segments","Segment","customers","Customer Name","Customer ID","segment_id"],
    ["sub_categories","Sub-Category","products","Product Name","Product ID","sub_category_id"]
]
for item in data_map:
    insert_customID_name_fk(item[0],item[1],item[2],item[3],item[4],item[5])

dt = df[['Order ID','Order Date','Ship Date','Postal Code','Customer ID','Ship Mode','City','Region']].groupby(["Order ID"]).first().to_dict()


# get datas
# customers = get_data("customers")
ship_modes = get_data("ship_modes")
cities = get_data("cities")
regions = get_data("regions")


data_map = {}
for item in dt:
    for order_id in dt[item]:
        if item == "Ship Mode":
            dt[item][order_id] = ship_modes[dt[item][order_id]]
        elif item == "City":
            dt[item][order_id] = cities[dt[item][order_id]]
        elif item == "Region":
            dt[item][order_id] = regions[dt[item][order_id]]
        elif item == "Order Date" or item == "Ship Date":
            temp = dt[item][order_id].split("/")
            dt[item][order_id] = date(eval(temp[2]),eval(temp[0]),eval(temp[1]))
            # print(dt[item][order_id])


        if order_id not in data_map:
            data_map[order_id]=[dt[item][order_id]]
            continue
        data_map[order_id].append(dt[item][order_id])
results = []
for item in data_map:
    temp = data_map[item]
    item = [item]
    item+=temp
    results.append(item)

sql = "INSERT INTO orders(id,order_date,ship_date,postal_code,customer_id,ship_mode_id,city_id,region_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
insert_data(sql,results)

dt = df[['Order ID','Sales','Quantity','Discount','Profit','Product ID']].to_dict()

data_map = {}
for item in dt:
    for order_id in dt[item]:
        if order_id not in data_map:
            data_map[order_id]=[dt[item][order_id]]
            continue
        data_map[order_id].append(dt[item][order_id])
results = []
for item in data_map:
    temp = data_map[item]
    results.append(temp)
print(results)

sql = "INSERT INTO order_details(order_id,sales,quantity,discount,profit,product_id) VALUES(%s,%s,%s,%s,%s,%s)"
insert_data(sql,results)


dbconn.close()
print("Seeding completed")