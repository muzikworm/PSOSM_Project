from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.all("/api/*", function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Cache-Control, Pragma, Origin, Authorization, Content-Type, X-Requested-With");
  res.header("Access-Control-Allow-Methods", "GET, PUT, POST");
  return next();
});
cors = CORS(app, support_credentials=True)


@app.route('/test')
@cross_origin(supports_credentials=True)
def get_x():
    return jsonify({'success': 'ok'})

if __name__ == "__main__":
    # here is starting of the development HTTP server
    app.run(host='0.0.0.0', port=8000, debug=True)