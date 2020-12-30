import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def get_questions_for_page(page, selection):
    # function to return books as per input page number
    start = (page - 1) * QUESTIONS_PER_PAGE
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
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories", methods=["GET"])
    def get_categories():
        """ 
        get_categories() provides a
        endpoint to handle GET requests 
        for all available categories.
        """
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id: category.type for category in categories}

        return jsonify({"success": True, "categories": formatted_categories})

    @app.route("/questions", methods=["GET"])
    def get_questions():
        """
        get_questions() a GET endpoint to handle GET requests for questions, 
        including pagination (every 10 questions). This endpoint returns a
        list of questions, number of total questions, current category, categories.
        """
        page = request.args.get("page", 1, type=int)
        all_questions = Question.query.order_by(Question.id).all()
        current_questions = get_questions_for_page(page, all_questions)
        current_category = request.args.get("currentCategory", None)
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id: category.type for category in categories}

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(all_questions),
                "current_category": current_category,
                "categories": formatted_categories,
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """
        delete_question(question_id) provides an endpoint to DELETE
        question using a question ID.
        """
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            return jsonify({"success": True})
        except:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def create_or_search_question():
        """
        create_or_search_question() provides POST endpoint to create or
        search question. Creating a new question will require the 
        question and answer text, category, and difficulty score.
        Also serves as a endpoint to get questions based on a search term.
        Returns any questions for whom the search term is a substring of
        the question.
        """
        body = request.get_json()
        question = body.get("question", "")
        answer = body.get("answer", "")
        category = body.get("category", 0)
        difficulty = body.get("difficulty", 0)
        search = body.get("searchTerm", None)
        try:
            if search:
                search_results = (
                    Question.query.order_by(Question.id)
                    .filter(Question.question.ilike("%{}%".format(search)))
                    .all()
                )
                page = request.args.get("page", 1, type=int)
                current_search_results = get_questions_for_page(page, search_results)
                return jsonify(
                    {
                        "success": True,
                        "totalQuestions": len(current_search_results),
                        "questions": current_search_results,
                        "currentCategory": None,
                    }
                )
            else:
                new_question = Question(question, answer, category, difficulty)
                new_question.insert()

                return jsonify({"success": True, "newQuestionId": new_question.id})
        except:
            abort(422)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        """
        get_questions_by_category(category_id) provides a GET endpoint
        to get questions based on category.
        """
        search_results = (
            Question.query.order_by(Question.id)
            .filter(Question.category == category_id)
            .all()
        )
        page = request.args.get("page", 1, type=int)
        current_search_results = get_questions_for_page(page, search_results)
        return jsonify(
            {
                "success": True,
                "totalQuestions": len(current_search_results),
                "questions": current_search_results,
                "currentCategory": category_id,
            }
        )

    @app.route("/quizzes", methods=["POST"])
    def get_next_quiz_question():
        """
        get_next_quiz_question() provides a POST endpoint to get
        questions to play the quiz. This endpoint should take
        category and previous question parameters and return a 
        random questions within the given category, if provided, 
        and that is not one of the previous questions.
        """
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", [])
            quiz_category = body.get("quiz_category", None)
            previous_question_dict = {}
            category = Category.query.get(quiz_category["id"])

            # create a hash table of previous qs ids
            if len(previous_questions) > 0:
                for question in previous_questions:
                    if previous_question_dict.get(question, None) == None:
                        previous_question_dict[question] = 1

            # collect all questions or by category if provided
            all_questions = []
            if category != None:
                all_questions = Question.query.filter(
                    Question.category == category.id
                ).all()
            else:
                all_questions = Question.query.all()

            # filter out previous questions
            unused_questions = []
            for question in all_questions:
                if previous_question_dict.get(question.id, None) == None:
                    unused_questions.append(question)

            # randomly chose a new question from unused questions
            current_question = None
            if len(unused_questions) > 0:
                random_question = random.choice(unused_questions)
                current_question = random_question.format()

            return jsonify({"success": True, "question": current_question})

        except:
            abort(500)

    """
      Error handlers for all expected errors 
    """

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"success": False, "error": 500, "message": "server error"}), 500

    return app
