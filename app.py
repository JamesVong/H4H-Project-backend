from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
import json
from user import User

app = Flask(__name__)


def check_username_and_pass(username, password):
    user = User.find_data_by_username(username)
    if user:
        if user.username and user.password:
            if check_password_hash(user.password, password):
                return jsonify({'message': 'Success'})
    return jsonify({
        "error": "Incorrect username or password."
    })


def edit_careers(username, career_name, remove):
    user = User.find_data_by_username(username)
    if user:
        careers_list = json.loads(user.careers)
        if not remove:
            if career_name not in careers_list:
                careers_list.append(career_name)

                user.careers = json.dumps(careers_list)
                user.db_update_career()
                return jsonify({'message': 'Success'})
            else:
                return jsonify({
                    "error": "Already in the list."
                })
        else:
            if career_name in careers_list:
                careers_list.remove(career_name)

                user.careers = json.dumps(careers_list)
                user.db_update_career()
                return jsonify({'message': 'Success'})
            else:
                return jsonify({
                    "error": "Already not in the list."
                })
    return jsonify({
        "error": "Incorrect username or password."
    })

"""
POST
{
    "username": "Ex",
    "password": "Ex",
    "email": Ex,
    "first_name": Ex,
    "last_name": Ex,
    "careers": {}
}
"""
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    # Interpret the format
    if request.method == 'POST':
        info = {"username": None, "password": None, "email": None, "first_name": None, "last_name": None, "career": json.dumps([])}
        requests = [request.form, request.get_json(), request.get_data()]

        for req in [i for i in requests if i]:  # Check if it's None
            try:
                # Fill the dictionary of info with stuff
                for key, val in info.items():
                    if key != "career":
                        try:
                            info[key] = req[key]
                        except KeyError:
                            return "Invalid input, missing field: " + key

                user_exists = User.find_data_by_username(info["username"])
                if not user_exists:
                    user = User(info["username"], info["password"], info["email"], info["first_name"], info["last_name"],
                                info["career"])
                    user.db_add_user()
                    return jsonify({'message': 'Success'})
                else:
                    return jsonify({"error": "Username already used."}), 400
            except Exception as e:
                print(e)
                return jsonify({"error": "Something went wrong, sending a Bad Request."}), 400
        return jsonify({"error": "?????"}), 400
    elif request.method == "GET":
        username = request.args.get('username')
        if username:
            user = User.find_data_by_username(username)
            if user:
                return jsonify(
                    {
                        "result": {
                            "username": user.username,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "email": user.email
                        }
                    }
                )
            return "User not found", 400
        return "Username parameter not filled", 400


"""
Look for:
{
    "username": "Ex",
    "password": "Ex"
}
"""
# The code repeats, but it's kind of more clear to do it this way versus signup
@app.route('/login/', methods=['POST'])
def login():
    # Interpret the format
    if request.form:
        username = request.form['username']
        password = request.form['password']

        return check_username_and_pass(username, password)
    elif request.get_json():
        json_data = request.get_json()

        username = json_data['username']
        password = json_data['password']

        return check_username_and_pass(username, password)
    elif request.get_data():
        try:
            data = json.loads(request.get_data())
            username = data['username']
            password = data['password']

            return check_username_and_pass(username, password)
        except Exception as e:
            print(e)
            return jsonify({"error": "Something went wrong, sending a Bad Request."}), 400
    return jsonify({"error": "?????"}), 400


"""
POST (Add career):
{
    "username": "Ex",
    "career": "Ex",
    "remove": false
}

GET (return json list)
{
    "result": ["Financial Analyist", "Consultant"]
}
"""  # The code repeats, but it's kind of more clear to do it this way
@app.route('/career/', methods=['GET', 'POST'])
def career():
    # Interpret the format
    if request.method == "POST":
        if request.form:
            username = request.form['username']
            career_name = request.form['career']
            remove = request.form['remove']
            return edit_careers(username, career_name, remove)
        elif request.get_json():
            json_data = request.get_json()

            username = json_data['username']
            career_name = json_data['career']
            remove = json_data['remove']
            return edit_careers(username, career_name, remove)
        elif request.get_data():
            try:
                data = json.loads(request.get_data())
                username = data['username']
                career_name = data['career']
                remove = data['remove']
                return edit_careers(username, career_name, remove)
            except Exception as e:
                print(e)
                return jsonify({"error": "Something went wrong, sending a Bad Request."}), 400
        return jsonify({"error": "?????"}), 400
    elif request.method == "GET":
        username = request.args.get('username')
        if username:
            user = User.find_data_by_username(username)
            if user:
                return jsonify({"result": json.loads(user.careers)})
            return "User not found", 400
        return "Username parameter not filled", 400


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1> Welcome to the server </h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
