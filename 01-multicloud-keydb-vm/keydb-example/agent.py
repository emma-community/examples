import requests
import os
import time
import random
import sys

def submit_score(url, username, score):
    data = {'username': username, 'score': score}
    response = requests.post(url, json=data)
    print(response.json())

def run_agent(url, username):
    while True:
        score = random.randint(50, 100)
        submit_score(url, username, score)
        time.sleep(0.5)

ip = sys.argv[1]
username = sys.argv[2]
url = f'http://{ip}:5000/api/submit_score'
print(f"Using URL: {url}")
print(f"Using username: {username}")

run_agent(url, username)
