import bcrypt

from app import users, app


def user_exist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True


def verify_password(username, password):
    if not user_exist(username):
        return False

    hashed_password = users.find_one({"Username": username})["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_password) == hashed_password:
        return True
    else:
        return False


def cash_with_user(username):
    cash = users.find_one({"Username": username})["Own"]

    return cash


def debt_with_user(username):
    debt = users.find_one({"Username": username})["Debt"]

    return debt


def gen_return_dictionary(status, msg):
    retJson = {
        "status": status,
        "message": msg
    }

    return retJson


def verify_credentials(username, password):
    if not user_exist(username):
        return gen_return_dictionary(301, "Invalid Username"), True

    correct_password = verify_password(username, password)

    if not correct_password:
        return gen_return_dictionary(302, "Incorrect Password"), True

    return None, False


def create_account(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    users.insert({
        "Username": username,
        "Password": hashed_password,
        "Own": 0,
        "Debt": 0,
    })


def find_account(username):
    result = users.find_one({"Username": username}, {"Password": 0, "_id": 0})

    return result


def update_account(username, balance):
    users.update({"Username": username}, {"$set": {"Own": balance}})


def update_debt(username, balance):
    users.update({"Username": username}, {"$set": {"Debt": balance}})
