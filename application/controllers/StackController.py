# Controller to handle stack api interactions

from dataclasses import dataclass
from stackapi import StackAPI
import json

 
@dataclass
class User:
    reputation: int = 0
    total_answer_score: int = 0
    count_is_accepted: int = 0

def fetchUserData(userID):

    SITE = StackAPI('stackoverflow')
    SITE = StackAPI('stackoverflow', key='')

    answers = SITE.fetch('users/{}/answers'.format(userID))
    response = json.loads(json.dumps(answers))

    reputation = response['items'][0]['owner']['reputation']
    total_answer_score = 0
    count_is_accepted = 0

    for answer in response['items']:
        total_answer_score += answer['score']
        if (answer['is_accepted']):
            count_is_accepted += 1
    
    # Future: Add these parameters to the database table for analytics dashboard
    user = User(reputation,total_answer_score,count_is_accepted)

    return user


def calculateRewardPoints(user):
    reward_points = int(user.reputation/10000 + user.total_answer_score + user.count_is_accepted)
    return reward_points


def main():

    # Future: input user id from database table post user registration
    print("Enter the User ID")
    userId = input()

    user = fetchUserData(userId)
    reward_points = calculateRewardPoints(user)

    # Future: update database table column with the reward points
    print(reward_points)

if __name__ == "__main__":
    main()
