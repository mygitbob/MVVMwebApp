from flask import Flask, jsonify, make_response, request, abort, render_template, send_from_directory, session, redirect, url_for
import json
import sqlite3
import sys
import os
import platform
import datetime

db_name = 'firstmicrodb'
r""" db_path = ''
print(platform.system())
if platform.system().lower().startswith('win'):
    db_path = r'C:\Users\winbob\py_data_eng_projects\py_cloud_ebook\sqlite\{}'.format(db_name)
else:
    db_path = r'/mnt/c/Users/winbob/py_data_eng_projects/py_cloud_ebook/sqlite/{}'.format(db_name)
"""
app = Flask(__name__)
app.debug = True
app.secret_key = 'schreib was hin'

#to avoid the error message, add a favicon
@app.route('/favicon.ico')
def favicon():
    print('FAVICON')
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/x-icon')

@app.route('/', strict_slashes=False) 
def main():
    return render_template('main.html')

@app.route("/api/v3/info", methods=['GET'], strict_slashes=False)
def get_api():
    return list_api()
def list_api():
    conn = sqlite3.connect(db_name)
    api_list = []
    my_query = 'SELECT buildtime, version, methods, links from apirelease'
    print(f'SQL query : {my_query}')
    cursor = conn.execute(my_query)

    for row in cursor:
        row_dict = {}
        row_dict['buildtime'] = row[0]
        row_dict['version'] = row[1]
        row_dict['methods'] = row[2]
        row_dict['links'] = row[3]
        api_list.append(row_dict)
    conn.close()
    return jsonify({'api_version':api_list}), 200
    
@app.route('/api/v3/users', methods=['GET'], strict_slashes=False)
def get_users():
    return list_users()
def list_users():
    conn = sqlite3.connect(db_name)
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
    
@app.route('/api/v3/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)
def list_user(user_id):
    conn = sqlite3.connect(db_name)
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


@app.route('/api/v3/users', methods=['POST'], strict_slashes=False)
def create_user():
    required_dat = ('username', 'email', 'password')
    if  not request.json or \
        not all(i in request.json for i in required_dat):
            abort(400)
    if 'name' in request.json:
        name = request.json['name']
    else:
        name = ''
    user = {
        'username' : request.json['username'],
        'email' : request.json['email'],
        'password' : request.json['password'],
        'name' : name,
    }
    return jsonify({'status': add_user(user)}), 201

def add_user(new_user):
    conn = sqlite3.connect(db_name)
    my_query = f"SELECT * from users where username=\"{new_user['username']}\" or emailid=\"{new_user['email']}\""
    print('aa_user query:', my_query)
    list = []
    cursor = conn.cursor()
    cursor.execute(my_query)
    data = cursor.fetchall()
    if len(data) != 0:
        print(data)
        conn.close()
        abort(409)
    else:
        my_query = f"INSERT INTO users (username, emailid, password, full_name)\
        VALUES(\"{new_user['username']}\",\"{new_user['email']}\",\
        \"{new_user['password']}\",\"{new_user['name']}\")"
        cursor.execute(my_query)
        conn.commit()
        conn.close()
        return "Success"
    conn.close()
    return "Failure"
    
@app.route('/api/v3/users', methods=['DELETE'], strict_slashes=False)
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user_id = request.json['username']
    return jsonify({'status': delete_user(user_id)}), 200
    
def delete_user(user_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    my_query = f'SELECT * from users where username="{user_name}"'
    cursor.execute(my_query)
    data = cursor.fetchall()
    if len(data):
        my_query = f'DELETE from users WHERE username="{user_name}"'
        cursor.execute(my_query)
        conn.commit()
        conn.close()
        return "Success"
    else:
        conn.close()
        abort(404)

@app.route('/api/v3/users/<int:user_id>', methods=['PUT'], strict_slashes=False)        
def update_user(user_id):       
    user = {}
    if not request.json:
        abort(400)
    user['id'] = user_id
    key_list = request.json.keys()
    for i in key_list:
        print(i)
        print(request.json[i])
        user[i] = request.json[i]
    print(user)
    return jsonify({'status': update_user(user)}), 200
    
def update_user(user):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    my_query = f"SELECT * FROM users WHERE id={user['id']}"
    cursor.execute(my_query)
    data = cursor.fetchall()
    if data:
        key_list = user.keys()
        for i in key_list:
            if i != 'id':
                my_query = f"UPDATE users SET {i}=\"{user[i]}\" WHERE id={user['id']}"
                #print(my_query)
                cursor.execute(my_query)
                conn.commit()
        conn.close()
        return "Success"
    else:
        conn.close()
        abort(404)

@app.route('/addname', strict_slashes=False)
def addname():
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        return redirect(url_for('main'))
    else:
        return render_template('addname.html', session=session)
        
@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('main'))

@app.route('/api/v3/tweets', methods=['GET'], strict_slashes=False)
def get_tweets():
        return list_tweets(), 200

def list_tweets():
    conn = sqlite3.connect(db_name)
    api_list = []
    my_query = "SELECT * FROM tweets"
    cursor = conn.execute(my_query)
    data = cursor.fetchall()
    if not data: return api_list
    for row in data:
        tweet = {}
        tweet['id'] = row[0]
        tweet['username'] = row[1]
        tweet['body'] = row[2]
        tweet['timestamp'] = row[3]
        api_list.append(tweet)
    conn.close()
    return jsonify({'tweets_list': api_list})

@app.route('/api/v3/tweets/<int:tweet_id>', methods=['GET'], strict_slashes=False)        
def get_tweet(tweet_id):
    conn = sqlite3.connect(db_name)
    my_query = f"SELECT * FROM tweets WHERE id={tweet_id}"
    cursor = conn.execute(my_query)
    data = cursor.fetchall()
    if not data:
        conn.close()
        abort(404)
    else:
        tweet = {}
        tweet['id'] = data[0][0]
        tweet['username'] = data[0][1]
        tweet['body'] = data[0][2]
        tweet['tweet_time'] = data[0][3]
    conn.close()
    return jsonify(tweet), 200

@app.route('/api/v3/tweets', methods=['POST'], strict_slashes=False)
def add_tweets():
    user_tweet = {}
    if not request.json or any(i not in request.json for i in ('username','body')):
        abort(400)
    user_tweet['username'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['created_at'] = str(datetime.datetime.now().replace(microsecond=0))
    return jsonify({'status': add_tweet(user_tweet)}), 200
    
def add_tweet(new_tweets):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    my_query = f"SELECT * from users WHERE username='{new_tweets['username']}'"
    cursor.execute(my_query)
    data = cursor.fetchall()
    if not data:
        conn.close()
        abort(404)
    else:
        my_query = f"INSERT INTO tweets(username, body, tweet_time) \
        VALUES('{new_tweets['username']}','{new_tweets['body']}','{new_tweets['created_at']}')"
        #print('QUERY:',my_query)
        cursor.execute(my_query)
        conn.commit()
        conn.close()
        return "Success"

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Bad Request', 'source': 'Errorhandler 400', 'request':request.url}), 400)
    
@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error': 'Ressource ist nicht vorhanden', 'source': 'Errorhandler 404', 'request':request.url}),404)
    
@app.errorhandler(405)
def method_not_implemented(error):
    return make_response(jsonify({'error': f'Methode:{request.method} ist nicht implementiert', 'source': 'Errorhandler 405', 'request':request.url}), 405)
    
@app.errorhandler(409)
def invalid_request(error):
    return make_response(jsonify({'error': 'Conflict', 'source': 'Errorhandler 409', 'request':request.url}), 409)
    
@app.route('/adduser')
def adduser():
    return render_template('adduser.html')
    
@app.route('/addtweets')
def addtweets():
    return render_template('addtweets.html')
    
        
if __name__ == '__main__':
    print('connecting to db', db_name)
    conn = sqlite3.connect(db_name)
    my_query = 'SELECT * from users'
    cursor = conn.cursor()
    cursor.execute(my_query)
    data = cursor.fetchall()
    print('Data found:',len(data))
    for i in data: print(i)
    print('connect test done')
    app.run(host='0.0.0.0', port='5000', use_reloader=False)
    