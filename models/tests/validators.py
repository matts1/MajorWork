from models.tests import BaseTestCase
from models.validators import is_email, is_alphabetic, is_name


class BaseTestValidators(BaseTestCase):
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
