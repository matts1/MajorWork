import re
import string


def is_alphabetic(x, allowed=""):
    allowed = set(string.letters + allowed)
    return x and all([l in allowed for l in x])


def is_email(word):
    if word is None or word.count("@") != 1:
        return False
    user, dom = word.split("@")
    return is_alphabetic(user, "1234567890.!#$%&'*+-/=?^_`{|}~") and is_alphabetic(dom, "1234567890-.")


def matches_regex(word, exp):
    return word is not None and bool(re.match('^(' + exp + ')$', word, re.I | re.M | re.S))


def is_name(word):
    return matches_regex(word, '[a-z]|([a-z]+[a-z-]*[a-z]+)')

def is_title(word):
    return word is not None and word.strip()

def make_title(word):
    return re.sub(r'\s+', ' ', word.strip()).title()
