from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request,jsonify

import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
cors = CORS(app, support_credentials=True)


@app.route('/test')
@cross_origin(supports_credentials=True)
def get_x():
    return jsonify("Are maa chudi pari hai")



def get_followers(f) :
    if ',' in f :
        return int(f.replace(',' , ''))
    elif 'k' in f :
        return float(f.replace('k' , ''))*1000
    elif 'm' in f :
        return float(f.replace('m' , ''))*1000000
    else :
        return int(f)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/getUser',methods = ['POST','OPTIONS'])
@crossdomain(origin='*')
def get_user(): 
    dat = request.get_json()     
    print(type(dat))
    user = {}
    user['username'] = request.json['username']
    username = user['username']
    link = "https://www.instagram.com/" + username
    req = requests.get(link).text
    soup = BeautifulSoup(req, "html.parser")

    title = str(soup.find('title'))
    
    if "Page Not Found" in title :
        return jsonify("Not Found")
    
    ########## Followers/Following ##########
    for i in soup.find_all('meta') :
        try :
            if "Followers" in i['content']  :
                data = i['content'].split(", ")
            followers = get_followers(data[0].split(" ")[0])
            following = get_followers(data[1].split(" ")[0])
            if followers == 0 :
                followers = 1
            break
        except :
            pass
        
    ########## Profile Details ##########
    script = str(soup.find_all('script')[2])
    data = json.loads(script[52:-10])
    profile = data['entry_data']['ProfilePage'][0]

    name = profile['user']['full_name']
    id = profile['user']['id']
    bio = profile['user']['biography']
    posts_cnt = int(profile['user']['media']['count'])
    nodes = profile['user']['media']['nodes']

    ind = posts_cnt
    total_likes = 0
    total_comments = 0

    for node in nodes :
        comments = int(node['comments']['count'])
        likes = int(node['likes']['count'])
        total_likes += likes
        total_comments += comments
        ind -= 1

    like_rate = total_likes / float(10 * followers)
    comment_rate = total_comments / float(10 * followers)
    eng_rate = (total_likes + total_comments) / float(10 * followers)

    obj = {}
    obj['name'] = name
    obj['id'] = int(id)
    obj['followers'] = followers
    obj['following'] = following
    obj['bio'] = bio
    obj['posts'] = int(posts_cnt)
    obj['likes'] = total_likes
    obj['comments'] = total_comments
    obj['engagement_rate'] = eng_rate
    obj['comment_rate'] = comment_rate
    obj['like_rate'] = like_rate
  
    
    return jsonify(status="success",data=obj);

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True,automatic_options=True):

    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
if __name__ == "__main__":
    # here is starting of the development HTTP server
    app.run(host='0.0.0.0', port=8000, debug=True)
