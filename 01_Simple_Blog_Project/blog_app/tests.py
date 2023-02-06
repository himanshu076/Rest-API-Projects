from django.test import TestCase

from blog_app.models import Post, Upvote, Comment
from accounts.models import User

# Create your tests here.
class PostTestCase(TestCase):
    user = User.objects.get(id=2)
    def setUp(self):
        Post.objects.create(user=self.user, title="testing_post_title",
            body="this is testing post body.")
        # userr = User.objects.get(id=1)
        Post.objects.create(user=self.user, title="testing_post_title_0001",
            body="this is testing_0001 post body.")

    def test_post_model(self):
        post_01 = Post.objects.get(title="testing_post_title")
        post_02 = Post.objects.get(title="testing_post_title_0001")
        self.assertEqual(post_01, 'The lion says "roar"')
        self.assertEqual(post_02, 'The cat says "meow"')