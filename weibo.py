import os

from flask import Flask,render_template,session,redirect,url_for,flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
# 定义表单类：
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
# 配置数据库
from flask.ext.sqlalchemy import SQLAlchemy




basedir=os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY']='hard to guess string'
# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db = SQLAlchemy(app)




@app.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name = name)

@app.route('/formdemo', methods=['GET','POST'])
def formdemo():
    form = NameForm()
    if form.validate_on_submit():
        old_name=session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('look like you have changed your name!')
        session['name']=form.name.data
        return redirect(url_for('formdemo'))
    return render_template('formdemo.html',form=form,name=session.get('name'))





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500




# 定义表单类：
class NameForm(Form):
    name= StringField('what is your name?',validators=[Required()])
    submit = SubmitField('Submit')

# 定义数据库中Role和User模型：
class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String(64),unique=True)



    def __init__(self,nickname):
        self.nickname = nickname


    def __repr__(self):
        return '<Role %r>' %(self.nickname)
    # users = db.relationship('User',backref='role')#和user之间关系，定义反向关系，这一属性可替代role_id访问Role模型，此时获取的是模型对象而不是外键的值
    #

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)

    def __init__(self,username):
        self.username = username

    def __repr__(self):
        return '<User %r>' %(self.username)

    # role_id = db.column(db.Integer,db.ForeignKey('roles.id'))#和role之间关系


if __name__ == '__main__':
    app.run()
