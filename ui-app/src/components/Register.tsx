import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Register.css';

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [firstName, setFistName] = useState('');
    const [lastName, setLastName] = useState('');
    const [phone, setPhone] = useState('');
    const [privacyAccepted, setPrivacyAccepted] = useState(false);
    const navigate = useNavigate();

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        if (password !== confirmPassword) {
            alert("Passwords do not match");
            return;
        }
        try {
            const response = await axios.post('http://localhost:8000/api/register/', {
                username: username,
                email: email,
                password: password,
                first_name: firstName,
                last_name: lastName,
                phone_number: phone
            });
            console.log('Registration response:', response.data);
            alert('Registration successful!');
            navigate('/login');
        } catch (error) {
            console.error('Registration error:', error);
        }
    };

    return (
        <div className="form-container">
            <h1 className="form-header">Register</h1>
            <form onSubmit={handleRegister}>
                <div className="form-group">
                    <label className="form-label">Login</label>
                    <input
                        type="text"
                        className="form-input"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Email</label>
                    <input
                        type="email"
                        className="form-input"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Password</label>
                    <input
                        type="password"
                        className="form-input"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Repeat Password</label>
                    <input
                        type="password"
                        className="form-input"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">First Name</label>
                    <input
                        type="text"
                        className="form-input"
                        value={firstName}
                        onChange={(e) => setFistName(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Last Name</label>
                    <input
                        type="text"
                        className="form-input"
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Phone number</label>
                    <input
                        type="tel"
                        pattern="[0-9]{9}"
                        className="form-input"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <input
                        type="checkbox"
                        id="privacyPolicy"
                        checked={privacyAccepted}
                        onChange={(e) => setPrivacyAccepted(e.target.checked)}
                    />
                    <label htmlFor="privacyPolicy">Accept privacy</label>
                </div>

                <button type="submit" className="submit-button">
                    Register
                </button>
            </form>
        </div>
    );
};

export default Register;
