from flask import Flask, render_template,request
import mysql.connector
conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='taskmanagementsystem'
)
mycursor=conn.cursor()
user_dict={'noble':'1234','daniel':'1234'}

#create a flask application
app = Flask(__name__)
user_dict={'admin':'admin','noble':'1234'}
#define the route

@app.route('/')
def hello():
  
     return render_template('index.html') 

@app.route('/login')
def login():
     return render_template('login.html')

@app.route('/home',methods=['POST'])
def home():
     uname=request.form['username']
     pwd=request.form['password']
     if uname not in user_dict:
          return render_template('login.html',msg='invalid user')
     elif user_dict[uname]!=pwd:
          return render_template('login.html',msg='invalid pswrd')
     else:
          return render_template('home.html')

#SIGNUP
@app.route('/signup')
def signup():
     return render_template('signup.html')

@app.route('/sign',methods=['POST'])
def sign():
     name=request.form['name']
     user_id=request.form['user_id']
     password=request.form['password']
     query="insert into users values(%s,%s,%s)"
     values=(user_id,name,password)
     mycursor.execute(query,values)
     conn.commit()
     return render_template('signup.html',signmsg='Signed Successfully')


#VIEW   
@app.route('/view0')
def viewresult():
     return render_template('view0.html')

@app.route('/view',methods=['POST'])
def view():
     userid=request.form['userid']
     query='select * from tasks where user_id='+userid
     mycursor.execute(query)
     data=mycursor.fetchall()
     return render_template('view.html',sqldata=data)

#ADD
@app.route('/add')
def add():
     return render_template('add.html')

@app.route('/read',methods=['POST'])
def read():
     task_id=request.form['task_id']
     user_id=request.form['user_id']
     title=request.form['title']
     description=request.form['description']
     due_date=request.form['due_date']
     status=request.form['status']
     category=request.form['category']
     query="insert into tasks values(%s,%s,%s,%s,%s,%s,%s)"
     values=(task_id,user_id,title,description,due_date,status,category)
     mycursor.execute(query,values)
     conn.commit()
     return render_template('add.html',addmsg='Added Successfully')

#SEARCH
@app.route('/search')
def searchresult():
     return render_template('search.html')

@app.route('/searchresult',methods=['POST'])
def search():
     user_id=request.form['user_id']
     task_name=request.form['task_name']
     query="SELECT * FROM tasks WHERE title LIKE '%{}%' AND user_id = {}".format(task_name, user_id)
     mycursor.execute(query)
     data=mycursor.fetchall()
     return render_template('view.html',sqldata=data)

#FILTER
@app.route('/filter')
def filterresult():
     return render_template('filter.html')

@app.route('/filterresult',methods=['POST'])
def filter():
     user_id=request.form['user_id']
     category=request.form['category']
     query="SELECT * FROM tasks WHERE category LIKE '%{}%' AND user_id = {}".format(category,user_id)
     mycursor.execute(query)
     data=mycursor.fetchall()
     return render_template('view.html',sqldata=data)

#DELETE
@app.route('/delete')
def deleteresult():
     return render_template('delete.html')

@app.route('/deleteresult',methods=['POST'])
def delete():
     user_id=request.form['user_id']
     title=request.form['title']
     query="DELETE FROM tasks WHERE title LIKE '%{}%' AND user_id = {}".format(title,user_id)
     mycursor.execute(query)
     data=mycursor.fetchall()
     return render_template('delete.html',dltmsg='Deleted Successfully')

#Run flask appln
if __name__ == '__main__':
    app.run(debug=True)