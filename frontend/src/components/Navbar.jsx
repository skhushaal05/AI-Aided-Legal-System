import { useState } from "react";
import { Link } from "react-router-dom";

import Sidebar from "./Sidebar";
import vritonaLogo from "../assets/vritona-logo.jpeg";

function Navbar({ onLogout }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  function openSidebar() {
    setSidebarOpen(true);
  }

  function closeSidebar() {
    setSidebarOpen(false);
  }

  return (
    <>
      <header className="home-navbar">

        <div className="home-navbar-left">

          <button
            className="menu-button"
            onClick={openSidebar}
            aria-label="Open navigation menu"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.6"
              strokeLinecap="round"
            >
              <path d="M3 6h18" />
              <path d="M3 12h18" />
              <path d="M3 18h18" />
            </svg>
          </button>

          <Link to="/" className="home-logo">
            <img
              src={vritonaLogo}
              alt="Vritona"
              className="vritona-logo"
            />
          </Link>

        </div>

        <nav className="home-nav-links">

          <Link to="/about">
            About
          </Link>

          <Link to="/products">
            Products
          </Link>

          <button
            className="home-account"
            aria-label="Account"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.6"
            >
              <circle cx="12" cy="8" r="3" />
              <path d="M5.5 20c.7-3.3 3-5 6.5-5s5.8 1.7 6.5 5" />
            </svg>
          </button>

        </nav>

      </header>

      <Sidebar
        isOpen={sidebarOpen}
        onClose={closeSidebar}
        onLogout={onLogout}
      />
    </>
  );
}

export default Navbar;