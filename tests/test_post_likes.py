import os
import re
import unittest
from app import create_app, db
from app.models import User, Post, post_likes
from config import Config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIG = os.path.join(ROOT, 'migrations', 'versions', '5b1c2d3e4f60_post_likes.py')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


class PostLikesCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.u = User(username='u', email='u@example.com')
        self.v = User(username='v', email='v@example.com')
        self.p = Post(body='hi', author=self.u)
        db.session.add_all([self.u, self.v, self.p])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_c1_post_likes_relationship(self):
        self.assertTrue(hasattr(Post, 'likes'))
        self.assertIs(Post.likes.property.mapper.class_, User)

    def test_c2_c5_secondary_table(self):
        self.assertIs(Post.likes.property.secondary, post_likes)
        self.assertEqual(post_likes.name, 'post_likes')

    def test_c3_orm_mapped(self):
        self.assertIn('likes', Post.__mapper__.relationships)

    def test_c4_user_liked_posts(self):
        self.assertIs(User.liked_posts.property.mapper.class_, Post)

    def test_c6_c7_post_like_unlike(self):
        self.p.like(self.v)
        db.session.commit()
        self.p.like(self.v)
        db.session.commit()
        self.assertEqual(self.p.like_count(), 1)
        self.p.unlike(self.v)
        db.session.commit()
        self.assertEqual(self.p.like_count(), 0)

    def test_c8_c9_user_like_unlike(self):
        self.v.like_post(self.p)
        db.session.commit()
        self.assertEqual(self.p.like_count(), 1)
        self.v.unlike_post(self.p)
        db.session.commit()
        self.assertEqual(self.p.like_count(), 0)

    def test_c10_is_liked_by(self):
        self.assertIs(self.p.is_liked_by(self.v), False)
        self.p.like(self.v)
        db.session.commit()
        self.assertIs(self.p.is_liked_by(self.v), True)

    def test_c11_like_count_int(self):
        self.assertIsInstance(self.p.like_count(), int)

    def test_c12_has_liked_post(self):
        self.assertIs(self.v.has_liked_post(self.p), False)
        self.v.like_post(self.p)
        db.session.commit()
        self.assertIs(self.v.has_liked_post(self.p), True)

    def test_c13_c14_c15_migration(self):
        self.assertTrue(os.path.exists(MIG))
        src = open(MIG).read()
        self.assertIn("create_table('post_likes'", src)
        self.assertIn("PrimaryKeyConstraint('user_id', 'post_id')", src)
        self.assertIn("['post.id']", src)
        self.assertIn("['user.id']", src)
        self.assertIn("down_revision = '834b1a697901'", src)


if __name__ == '__main__':
    unittest.main()
