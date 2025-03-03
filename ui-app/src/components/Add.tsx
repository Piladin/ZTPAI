import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Add.css';

const subjects = ["Matematyka", "Fizyka", "Chemia", "Informatyka", "Biologia", "Język angielski"];

const Add = () => {
    const [subject, setSubject] = useState(subjects[0]);
    const [content, setContent] = useState('');
    const [price, setPrice] = useState('');
    const [termsAccepted, setTermsAccepted] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const token = sessionStorage.getItem('access_token');
        if (!token) {
            alert('You must be logged in to add an announcement.');
            navigate('/login');
            return;
        }

        try {
            const response = await axios.post('http://localhost:8000/api/announcements/add/', {
                subject,
                content,
                hourly_rate: price,
            }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            console.log('Listing added:', response.data);
            alert('Ogłoszenie dodane!');
            navigate('/announcements');
        } catch (error) {
            console.error('Error adding listing:', error);
            alert('Error adding listing. Please try again.');
        }
    };

    return (
        <div className="form-container">
            <h1 className="form-header">Dodawanie ogłoszenia</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label className="form-label">Przedmiot</label>
                    <select
                        className="form-input"
                        value={subject}
                        onChange={(e) => setSubject(e.target.value)}
                    >
                        {subjects.map((subj) => (
                            <option key={subj} value={subj}>
                                {subj}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label className="form-label">Opis</label>
                    <textarea
                        className="form-input"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Stawka za zajęcia</label>
                    <input
                        type="number"
                        className="form-input"
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <input
                        type="checkbox"
                        id="terms"
                        checked={termsAccepted}
                        onChange={(e) => setTermsAccepted(e.target.checked)}
                    />
                    <label htmlFor="terms">I accept the terms</label>
                    <a href="/terms" className="terms-link">Read our T&Cs</a>
                </div>

                <button type="submit" className="submit-button" disabled={!termsAccepted}>
                    Dodaj ogłoszenie
                </button>
            </form>
        </div>
    );
};

export default Add;
