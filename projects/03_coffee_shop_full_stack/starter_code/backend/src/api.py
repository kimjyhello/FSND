import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# CORS Headers 
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response

'''
Initialize the datbase
'''
db_drop_and_create_all()

'''
Populate the db with some drinks
'''
#drink = Drink()
#drink.title = 'Iced Americano'
#drink.recipe = json.dumps([{'name':'Espresso Shots','color':'black','parts':1},
#    {'name':'Water','color':'blue','parts':2}])
#drink.insert()

#drink = Drink()
#drink.title = 'Espresso'
#drink.recipe = json.dumps([{'name':'Espresso Shots','color':'black','parts':2}])
#drink.insert()



## ROUTES
'''
GET /drinks
    - public endpoint
        it should contain only the drink.short() data representation
    - returns status code 200 and json {"success": True, "drinks": drinks} 
        where drinks is the list of drinks with drink.short() representation,
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except:
        abort(404)


'''
GET /drinks-detail
    - requires the 'get:drinks-detail' permission
    - returns status code 200 and json {"success": True, "drinks": drinks} 
        where drinks is the list of drinks with drink.long() representation,
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    errorcode = 0
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        if drinks is None:
            errorcode = 404

        return jsonify({
            'success': True,
            'drinks': drinks
        }), 200
    except:
        errorcode = 422
    finally:
        if errorcode != 0:
            abort(errorcode)

'''
POST /drinks
    - creates a new row in the drinks table
    - requires the 'post:drinks' permission
    - returns status code 200 and json {"success": True, "drinks": drink} 
        where drink an array containing only the newly created drink
        in its drink.long() representation, 
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    body = request.get_json()
    try:
        drink = Drink()
        drink.title = body.get('title')
        drink.recipe = json.dumps(body.get('recipe'))
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        }), 200
    except:
        abort(422)


'''
PATCH /drinks/<id>
    - where <id> is the existing model id
    - requires the 'patch:drinks' permission
    - updates the corresponding row for <id>
    - returns status code 200 and json {"success": True, "drinks": drink} 
        where drink an array containing only the updated drink in
        its drink.long() representation, 
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:d_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, d_id):
    drink = Drink.query.get(d_id)
    
    if drink is None:
        abort(404)

    body = request.get_json()

    try:
        drink.title = body.get('title')
        drink.recipe = json.dumps(body.get('recipe'))
        drink.update()

        return jsonify({
                'success': True,
                'drinks': [drink.long()]
            }), 200
    except:
        abort(422)

'''
DELETE /drinks/<id>
    - where <id> is the existing model id
    - requires the 'delete:drinks' permission
    - returns status code 200 and json {"success": True, "delete": id} 
        where id is the id of the deleted record, 
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:d_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, d_id):
    drink = Drink.query.get(d_id)
    
    if drink is None:
        abort(404)

    try:
        drink.delete()

        return jsonify({
                'success': True,
                'delete': d_id
            }), 200
    except:
        abort(422)


## Error Handling
'''
Error handler for 422, unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
error handler for 404
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
error handler for 401 unauthorized error
'''

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

'''
error handler for AuthError
'''
@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify({
        "success": False,
        "error": e.status_code,
        "message": e.error['description']
    }), e.status_code