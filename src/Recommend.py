from UseSqlite import InsertQuery, RiskQuery
from bookmark_analysis import BookMark


class Applicant:
    def __init__(self, scores, bookmark_file):
        self.scores = scores
        self.bookmark_file = bookmark_file

    def get_browse_history(self):
        pass


class MajorRecommender:
    def recommend_for(self):
        pass


def read_browse_history():
    rq = RiskQuery('data.db')
    rq.instructions("SELECT bookmark_file FROM admission WHERE bookmark_file is not null")
    rq.do()
    bookmarks = rq.format_results()
    print(bookmarks)
    for bookmark in bookmarks:
        rq.instructions("UPDATE admission SET browse_history =(\'%s\') WHERE bookmark_file = (\'%s\')" % \
                        (BookMark.like_vector(bookmark), bookmark))
        rq.do()
    print(rq.format_results())


if __name__ == '__main__':
    read_browse_history()
