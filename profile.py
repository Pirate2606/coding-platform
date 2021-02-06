import requests
import bs4
from models import Profile, db, User
from app import app

def codechef_info(user_name, email):

	with app.app_context():
		print("STARTED codechef")
		profile = Profile().query.filter_by(username=email).first()

		url = 'https://www.codechef.com/users/' + user_name
		r = requests.get(url)
		not_found = requests.head(url)
		if not_found.status_code == 302:
			print("NO PAGE FOUND")
			profile.codechef_username_correct = 0
			db.session.add(profile)
			db.session.commit()
			return
		else:
			profile.codechef_username_correct = 1
			db.session.add(profile)
			db.session.commit()
		soup = bs4.BeautifulSoup(r.text, 'html.parser')

		ratingList = soup.find_all("div", class_="rating-number")
		ranks = soup.find_all("div", class_="rating-ranks")
		country = soup.find_all("span", class_="user-country-name")
		name = soup.find_all("h2")

		if len(ratingList) != 0:
			rating = ratingList[0].text
			profile.codechef_rating = rating

		if len(ranks) != 0:
			ranks = ranks[0].text.strip().split()
			profile.codechef_global_rank = ranks[0]
			profile.codechef_local_rank = ranks[-1]

		if len(country) != 0:
			user_country = country[0].text
			profile.codechef_country = user_country

		if len(name) != 0:
			for i in name:
				if "class" in i:
					continue
				else:
					realname = i.text
			profile.codechef_realname = realname

		db.session.add(profile)
		db.session.commit()
		print("SUCCESS codechef")


def leetcode_info(user_name, email):

	with app.app_context():
		print("STARTED leetcode")
		profile = Profile().query.filter_by(username=email).first()

		url = 'https://leetcode.com/' + user_name + '/'
		r = requests.get(url)
		if r.status_code != 200:
			print("NO PAGE FOUND")
			profile.leetcode_username_correct = 0
			db.session.add(profile)
			db.session.commit()
			return
		else:
			profile.leetcode_username_correct = 1
			db.session.add(profile)
			db.session.commit()
		soup = bs4.BeautifulSoup(r.text, 'html.parser')

		contests = soup.find_all("span", class_="progress-bar-success")
		name = soup.find_all("h4", class_="realname")

		if len(contests) != 0:
			if len(contests) == 9:
				profile.leetcode_contest_finished = contests[0].text.strip()
				profile.leetcode_contest_rating = contests[1].text.strip()
				profile.leetcode_global_rank = contests[2].text.strip().split(" / ")[0]
				profile.leetcode_solved_questions = contests[3].text.strip().split(" / ")[0]
				profile.leetcode_accepted_submissions = contests[4].text.strip()
			else:
				profile.leetcode_contest_finished = contests[0].text.strip()
				profile.leetcode_contest_rating = "NA"
				profile.leetcode_global_rank = "NA"
				profile.leetcode_solved_questions = contests[1].text.strip().split(" / ")[0]
				profile.leetcode_accepted_submissions = contests[2].text.strip()

		if len(name) != 0:
			if name[0].text.strip() == "":
				profile.leetcode_realname = "NA"
			else:
				profile.leetcode_realname = name[0].text.strip()

		db.session.add(profile)
		db.session.commit()
		print("SUCCESS leetcode")


def hackerearth_info(user_name, email):

	with app.app_context():
		print("STARTED hackerearth")
		profile = Profile().query.filter_by(username=email).first()

		url = 'https://www.hackerearth.com/@' + user_name
		r = requests.get(url)
		if r.status_code != 200:
			print("NO PAGE FOUND")
			profile.hackerearth_username_correct = 0
			db.session.add(profile)
			db.session.commit()
			return
		else:
			profile.hackerearth_username_correct = 1
			db.session.add(profile)
			db.session.commit()
		soup = bs4.BeautifulSoup(r.text, 'html.parser')

		skill = soup.find_all("div", class_="skill-names")
		name = soup.find_all("h1", class_="name")
		rating = soup.find_all("span", class_="track-following-num")

		if len(skill) != 0:
			profile.hackerearth_skills = skill[0].text.strip()
			if len(skill) == 2:
				profile.hackerearth_education = skill[1].text.strip()
			else:
				profile.hackerearth_education = "NA"

		if len(rating) != 0:
			if len(rating) == 1:
				profile.hackerearth_rating = "NA"
			else:
				profile.hackerearth_rating = rating[1].text.strip()

		if len(name) != 0:
			profile.hackerearth_realname = name[1].text.strip()

		db.session.add(profile)
		db.session.commit()
		print("SUCCESS hackerearth")
