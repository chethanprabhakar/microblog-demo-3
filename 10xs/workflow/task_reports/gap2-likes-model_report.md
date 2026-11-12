# gap2-likes-model report

- [x] T1. Post.likes relationship — WriteOnlyMapped via `post_likes` secondary
- [x] T2. User.liked_posts relationship — same secondary table
- [x] T3. Post.like/unlike, User.like_post/unlike_post — no commits, guarded
- [x] T4. is_liked_by, like_count, has_liked_post
- [x] T5. Migration `migrations/versions/5b1c2d3e4f60_post_likes.py`, down_revision `834b1a697901` (single head; no comments migration present)

Scope extension: the migration file and tests/test_post_likes.py are outside app/models.py (required by criteria).

Mutation: removing the is_liked_by guard in Post.like made `test_c6_c7_post_like_unlike` error (IntegrityError); code restored, tests pass.

Note: tests live in tests/test_post_likes.py; run with `PYTHONPATH=. /tmp/mbvenv/bin/python tests/test_post_likes.py` (tests.py shadows a `tests` package). `tests.UserModelCase` still passes.

## Criteria
- C1: tests/test_post_likes.py
- C2: tests/test_post_likes.py
- C3: tests/test_post_likes.py
- C4: tests/test_post_likes.py
- C5: tests/test_post_likes.py
- C6: tests/test_post_likes.py
- C7: tests/test_post_likes.py
- C8: tests/test_post_likes.py
- C9: tests/test_post_likes.py
- C10: tests/test_post_likes.py
- C11: tests/test_post_likes.py
- C12: tests/test_post_likes.py
- C13: tests/test_post_likes.py
- C14: tests/test_post_likes.py
- C15: tests/test_post_likes.py
