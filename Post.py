
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
        return " ".join(self.project.split(" "))
