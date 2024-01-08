from flask import Flask, render_template
from flask import url_for, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL_URI'] = 'postgresql://keti_superuser:madcoder@keties.iptime.org:55432/data_3dsystems'
# db = SQLAlchemy(app)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/event", methods=['POST'])
def create_event():
    description = request.json['description']

@app.route('/users')
def users():
	# users 데이터를 Json 형식으로 반환한다
    print("test!!")
    return {"members": [{ "id" : 1, "name" : "yerin" },
    					{ "id" : 2, "name" : "dalkong" }]}

@app.route('/whynot', methods = ['GET','POST'])
def postTest():
    if request.method == 'GET':
        return {"members": [{ "id" : 1, "name" : "yerin" },
    					{ "id" : 2, "name" : "dalkong" }]}
    elif request.method == 'POST':
        print("post test")
        username = request.json("username")
        password = request.json("password")
        print(username)
        print(password)
        return {"members": [{ "id" : 1, "name" : "yerin" },
    					{ "id" : 2, "name" : "dalkong" }]}

	

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80) 