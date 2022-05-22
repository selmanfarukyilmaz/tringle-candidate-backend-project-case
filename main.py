from flask import *
from API_operations.post_API import post_API
from API_operations.get_API import get_API

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(post_API)
    app.register_blueprint(get_API)
    app.run(host="0.0.0.0")



