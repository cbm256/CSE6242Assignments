from flask import Flask, render_template, request, json,jsonify
import re
app= Flask(__name__)

def password_checker(password):
    passed=[]
    if len(password) < 8:
       passed.append(1)
    if not re.search(r"[A-Z]", password):
       passed.append(2)
    if not re.search(r"\d", password):
       passed.append(3)
    if passed==[]:
       return password
    else:
       return passed



@app.route('/')
def index():
    return render_template('hello.html')
@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/signUpUser', methods=['POST'])

def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    #return "I am so dumb"
    #if user and password and password_checker(password)==password:
     #   newUser='Congratulations on registering for CSE6242, '+user+'! Redirecting you to the course homepage...'
      #  return jsonify({'message':newUser})
    passed=password_checker(password)
    if user and password and passed==password:
       return json.dumps({'status':'OK','user':user,'pass':password});
    if user and password:
       return json.dumps({'status':'BAD','user':user,'pass':passed});



if __name__=="__main__":
    app.run()
