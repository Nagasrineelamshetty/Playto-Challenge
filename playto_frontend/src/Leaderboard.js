import { useEffect, useState } from "react";

const API_BASE = process.env.API_BASE_URL;

function Leaderboard() {
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/leaderboard/`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        setLeaders(data);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h2 className="text-xl font-bold mb-4 text-center">
        Leaderboard (Last 24h)
      </h2>

      {loading && (
        <p className="text-center text-gray-500">
          Loading leaderboard...
        </p>
      )}

      {!loading && leaders.length === 0 && (
        <p className="text-center text-gray-500">
          No karma activity in the last 24 hours.
        </p>
      )}

      {!loading && leaders.length > 0 && (
        <ol className="list-decimal pl-6 space-y-2">
          {leaders.map((user) => (
            <li key={user.user_id}>
              <span className="font-semibold">
                {user.username}
              </span>{" "}
              — {user.karma} points
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}

export default Leaderboard;
