import { FaGithub } from "react-icons/fa";

function Navbar() {
  return (
    <div className="navbar">
      <div className="nav-left">Customer Churn AI Platform</div>
      <div className="nav-right">
        <a
          href="https://github.com/Mujjjtaba/customer-churn-ai-system"
          target="_blank"
        >
          <FaGithub size={22} />
        </a>
      </div>
    </div>
  );
}

export default Navbar;