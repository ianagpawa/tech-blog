
import random
import hashlib
from string import letters

from google.appengine.ext import ndb



class User(ndb.Model):
    """
    This class is for blog users
    Attributes:
        name (str): Username.
        pass_hash (str): The hashed password of a user.
        email (str): User's email address.
    """
    name = ndb.StringProperty(required = True)
    pass_hash = ndb.StringProperty(required = True)
    email = ndb.StringProperty()
