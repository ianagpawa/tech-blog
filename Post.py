
from google.appengine.ext import ndb

class Post(ndb.Model):
    """
    This class is for blog posts
    Attributes:
        title (str):  Title of post.
        content (str): Content of the post.
        creator (str): Author of the post.
        created (date): Date of when the blog post was created.
        last_modified (date): Date of when the blog post was last modified.
    """


    title = ndb.StringProperty(required=True)
    project = ndb.StringProperty()
    project_link = ndb.StringProperty()
    github = ndb.StringProperty()
    content = ndb.TextProperty(required=True)
    creator = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)


    def rendered_content(self):
        """
        rendered_content:  Method for retaining the multiline format of the
                            blogpost.

        Returns:
            String of blog post content with newlines replaced with html breaks.
        """
        return self.content.replace("\n", "<br>")


    def render_back(self):
        """
        render_back:  Method for retaining the multiline format of the
                        blogpost after it has been retrieved from the database.
        Returns:
            String of blog post content with html breaks replaced with newlines.
        """
        return self.content.replace("<br>", "\n")

    def convert_project_name(self):
        return "_".join(self.project.split(" "))


    # @classmethod
    # def cursor_pagination(cls, prev_cursor_str, next_cursor_str):
    #     ITEMS = 2
    #     posts = cls.query().order(-cls.created)
    #     if not prev_cursor_str and not next_cursor_str:
    #         objects, next_cursor, more = posts.fetch_page(ITEMS)
    #         prev_cursor_str = ''
    #         if next_cursor:
    #             next_cursor_str = next_cursor.urlsafe()
    #         else:
    #             next_cursor_str = ''
    #         next_ = True if more else False
    #         prev = False
    #     elif next_cursor_str:
    #         cursor = Cursor(urlsafe=next_cursor_str)
    #         objects, next_cursor, more = cls.query().order(cls.number).fetch_page(ITEMS, start_cursor=cursor)
    #         prev_cursor_str = next_cursor_str
    #         next_cursor_str = next_cursor.urlsafe()
    #         prev = True
    #         next_ = True if more else False
    #     elif prev_cursor_str:
    #         cursor = Cursor(urlsafe=prev_cursor_str)
    #         objects, next_cursor, more = cls.query().order(-cls.number).fetch_page(ITEMS, start_cursor=cursor)
    #         objects.reverse()
    #         next_cursor_str = prev_cursor_str
    #         prev_cursor_str = next_cursor.urlsafe()
    #         prev = True if more else False
    #         next_ = True
    #     return objects, next_cursor_str, prev_cursor_str, prev, next_
        

#
#
# post1 = Post(
#             title="Test1",
#             content="Test1",
#             project='Music Catalog',
#             project_link="Test1",
#             github="Test1",
#             creator="Me"
# )
#
# post1.put()
#
# post2 = Post(
#             title="Test2",
#             content="Test2",
#             project='Test',
#             project_link="Test1",
#             github="Test1",
#             creator="Me"
# )
#
# post2.put()
#
#
# post3 = Post(
#             title="Test3",
#             content="Test3",
#             project='Music Catalog',
#             project_link="Test3",
#             github="Test3",
#             creator="Me"
# )
#
# post3.put()
#
#
# post4 = Post(
#             title="Test4",
#             content="Test4",
#             project='Rabdin',
#             project_link="Test4",
#             github="Test4",
#             creator="Me"
# )
#
# post4.put()
