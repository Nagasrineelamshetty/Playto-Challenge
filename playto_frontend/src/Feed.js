import { useEffect, useState } from "react";
import Comment from "./Comment";

const API_BASE = import.meta.env.VITE_API_BASE_URL;

function Feed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/posts/`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => setPosts(data));
  }, []);

  const like = async (type, id) => {
    await fetch(`${API_BASE}/api/like/`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content_type: type,
        object_id: id,
      }),
    });
  };

  return (
    <div className="space-y-6">
      {posts.map((post) => (
        <div
          key={post.id}
          className="border rounded-lg p-4 shadow-sm"
        >
          <p className="font-semibold">
            {post.author.username}
          </p>
          <p className="mb-2">{post.content}</p>

          <button
            onClick={() => like("post", post.id)}
            className="text-sm text-blue-600 hover:underline"
          >
            Like Post · {post.like_count}
          </button>


          <div className="mt-4 pl-4 border-l">
            {post.comments.map((comment) => (
              <Comment
                key={comment.id}
                comment={comment}
                like={like}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Feed;
