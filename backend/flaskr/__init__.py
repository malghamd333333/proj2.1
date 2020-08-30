import os
from flask import Flask, request, abort, jsonify ,render_template
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
    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type , Authorization")
        response.headers.add("Access-Control-Allow-Headers", "GET , POST , PATCH , DELETE , OPTIONS")
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

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

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    # curl http://127.0.0.1:5000/questionsdelete/2
    @app.route('/questionsdelete/<int:question_id>', methods=["GET", "DELETE"])
    def delete_question(question_id):

        try:
            curr_question = Question.query.filter_by(id=question_id).first_or_404()
            Question.query.filter_by(id=question_id).delete()
            db.session.commit()
            return jsonify({
                "success": True,
                "data": "delete",
                "book_id": question_id
            })
        except:
            abort(400)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    # curl -d '{"question":"Java3322" , "answer":"Antony222" , "difficulty":"2" , "category":"2" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/addquestions
    # curl http://127.0.0.1:5000/addquestions -X POST -H "Content-Type: application/json" -d "{\"question\": \"test\", \"answer\":\"test\", \"category\":\"4\", \"difficulty\":\"3\"}"

    @app.route("/addquestions", methods=["GET", "POST"])
    def add_question():

        body_allData = request.get_json()
        try:
            question = body_allData.get("question", None)
            answer = body_allData.get("answer", None)
            difficulty = body_allData.get("difficulty", None)
            category = body_allData.get("category", None)
            new_q = Question(question, answer, category, int(difficulty))
            Question.insert(new_q)
            return jsonify({
                "success": True,
                "data": body_allData
            })
        except:
            abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

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

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

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
            abort(400)

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

    # curl -d '{ "name":"Java" , "auth":"Antony222" , "rate":"2" }' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/add
    @app.route("/add", methods=["GET", "POST"])
    def add_test():
        body_allData = request.get_json()

        question = body_allData.get("question", None)
        answer = body_allData.get("answer", None)
        difficulty = body_allData.get("difficulty", None)
        category = body_allData.get("category", None)

        print(question)

        return jsonify({
            "success": True,
            "qu": question,
            "ans": answer,
            "diff": difficulty,
            "cat": category
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
            for n in query1:
                query_ids.append(n.id)
        else:
            query1 = Question.query.all()
            for n in query1:
                query_ids.append(n.id)

        if len(previous_questions_arr) > 0:
            for x in previous_questions_arr:
                previous_id.append(x)

        differences = set(query_ids) - set(previous_id)
        new_ids = list(differences)

        print("Previous_id == ")
        print(previous_id)
        print("newIDs == ")
        print(new_ids)

        rand = random.randint(0, len(new_ids))
        selected_id = new_ids[rand]

        new_question = Question.query.get(selected_id)
        new_question_dic = {
            "id": new_question.id,
            "question": new_question.question,
            "answer": new_question.answer,
            "category": new_question.category,
            "difficulty": new_question.difficulty,
        }
        return jsonify({
            "success": True,
            "question": new_question_dic
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

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    return app
