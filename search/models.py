from django.db import models

from globals import COURSE_TABLE


class Search(models.Model):
    word = models.TextField(required=True)
    tblkey = models.IntegerField(required=True)
    table = models.IntegerField(required=True)
    weight = models.IntegerField(required=True)

    @classmethod
    def add_words(cls, line, key, table):
        for word in line.lower().split():
            # len(word) means more common words like 'and' will have less weight because they're short
            weight = 1000 * len(word) / len(line)  # scale factor so I can use int instead of
            # float
            cls(word=word, tblkey=key, table=table, weight=weight).save()

    @classmethod
    def search(cls, line, user):
        count = {}
        for word in line.lower().split():
            for result in cls.all().filter(word=word):
                key = (result.table, result.tblkey)
                count[key] = count.get(key, 0) + result.weight
        values = []
        from courses.models import Course  # cross referencing between files
        for (table, key) in sorted(count, key=count.get, reverse=True):
            if table == COURSE_TABLE:
                course = Course.get_by_id(key)
                if user.has_permission(course):
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
        cls.all().filter(tblkey=key, table=table).delete()
