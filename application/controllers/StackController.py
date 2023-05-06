# Controller to handle stack api interactions
from datetime import datetime
from dataclasses import dataclass
from stackapi import StackAPI
from controllers.DBController import connectToDB
from flask_session import Session
from flask import session,redirect,render_template,url_for
from controllers.DBController import connectToDB
import json

 
@dataclass
class User:
    user_id: str
    reputation: int = 0
    total_answers: int = 0
    answers_accepted: int = 0
    answers_rejected: int = 0
    total_answer_score: int = 0

def fetchUserData():

    SITE = StackAPI('stackoverflow')
    SITE = StackAPI('stackoverflow', key='')
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute("SELECT stackoverflow_id FROM employee WHERE emp_email=%s", (session['username'],))
    user_id = cur.fetchone()
    user_id = user_id[0]
    answers = SITE.fetch('users/{}/answers'.format(user_id))
    response = json.loads(json.dumps(answers))
    
    reputation = response['items'][0]['owner']['reputation']
    total_answers = 0
    total_answer_score = 0
    answers_accepted = 0
    answers_rejected = 0
    
    for answer in response['items']:
        total_answer_score += answer['score']
        if (answer['is_accepted']):
            answers_accepted += 1
    total_answers = len(response['items'])
    answers_rejected = total_answers - answers_accepted
    # Future: Add these parameters to the database table for analytics dashboard
    user = User(user_id,reputation,total_answers,answers_accepted,answers_rejected,total_answer_score)
    reward_points = calculateRewardPoints(user)
    cur.execute("SELECT user_id FROM dashboard_data WHERE user_id=%s", (user_id,))
    user_data = cur.fetchone()
    if user_data:
        cur.close()
        conn.close()
    else:
        cur.execute('INSERT INTO dashboard_data (user_id, reputation, total_answers, answers_accepted,total_score,created_at, created_by,modified_at, modified_by,answers_rejected,reward_points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)', (user_id, user.reputation, user.total_answers, user.answers_accepted,user.total_answer_score, datetime.now(), 'admin',datetime.now(), 'admin',user.answers_rejected,reward_points))
        conn.commit()
    cur.close()
    conn.close()
    return user

def calculateRewardPoints(user):
    reward_points = int(user.reputation/10000 + user.total_answer_score + user.answers_accepted)
    return reward_points


def main():
    fetchUserData()

if __name__ == "__main__":
    main()
