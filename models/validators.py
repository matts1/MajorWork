import re
import string
from models.tests import TestCase


def is_alphabetic(x, allowed=""):
    allowed = set(string.letters + allowed)
    return x and all([l in allowed for l in x])

def is_email(word):
    if word is None or word.count("@") != 1:
        return False
    user, domain = word.split("@")
    return is_alphabetic(user, "1234567890.!#$%&'*+-/=?^_`{|}~") and is_alphabetic(domain, "1234567890-.")

def matches_regex(word, exp):
    return word is not None and bool(re.match('^(' + exp + ')$', word, re.I | re.M | re.S))

def is_name(word):
    return matches_regex(word, '[a-z]|([a-z]+[a-z-]*[a-z]+)')

class TestValidators(TestCase):
    def test_email(self):
        self.assertTrue(is_email("mAt1234567890.!#$%&'*+-/=?^_`{|}~@gmail1234567890-.com"))

        self.assertFalse(is_email(" matt@gmail.com"))
        self.assertFalse(is_email(" matt@gmail.com "))
        self.assertFalse(is_email("abc@gma@il.com"))
        self.assertFalse(is_email(r"\abc@gmail.com"))
        self.assertFalse(is_email("abc@gmail_.com"))
        self.assertFalse(is_email(None))

    def test_alphabetic(self):
        self.assertTrue(is_alphabetic("abc"))
        self.assertTrue(is_alphabetic("abc ", " "))

        self.assertFalse(is_alphabetic("abc "))
        self.assertFalse(is_alphabetic(None))

    def test_name(self):
        self.assertTrue(is_name("abc"))
        self.assertTrue(is_name("ab-c"))
        self.assertTrue(is_name("a"))

        self.assertFalse(is_name("-abc"))
        self.assertFalse(is_name("abc-"))
        self.assertFalse(is_name("a bc"))
        self.assertFalse(is_name(""))
        self.assertFalse(is_name(None))
