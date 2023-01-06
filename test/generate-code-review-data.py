from pymongo import MongoClient
import random
import datetime
import time

from secret import MONGO_URL

if __name__ == "__main__":
    num = 1000
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    db = client['code_review']
    collection = db['code_review_data_start_end']
    random_commits_file = open('amazing-grace.txt', 'r')
    random_commits = random_commits_file.readlines()
    random_commits_file.close()
    print('generating code review data...')
    for i in range(num):
        commit = random.choice(random_commits).strip()
        new_data = {
            'start_line': random.randint(1, 50),
            'end_line': random.randint(51, 100),
            'commit': commit,
            'date': datetime.datetime.now(),
            'reviewer': 'reviewer' + str(random.randint(1, 100)),
        }
        collection.insert_one(new_data)
        print('inserted data: ', new_data)