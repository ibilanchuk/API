from flask import Flask, abort,render_template, flash, redirect,jsonify,request,make_response
from pymongo import MongoClient 
from bson import json_util 
import json
import datetime
from datetime import datetime
import random
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


app = Flask(__name__) 
#connecting to bd
client = MongoClient("mongodb://localhost:27017") 
db = client.nws 

#add admin
@app.route('/api/add_admin/', methods=['POST'])
def add_admin(): 
    if not request.json: 
        abort(400) 
    if (not 'login' in request.json): 
        return jsonify({'error': 'login not found'}),400 
    if (not 'password' in request.json): 
        return jsonify({'error': 'password not found'}),400 
    id = db.auth.count()+1 
    admin={'_id':id,'login':request.json['login'],'password':request.json['password']} 
    db.auth.insert(admin) 
    return jsonify({'response': 'success'}), 201

#get auth data for checking
@auth.get_password
def get_password(username):
    filter = {"login" : username}
    data=db.auth.find(filter)
    if(data):
        return data[0]['password']
    return None

#show error if u not authorized
@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 403

#add new data in db
@app.route('/api/add_news/', methods=['POST'])
@auth.login_required
def add_news(): 
    if not request.json: 
        abort(400) 
    if (not 'title' in request.json): 
        return jsonify({'error': 'title not found'}),400 
    if (not 'text' in request.json): 
        return jsonify({'error': 'text not found'}),400 
    if (not 'category' in request.json): 
        return jsonify({'error': 'Category not found'}),400 
    if (not request.json['category']): 
        return jsonify({'error': 'Category not exist'}),400 
    id = db.nws.count()+1 
    news={'_id':id,'title':request.json['title'],'text':request.json['text'],'category':request.json['category'],'date': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} 
    db.nws.insert(news) 
    return jsonify({'response': 'success'}), 201

#delete data from db
@app.route('/api/delete_news/<int:_id>', methods=['DELETE'])
@auth.login_required
def delete_news(_id): 
    filter = {"_id":_id} 
    data = json.loads(json_util.dumps(db.nws.find(filter)))
    if len(data)==0:
        abort(404)
    data = {"_id":_id} 
    db.nws.remove(data) 
    return jsonify({'response': 'success'}),201

#get news by id
@app.route('/api/get_news/<int:_id>', methods=['GET']) 
def get_newsid(_id): 
    filter = {"_id":_id} 
    data = json.loads(json_util.dumps(db.nws.find(filter)))
    if len(data)==0:
        abort(404)
    return jsonify({'news': data})

 #get news by category
@app.route('/api/news_cat/<string:cat>', methods=['GET']) 
def news_bycat(cat): 
    filter = {"category":cat} 
    data = json.loads(json_util.dumps(db.nws.find(filter)))
    if len(data)==0:
        abort(404)
    return jsonify({'news': data})
 
#get all news
@app.route('/api/get_news/', methods=['GET']) 
def get_news(): 
    data = json.loads(json_util.dumps(db.nws.find()))
    return jsonify({'news': data})

#update data in db by id
@app.route('/api/update_news/<int:_id>', methods=['PUT']) 
@auth.login_required
def update_news(_id): 
    filter = {"_id":_id} 
    if not request.json: 
        abort(400) 
    if (not 'title' in request.json): 
        return jsonify({'error': 'title not found'}),400 
    if (not 'text' in request.json): 
        return jsonify({'error': 'text not found'}),400 
    if (not 'category' in request.json): 
        return jsonify({'error': 'Category not found'}),400 
    if (not request.json['category']): 
        return jsonify({'error': 'Category not exist'}),400 
    news={'title':request.json['title'],'text':request.json['text'],'category':request.json['category'],'date': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} 
    db.nws.update(filter,news) 
    return jsonify({'response': 'success'}), 201

if __name__ == '__main__':  
    app.debug = True
    app.run()