import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    with app.app_context():
        db.create_all()


    cors = CORS(app, resources={r"/*": {"origins": "*"}})


    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type , Authorization")
        response.headers.add("Access-Control-Allow-Headers", "GET , POST , PATCH , DELETE , OPTIONS")
        return response



    @app.route("/getquestions", methods=['GET', 'POST'])
    def get_quesions():

        quesions_arr = []
        catagory_dic = {}
        for u in Question.query.order_by('id').all():
            quesions_arr.append({
                "id": u.id,
                "question": u.question,
                "answer": u.answer,
                "category": u.category,
                "difficulty": u.difficulty,
            })

        for cat in Category.query.all():
            catagory_dic[cat.id] = cat.type

        # curl http://127.0.0.1:5000/getquestions?page=1
        show_each_time = QUESTIONS_PER_PAGE
        num_elem_show = request.args.get('page', 1, type=int)
        start = (num_elem_show - 1) * show_each_time
        end = start + show_each_time
        return jsonify({
            "success": True,
            "questions": quesions_arr[start:end],
            "total_questions": len(quesions_arr),
            "categories": catagory_dic,
            #   "current_category": catagory_arr,
        })



    # curl http://127.0.0.1:5000/questionsdelete/2
    @app.route('/questionsdelete/<int:question_id>', methods=["GET", "DELETE"])
    def delete_question(question_id):
        Question.query.filter_by(id=question_id).first_or_404()
        try:
            Question.query.filter_by(id=question_id).delete()
            db.session.commit()
            return jsonify({
                "success": True,
                "data": "delete",
                "deleted": question_id
            })
        except:
            abort(404)


    # curl -d '{"question":"Java3322" , "answer":"Antony222" , "difficulty":"2" , "category":"2" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/addquestions
    # curl http://127.0.0.1:5000/addquestions -X POST -H "Content-Type: application/json" -d "{\"question\": \"test\", \"answer\":\"test\", \"category\":\"4\", \"difficulty\":\"3\"}"

    @app.route("/addquestions", methods=["POST"])
    def add_question():

        body_allData = request.get_json()
        question = body_allData.get("question")
        answer = body_allData.get("answer")
        difficulty = body_allData.get("difficulty")
        category = body_allData.get("category")
        if not question or not answer:
            abort(422)
        try:
            new_q = Question(question, answer, category, int(difficulty))
            Question.insert(new_q)
            return jsonify({
                "success": True,
                "data": body_allData
            })
        except:
            abort(422)


    # curl -d '{"searchTerm":"aa"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/questionssearch
    @app.route("/questionssearch", methods=['GET', 'POST'])
    def questions_search():

        body_allData = request.get_json()

        try:
            searchTerm = body_allData.get("searchTerm", None)
            quesions_arr = []
            catagory_dic = {}
            for u in Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(searchTerm))):
                quesions_arr.append({
                    "id": u.id,
                    "question": u.question,
                    "answer": u.answer,
                    "category": u.category,
                    "difficulty": u.difficulty,
                })

            for cat in Category.query.all():
                catagory_dic[cat.id] = cat.type

            return jsonify({
                "success": True,
                "total_questions": len(quesions_arr),
                # "current_category": all_cateogry_arr,
                "questions": quesions_arr
            })
        except:
            abort(422)


    # curl http://127.0.0.1:5000/categories/2/questions
    @app.route("/categories/<int:category_id>/questions", methods=['GET'])
    def update_record(category_id):
        quesions_arr = []
        try:
            for u in Question.query.filter_by(category=category_id).all():
                quesions_arr.append({
                    "id": u.id,
                    "question": u.question,
                    "answer": u.answer,
                    "category": u.category,
                    "difficulty": u.difficulty,
                })
            curren_category = Category.query.filter_by(id=category_id).first()

            return jsonify({
                "success": True,
                "questions": quesions_arr,
                "total_questions": len(quesions_arr),
                "current_category": curren_category.type
            })
        except:
            abort(404)

    # curl http://127.0.0.1:5000/categories
    @app.route("/categories", methods=['GET'])
    def show_database():
        categories_dic = {}
        for u in Category.query.order_by('id').all():
            categories_dic[u.id] = u.type
        return jsonify({
            "success": True,
            "categories": categories_dic
        })





    # curl -d '{ "previous_questions":"[2,3,4,5,16,17,18,9,11,12,41,37]" , "quiz_category" :"{type: "History", id: "4"}"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/quizzes
    @app.route("/quizzes", methods=['GET', 'POST'])
    def random_quizzes():
        body_allData = request.get_json()

        previous_questions_arr = body_allData.get("previous_questions", None)
        quiz_category = body_allData.get("quiz_category", None)
        query_ids = []
        previous_id = []

        if int(quiz_category['id']) > 0:
            query1 = Question.query.filter_by(category=quiz_category['id']).all()
            for quary_ele in query1:
                query_ids.append(quary_ele.id)
        else:
            query1 = Question.query.all()
            for quary_ele in query1:
                query_ids.append(quary_ele.id)

        if len(previous_questions_arr) > 0:
            for x in previous_questions_arr:
                previous_id.append(x)

        differences = set(query_ids) - set(previous_id)
        new_ids = list(differences)

        rand = random.randint(0, len(new_ids) - 1)
        selected_id = new_ids[rand]

        if len(new_ids) - 1 > 0:
            new_question = Question.query.get(selected_id)
            new_question_dic = {
                "id": new_question.id,
                "question": new_question.question,
                "answer": new_question.answer,
                "category": new_question.category,
                "difficulty": new_question.difficulty,
            }
        else:
            new_question_dic = {
                "id": 0,
                "question": "Sorry, there is no more questions",
                "answer": '',
                "category": 0,
                "difficulty": 0,
            }

        return jsonify({
            "success": True,
            "question": new_question_dic
        })


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
