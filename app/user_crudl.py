from werkzeug.security import generate_password_hash, check_password_hash
from models import db_session, User
from flask import Flask, render_template, request


def generate_pass_hash(password):
    pass_hash = generate_password_hash(str(password), salt_length=100)
    return pass_hash


def check_pass(password_hash, password):
    return check_password_hash(password_hash, str(password))


def create_user(first_name, email, password, last_name=None):
    pass_hash = generate_pass_hash(password)
    new_user = User(first_name, email, pass_hash, last_name)
    db_session.add(new_user)
    db_session.commit()
    return "Пользователь успешно создан"


def read_user(first_name=None, email=None, last_name=None, id=None):
    u = User
    if id is not None:
        return u.query.filter(User.id == id).first()
    elif email is not None:
        return u.query.filter(User.email == email).first()
    elif first_name and last_name is not None:
        return u.query.filter(User.first_name == first_name, User.last_name == last_name).first()
    else:
        return 'Такого пользователя не существует'


def delete_user(first_name=None, email=None, last_name=None, id=None):
    del_user = read_user(first_name, email, last_name, id)
    db_session.delete(del_user)
    db_session.commit()
    return 'Пользователь удалён'


def list_users():
    pass


def auth(email, password):
    u = User.query.filter(User.email == email).first()
    if u is None:
        print('No user')
    elif u and check_pass(u.password_hash, password):
        print('Yes')
    else:
        print('Password error')


def change_password(user_id, new_password):
    u = User
    if read_user(id=user_id):
        new_pass = generate_pass_hash(new_password)
        u = User.query.filter_by(id=user_id).update(password_hash=new_pass)
    else:
        return 'Такого пользователя не существует'


#create_user(first_name='Test', email='test@test.ru', password='test')


auth('test@testf.ru', 'test')