from models.tests import BaseTestCase
from models.validators import is_email, is_alphabetic, is_name, is_title, make_title


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

    def test_title(self):
        self.assertFalse(is_title(''))
        self.assertFalse(is_title(' '))
        self.assertTrue(is_title('blah'))
        self.assertTrue(is_title(' \n\t\r\v\fblah\n\t\v\r\f'))
        self.assertTrue(is_title(' public course \n'))

    def test_make_title(self):
        self.assertEqual(make_title(' \n\t\r\v\fblah\n\t\v\r\f'), 'Blah')
        self.assertEqual(make_title('course'), 'Course')
        self.assertEqual(make_title('course blah'), 'Course Blah')
