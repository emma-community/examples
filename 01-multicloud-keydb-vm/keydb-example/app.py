import os
from flask import Flask, render_template, request, jsonify
import redis
from datetime import datetime
import json
from modules.emma_api import get_VMs

app = Flask(__name__)

REDIS_HOST = os.getenv('REDIS_HOST') or 'localhost'
REDIS_PORT = os.getenv('REDIS_PORT') or 6379

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password='', decode_responses=True)

@app.route('/')
def homepage():
    # Retrieve top 10 scores from Redis
    top_scores = r.lrange('scores', -10, -1)  # Get the last 10 scores
    top_scores = [json.loads(score) for score in top_scores]  # Parse JSON strings
    top_scores.reverse()  # Reverse to show most recent first
    return render_template('index.html', top_scores=top_scores)


@app.route('/status/cluster')
def status_cluster():
    replication_info = r.info('replication')
    return jsonify(replication_info)
    # NOTE: get_VMs() is currently not working for K8s deployments
    # vm_info = get_VMs()
    # n_slaves = replication_info['connected_slaves']
    # for i in range(n_slaves):
    #     slave = replication_info[f"slave{i}"]
    #     ip = slave["ip"]
    #     vm_info[ip]['replication_state'] = slave["state"]
    # return jsonify(vm_info)

@app.route('/api/submit_score', methods=['POST'])
def api_submit_score():
    data = request.get_json()
    username = data['username']
    score = data['score']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    score_entry = {'username': username, 'score': score, 'timestamp': timestamp}
    r.rpush('scores', json.dumps(score_entry))
    r.zadd('leaderboard', {username: score})
    return jsonify({'message': 'Score submitted successfully!'}), 200

@app.route('/api/scores')
# Retrieve all scores from Redis
def apo_get_scores():
    scores = r.lrange('scores', 0, -1)
    scores_data = [json.loads(score) for score in scores]
    return jsonify(scores_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
