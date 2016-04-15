from flask import Flask, abort,render_template, flash, redirect,jsonify,request
from pymongo import MongoClient 
from bson import json_util 
import json
import datetime
from datetime import datetime
import random
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


app = Flask(__name__) 
client = MongoClient("mongodb://localhost:27017") 
db = client.nws 

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'psswd'
    return None
@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 403

#admin= {
#    "login":"admin",
#    "password":"admin" 
#    }
#k_val= 0
#@app.route('/api/auth/', methods=['POST']) 
#def auth():
#    if (request.json['login']==admin['login'] and request.json['password']==admin['password']):
#        k_val = random.randint(1,50)
#        return jsonify({'key': k_val}), 201
#    else:
#        return jsonify({'error': 'wrong login or password'}),400 
    
@app.route('/api/add_news/', methods=['POST'])
@auth.login_required
def add_news(): 
    if not request.json: 
        abort(400) 
    if (request.json['key'] != k_val):
         return jsonify({'error': 'not enough rights'}),400 
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

@app.route('/api/get_news/<int:_id>', methods=['GET']) 
def get_newsid(_id): 
    filter = {"_id":_id} 
    data = json.loads(json_util.dumps(db.nws.find(filter)))
    if len(data)==0:
        abort(404)
    return jsonify({'news': data})
 

@app.route('/api/get_news/', methods=['GET']) 
def get_news(): 
    data = json.loads(json_util.dumps(db.nws.find()))
    return jsonify({'news': data})

@app.route('/api/update_news/<int:_id>', methods=['PUT']) 
@auth.login_required
def update_news(_id): 
    filter = {"_id":_id} 
    if not request.json: 
        abort(400) 
    #if (request.json['key'] != k_val):
    #     return jsonify({'error': 'not enough rights'}),400 
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