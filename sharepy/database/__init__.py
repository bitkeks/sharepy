from database import session, database_init
from model import User, File, Role


def get_userfiles(userid):
    """Query all files of a user.
    """
    return File.q.filter(File.owner_id == userid).all()
