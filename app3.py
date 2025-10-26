from flask import Flask, request, jsonify
import psycopg2
import redis
import json
import os

app = Flask(__name__)



conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB", "sqlda"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "stat1234"),
    host=os.getenv("POSTGRES_HOST", "db")
)

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0
)

def get_user_from_db(user_id):
    with conn.cursor() as cur:
        cur.execute("SELECT customer_id, first_name, last_name, email FROM customers WHERE customer_id = %s;", (user_id,))
        user = cur.fetchone()
        if user:
            return {'id': user[0], 'first_name': user[1], 'last_name':user[2],'email': user[3]}
        return None


def cache_user(user):
    cache_key = f"user:{user['id']}"
    redis_client.setex(cache_key, 300, json.dumps(user))  # 5 minutes expiration

def get_user(user_id):
    struse = str(user_id)
    cache_key = f"user:{struse}"
    cached_user = redis_client.get(cache_key)
    if cached_user:
#       print("Fetching User from cache")
        temp = json.loads(cached_user)
        temp['source'] = 'cache'
        return  temp
    else:
        user = get_user_from_db(user_id)
        if user:

            cache_user(user)
            user['source']='postgres'

        return user

@app.route('/user', methods=['POST'])
def user():
    data = request.json
    if not data or 'id' not in data:
        return jsonify({'error': 'Please provide user id in JSON body'}), 400

    user_id = data['id']
    user_data = get_user(user_id)
#    user_data=get_user.get(user_id)
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


