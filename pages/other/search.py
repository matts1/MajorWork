from models import Search
from pages import BaseHandler


class SearchHandler(BaseHandler):
    template = 'other/search.html'

    def myget(self):
        query = self.request.get('query')
        return dict(
            query=query,
            results=Search.search(query, self.user)
        )
