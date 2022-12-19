from flask import Flask, jsonify, make_response, request
from flask_debugtoolbar import DebugToolbarExtension
import json
import sqlite3
import sys
import platform

db_name = 'firstmicrodb'
db_path = ''
print(platform.system())
if platform.system().lower().startswith('win'):
    db_path = r'C:\Users\winbob\py_data_eng_projects\py_cloud_ebook\sqlite\{}'.format(db_name)
else:
    db_path = r'/mnt/c/Users/winbob/py_data_eng_projects/py_cloud_ebook/sqlite/{}'.format(db_name)
db_path = '.'
app = Flask(__name__)
app.debug = True
#app.config['SECRET_KEY'] = 'Apfelkuchen'
#toolbar = DebugToolbarExtension(app)

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Ressource ist nicht vorhanden', 'source': 'Errorhandler 404'}),404)
    
@app.errorhandler(405)
def method_not_implemented(error):
    return make_response(jsonify({'error': f'Methode:{request.method} ist nicht implementiert', 'source': 'Errorhandler 405'}), 405)
    
@app.route("/api/v1/info", methods=['GET'], strict_slashes=False)
#@app.route("/")
def get_api():
    return list_api()
def list_api():
    conn = sqlite3.connect(db_path)
    api_list = []
    my_query = 'SELECT buildtime, version, methods, links from apirelease'
    print(f'SQL query : {my_query}')
    cursor = conn.execute(my_query)

    for row in cursor:
        row_dict = {}
        row_dict['version'] = row[0]
        row_dict['buildtime'] = row[1]
        row_dict['methods'] = row[2]
        row_dict['links'] = row[3]
        api_list.append(row_dict)
    conn.close()
    return jsonify({'api_version':api_list}), 200
    
@app.route('/api/v1/users', methods=['GET'], strict_slashes=False)
#@app.route("/")
def get_users():
    return list_users()
def list_users():
    conn = sqlite3.connect(db_path)
    my_query = 'SELECT username, full_name, emailid, password, id from users'
    cursor = conn.execute(my_query)
    user_list = []
    for row in cursor:
        row_dict = {}
        row_dict['username'] = row[0]
        row_dict['name'] = row[1]
        row_dict['email'] = row[2]
        row_dict['password'] = row[3]
        row_dict['id'] = row[4]
        user_list.append(row_dict)
    conn.close()
    return jsonify({'user_list': user_list}), 200
    
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)
def list_user(user_id):
    conn = sqlite3.connect(db_path)
    my_query = f'SELECT * from users where id={user_id}'
    cursor = conn.execute(my_query)
    data = cursor.fetchall()
    user = {}
    if len(data) != 0:
        user['result'] = f'SUCCESS: user with id:{user_id} is a vaild db entry'
        user['username'] = data[0][0]
        user['name'] = data[0][1]
        user['email'] = data[0][2]
        user['password'] = data[0][3]
        user['id_db'] = data[0][4]
        user['id_request'] = user_id
    else:    
        user['result'] = f'FAILURE: user with id:{user_id} is NOT a vaild db entry'
    conn.close()
    return jsonify(user), 200


@app.route('/api/v1/users', methods=['POST'], strict_slashes=False)
def create_user():
    required_dat = ('username', 'email', 'password')
    print('Request:', request.json)
    if  not request.json or \
        not all(i in request.json for i in required_dat):
            abort(400)
    user = {
        'username' : request.json['username'],
        'email' : request.json['email'],
        'password' : request.json['password'],
        'name' : request.json['name'],
    }
    return jsonify({'status': add_user(user)}), 201

@app.route('/api/v1/testpost', methods=['POST'], strict_slashes=False)
def testpost():
    for i in request.json:
        print(i)
    return make_response(jsonify({'Response': 'alles schick'}), 200)
    
@app.route('/api/v1/testbar', methods=['GET'], strict_slashes=False)
def testbar():
    return '<html><body>hello</body></html>'

  
def add_user(new_user):
    conn = sqlite3.connect(db_path)
    my_query = f"SELECT * from users where username={new_user['username']} or emailid={new_user['email']}"
    list = []
    cursor = conn.cursor()
    cursor.execute(my_query)
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        my_query = f"INSERT INTO users (username, emailid, password, full_name)\
        VALUES({new_user['username']},{new_user['emailid']},\
        {new_user['password']},{new_user['full_name']})"
        cursor.execute(my_query)
        conn.commit()
        return "Success"
    con.close()
    return "Failure"

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request', 'source': 'Errorhandler 400'}), 400)
    
@app.errorhandler(409)
def invalid_request(error):
    return make_response(jsonify({'error': 'Conflict', 'source': 'Errorhandler 409'}), 409)

if __name__ == '__main__':
    print('connecting to db')
    conn = sqlite3.connect(db_path)
    my_query = 'SELECT * from sqlite_master'
    print('send query',conn, type(conn))
    cursor = conn.cursor()
    cursor.execute(my_query)
    data = cursor.fetchall()
    print('Data found:',len(data))
    for i in data: print(i)
    print('connect test done')
    app.run(host='0.0.0.0', port='5000', use_reloader=False)
    