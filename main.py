from fastapi import FastAPI, Form
from tensorflow import keras
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from keras.models import load_model
import uvicorn
import responses
import json
import pyodbc
import collections

# Load Prediction Model
model = load_model('project3.h5')


# ประกาศ Object FastAPI
app = FastAPI()

# เชื่อม DATABASE MSSQL
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=GENG\SQLEXPRESS;'
                      'Database=Project;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

Email = "sitthiporn.k@ku.th"
Password = "555"
find_user = ("SELECT * FROM accounts WHERE email = ? AND password = ?")
cursor.execute(find_user, [(Email), (Password)])
accounts = cursor.fetchall()
print(accounts, type(accounts))
if accounts:
    print("TRUE")
    for loop in accounts:
        print("ID       "+loop[0])
        print("USER     "+loop[1])
        print("PASSWORD "+loop[2])
        print("EMAIL    "+loop[3])
    # return {"status": int(1),
    #         "Email": str(Email)}
else:
    print("username and password not recognised")
    # return {"status": int(0)}


# กำหนดให้สามารถเข้าถึงโดเมนที่ต่างกันได้ระหว่าง frontend และ backend
origins = [
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)


# กำหนด PATH ของ API
@app.get("/")
async def main():
    return 'WELCOME TO SALES FORCAST '


@app.get("/test")
async def test():
    cursor.execute('SELECT * FROM Project.dbo.features')
    fetched_data = cursor.fetchall()
    data = [list(rows) for rows in fetched_data]
    # print(data)
    # print(type(data))
    # numbers = ["1", "2", "3"]
    json_numbers = json.dumps(data)
    print(json_numbers)          # ["1", "2", "3"]
    print(type(json_numbers))    # <class 'str'>
    return {"data": str(json_numbers)}


@app.get("/query_select")
async def query_select():
    cursor.execute('selectFeatures')
    value = cursor.fetchall()
    objects_list = []
    data = [list(rows) for rows in value]
    for row in data:
        d = collections.OrderedDict()
        d["id_features"] = row[0]
        d["name_features"] = row[1]
        objects_list.append(d)
    return objects_list

# ยอดขายเดือนที่แล้ว(เดือน 8)


@app.get("/selectsalelastmonth")
async def selectsalelastmonth():
    cursor.execute('selectSalelastmonth')
    value = cursor.fetchall()
    objects_list = []
    data = [list(rows) for rows in value]
    for row in data:
        d = collections.OrderedDict()
        d["Month"] = row[0]
        d["SalesAct_Month"] = row[1]
        objects_list.append(d)
    return objects_list

# ยอดขายจากการ FORECAST ล่าสุด(เดือน 9)


@app.get("/selectsalelastpredict")
async def selectsalelastpredict():
    cursor.execute('selectsalelastpredict')
    value = cursor.fetchall()
    objects_list = []
    data = [list(rows) for rows in value]
    for row in data:
        d = collections.OrderedDict()
        d["predicts"] = row[0]
        objects_list.append(d)
    return objects_list

#  ยอดขายเฉลี่ย 3 ปีย้อนหลังของเดือนที่แล้ว(เดือน 8)


@app.get("/selectsaleavgtreeyear")
async def selectsaleavgtreeyear():
    cursor.execute('selectsaleavgtreeyear')
    value = cursor.fetchall()
    objects_list = []
    data = [list(rows) for rows in value]
    for row in data:
        d = collections.OrderedDict()
        d["month"] = row[0]
        d["saleavgtreeyear"] = row[1]
        objects_list.append(d)
    return objects_list

# ยอดขายเดือนปัจจุบันของปีที่แล้ว เดือน(9)


@app.get("/selectsalelastyear")
async def selectsalelastyear():
    cursor.execute('selectsalelastyear')
    value = cursor.fetchall()
    objects_list = []
    data = [list(rows) for rows in value]
    for row in data:
        d = collections.OrderedDict()
        d["month"] = row[0]
        d["salelastyear"] = row[1]
        objects_list.append(d)
    return objects_list


@app.get("/query_insert1")  # insert ข้อมูลตรงจากตาราง
async def query_insert(Id: str,
                       Features: str):
    insert = (
        "INSERT INTO features (id_features, name_features) VALUES (?, ?) COMMIT")
    cursor.execute(insert, [(Id), (Features)])
    return {"Id": Id,
            "Features": Features}


@app.get("/query_insert2")  # insert ข้อมูลผ่าน store procedure
async def query_insert2(id_features: str,
                        name_features: str):
    query = "{CALL insertFeatures (?, ?)}"
    cursor.execute(query, (id_features), (name_features))
    cursor.commit()

# @app.get("/query_delete")
# async def querylete():
#     delete = ("DELETE FROM features WHERE ")


@app.get("/predict")
async def create_item(WageRate: float,
                      Jobless: float,
                      ExchangeRate_BathToDollar: float,
                      GoldPrice: float,
                      GasoholNineOne: float,
                      NewRegis: int,
                      NewRegisRed: int,
                      RegisAll_IncreaseYear: float,
                      RegisAll_IncreaseAvgYear: float,
                      BankHoliday: int,
                      Monday: int,
                      EggPrice: float,
                      PalmOilPrice: float,
                      AgentAct_IncMonth: int,
                      AgentAct_IncConEachYear: int,
                      SalesAct_BeforeMonthPresent: int,
                      SalesAct_IncConYear: int,
                      SalesAct_AvgMonth_OfSalesIncConYear: float,
                      SalesAct_AllYear: float,
                      SalesAct_AvgMonth_OfSalesAllYear: float,
                      SalesAct_TotalSpecMonth: int,
                      SalesAct_AvgMonth_OfSalesTotalSpecMonth: float,
                      SalesAct_IncConSpecMonth: int,
                      SalesAct_AvgMonth_OfSalesIncConSpecMonth: float,
                      SalesAct_MonthOfYearBefore: int,
                      SalseAct_TotalThreeYearBefore_AvgMonth: float,
                      Date: str,
                      Month: str):
    instant = [[WageRate, Jobless, ExchangeRate_BathToDollar, GoldPrice, GasoholNineOne, NewRegis, NewRegisRed, RegisAll_IncreaseYear,
                RegisAll_IncreaseAvgYear, BankHoliday, Monday, EggPrice, PalmOilPrice, AgentAct_IncMonth,
                AgentAct_IncConEachYear, SalesAct_BeforeMonthPresent, SalesAct_IncConYear, SalesAct_AvgMonth_OfSalesIncConYear, SalesAct_AllYear,
                SalesAct_AvgMonth_OfSalesAllYear, SalesAct_TotalSpecMonth, SalesAct_AvgMonth_OfSalesTotalSpecMonth, SalesAct_IncConSpecMonth,
                SalesAct_AvgMonth_OfSalesIncConSpecMonth, SalesAct_MonthOfYearBefore, SalseAct_TotalThreeYearBefore_AvgMonth]]
    result = model.predict(instant)[0]
    
    # month_str = Date[5:7]  # ตัดสตริงให้เหลือแค่เดือน
    month_int = int(Month) # แปลงสตริงเป็นเลขจำนวนเต็ม
    value = [] # สร้าง list ไว้เก็บค่าที่ predict
    value.append(result[0]) # เก็บค่า predict เดือนถัดไป 
    
    print("predict month", Month, "=", result[0])
    for next_month in range(12-month_int):
        month_int = month_int+1
        month_str = str(month_int)
        instant = [[WageRate, Jobless, ExchangeRate_BathToDollar, GoldPrice, GasoholNineOne, NewRegis, NewRegisRed, RegisAll_IncreaseYear,
                    RegisAll_IncreaseAvgYear, BankHoliday, Monday, EggPrice, PalmOilPrice, AgentAct_IncMonth,
                    AgentAct_IncConEachYear, value[-1], SalesAct_IncConYear, SalesAct_AvgMonth_OfSalesIncConYear, SalesAct_AllYear,
                    SalesAct_AvgMonth_OfSalesAllYear, SalesAct_TotalSpecMonth, SalesAct_AvgMonth_OfSalesTotalSpecMonth, SalesAct_IncConSpecMonth,
                    SalesAct_AvgMonth_OfSalesIncConSpecMonth, SalesAct_MonthOfYearBefore, SalseAct_TotalThreeYearBefore_AvgMonth]]
        result2 = model.predict(instant)[0]
        value.append(result2[0])
        print("predict month", month_str, "=", result2[0])
    return {"Forecast": int(result)}


@app.get("/predict2")
async def create_predict2(Inputlist: int):
    result = model.predict(Inputlist)
    return {"Output": int(result)}


@app.get("/saveinput")
async def saveinput(
        WageRate: int,
        Jobless: int,
        ExchangeRate_BathToDollar: int,
        GoldPrice: int,
        GasoholNineOne: int,
        NewRegis: int,
        NewRegisRed: int,
        RegisAll_IncreaseYear: int,
        RegisAll_IncreaseAvgYear: int,
        BankHoliday: int,
        Monday: int,
        EggPrice: int,
        PalmOilPrice: int,
        AgentAct_IncMonth: int,
        AgentAct_IncConEachYear: int,
        SalesAct_BeforeMonthPresent: int,
        SalesAct_IncConYear: int,
        SalesAct_AvgMonth_OfSalesIncConYear: int,
        SalesAct_AllYear: int,
        SalesAct_AvgMonth_OfSalesAllYear: int,
        SalesAct_TotalSpecMonth: int,
        SalesAct_AvgMonth_OfSalesTotalSpecMonth: int,
        SalesAct_IncConSpecMonth: int,
        SalesAct_AvgMonth_OfSalesIncConSpecMonth: int,
        SalesAct_MonthOfYearBefore: int,
        SalseAct_TotalThreeYearBefore_AvgMonth: int,
        Date: str,
        Month: str):
    # รับค่าตัวแปรเพื่อใช้คำนวณใน model
    input_pred1 = [[WageRate, Jobless, ExchangeRate_BathToDollar, GoldPrice, GasoholNineOne, NewRegis, NewRegisRed, RegisAll_IncreaseYear,
                    RegisAll_IncreaseAvgYear, BankHoliday, Monday, EggPrice, PalmOilPrice, AgentAct_IncMonth,
                    AgentAct_IncConEachYear, SalesAct_BeforeMonthPresent, SalesAct_IncConYear, SalesAct_AvgMonth_OfSalesIncConYear, SalesAct_AllYear,
                    SalesAct_AvgMonth_OfSalesAllYear, SalesAct_TotalSpecMonth, SalesAct_AvgMonth_OfSalesTotalSpecMonth, SalesAct_IncConSpecMonth,
                    SalesAct_AvgMonth_OfSalesIncConSpecMonth, SalesAct_MonthOfYearBefore, SalseAct_TotalThreeYearBefore_AvgMonth]]


    # รับค่าเพื่อบันทึกลง database
    input_pred2 = [WageRate, Jobless, ExchangeRate_BathToDollar, GoldPrice, GasoholNineOne, NewRegis, NewRegisRed, RegisAll_IncreaseYear,
                   RegisAll_IncreaseAvgYear, BankHoliday, Monday, EggPrice, PalmOilPrice, AgentAct_IncMonth,
                   AgentAct_IncConEachYear, SalesAct_BeforeMonthPresent, SalesAct_IncConYear, SalesAct_AvgMonth_OfSalesIncConYear, SalesAct_AllYear,
                   SalesAct_AvgMonth_OfSalesAllYear, SalesAct_TotalSpecMonth, SalesAct_AvgMonth_OfSalesTotalSpecMonth, SalesAct_IncConSpecMonth,
                   SalesAct_AvgMonth_OfSalesIncConSpecMonth, SalesAct_MonthOfYearBefore, SalseAct_TotalThreeYearBefore_AvgMonth]

    cursor.execute('SelectIdInputform')
    data = [list(rows) for rows in cursor]

    # เงื่อนไข check list ของ field id_predicts ว่ามีค่าหรือไม่มีค่า
    if len(data) == 0:
        print("list is empty")
        data.append(1)
        id_pred = data[0]
        print(id_pred)
    else:
        print("list is not empty")
        for row in input_pred2:
            id_pred = (data[0])[0]+1
        print(id_pred)

    # loop บันทึกค่าลง ตาราง inputform
    number_int = 1
    for row in input_pred2:
        number_str = str(number_int)
        query1 = "{CALL InsertInputform (?, ?, ?)}"
        cursor.execute(query1, id_pred, number_str.zfill(3), row)
        number_int = number_int+1

    ############################### บันทึกค่าจากการ forecast ลงตาราง predicts ค่าเดือนถัดไปจริงๆ #################################################
    result = model.predict(input_pred1)[0]
    result = int(result)
    status1 = "1"
    query2 = "{CALL insertpredict (?, ?, ?, ?, ?)}"
    cursor.execute(query2, id_pred, result, Date, status1, Month)
    cursor.commit()

    # month_str = Date[5:7]  # ตัดสตริงให้เหลือแค่เดือน
    month_int = int(Month) # แปลงสตริงเป็นเลขจำนวนเต็ม
    value = [] # สร้าง list ไว้เก็บค่าที่ predict
    value.append(result) # เก็บค่า predict เดือนถัดไป 
    print("predict month", Month, "=", result)
    ############################### บันทึกค่าจากการ forecast ลงตาราง predicts ค่าเดือนที่แถมจนครบ 12 เดือน #########################################
    for next_month in range(12-month_int):
        month_int = month_int+1
        month_str = str(month_int)
        instant = [[WageRate, Jobless, ExchangeRate_BathToDollar, GoldPrice, GasoholNineOne, NewRegis, NewRegisRed, RegisAll_IncreaseYear,
                    RegisAll_IncreaseAvgYear, BankHoliday, Monday, EggPrice, PalmOilPrice, AgentAct_IncMonth,
                    AgentAct_IncConEachYear, value[-1], SalesAct_IncConYear, SalesAct_AvgMonth_OfSalesIncConYear, SalesAct_AllYear,
                    SalesAct_AvgMonth_OfSalesAllYear, SalesAct_TotalSpecMonth, SalesAct_AvgMonth_OfSalesTotalSpecMonth, SalesAct_IncConSpecMonth,
                    SalesAct_AvgMonth_OfSalesIncConSpecMonth, SalesAct_MonthOfYearBefore, SalseAct_TotalThreeYearBefore_AvgMonth]]
        result2 = model.predict(instant)[0]
        result2 = int(result2)
        value.append(result2)
        print("predict month", month_str, "=", result2)
        status2 = "2"
        query2 = "{CALL insertpredict (?, ?, ?, ?, ?)}"
        cursor.execute(query2, id_pred, result2, Date, status2, month_str)
        cursor.commit()

@app.get("/login")
async def create_login(Email: str,
                       Password: str):
    find_user = ("SELECT * FROM accounts WHERE email = ? AND password = ?")
    cursor.execute(find_user, [(Email), (Password)])
    accounts = cursor.fetchall()

    objects_list = []
    data = [list(rows) for rows in accounts]

    if accounts:
        print("welcome to Forecast")
        for loop in accounts:
            print("Welcome "+loop[1])
        return {"status": int(1)}
    else:
        print("username and password not recognised")
        for row in data:
            d = collections.OrderedDict()
            d["id"] = row[0]
            d["user"] = row[1]
            objects_list.append(d)
        return objects_list

#  ตาราง


@app.get("/DSS")
async def Get_All_DS():
    cursor.execute('DataTable')  # store pro  body
    query_results3 = cursor.fetchall()

    objects_list3 = []
    for row in query_results3:
        d = collections.OrderedDict()
        d['เดือน'] = row[0]
        d['ยอดขายจริงและforecast'] = row[1]
        d['ยอดขายปีนี้ทั้งปี'] = row[2]
        d['ยอดขายปีที่แล้ว'] = row[3]
        d['ยอดขายเฉลี่ย3ปีย้อนหลัง'] = row[4]

        objects_list3.append(d)

    cursor.execute('GetHeaders')  # store pro
    query_results2 = cursor.fetchall()
    objects_list2 = []
    for row in query_results2:
        d = collections.OrderedDict()
        d['text'] = row[0]
        d['value'] = row[1]

        objects_list2.append(d)
    return {"desserts": objects_list3, "headers": objects_list2}

# กราฟ visualization


@app.get("/apexchart")
async def Apexchart():
    cursor.execute('selectsalelastyearallmonth')  # store pro
    query_results = cursor.fetchall()
    objects_list = []
    for row in query_results:
        d = collections.OrderedDict()
        d['x'] = row[0]
        d['y'] = row[2]

        objects_list.append(d)

    cursor.execute('selectsalethisyearallmonth')
    query_results2 = cursor.fetchall()
    objects_list2 = []
    for row in query_results2:
        d = collections.OrderedDict()
        d['x'] = row[0]
        d['y'] = row[2]

        objects_list2.append(d)

    cursor.execute('selectsaleavgtreeyearallmonth')
    query_results3 = cursor.fetchall()
    objects_list3 = []
    for row in query_results3:
        d = collections.OrderedDict()
        d['x'] = row[0]
        d['y'] = row[2]

        objects_list3.append(d)

    cursor.execute('selectsaletrueandsalepredict')
    query_results4 = cursor.fetchall()
    objects_list4 = []
    for row in query_results4:
        d = collections.OrderedDict()
        d['x'] = row[0]
        d['y'] = row[2]

        objects_list4.append(d)

    return {"data1": objects_list, "data2": objects_list2, "data3": objects_list3, "data4": objects_list4}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5000, debug=True)
