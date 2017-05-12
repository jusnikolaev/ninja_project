from models import db_session, User, Post
import datetime


def create_post(chat_id, title, description, updated_at=None, approve_voices=1,
                decline_voices=0, isActive=True):
    u = User.query.filter_by(telegram_id=chat_id).first()
    if u is None:
        return False
    else:
        created_at = datetime.datetime.now()
        new_post = Post(title, description, created_at,
                        updated_at, approve_voices, decline_voices, isActive, u.id)
        db_session.add(new_post)
        db_session.commit()
        return True


def list_of_posts(chat_id):
    u = User.query.filter_by(telegram_id=chat_id).first()
    list_of_posts = u.posts
    return list_of_posts






# def test_2(user):
#     u = User.query.filter_by(id=user).first()
#     print(str(u.posts[0].title))
#
# test_2(1)
