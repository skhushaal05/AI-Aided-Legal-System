import { useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import "./App.css";

import Landing from "./pages/Landing";
import Home from "./pages/Home";
import About from "./pages/About";
import Products from "./pages/Products";
import LawChatbot from "./pages/LawChatbot";
import Complaints from "./pages/Complaints";
import Status from "./pages/Status";

import AuthenticatedLayout from "./components/AuthenticatedLayout";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  function handleLogin() {
    setLoggedIn(true);
  }

  function handleLogout() {
    setLoggedIn(false);
  }

  if (!loggedIn) {
    return <Landing onLogin={handleLogin} />;
  }

  return (
    <BrowserRouter>
      <Routes>

        <Route
          element={
            <AuthenticatedLayout
              onLogout={handleLogout}
            />
          }
        >

          {/* Main Pages */}

          <Route
            path="/"
            element={<Home />}
          />

          <Route
            path="/about"
            element={<About />}
          />

          <Route
            path="/products"
            element={<Products />}
          />

          {/* Sidebar Pages */}

          <Route
            path="/law-chatbot"
            element={<LawChatbot />}
          />

          <Route
            path="/complaints"
            element={<Complaints />}
          />

          <Route
            path="/status"
            element={<Status />}
          />

        </Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;