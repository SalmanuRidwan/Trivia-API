from functools import total_ordering
import json
from multiprocessing.dummy import current_process
import os
from sre_parse import CATEGORIES
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def list_categories(selection):
    categories = Category.query.all()
    data = {}
    for category in categories:
        first = category.id
        second = category.type
        data.update({"".replace("", str(first)): "".replace("", second)})

    return data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        selection = Category.query.order_by(Category.id).all()
        current_categories = list_categories(selection)

        return jsonify({
            'success': True,
            'categories': current_categories,
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Category.query.order_by(Category.id).all()
        questions = Question.query.order_by(Question.id).all()
        current_categories = list_categories(selection)
        current_questions = paginate_questions(request, questions)
        questions_count = len(current_questions)
        total_questions = Question.query.all()

        if questions_count == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': current_categories,
            'questions': current_questions,
            'total_questions': len(total_questions)

        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_specific_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
            })
        except BaseException:
            abort(404)

    @app.route('/questions', methods=['POST'])
    def create_or_search_question():
        body = request.get_json()

        try:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)
            search = body.get('searchTerm', None)

            if search:
                selection = Question.query.order_by(
                    Question.id).filter(
                    Question.question.ilike(
                        '%{}%'.format(search)))

                questions = [question.format() for question in selection]
                total_questions = len(selection.all())

                return jsonify({
                    'success': True,
                    'questions': questions,
                    'total_questions': total_questions
                })

            if new_question:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                )
                question.insert()

            return jsonify({
                'success': True,
            })

        except BaseException:
            abort(405)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        selection = Question.query.order_by(
            Question.id).filter(
            Question.category == category_id)
        questions = [question.format() for question in selection]
        questions_count = len(questions)

        if questions_count == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': questions_count,
        })

    @app.route('/quizzes', methods=['POST'])
    def quiz_questions():

        ################  IMPROVED ENDPOINT LOGIC  ##########################
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        questions = []
        random_question = None

        try:
            if quiz_category is None or quiz_category['id'] == 0:
                formatted_questions = [question.format()
                                       for question in Question.query.all()]
            else:
                formatted_questions = [
                    question.format() for question in Question.query.filter(
                        Question.category == quiz_category['id']).all()]

            for question in formatted_questions:
                if question['id'] not in previous_questions:
                    questions.append(question)

            if len(questions) > 0:
                random_question = random.choice(questions)

            return jsonify({
                'success': True,
                'question': random_question,
                'previous_questions': previous_questions
            })
        except BaseException:
            abort(422)

    ### ERROR HANDLERS 400, 404, 405, 422 & 500  ###

    @app.errorhandler(400)
    def bad_request(error):
        jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'messsage': 'method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        jsonify({
            'success': False,
            'error': 500,
            'message': "server error"
        }), 500

    return app
