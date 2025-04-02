import { Link } from "react-router-dom";
import './Header.css';
import genericIcon from '../assets/thumbnail.png';
import logoutIcon from '../assets/logout.png';

const handleLogout = () => {
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('refresh_token');
    console.log('User logged out');
    // Optionally, redirect to the login page
    window.location.href = '/login';
};

const isLoggedIn = !!sessionStorage.getItem('access_token');
const isAdmin = JSON.parse(sessionStorage.getItem("is_staff") || "false");


const Header = () => {
    return (
      <nav className="sidebar">
        <ul className="nav-list">
          <li className="nav-item">
            <Link to="/" className="nav-link">
              <img src={genericIcon} alt="Home" className="nav-icon" style={{ cursor: 'pointer', width: '48px', height: '48px' }}/>
              
              Home
            </Link>
          </li>
          <li className="nav-item">
          <Link to={isLoggedIn ? "/profile" : "/login"} className="nav-link">
            <img src={genericIcon} alt="Profile" className="nav-icon" style={{ cursor: 'pointer', width: '48px', height: '48px' }} />
            <br />
            Profil
          </Link>
          </li>
          {isLoggedIn && isAdmin && (
          <li className="nav-item">
            <Link to="/users" className="nav-link">
              Manage Users
            </Link>
          </li>
        )}
          <li>
          <img
          src={logoutIcon}
          alt="Logout"
          onClick={handleLogout}
          style={{ cursor: 'pointer', width: '48px', height: '48px' }} // Stylizacja ikony
            />
          </li>
        </ul>
      </nav>
    );
  };
  
  export default Header;