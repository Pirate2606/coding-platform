import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import unittest
from models import db, Practice, Contest
from app import app


class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        self.assertFalse(app.config["DEBUG"])
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()
            db.session.commit()

    def test_Practice_table(self):
        with app.app_context():
            practice = Practice()
            practice.problem_title = "Testing"
            practice.problem_desc = "It is the description of the problem."
            practice.problem_link = "https://www.testing_practice.com"
            practice.problem_site = "Test Site"
            practice.problem_diff = "easy"
            db.session.add(practice)
            db.session.commit()

            practice = Practice().query.filter_by(problem_title="Testing").first()
            self.assertEqual("https://www.testing_practice.com", practice.problem_link)

    def test_Contest_table(self):
        with app.app_context():
            contest = Contest()
            contest.contest_name = "Testing"
            contest.contest_status = "ongoing"
            contest.contest_link = "https://www.testing_contest.com"
            contest.start = "30 Mar 2020 00:00:00"
            contest.end = "30 Mar 2021 00:00:00"
            contest.timing_id = "1"
            db.session.add(contest)
            db.session.commit()

            contest = Contest().query.filter_by(contest_name="Testing").first()
            self.assertEqual("https://www.testing_contest.com", contest.contest_link)


if __name__ == "__main__":
    unittest.main()
