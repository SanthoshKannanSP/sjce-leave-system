import db_configuration as dbc
import pymongo.errors as pymon_err
import datetime


def get_student_detail(roll_no):
    details = dbc.student_detail_van.find({"roll_no":roll_no}, {'_id': 0})

    return details[0]


def add_student_detail():
    try:
        last_id = dbc.student_detail_van.find().sort([('student_id', -1)]).limit(1)
        last_id = last_id[0]['student_id']
    except IndexError:
        last_id = 0

    course_dict = {
        "student_id": last_id + 1,
        "name": "Vijay A",
        "roll_no": "21AD203",
        "graduate": "UG",
        "course": "B.Tech",
        "year": 2,
        "branch": "ADS",
        "section": "A",
        "batch": 2021
    }

    try:
        x = dbc.student_detail_van.insert_one(course_dict)
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')
        
def add_leave_form_student(roll_no, detail_dict):
    try:
        last_id = dbc.leave_form_van.find().sort([('leave_id', -1)]).limit(1)
        last_id = last_id[0]['leave_id']
    except IndexError:
        last_id = 0
        
    try:
        data = get_student_detail(roll_no)
        print(data)
    except:
        print("Wrong roll no")
        
    if detail_dict["number_of_days"]==1:
        end_date = detail_dict["start_date"]
    else:
        date_format = r"%Y-%m-%d"

        parsed_date = datetime.datetime.strptime(detail_dict["start_date"], date_format)
        end_date = parsed_date + datetime.timedelta(days=int(detail_dict["number_of_days"])-1)
        end_date = end_date.strftime(date_format)

    course_dict = {
        "leave_id": last_id + 1,
        "name": data["name"],
        "roll_no": data["roll_no"],
        "graduate": data["graduate"],
        "course": data["course"],
        "year": data["year"],
        "branch": data["branch"],
        "section": data["section"],
        "batch": data["batch"],
        "number_of_days": detail_dict["number_of_days"],
        "reason": detail_dict["reason"],
        "type": detail_dict["type"],
        "start_date": detail_dict["start_date"],
        "end_date": end_date,
        "status": 1
    }

    try:
        x = dbc.leave_form_van.insert_one(course_dict)
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')
        
        
def get_number_of_leaves(roll_no):
    try:
        details = dbc.leave_form_van.find({"roll_no":roll_no}, {'_id': 0})
    except:
        details = []
    
    leave_dict = {
        "leave_taken": 0,
        "ll": 0,
        "ml": 0,
        "pl": 0,
        "ab": 0
    }
    
    try:
        for i in details:
            leave_dict["leave_taken"] += int(i["number_of_days"])
            if i["status"]==4:
                typ = i["type"]
                leave_dict[typ] += int(i["number_of_days"])
            else:
                leave_dict["ab"] += int(i["number_of_days"])
            
    except Exception as e: 
        print(e)
        pass
    return leave_dict
        
def add_password():
    try:
        data = dbc.student_detail_van.find({})
    except:
        data = []
        
    for i in data:
        login_dict = {
            "username": i["roll_no"],
            "password": "test"
        }
    
        try:
            x = dbc.login_detail_van.insert_one(login_dict)
        except pymon_err.DuplicateKeyError as e:
            # print(e)
            print('Duplicate Error')
            
def is_login_correct(roll_no,password):
    try:
        data = dbc.login_detail_van.find_one({"username":roll_no})
    except:
        return False
    
    if data["password"]==password:
        return True

    return False

def admin_get_leave_details(status):
    
    try:
        data = dbc.leave_form_van.find({"status":status})
    except:
        data = []
        
    data_list = []
    
    for i in data:
        data_list.append(i)
        
    return data_list

def approve_leave_detail(leave_id):
    
    try:
        data = dbc.leave_form_van.find_one({"leave_id":leave_id})
    except:
        return
    
    course_dict = {
        "leave_id": leave_id,
        "name": data["name"],
        "roll_no": data["roll_no"],
        "graduate": data["graduate"],
        "course": data["course"],
        "year": data["year"],
        "branch": data["branch"],
        "section": data["section"],
        "batch": data["batch"],
        "number_of_days": data["number_of_days"],
        "reason": data["reason"],
        "type": data["type"],
        "start_date": data["start_date"],
        "end_date": data["end_date"],
        "status": data["status"]+1
    }
    
    updated_app_details = { "$set": course_dict}
    filter_criteria = { "leave_id": leave_id}
    dbc.leave_form_van.update_one(filter_criteria,updated_app_details)
    
def add_admin_password():
    
    login_dict = {
        "username": "admin03",
        "password": "test",
        "status": 3
    }

    try:
        x = dbc.admin_login_van.insert_one(login_dict)
    except pymon_err.DuplicateKeyError as e:
        # print(e)
        print('Duplicate Error')
        
def is_admin_login_correct(username,password):
    try:
        data = dbc.admin_login_van.find_one({"username":username})
    except:
        return False,None
    
    if data["password"]==password:
        return True,data["status"]

    return False,None


if __name__ == "__main__":
    add_admin_password()