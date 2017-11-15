from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, support_credentials=True)


@app.route('/test')
@cross_origin(supports_credentials=True)
def get_x():
    return ("Are maa chudi pari hai")

if __name__ == "__main__":
    # here is starting of the development HTTP server
    app.run(host='0.0.0.0', port=8000, debug=True)