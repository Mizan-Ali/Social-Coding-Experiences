from flask import Flask, request, jsonify

from codechef_scrape import CodechefUser

app = Flask(__name__)


@app.route('/<username>')
def home(username):
    user_data = CodechefUser(username)

    return jsonify(user_data.get_user_data())

if __name__ == '__main__':
    app.run()