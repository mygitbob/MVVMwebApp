from flask import render_template
from app import app

@app.route('/adduser')
def adduser():
    return render_template('adduser.html')

