import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Announcements.css';
import avatar from '../assets/avatar.png';

const Announcements = () => {
    interface Announcement {
        id: number;
        subject: string;
        content: string;
        date_added: string;
        hourly_rate: number;
        author: {
            id: number;
            first_name: string;
            last_name: string;
            email: string;
            phone_number?: string;
        };
    }
    const subjects = ["Matematyka", "Fizyka", "Chemia", "Informatyka", "Biologia", "Język angielski"];
    const [announcements, setAnnouncements] = useState<Announcement[]>([]);
    const [next, setNext] = useState<string | null>(null);
    const [previous, setPrevious] = useState<string | null>(null);
    const [count, setCount] = useState<number>(0);
    const [page, setPage] = useState<number>(1);
    const [searchSubject, setSearchSubject] = useState('');
    const [searchMinRate, setSearchMinRate] = useState('');
    const [searchMaxRate, setSearchMaxRate] = useState('');
    const [isSearching, setIsSearching] = useState(false);
    interface User {
        id: number;
        first_name: string;
        last_name: string;
        email: string;
        phone_number?: string;
        is_staff: boolean;
    }

    const [user, setUser] = useState<User | null>(null);
    const navigate = useNavigate();

    const fetchAnnouncements = async (page = 1) => {
        try {
            const response = await axios.get(`http://localhost:8000/api/announcements/?page=${page}`);
            setAnnouncements(Array.isArray(response.data.results) ? response.data.results : []);
            setNext(response.data.next);
            setPrevious(response.data.previous);
            setCount(response.data.count);
            setPage(page);
        } catch (error) {
            console.error('Błąd pobierania ogłoszeń:', error);
        }
    };

    const fetchUser = async () => {
        const token = sessionStorage.getItem('access_token');
        if (!token) {
            return;
        }
        try {
            const response = await axios.get('http://localhost:8000/api/user/me/', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUser(response.data);
        } catch {
            setUser(null);
        }
    };

    const handleDelete = async (id: number) => {
        if (!window.confirm("Czy na pewno chcesz usunąć to ogłoszenie?")) return;
        const token = sessionStorage.getItem('access_token');
        if (!token) {
            return;
        }
        try {
            await axios.delete(`http://localhost:8000/api/announcements/delete/${id}/`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setAnnouncements(announcements.filter(a => a.id !== id));
        } catch (error) {
            console.error('Błąd podczas usuwania ogłoszenia:', error);
        }
    };

    const searchAnnouncements = async () => {
    try {
        const params: any = {};
        if (searchSubject) params.subject = searchSubject;
        if (searchMinRate) params.min_rate = searchMinRate;
        if (searchMaxRate) params.max_rate = searchMaxRate;

        const response = await axios.get('http://localhost:8000/api/announcements/search/', { params });
        setAnnouncements(Array.isArray(response.data) ? response.data : []);
        setNext(null);
        setPrevious(null);
        setCount(response.data.length || 0);
        setPage(1);
        setIsSearching(true);
    } catch (error) {
        console.error('Błąd wyszukiwania ogłoszeń:', error);
    }
    };

    const resetSearch = () => {
    setSearchSubject('');
    setSearchMinRate('');
    setSearchMaxRate('');
    setIsSearching(false);
    fetchAnnouncements(1);
    };

useEffect(() => {
    if (!isSearching) {
        fetchAnnouncements(page);
    }
    fetchUser();
    }, [page, isSearching]);

    return (
        <div className="announcements-container">
            <button className="add-button" onClick={() => navigate(user ? "/add" : "/login")}>
                Add Announcement
            </button>
            <div className="announcements-grid">
                {Array.isArray(announcements) && announcements.map(announcement => (
                    <div key={announcement.id} className="announcement-card">
                        <div className="left-section">
                            <h3 className="subject">{announcement.subject}</h3>
                            <textarea className="content" readOnly value={announcement.content} />
                            <div className="bottom-info">
                                <span className="date">{announcement.date_added}</span>
                                <span className="price">{announcement.hourly_rate} zł/h</span>
                            </div>
                        </div>
                        <div className="right-section">
                            <img className="avatar" src={avatar} alt="User Avatar" />
                            <p className="author-name">{announcement.author.first_name} {announcement.author.last_name}</p>
                            <p className="email">{announcement.author.email}</p>
                            {announcement.author.phone_number && <p className="phone">{announcement.author.phone_number}</p>}

                            {(user && (user.id === announcement.author.id || user.is_staff)) && (
                                <div className="admin-actions">
                                    <button className="edit-button" onClick={() => navigate(`/edit/${announcement.id}`)}>✏️</button>
                                    <br></br>
                                    <button className="delete-button" onClick={() => handleDelete(announcement.id)}>🗑️</button>
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>
            <div className="pagination">
                <span>Total: {count}</span>
                <button disabled={!previous} onClick={() => fetchAnnouncements(page - 1)}>Previous</button>
                <span>Page {page}</span>
                <button disabled={!next} onClick={() => fetchAnnouncements(page + 1)}>Next</button>
            </div>
            <div className="search-bar">
                <select
                    value={searchSubject}
                    onChange={e => setSearchSubject(e.target.value)}
                >
                    <option value="">Wszystkie przedmioty</option>
                    {subjects.map(subj => (
                        <option key={subj} value={subj}>{subj}</option>
                    ))}
                </select>
                <input
                    type="number"
                    placeholder="Min rate"
                    value={searchMinRate}
                    onChange={e => setSearchMinRate(e.target.value)}
                />
                <input
                    type="number"
                    placeholder="Max rate"
                    value={searchMaxRate}
                    onChange={e => setSearchMaxRate(e.target.value)}
                />
                <button onClick={searchAnnouncements}>Search</button>
                <button onClick={resetSearch}>Reset</button>
            </div>
        </div>
    );
};

export default Announcements;
