function Comment({ comment, like }) {
  return (
    <div className="mt-3">
      <p className="text-sm">
        <span className="font-semibold">
          {comment.author.username}
        </span>
        : {comment.content}
      </p>

      <button
        onClick={() => like("comment", comment.id)}
        className="text-xs text-blue-500 hover:underline"
      >
        Like · {comment.like_count}
      </button>


      <div className="pl-4 border-l mt-2">
        {comment.replies.map((reply) => (
          <Comment
            key={reply.id}
            comment={reply}
            like={like}
          />
        ))}
      </div>
    </div>
  );
}

export default Comment;
