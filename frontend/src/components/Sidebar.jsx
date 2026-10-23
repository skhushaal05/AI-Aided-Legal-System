import { Link } from "react-router-dom";

import vritonaLogo from "../assets/vritona-logo.jpeg";

function Sidebar({ isOpen, onClose, onLogout }) {
  return (
    <>
      {/* =====================================================
          OVERLAY
          ===================================================== */}

      <div
        className={`sidebar-overlay ${
          isOpen ? "sidebar-overlay-open" : ""
        }`}
        onClick={onClose}
        aria-hidden={!isOpen}
      />


      {/* =====================================================
          SIDEBAR
          ===================================================== */}

      <aside
        className={`sidebar ${
          isOpen ? "sidebar-open" : ""
        }`}
        aria-hidden={!isOpen}
      >

        {/* =================================================
            SIDEBAR HEADER
            ================================================= */}

        <div className="sidebar-header">

          <span>
            MENU
          </span>

          <button
            className="sidebar-close"
            onClick={onClose}
            aria-label="Close navigation"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            >
              <path d="M5 5l14 14" />
              <path d="M19 5L5 19" />
            </svg>
          </button>

        </div>


        {/* =================================================
            NAVIGATION
            ================================================= */}

        <nav className="sidebar-navigation">

          {/* LAW CHATBOT */}

          <Link
            to="/law-chatbot"
            onClick={onClose}
          >
            <span>
              01
            </span>

            <div>
              <strong>
                Law Chatbot
              </strong>

              <small>
                Ask about POSH law
              </small>
            </div>
          </Link>


          {/* COMPLAINTS */}

          <Link
            to="/complaints"
            onClick={onClose}
          >
            <span>
              02
            </span>

            <div>
              <strong>
                Complaints
              </strong>

              <small>
                Submit a complaint
              </small>
            </div>
          </Link>


          {/* STATUS */}

          <Link
            to="/status"
            onClick={onClose}
          >
            <span>
              03
            </span>

            <div>
              <strong>
                Status
              </strong>

              <small>
                Track your complaint
              </small>
            </div>
          </Link>


          {/* LOGOUT */}

          <button
            className="sidebar-logout"
            onClick={onLogout}
          >
            <span>
              04
            </span>

            <div>
              <strong>
                Logout
              </strong>

              <small>
                Sign out of your account
              </small>
            </div>
          </button>

        </nav>


        {/* =================================================
            SIDEBAR FOOTER
            ================================================= */}

        <div className="sidebar-bottom">

          <img
            src={vritonaLogo}
            alt="Vritona"
            className="sidebar-vritona-logo"
          />

          <small>
            Workplace safety & awareness
          </small>

        </div>

      </aside>
    </>
  );
}

export default Sidebar;