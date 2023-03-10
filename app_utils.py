from flask import session


def is_logged_in():
    if "roll_no" in session:
        return True
    return False