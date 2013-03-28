from flask.ext.login import UserMixin

__author__ = 'tigra'


#virtual user class, do not use in production :)
class User(UserMixin):
    def __init__(self,name="default"):
        self.name=name
        self.id=self.name
        self.user_id=self.name
        return None

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        """
        Magic function for comparing, used by checking item user level permission
        :param other:
        :return:
        """
        return self.id==other.id