from werkzeug.security import generate_password_hash, check_password_hash
from models import db_session, User
import uuid

"""Большинство методов, связанных с пользователем"""


# Проверка активной сессии
def check_session(session_id):
    try:
        u = User.query.filter_by(session_id=session_id).first()
        return u.first_name
    except AttributeError:
        return None


# Удаление сессии пользователя
def delete_session(session_id):
    try:
        u = User.query.filter_by(session_id=session_id).first()
        u.session_id = None
        db_session.commit()
    except AttributeError:
        pass


# Генерация пароля
def generate_pass_hash(password):
    pass_hash = generate_password_hash(str(password), salt_length=100)
    return pass_hash


# Смена пароля
def change_password(user_id, new_password):
    new_pass = generate_pass_hash(new_password)
    u = User.query.filter(User.id == user_id).first()
    u.password_hash = new_pass
    db_session.commit()


# Проверка пароля
def check_pass(password_hash, password):
    return check_password_hash(password_hash, str(password))


# Создание пользователя
def create_user(first_name, email, password, last_name=None):
    pass_hash = generate_pass_hash(password)
    new_user = User(first_name, email, pass_hash, last_name)
    db_session.add(new_user)
    db_session.commit()
    return "Пользователь успешно создан"


# Получение данных пользователя
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


# Удаление пользователя
def delete_user(first_name=None, email=None, last_name=None, id=None):
    del_user = read_user(first_name, email, last_name, id)
    db_session.delete(del_user)
    db_session.commit()
    return 'Пользователь удалён'


# Обновление пользователей
def update_users():
    pass


# Список пользователей
def list_user():
    pass


# Авторизация, генерация и запись в куки сессии
def auth(email, password):
    u = User.query.filter(User.email == email).first()
    if u is None:
        return False
    elif u and check_pass(u.password_hash, password):
        session_id = str(uuid.uuid4())
        u = User.query.filter(User.email == email).first()
        u.session_id = session_id
        db_session.commit()
        return session_id
    else:
        return False
