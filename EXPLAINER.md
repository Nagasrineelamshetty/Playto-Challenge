
# EXPLAINER.md

This document explains the key technical decisions behind the **Playto Community Feed** prototype, with a focus on correctness, performance, and data integrity.

---

## 1. The Tree — Nested Comments Design

### Database Modeling

Nested comments are modeled using a **self-referential foreign key** on the `Comment` model.

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
````

* A top-level comment has `parent = NULL`
* A reply references another `Comment` via `parent`
* This supports **arbitrary depth** (Reddit-style threading)
* No recursive schemas or closure tables are used

This adjacency-list approach keeps writes simple and supports deep nesting.

---

### Avoiding the N+1 Query Problem

To avoid N+1 queries when loading deeply nested comment trees:

1. **All comments are fetched in a single query**
2. The hierarchy is constructed **in memory**, not via recursive database calls

```python
posts = Post.objects.select_related("author").annotate(...)
comments = Comment.objects.select_related("author").annotate(...)

```

This ensures a constant number of database queries regardless of comment depth.

---

### Tree Construction (In Memory)

```python
def build_comment_tree(comments):
    comment_map = {}
    roots = []

    for comment in comments:
        comment.replies_list = []
        comment_map[comment.id] = comment

    for comment in comments:
        if comment.parent_id:
            parent = comment_map.get(comment.parent_id)
            if parent:
                parent.replies_list.append(comment)
        else:
            roots.append(comment)

    return roots
```

* Runs in **O(n)** time
* Avoids recursive database access
* Scales cleanly for large and deeply nested threads

---

### Serialization

Once the tree is built, it is serialized:

```python
def serialize_tree(self, comments):
        data = []
        for comment in comments:
            serialized = CommentSerializer(comment).data
            serialized["replies"] = self.serialize_tree(comment.replies_list)
            data.append(serialized)
        return data
```

Database access is completed **before** serialization, keeping performance predictable.

---

## 2. The Math — Last 24h Leaderboard Query

### Design Constraints

The leaderboard must:

* Rank users by karma earned in the **last 24 hours only**
* Calculate karma **dynamically**, not store it
* Avoid denormalized or cached karma fields
* Remain correct under concurrent likes

To satisfy these constraints, karma is derived at query time from immutable `Like` records.

---

### Scoring Rules

* Like on a **Post** → +5 karma (awarded to the post author)
* Like on a **Comment** → +1 karma (awarded to the comment author)

---

### Aggregation Strategy

Each `Like` row represents a single immutable event.
At query time, conditional aggregation is used to:

1. Filter likes to the last 24 hours
2. Assign weights based on whether the like targets a post or a comment
3. Attribute karma to the correct content author
4. Aggregate totals per user

---

### Query Used

```python
leaderboard = (
    Like.objects
    .filter(created_at__gte=since)
    .annotate(
        points=Case(
            When(post__isnull=False, then=5),
            When(comment__isnull=False, then=1),
            output_field=IntegerField(),
        ),
        karma_user=Case(
            When(post__isnull=False, then=F("post__author")),
            When(comment__isnull=False, then=F("comment__author")),
        )
    )
    .values("karma_user")
    .annotate(total_karma=Sum("points"))
    .order_by("-total_karma")[:5]
)

```

---

### Why This Works

* Karma is **fully derived** from activity history
* No duplicated or materialized state
* Scoring rules can change without migrations
* Aggregation runs in a **single database query**
* Correct under concurrency due to immutable likes and DB constraints

---

## 3. The AI Audit — Buggy / Inefficient AI Code & Fix

### Removing a Derived-State Anti-Pattern

An AI-generated suggestion introduced a `KarmaEvent` model to record points when likes occurred.

While this simplified leaderboard queries, it violated a core system constraint:
**karma must be derived dynamically from user activity rather than stored**.

This approach also duplicated state already represented by the `Like` model, creating a second source of truth and increasing the risk of inconsistency if scoring rules changed.

I removed the `KarmaEvent` model entirely and implemented the leaderboard using conditional aggregation on the `Like` table, applying point weights at query time and filtering to the last 24 hours. This ensured a single source of truth, improved correctness, and aligned with production-grade data modeling principles.




