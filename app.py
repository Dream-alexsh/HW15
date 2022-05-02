from flask import jsonify, Flask
from main import app_main

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/animal/<id>')
def animal_search(id):
    data = app_main(id)
    return jsonify(data)


if __name__ == "__main__":
    app.run()
