import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_questions_for_page(page, selection):
  # function to return books as per input page number
  start = (page - 1)*QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  current_selection = selection[start:end]
  current_questions = [question.format() for question in current_selection]
  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = {category.id: category.type for category in categories}

    return jsonify({
      'success': True,
      'categories': formatted_categories
      })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    all_questions = Question.query.order_by(Question.id).all()
    current_questions = get_questions_for_page(page, all_questions)
    current_category = request.args.get('currentCategory', None)
    categories = Category.query.order_by(Category.id).all()
    formatted_categories = {category.id: category.type for category in categories}

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(all_questions),
      'current_category': current_category,
      'categories': formatted_categories
      })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
          abort(404)

      question.delete()
      return jsonify({
        'success': True
        })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def create_or_search_question():
    body = request.get_json()
    question = body.get('question', "")
    answer = body.get('answer', "")
    category = body.get('category', 0)
    difficulty = body.get('difficulty', 0)
    search = body.get('searchTerm', None)
    try:
      if search:
        search_results = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()
        print(search_results)
        page = request.args.get('page', 1, type=int)
        current_search_results = get_questions_for_page(page, search_results)
        print(current_search_results)
        return jsonify({
          'success': True,
          'totalQuestions': len(current_search_results),
          'questions': current_search_results,
          'currentCategory': None
          })
      else:
        new_question = Question(question, answer, category, difficulty)
        new_question.insert()

        return jsonify({
          'success': True
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
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    search_results = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
    page = request.args.get('page', 1, type=int)
    current_search_results = get_questions_for_page(page, search_results)
    return jsonify({
      'success': True,
      'totalQuestions': len(current_search_results),
      'questions': current_search_results,
      'currentCategory': category_id
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def get_next_quiz_question():
    body = request.get_json()
    previous_questions = body.get('previous_questions', [])
    quiz_category = body.get('quiz_category', None)
    previous_question_dict = {}
    category = Category.query.get(quiz_category['id'])

    #create a hash table of previous qs ids
    if(len(previous_questions) > 0):
      for question in previous_questions:
        if(previous_question_dict.get(question, None) == None):
          previous_question_dict[question] = 1

    #collect all questions or by category if provided
    print(quiz_category)
    all_questions = []
    if(category != None):
      all_questions = Question.query.filter(Question.category == category.id).all()
    else:
      all_questions = Question.query.all()

    print(all_questions)
    #filter out previous questions
    unused_questions = []
    for question in all_questions:
      if (previous_question_dict.get(question.id, None) == None):
        unused_questions.append(question)
    print(unused_questions)
    #randomly chose a new question from unused questions
    current_question = None
    if(len(unused_questions) > 0):
      random_question = random.choice(unused_questions)
      current_question = random_question.format()

    print(current_question)
    return jsonify({
        'success': True,
        'question': current_question
      }) 


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422

  return app

    