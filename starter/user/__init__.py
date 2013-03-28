from starter import login_manager
from starter.user.models import User

__author__ = 'tigra'

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)