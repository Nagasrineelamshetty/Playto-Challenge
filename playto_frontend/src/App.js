import { useState } from "react";
import Feed from "./Feed";
import Leaderboard from "./Leaderboard";

function App() {
  const [activeTab, setActiveTab] = useState("feed");

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Playto Community
      </h1>

      {/* Tabs */}
      <div className="flex justify-center mb-6 space-x-4">
        <button
          onClick={() => setActiveTab("feed")}
          className={`px-4 py-2 rounded ${
            activeTab === "feed"
              ? "bg-blue-600 text-white"
              : "bg-gray-200"
          }`}
        >
          Feed
        </button>

        <button
          onClick={() => setActiveTab("leaderboard")}
          className={`px-4 py-2 rounded ${
            activeTab === "leaderboard"
              ? "bg-blue-600 text-white"
              : "bg-gray-200"
          }`}
        >
          Leaderboard
        </button>
      </div>

      {/* Content */}
      {activeTab === "feed" ? <Feed /> : <Leaderboard />}
    </div>
  );
}

export default App;
