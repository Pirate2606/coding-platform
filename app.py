from flask import Flask, render_template, request, redirect, url_for, flash, g
from form import Feedback
from flask_login import logout_user, login_required, current_user
import subprocess, os
from subprocess import PIPE
from config import Config
from models import db, login_manager, User, Contest, Practice, Profile
from oauth import blueprint
from cli import create_db
from flask_migrate import Migrate
import datetime
from time import strptime
from threading import Thread
from sqlalchemy.exc import IntegrityError


#################################
#### SETTING UP APP ############
################################

app = Flask(__name__)
from sendMail import send_mail
from profile import codechef_info, leetcode_info, hackerearth_info

Migrate(app, db)

app.config.from_object(Config)                                   #app.config
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)                                  #creating database
db.init_app(app)
login_manager.init_app(app)

# For insecure login
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


##################################
########### ROUTES ###############
##################################


@app.route("/", methods = ['GET','POST'])
def home():
	home = 1
	form = Feedback()
	profile_pic = get_profile_pic()
	try:
		email = get_email().split("@")[0]
		profile = Profile()
		current_user_profile = profile.query.filter_by(username=email).first()
	except :
		current_user_profile = None
	try:
		if request.method == "POST":
				name = request.form['user_name']
				current_user_profile.name = name
				db.session.add(current_user_profile)
				db.session.commit()
	except:
		pass
	if form.validate_on_submit():

		email = form.email.data
		message = form.message.data

		send_mail(email, message)
		flash('Thanks for the feedback!')

		return redirect(url_for('home'))

	return render_template("home.html", form = form, home = home, profile_pic = profile_pic, current_user_profile=current_user_profile)


@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("You have logged out")
	return redirect(url_for("home"))


@app.route('/compile')
def compiler():
	profile_pic = get_profile_pic()
	check = ''
	flag = 1            # none of the language is selected before-hand
	return render_template('compiler.html',
							flag = flag,
							check = check,
							profile_pic = profile_pic,
							data = [{'language':'C'}, {'language':'Python'}, {'language':'Java'}]
	)


@app.route('/submit', methods = ['GET','POST'])
def submit():
	flag = 0
	profile_pic = get_profile_pic()
	if request.method == "POST":
		code = request.form['code']
		inp = request.form['input']
		chk = request.form.get('check')
		lan = request.form.get('comp_select')
		if  not chk == '1':
			inp = ""
			check = ''
		else:
			check = 'checked'

		output = complier_output(code, inp, chk, lan)
		return render_template('compiler.html',
								lang = lan,
								flag = flag,
								code = code,
								input = inp,
								output = output,
								check = check,
								profile_pic = profile_pic,
								data = [{'language':'C'}, {'language':'Python'}, {'language':'Java'}]
		)


@app.route('/contest')
@login_required
def contest():
	profile_pic = get_profile_pic()
	contest = Contest()
	allContests = contest.query.all()
	for time in allContests:
		if time.start is not None:
			start = time.start.split(' - ')
			startDateTime = get_dateTime(start)
			started = startDateTime < datetime.datetime.now()
			if started == True and time.contest_status == "future":
				time.contest_status = "active"
				db.session.add(time)
				db.session.commit()

		if time.end is not None:
			end = time.end.split(' - ')
			endDateTime = get_dateTime(end)
			ended = endDateTime < datetime.datetime.now()
			if ended == True and time.contest_status != "in-active":
				time.contest_status = "in-active"
				db.session.add(time)
				db.session.commit()


	active_contests = contest.query.filter_by(contest_status = "active").all()
	in_active_contests = contest.query.filter_by(contest_status = "in-active").all()
	in_active_contests.reverse()              # for arraging the ended conests in reverse order
	future_contests = contest.query.filter_by(contest_status = "future").all()

	return render_template('contest.html',
							profile_pic = profile_pic,
							active_contests = active_contests,
							future_contests = future_contests,
							in_active_contests = in_active_contests
	)


@app.route('/practice')
@login_required
def practice():
	profile_pic = get_profile_pic()
	practice = Practice()
	page = request.args.get("page", 1, type=int)
	practice_info = practice.query.paginate(page=page, per_page=5)
	return render_template('practice.html',
							profile_pic = profile_pic,
							practice_info = practice_info
	)


@app.route('/refresh_codechef')
def refreshCodechef():
	print("Started refresh codechef")
	email = get_email().split("@")[0]
	profile = Profile()
	current_user_profile = profile.query.filter_by(username=email).first()

	user_name = current_user_profile.codechef_username
	background_thread = Thread(target=codechef_info, args=(user_name, email,))
	background_thread.start()

	print("Doing Refresh codechef")
	return ("nothing")


@app.route('/refresh_leetcode')
def refreshLeetcode():
	print("Started refresh leetcode")
	email = get_email().split("@")[0]
	profile = Profile()
	current_user_profile = profile.query.filter_by(username=email).first()

	user_name = current_user_profile.leetcode_username
	background_thread = Thread(target=leetcode_info, args=(user_name, email,))
	background_thread.start()

	print("Doing Refresh leetcode")
	return ("nothing")


@app.route('/refresh_hackerearth')
def refreshHackerearth():
	print("Started refresh hackerearth")
	email = get_email().split("@")[0]
	profile = Profile()
	current_user_profile = profile.query.filter_by(username=email).first()

	user_name = current_user_profile.hackerearth_username
	background_thread = Thread(target=hackerearth_info, args=(user_name, email,))
	background_thread.start()

	print("Doing Refresh hackerearth")
	return ("nothing")


@app.route('/profile', methods = ['GET','POST'])
@login_required
def profile_page():
	profile_pic = get_profile_pic()
	email = get_email().split("@")[0]
	profile = Profile()
	current_user_profile = profile.query.filter_by(username=email).first()

	if current_user_profile.codechef_username_correct == "0":
		codechef_is_connected = 0
		current_user_profile.codechef_username = None
		db.session.add(current_user_profile)
		db.session.commit()

	if current_user_profile.leetcode_username_correct == "0":
		leetcode_is_connected = 0
		current_user_profile.leetcode_username = None
		db.session.add(current_user_profile)
		db.session.commit()


	if current_user_profile.hackerearth_username_correct == "0":
		hackerearth_is_connected = 0
		current_user_profile.hackerearth_username = None
		db.session.add(current_user_profile)
		db.session.commit()

	if current_user_profile is not None:

		if current_user_profile.codechef_username is not None:
			codechef_is_connected = 1
		else:
			codechef_is_connected = 0
			if request.method == "POST":
				try:
					current_user_profile.codechef_username = request.form['codechef_username']
					try:
						db.session.add(current_user_profile)
						db.session.commit()
						flash("Your codechef profile will be linked within 9-10 minutes.")
						codechef_is_connected = 1
						user_name = current_user_profile.codechef_username
						background_thread = Thread(target=codechef_info, args=(user_name, email,))
						background_thread.start()
					except IntegrityError:
						print("FAILED")
						db.session.rollback()
						flash("This codechef profile is already linked to some other account.")
				except :
					pass

		if current_user_profile.leetcode_username is not None:
			leetcode_is_connected = 1
		else:
			leetcode_is_connected = 0
			if request.method == "POST":
				try:
					current_user_profile.leetcode_username = request.form['leetcode_username']
					try:
						db.session.add(current_user_profile)
						db.session.commit()
						flash("Your leetcode profile will be linked within 4-5 minutes.")
						leetcode_is_connected = 1
						user_name = current_user_profile.leetcode_username
						background_thread = Thread(target=leetcode_info, args=(user_name, email,))
						background_thread.start()
					except IntegrityError:
						print("FAILED")
						db.session.rollback()
						flash("This leetcode profile is already linked to some other account.")
				except :
					pass

		if current_user_profile.hackerearth_username is not None:
			hackerearth_is_connected = 1
		else:
			hackerearth_is_connected = 0
			if request.method == "POST":
				try:
					current_user_profile.hackerearth_username = request.form['hackerearth_username']
					try:
						db.session.add(current_user_profile)
						db.session.commit()
						flash("Your hackerearth profile will be linked within 4-5 minutes.")
						hackerearth_is_connected = 1
						user_name = current_user_profile.hackerearth_username
						background_thread = Thread(target=hackerearth_info, args=(user_name, email,))
						background_thread.start()
					except IntegrityError:
						print("FAILED")
						db.session.rollback()
						flash("This hackerearth profile is already linked to some other account.")
				except :
					pass

		return render_template('profile_page.html',
								profile_pic=profile_pic,
								codechef_is_connected=codechef_is_connected,
								leetcode_is_connected=leetcode_is_connected,
								hackerearth_is_connected=hackerearth_is_connected,
								current_user_profile=current_user_profile
		)


@app.errorhandler(404)
def page_not_found(error):
	profile_pic = get_profile_pic()
	return render_template('404.html', profile_pic = profile_pic), 404



##################################
######### FUNCTIONS #############
#################################


def get_dateTime(dateTime):
	dateList = str(dateTime[0]).split(" ")    # dateList = [date, month, year]
	timeList = str(dateTime[1]).split(":")    # timeList = [hour, minutes, second]
	finalDateTime = datetime.datetime(int(dateList[2]),                        # year
									  strptime(dateList[1], '%b').tm_mon,      # month
									  int(dateList[0]),                        # date
									  int(timeList[0]),                        # hour
									  int(timeList[1]),                        # minutes
									  int(timeList[2]),                        # seconds
									  0                                        # microseconds
					)
	return finalDateTime


def get_email():

	email = ""
	g.user = current_user.get_id()
	if g.user:
		id = int(g.user)
		email = User.query.get(id).email

	return email


def get_profile_pic():

	profile_pic = ""
	g.user = current_user.get_id()
	if g.user:
		id = int(g.user)
		profile_pic = User.query.get(id).profile_pic

	return profile_pic


def createFile(code, lan):
	if lan == "Python":
		extension = ".py"
	elif lan == 'C':
		extension = ".c"
	else:
		extension = ".java"

	fileName = "try" + extension

	if not os.path.exists(fileName):
		os.open(fileName, os.O_CREAT)

	fd = os.open(fileName, os.O_WRONLY)

	os.truncate(fd, 0)
	fileadd = str.encode(code)
	os.write(fd, fileadd)
	os.close(fd)


def complier_output(code, inp, chk, lan):

	if lan == 'Python':

		createFile(code, lan)

		process = subprocess.Popen(['python', 'try.py'], stdout = PIPE, stdin = PIPE, stderr = PIPE)

		#communicate() returns a tuple (stdoutdata, stderrdata)
		process_out = process.communicate(input = inp.encode())
		output = process_out[0]
		error = process_out[1]
		check = process.returncode
		if check == 0:
			return output.decode("utf-8")
		else:
			return error.decode("utf-8")

	elif lan == "C":

		createFile(code, lan)
		process = subprocess.run(['gcc','-o','out','try.c'], stderr = PIPE,)
		check = process.returncode

		if check == 0:
			if chk == '1':
				run = subprocess.run(["./out"], input = inp.encode(), stdout = PIPE)
			else:
				run = subprocess.run(["./out"], stdout = PIPE)
			return run.stdout.decode("utf-8")
		else:
			return process.stderr.decode("utf-8")

	else:

		createFile(code, lan)
		process = subprocess.run(['javac','try.java'], stderr = PIPE,)
		check = process.returncode

		if check == 0:
			if chk == '1':
				run = subprocess.run(["java", "main"], input = inp.encode(), stdout = PIPE)
			else:
				run = subprocess.run(["java", "main"], stdout = PIPE)
			return run.stdout.decode("utf-8")
		else:
			return process.stderr.decode("utf-8")


if __name__ == '__main__':
	app.run()
