import React, { useState } from "react";
import Upload from "./components/Upload";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";

function App() {
  const [userId, setUserId] = useState(null);
  const [data, setData] = useState(null);

  if (!userId) {
    return <Login setUserId={setUserId} />;
  }

  if (!data) {
    return <Upload setData={setData} />;
  }

  return <Dashboard data={data} />;
}

export default App;