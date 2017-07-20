
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
#
# post5 = Post(
#             title="Test5",
#             content="Test5",
#             project='Music Catalog',
#             project_link="Test5",
#             github="Test5",
#             creator="Me"
# )
#
# post5.put()
#
#
# post6 = Post(
#             title="Test6",
#             content="Test6",
#             project='Rabdin',
#             project_link="Test6",
#             github="Test6",
#             creator="Me"
# )
#
# post6.put()
#
#
#
# post7 = Post(
#             title="Test1",
#             content="Test1",
#             project='Music Catalog',
#             project_link="Test1",
#             github="Test1",
#             creator="Me"
# )
#
# post7.put()
#
# post8 = Post(
#             title="Test2",
#             content="Test2",
#             project='Test',
#             project_link="Test1",
#             github="Test1",
#             creator="Me"
# )
#
# post8.put()
#
#
# post9 = Post(
#             title="Test3",
#             content="Test3",
#             project='Music Catalog',
#             project_link="Test3",
#             github="Test3",
#             creator="Me"
# )
#
# post9.put()
#
#
# post10 = Post(
#             title="Test4",
#             content="Test4",
#             project='Rabdin',
#             project_link="Test4",
#             github="Test4",
#             creator="Me"
# )
#
# post10.put()
#
# post11 = Post(
#             title="Test5",
#             content="Test5",
#             project='Music Catalog',
#             project_link="Test5",
#             github="Test5",
#             creator="Me"
# )
#
# post11.put()
#
#
# post12 = Post(
#             title="Test6",
#             content="Test6",
#             project='Rabdin',
#             project_link="Test6",
#             github="Test6",
#             creator="Me"
# )
#
# post12.put()
