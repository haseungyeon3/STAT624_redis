Here is a demonstration of how to use PostgreSQL for persistent data storage and Redis for caching in a Flask web API.

Run ''docker-compose up -d'' to start containers for Redis, Redissight (Redis GUI), PostgreSQL, pgAdmin (PostgreSQL GUI), and app3.
Test API caching by seeing which database the data is retrieved from. Use this command:
curl -X POST -H "Content-Type: application/json" -d '{"id":1}' http://localhost:5000/user
