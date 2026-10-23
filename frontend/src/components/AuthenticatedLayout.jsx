import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

function AuthenticatedLayout({ onLogout }) {
  return (
    <div className="authenticated-layout">
      <Navbar onLogout={onLogout} />

      <main className="authenticated-content">
        <Outlet />
      </main>
    </div>
  );
}

export default AuthenticatedLayout;