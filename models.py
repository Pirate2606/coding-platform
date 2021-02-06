from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask import Flask


db = SQLAlchemy()


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256))
    codechef_username = db.Column(db.String(256), unique=True)
    codechef_username_correct = db.Column(db.String(10))
    codechef_realname = db.Column(db.String(256))
    codechef_rating = db.Column(db.String(256))
    codechef_global_rank = db.Column(db.String(256))
    codechef_local_rank = db.Column(db.String(256))
    codechef_country = db.Column(db.String(256))
    leetcode_username = db.Column(db.String(256), unique=True)
    leetcode_username_correct = db.Column(db.String(10))
    leetcode_realname = db.Column(db.String(256))
    leetcode_contest_finished = db.Column(db.String(256))
    leetcode_contest_rating = db.Column(db.String(256))
    leetcode_global_rank = db.Column(db.String(256))
    leetcode_solved_questions = db.Column(db.String(256))
    leetcode_accepted_submissions = db.Column(db.String(256))
    hackerearth_username = db.Column(db.String(256), unique=True)
    hackerearth_username_correct = db.Column(db.String(10))
    hackerearth_realname = db.Column(db.String(256))
    hackerearth_rating = db.Column(db.String(256))
    hackerearth_skills = db.Column(db.String(256))
    hackerearth_education = db.Column(db.String(256))


class Practice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_title = db.Column(db.String(256))
    problem_desc = db.Column(db.String(256))
    problem_link = db.Column(db.String(256))
    problem_site = db.Column(db.String(256))
    problem_diff = db.Column(db.String(256))


class Contest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contest_name = db.Column(db.String(256))
    contest_link = db.Column(db.String(256))
    contest_status = db.Column(db.String(256))
    start = db.Column(db.String(256))
    end = db.Column(db.String(256))
    timing_id = db.Column(db.String(256))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    profile_pic = db.Column(db.String(256))


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)


# setup login manager
login_manager = LoginManager()
login_manager.login_view = "google.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
