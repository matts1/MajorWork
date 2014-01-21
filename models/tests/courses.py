from models import Course
from models.tests import BaseTestCase


class CourseTest(BaseTestCase):
    def test_creation(self):
        self.assertIsNotNone(
            Course.create(self.teacher, '', ''),
            'Empty course name'
        )
        self.assertIsNone(
            Course.create(self.teacher, 'pub', ''),
            'Create public course'
        )
        self.assertIsNotNone(
            Course.create(self.teacher, 'Pub', ''),
            'Recreate public course (bad)'
        )
        self.assertIsNone(
            Course.create(self.teacher, 'Pub2', None),
            'Create public course'
        )
        self.assertIsNone(
            Course.create(self.teacher, 'pvt', 'on'),
            'Create private course'
        )
        for name, private in [('Pvt', True), ('Pub', False), ('Pub2', False)]:
            course = Course.all().filter('name =', name).get()
            self.assertIsNotNone(course)
            if private:
                self.assertIsNotNone(course.code)
            else:
                self.assertIsNone(course.code)
            self.assertEqual(course.teacher.email, self.teacher.email)

    def test_joining(self):
        self.assertIsNotNone(
            self.teacher.join_course(self.public.key().id()),
            'Trying to join their own course'
        )

        self.assertEqual(len(self.teacher2.courses()), 0)
        start = len(self.public.students())
        self.assertIsNone(
            self.teacher2.join_course(self.public.key().id()),
            'Other teacher joins course'
        )
        self.assertEqual(len(self.public.students()), start + 1)
        self.assertEqual(len(self.teacher2.courses()), 1)

        self.assertIsNone(
            self.student.join_course(self.public.key().id()),
            'Student joins course'
        )
        self.assertIsNotNone(
            self.student.join_course(self.private.key().id()),
            'Trying to join a private course'
        )
        self.assertIsNone(
            self.student.join_course(self.private.key().id(), self.private.code),
            'Trying to join a private course with the correct code'
        )
        self.assertIsNotNone(
            self.student.join_course(self.private.key().id(), self.private.code),
            'Trying to rejoin a private course with the correct code'
        )

    def test_listing(self):
        self.assertEqual(len(list(self.teacher.courses_taught())), 2)
        self.assertIsNone(self.teacher2.courses_taught().get())
        self.assertIsNone(self.student.courses_taught().get())
