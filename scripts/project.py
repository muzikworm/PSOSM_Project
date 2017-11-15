
# coding: utf-8

# In[11]:

import requests
import json
import pymongo
from bs4 import BeautifulSoup


# In[13]:

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.user_data
record = db.user_data
print record


# In[21]:

def get_followers(f) :
    if ',' in f :
        return int(f.replace(',' , ''))
    elif 'k' in f :
        return float(f.replace('k' , ''))*1000
    elif 'm' in f :
        return float(f.replace('m' , ''))*1000000
    else :
        return int(f)


# In[73]:

def get_data(username) :
    link = "https://www.instagram.com/" + username
    req = requests.get(link).text
    soup = BeautifulSoup(req, "html.parser")

    title = str(soup.find('title'))
    
    if "Page Not Found" in title :
        return
    
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
    
    record.insert(obj)
    
    return eng_rate


# In[65]:

def categorise(username) :
    try :
        link = "https://www.instagram.com/" + username
        req = requests.get(link).text
        soup = BeautifulSoup(req, "html.parser")
    except :
        pass
        
    ########## Followers/Following ##########
    for i in soup.find_all('meta') :
        try :
            if "Followers" in i['content']  :
                data = i['content'].split(", ")
            followers = get_followers(data[0].split(" ")[0])
            following = get_followers(data[1].split(" ")[0])
            break
        except :
            pass
        
    try :
        if followers < 100 :
            lt_100.append(username)
        elif followers < 1000 :
            lt_1k.append(username)
        elif followers < 10000 :
            lt_10k.append(username)
        elif followers < 100000 :
            lt_100k.append(username)
        elif followers < 1000000 :
            lt_1m.append(username)
        elif followers < 10000000 :
            lt_10m.append(username)
        elif followers < 100000000 :
            lt_100m.append(username)
    except :
        pass


# In[77]:

get_data("my_instangram_")


# In[78]:

f = open('dataset.txt','r')
cnt = 1
for line in f :
    get_data(line.strip('\n'))
    print cnt, line.strip('\n')
    cnt += 1


# In[ ]:

lt_100 = []
lt_1k =[]
lt_10k = []
lt_100k = []
lt_1m = []
lt_10m = []
lt_100m = []

f = open('dataset.txt','r')
cnt = 1
for line in f :
    categorise(line.strip('\n'))
    print cnt, line.strip('\n')
    cnt += 1


# In[12]:

print lt_1k


# In[32]:

print lt_10k


# In[33]:

print lt_100k


# In[34]:

print lt_1m


# In[35]:

print lt_10m


# In[36]:

print lt_100m


# In[28]:

# lt_1k =['sahilruhela', 'charu_pathak','karan_datt','sahilruhela','vaibhav.gupta9395','pulkitrohilla','a3mayank','siddhant.gandhi',
#            'sach1n_delhiite','rishabhvarshneyrv','nikkuuu17']
# lt_10k = ['sam25malik','ezhik_amur','priyankak14','kumarvarun19','sidsince1996']
# lt_100k = ['ayush_mehta','gunjangulatii','deyakannesha','advait_vaidya','its_saileee95']
# lt_1m = ['sirino_er','disha.madan','nititaylor','shetroublemaker','asmita_s']
# lt_10m = ['katrinakaif','faroutakhtar','malaikaarorakhanofficial','bhuvan.bam22','thejohnabraham']
users = [lt_1k,lt_10k,lt_100k,lt_1m,lt_10m,lt_100m]

for i in users :
    rate_cnt = 0
    cnt = 0
    for j in i :
        rate = get_data(j)
        if rate > 0 :
            rate_cnt += rate
            cnt += 1
#                 print rate


print "Avg Eng Rate : ", 100*rate_cnt/float(cnt),'%'


# In[29]:

def check(username) :
    

rates = [16.8, 10.0, 8.0, 6.0, 3.95, 2.42]
buyed = []
username = "oberoi.manvi"

check(username)


# In[ ]:



