import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test_db"
        self.database_path = "postgres://postgres:postgres@{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)
        self.test_question_success = {
            "question": "Am I a test subect?",
            "answer": "yes",
            "category": "1",
            "difficulty": 1,
        }
        # invalid input as values are of wrong data type
        self.test_question_fail = {
            "question": 1,
            "answer": 1,
            "category": 1,
            "difficulty": "hard",
        }

        self.test_quiz = {
            "previous_questions": [],
            "quiz_category": {"type": "Science", "id": 1},
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions_for_valid_page(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_get_questions_by_categories(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])
        self.assertEqual(data["currentCategory"], 1)

    def test_create_and_delete_question(self):
        # dummy data is created and deleted to test both apis

        # test creation api
        creation_res = self.client().post("questions", json=self.test_question_success)
        creation_data = json.loads(creation_res.data)
        self.assertEqual(creation_res.status_code, 200)
        self.assertEqual(creation_data["success"], True)
        self.assertTrue(creation_data["newQuestionId"])
        created_question_id = creation_data["newQuestionId"]
        created_question = Question.query.filter(
            Question.id == created_question_id
        ).one_or_none()
        self.assertTrue(created_question.id)

        # test deletion api
        deletion_res = self.client().delete("questions/{}".format(created_question_id))
        deletion_data = json.loads(deletion_res.data)

        deleted_question = Question.query.filter(
            Question.id == created_question_id
        ).one_or_none()
        self.assertEqual(deletion_res.status_code, 200)
        self.assertEqual(deletion_data["success"], True)
        self.assertEqual(deleted_question, None)

    def test_422_if_question_to_delete_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_422_if_book_creation_fails(self):
        res = self.client().post("/questions", json=self.test_question_fail)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "tom"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertEqual(len(data["questions"]), 1)

    def test_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": "qjkli"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["totalQuestions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_get_next_quiz_question(self):
        res = self.client().post("/quizzes", json=self.test_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"]["id"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
