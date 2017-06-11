
import random
import hashlib
from string import letters

from google.appengine.ext import db


def make_salt():
    """
    make_salt:  Method for creating salt string for use of hashing user
                passwords.
    Returns:
        Random string of length five.

    """
    string = ''
    for x in range(0,5):
        string += random.choice(letters)
    return string


def make_pass_hash(name, password, salt = None):
    """
    make_pass_hash: Method for creating password hash.
    Args:
        name (data type: str): String of user's name.
        password (data type: str): String of user's password.
        salt (data type: str): Sting of random five characters.
    Returns:
        A string hashed with the password and a random salt string.
    """
    if not salt:
        salt = make_salt()
    hashed = hashlib.sha256(name + password + salt).hexdigest()
    return '%s|%s' % (hashed, salt)


def valid_pass(name, password, hashed):
    """
    valid_pass: Method for checking if a hashed string matches the string of a
                user's password after it has been hashed.
    Args:
        name (data type: str): User's name
        password (data type: str): User's password
        hashed (data type: str) Hashed password
    """
    salt = hashed.split('|')[1]
    return hashed == make_pass_hash(name, password, salt)


def users_key(group = 'default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    """
    This class is for blog users
    Attributes:
        name (str): Username.
        pass_hash (str): The hashed password of a user.
        email (str): User's email address.
    """
    name = db.StringProperty(required = True)
    pass_hash = db.StringProperty(required = True)
    email = db.StringProperty()


    @classmethod
    def retrieve_by_id(cls, user_id):
        """
        retrieve_by_id: Method for retrieving a user by their key id.
        Args:
            user_id (data type: str): String of user key id.
        Returns:
            Returns the user.
        """
        return User.get_by_id(user_id, parent = users_key())


    @classmethod
    def retrieve_by_name(cls, name):
        """
        retrieve_by_name: Method for retrieving a user by their name.
        Args:
            name (data type: str): String of user's name.
        Returns:
            Returns the user.
        """
        #   query = "SELECT * FROM User WHERE name=%s" % name
        user = User.all().filter('name =', name).get()
        return user


    @classmethod
    def register (cls, name, password, email = None):
        """
        register: Method for creating an instance of user.
        Args:
            name (data type: str): String of user's name.
            password (data type: str): String of user's password.
            email (data type: str): String of user's email.
        Returns:
            Returns the user object.
        """
        pass_hash = make_pass_hash(name, password)
        return User( parent = users_key(),
                    name = name,
                    pass_hash = pass_hash,
                    email = email
                    )

    @classmethod
    def login(cls,name, password):
        """
        login: Method for logging in a user.
        Args:
            name (data type: str): String of user's name.
            password (data type: str): String of user's password.
        Returns:
            Returns the user if valid.
        """
        user = cls.retrieve_by_name(name)
        if user and valid_pass(name, password, user.pass_hash):
            return user
