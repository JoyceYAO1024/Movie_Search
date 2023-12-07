from flask import Flask, jsonify, request
from search import Search
from user_info import User
from block_info import Block
from review import Review
from movie_info import Movie
import pickle
app = Flask(__name__)


current_user=''
genres_info = [
    {"type": "Drama", "value": 320 },
    {"type": "Thriller", "value": 96 },
    {"type": "Action", "value": 94 },
    {"type": "Comedy", "value": 92 },
    {"type": "Adventure", "value": 86 },
    {"type": "Romance", "value": 82 },
    {"type": "Crime", "value": 71 },
    {"type": "Family", "value": 46 },
    {"type": "Fantasy", "value": 42 },
    {"type": "Animation", "value": 39 },
    {"type": "Documentary", "value": 38 },
    {"type": "Science Fiction", "value": 37 },
    {"type": "Mystery", "value": 36 },
    {"type": "History", "value": 33 },
    {"type": "War", "value": 27 },
    {"type": "Music", "value": 24 },
    {"type": "Horror", "value": 11 },
    {"type": "Western", "value": 7 },
    {"type": "Foreign", "value": 3 }
]


# homepage 未修改
@app.route('/homepage')
def home():

    response = [{
        'title':'Band of Brothers',
        'image':'https://images-na.ssl-images-amazon.com/images/M/MV5BMTI3ODc2ODc0M15BMl5BanBnXkFtZTYwMjgzNjc3._V1_UX182_CR0,0,182,268_AL_.jpg'
    },
                {
        'title':'Toy Story',
        'image':'https://images-na.ssl-images-amazon.com/images/M/MV5BMDU2ZWJlMjktMTRhMy00ZTA5LWEzNDgtYmNmZTEwZTViZWJkXkEyXkFqcGdeQXVyNDQ2OTk4MzI@._V1_UX182_CR0,0,182,268_AL_.jpg',
        
                },
                {
        'title':'Death Race 2',
        'image':'https://images-na.ssl-images-amazon.com/images/M/MV5BMTk0OTUxNTYxNF5BMl5BanBnXkFtZTcwMzA1MDIyNQ@@._V1_UY268_CR5,0,182,268_AL_.jpg',
                },
                {
        'title':'The Dark Knight',
        'image':'https://images-na.ssl-images-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_UX182_CR0,0,182,268_AL_.jpg',
                },
                {
        'title':'India\'s Daughter',
        'image':'https://images-na.ssl-images-amazon.com/images/M/MV5BNmM1MDZiZDItYjZlMC00YjgwLWI2YzktYmE0ODk3MTE0MDAxXkEyXkFqcGdeQXVyMjAzMjcxNTE@._V1_UY268_CR1,0,182,268_AL_.jpg',
                }]
    return jsonify(response)

#search
''''''
''''''
#搜索，目前支持模糊搜索
#title 为电影名字，可以小写
@app.route('/search/moviename/<title>')
def searchmovie(title):
    result = Search.search_movie(title.lower())
    
    return result
#搜演员
#name 为演员名字
@app.route('/search/cast/<name>')
def searchcast(name):
    result = Search.search_cast(name.lower())
    
    return result
#搜导演
#name 为导演名字
@app.route('/search/crew/<name>')
def searchcrew(name):
    result = Search.search_crew(name.lower())
    return result

#电影分类查询
@app.route('/search/movieType')
def searchType():
    return jsonify(genres_info)

#根据分类搜索电影
#type 为电影类型名
@app.route('/search/movieByType/<type>')
def searchMovieByType(type):
    
    result = Search.search_type(type.lower())
    
    return result
''''''
''''''
''''''

#电影详情页，传准确的电影id
#返回 title,id,genres,overview,release_date,runtime,vote_average,Poster,`cast`,crew
@app.route('/movie/<id>')
def details(id):
    res=Movie.movie_info(id)
    return res


#根据电影id获取评论
#已经可以过滤掉黑名单用户
@app.route('/review/<movie_id>')
def get_review(movie_id):
    id=int(movie_id)
    with open('user.pickle', 'rb') as f:
        data = f.read()
        current_user = pickle.loads(data)
    res=Review.get_review(id,current_user)
    return res
#添加电影评论
#'email' TEXT
#'movie_id' INT
#'review' TEXT
#不需要添加时间
@app.route('/addreview',methods=['POST'])
def addreview():
    data=request.get_json()
    email = data.get('email')
    movie_id = data.get('movie_id')
    review = data.get('review')
    Review.add_review(email,movie_id,review)
    return jsonify({'message':'add successfully','success': 'true'})

#给电影添加评分
#movie_id 电影id
#score 用户的打分
#打分后需要重新根据id获取电影详情
@app.route('/score/<movie_id>/<score>')
def score(movie_id,score):
    Review.score(int(score),movie_id)
    return jsonify({'message':'score successfully','success': 'true'})


#注册
#'email' TEXT
#'password' TEXT
#'name' TEXT
@app.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')#注册邮箱
    password = data.get('password') #密码
    name = data.get('name') # 昵称
    if User.verify(email): #验证邮箱是否存在
        User.regist(email,password,name) #添加到数据库
        return jsonify({'message':'regist successfully','success': 'true'})
    else:
        return jsonify({'message':'have registed','success': 'false'})

#登录
#'email' TEXT
#'password' TEXT
@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email') #登录邮箱
    password = data.get('password') #密码
    if User.login(email,password):
        current_user=email
        with open("user.pickle", "wb") as f:
            pickle.dump(current_user, f)
        return jsonify({'message':current_user +' successfully','success': 'true'})
    else:
        return jsonify({'message':'password wrong','success': 'false'})
#登出
#仅作为服务端记录使用
#请logout之后发送请求
@app.route('/user/logout')
def logout():
    current_user=''
    with open("user.pickle", "wb") as f:
            pickle.dump(current_user, f)
    return jsonify({'message':'logout successfully','success': 'true'})

#更新头像
#email 用户email
#pid 前端图片编号 默认为0，当前数据库中有1，2
#更新后需要需要重新请求用户信息
@app.route('/user/update_picture/<email>/<pid>')
def update_picture(email,pid):
    User.update_picture(email,pid)
    return jsonify({'message':'update successfully','success': 'true'})

#更新背景
#email 用户email
#bid 前端图片编号 默认为0，当前数据库中有1，2
#更新后需要需要重新请求用户信息
@app.route('/user/update_background/<email>/<bid>')
def update_background(email,bid):
    User.update_background(email,bid)
    return jsonify({'message':'update successfully','success': 'true'})


#愿望单

#获取用户信息 #有更新!!!
#email 用户email(唯一身份标志)
@app.route('/personpage/<email>')
def personpage(email):
    return User.get_info(email)

#获取愿望单
#email 用户email(唯一身份标志)
#返回id,name,image
#id为电影id
#name 为电影名
#image为海报
@app.route('/getwishlist/<email>')
def show(email):
    wishlist = User.get_wishlist(email)
    
    return wishlist
#添加愿望单，添加电影id!!!! 
#id 电影id
@app.route('/addwishlist/<email>/<id>')
def addwishlist(email,id):

    wishlist=User.get_wishlist(email)
    if id not in wishlist:
        User.add_wishlist(email,id)
        return jsonify({'message':'add successfully','success': 'true'})
    else:
        return jsonify({'message':'the movie is in his wishlist','success': 'false'})

# 删除愿望单内某一电影操作，请使用电影id
#id 电影id
@app.route('/deletewishlist/<email>/<id>')
def delete(email,id):
    wishlist=User.get_wishlist(email)
    if id in wishlist:
        User.delete_wishlist(email,id)
        return jsonify({'message':'delete successfully','success': 'true'})
    else:
        return jsonify({'message':'the movie is not in his wishlist','success': 'false'})
    

#获取黑名单信息
#返回一个json格式的email的list
#包含block_user的email,name,picture(头像)
#已将不存在用户筛选掉
@app.route('/getblocklist/<email>')
def getblock(email):
    l=Block.get_block(email)
    return l

#添加黑名单
#email 当前用户
#block_user 被拉黑的用户
#添加的用户可以是未注册的用户
@app.route('/block/<email>/<block_user>')
def block(email,block_user):
    l=Block.get_block(email)
    if block_user not in l:
        Block.add(email,block_user)
        return jsonify({'message':'add successfully','success': 'true'})
    else:
        return jsonify({'message':'you have added him','success': 'false'})

if __name__ == '__main__':

    app.run(debug=True)