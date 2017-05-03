from flask import Flask, render_template, request, redirect, abort
import jinja2
from user_crudl import check_session, auth, delete_session

"""Сервер"""

# Меняем стандартный директории расположения шаблонов и стилей
app = Flask(__name__, static_folder='/Users/jusnikolaev/Desktop/LearnPython/ninja_project/static')
app.jinja_loader = jinja2.FileSystemLoader('/Users/jusnikolaev/Desktop/LearnPython/ninja_project/templates')


# Главная страница
@app.route('/')
def index():
    session_id = request.cookies.get('session_id')
    if session_id is None or check_session(session_id) is None:
        return render_template('index.html')
    else:
        return redirect('/home')


# Авторизация
@app.route('/login/', methods=['Post'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if auth(email, password):
        redirect_to_home = redirect('/home')
        response = app.make_response(redirect_to_home)
        session_id = auth(email, password)
        if session_id:
            response.set_cookie('session_id', value=session_id)
            return response
        else:
            return 'Error'
    else:
        return 'Error'


# Выход с сайта
@app.route('/logout/', methods=['Post'])
def logout():
    session_id = request.cookies.get('session_id')
    if session_id is None or check_session(session_id) is None:
        return abort(401)
    else:
        delete_session(session_id)
        return redirect('/')


# Главная страница
@app.route('/home')
def home():
    session_id = request.cookies.get('session_id')
    user_name = check_session(session_id)
    if session_id is None or user_name is None:
        return abort(401)
    else:
        return render_template('home.html', user_name=user_name)


if __name__ == "__main__":
    app.run(debug=True)
