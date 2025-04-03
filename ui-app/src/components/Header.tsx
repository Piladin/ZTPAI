import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import './Header.css';
import genericIcon from '../assets/thumbnail.png';
import logoutIcon from '../assets/logout.png';

const Header = () => {
    const [isAdmin, setIsAdmin] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const fetchUser = async () => {
        const token = sessionStorage.getItem("access_token");
        if (!token) {
            setIsLoggedIn(false);
            setIsAdmin(false);
            return;
        }

        try {
            const response = await axios.get("http://localhost:8000/api/user/me/", {
                headers: { Authorization: `Bearer ${token}` },
            });
            setIsLoggedIn(true);
            setIsAdmin(response.data.is_staff); // Set isAdmin based on the API response
        } catch (error) {
            console.error("Error fetching user data:", error);
            setIsLoggedIn(false);
            setIsAdmin(false);
        }
    };

    const handleLogout = () => {
        sessionStorage.removeItem("access_token");
        sessionStorage.removeItem("refresh_token");
        setIsLoggedIn(false);
        setIsAdmin(false);
        console.log("User logged out");
        window.location.href = "/login"; // Redirect to login page
    };

    useEffect(() => {
        fetchUser();
    }, []);

    return (
        <nav className="sidebar">
            <ul className="nav-list">
                <li className="nav-item">
                    <Link to="/" className="nav-link">
                        <img src={genericIcon} alt="Home" className="nav-icon" style={{ cursor: 'pointer', width: '48px', height: '48px' }} />
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
                          <img src={genericIcon} alt="Mngusers" className="nav-icon" style={{ cursor: 'pointer', width: '48px', height: '48px' }} />
                          <br />
                            Manage Users
                        </Link>
                    </li>
                )}
                {isLoggedIn && (
                    <li>
                        <img
                            src={logoutIcon}
                            alt="Logout"
                            onClick={handleLogout}
                            style={{ cursor: 'pointer', width: '48px', height: '48px' }}
                        />
                    </li>
                )}
            </ul>
        </nav>
    );
};

export default Header;