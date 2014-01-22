from google.appengine.ext import db
from globals import COURSE_TABLE


class Search(db.Model):
    word = db.StringProperty(required=True)
    tblkey = db.IntegerProperty(required=True)
    table = db.IntegerProperty(required=True)
    weight = db.IntegerProperty(required=True)

    @classmethod
    def add_words(cls, line, key, table):
        for word in line.lower().split():
            # len(word) means more common words like 'and' will have less weight because they're short
            weight = 1000 * len(word) / len(line)  # scale factor so I can use int instead of
            # float
            cls(word=word, tblkey=key, table=table, weight=weight).put()

    @classmethod
    def search(cls, line, user):
        count = {}
        for word in line.lower().split():
            # TODO: memcache this line if I start using ajax to search when they fill in each word
            for result in cls.all().filter('word =', word):
                key = (result.table, result.tblkey)
                count[key] = count.get(key, 0) + result.weight
        values = []
        from . import Course, UserCourse  # cross referencing between files
        for (table, key) in sorted(count, key=count.get, reverse=True):
            if table == COURSE_TABLE:
                course = Course.get_by_id(key)
                inside = UserCourse.all().filter('user =', user).filter('course =', course).get() \
                        is not None or course.teacher.key().id() == user.key().id()
                if course.code is None or inside:  # public or we're in it
                    course.inside = inside
                    values.append((table, course))
            else:
                raise NotImplementedError
        return values

    @classmethod
    def rename_words(cls, line, key, table):
        # for each record, there's only going to be one 'line' indexed
        cls.delete_words(key, table)
        cls.add_words(line, key, table)

    @classmethod
    def delete_words(cls, key, table):
        db.delete(cls.all().filter('tblkey =', key).filter('table =', table))
