from flask import request, jsonify, Blueprint

bp = Blueprint('users', __name__)

from helpers import user_exist, gen_return_dictionary, verify_credentials, cash_with_user, update_account, \
    create_account, debt_with_user, update_debt, find_account


@bp.route('/register', methods=['POST'])
def register():
    posted_data = request.get_json()

    username = posted_data['username']
    password = posted_data['password']

    if user_exist(username):
        retJson = {
            "status": 301,
            "message": "Invalid Username"
        }
        return jsonify(retJson)

    create_account(username, password)

    retJson = gen_return_dictionary(200, "You successfully signed up for the API.")
    return jsonify(retJson)


@bp.route('/add', methods=['POST'])
def add():
    posted_data = request.get_json()

    username = posted_data['username']
    password = posted_data['password']
    money = posted_data['amount']

    retJson, error = verify_credentials(username, password)

    if error:
        return jsonify(retJson)

    if money <= 0:
        return jsonify(gen_return_dictionary(304, "The money amount entered must be greater than 0."))

    cash = cash_with_user(username)

    money -= 1
    bank_cash = cash_with_user("BANK")
    update_account("BANK", bank_cash + 1)
    update_account(username, cash + money)

    return jsonify(gen_return_dictionary(200, "Amount added successfully to account"))


@bp.route('/transfer', methods=["POST"])
def transfer():
    posted_data = request.get_json()

    username = posted_data['username']
    password = posted_data['password']
    to = posted_data['to']
    money = posted_data['amount']

    retJson, error = verify_credentials(username, password)
    if error:
        return jsonify(retJson)

    cash = cash_with_user(username)
    if cash <= 0:
        return jsonify(gen_return_dictionary(304, "You're out of money, please add or take loan."))

    if not user_exist(username):
        return jsonify(gen_return_dictionary(301, "Receiver username is invalid."))

    cash_from = cash_with_user(username)
    cash_to = cash_with_user(to)
    bank_cash = cash_with_user("BANK")

    update_account("BANK", bank_cash + 1)
    update_account(to, cash_to + money - 1)
    update_account(username, cash_from - money)

    return jsonify(gen_return_dictionary(200, "Amount Transferred successfully"))


@bp.route('/balance', methods=["POST"])
def check_balance():
    posted_data = request.get_json()

    username = posted_data['username']
    password = posted_data['password']

    retJson, error = verify_credentials(username, password)
    if error:
        return jsonify(retJson)

    retJson = find_account(username)

    return jsonify(retJson)


@bp.route('/take_loan', methods=["POST"])
def take_loan():
    posted_data = request.get_json()

    username = posted_data['username']
    password = posted_data['password']
    money = posted_data['amount']

    retJson, error = verify_credentials(username, password)
    if error:
        return jsonify(retJson)

    cash = cash_with_user(username)
    debt = debt_with_user(username)
    update_account(username, cash + money)
    update_debt(username, debt + money)

    return jsonify(gen_return_dictionary(200, "Loan added to your account."))


@bp.route('/pay_loan', methods=["POST"])
def pay_loan():
    posted_data = request.get_json()

    username = posted_data['username']
    password = posted_data['password']
    money = posted_data['amount']

    retJson, error = verify_credentials(username, password)
    if error:
        return jsonify(retJson)

    cash = cash_with_user(username)

    if cash < money:
        return jsonify(gen_return_dictionary(303, "Not enough cash in your account."))

    debt = debt_with_user(username)

    update_account(username, cash - money)
    update_debt(username, debt - money)

    return jsonify(gen_return_dictionary(200, "You've successfully paid your loan."))
