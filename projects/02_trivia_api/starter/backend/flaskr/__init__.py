import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from random import randint 

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

'''
Helper to paginate questions
'''
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_qs = questions[start:end]

  return current_qs

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  cors = CORS(app, resources={r"*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Header', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    return response

  '''
  Endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()

    return jsonify({
      'success': True,
      'categories':[c.type for c in categories],
      'total_categories': len(categories)
      })

  '''
  Endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions')
  def get_questions():
    selection = Question.query.all()
    current_qs = paginate_questions(request, selection)

    if len(current_qs) == 0:
      abort(404)

    categories = Category.query.all()
    
    return jsonify({
      'success': True,
      'questions': current_qs,
      'total_questions': len(selection),
      'categories': [c.type for c in categories],
      'current_category': None
    })

  '''
  Endpoint to DELETE question using a question ID. 
  '''
  @app.route('/questions/<int:q_id>', methods=['DELETE'])
  def delete_question(q_id):
    try:
      question = Question.query.get(q_id)

      if question is None:
        abort(404)
      
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_qs = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': q_id,
        'questions': current_qs,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)

  '''
  POST a new question, 
  which requires the question and answer text, 
  category, and difficulty score.
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    body = request.get_json()

    error = False
    try:
      q = body.get('question', None)
      answer = body.get('answer', None)
      category = body.get('category', None)
      if category is not None:
        category = int(category) + 1
      difficulty = body.get('difficulty', None)

      if answer is None or q is None:
        abort(422)
      if answer == '':
        abort(422)
      if q == '':
        abort(422)

      question = Question(q, answer, category, difficulty)

      question.insert()
      question.update()
    except:
      error = True

    if not error:
      return jsonify({
        'success': True
      })
    else:
      abort(422)

  '''
  Get questions based on a search term. 
  Returns any questions for whom the search term 
  is a substring of the question. 
  '''
  @app.route('/searchQuestions', methods=['POST'])
  def search_questions():
    searchTerm = request.get_json().get('searchTerm', '')

    try:
      if searchTerm == '':
        selection = Question.query.all()
      else: 
        selection = Question.query.filter(Question.question.ilike('%' + searchTerm + '%')).all()
      
      questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions),
        'current_category': None
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:c_id>/questions')
  def get_questions_by_category(c_id):
    selection = Question.query.filter(Question.category==(c_id + 1)).all()
    current_qs = paginate_questions(request, selection)

    if len(current_qs) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_qs,
      'total_questions': len(selection),
      'current_category': c_id - 1
    })


  '''
  Get questions to play the quiz. 
  This endpoint takes category and previous question parameters 
  and returns a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    previous_questions = request.get_json().get('previous_questions', [])
    quiz_category = request.get_json().get('quiz_category')

    try:
      if quiz_category['type'] == 'click':
        questions = Question.query.all()
      else:
        cat = int(quiz_category['id']) + 1
        questions = Question.query.filter(Question.category==cat).all()

      if len(questions) == 0:
        abort(404)

      # Return None if all of the questions have been used
      if len(questions) == len(previous_questions):
        return jsonify({
          'success': True,
          'question': None
        })
    except:
      abort(404)


    try: 
      rand = randint(0, len(questions) - 1)

      while questions[rand].question is None:
        questions.pop(rand)
        rand = randint(0, len(questions) - 1)

      if len(previous_questions) > 0:
        while questions[rand].question is None or questions[rand].id in previous_questions:
          questions.pop(rand)
          rand = randint(0, len(questions) - 1)

      currentQuestion = questions[rand].format()

      return jsonify({
        'success': True,
        'question': currentQuestion
      })
      
    except:
      abort(422)

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
    "success": False, 
    "error": 404,
    "message": "Resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable"
    }), 422
  
  return app

    