import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import './Add.css';

const EditAnnouncement = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        subject: "",
        content: "",
        hourly_rate: "",
    });

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const fetchAnnouncement = async () => {
        try {
            const token = sessionStorage.getItem("access_token");
            if (!token) {
                navigate("/login");
                return;
            }

            const response = await axios.get(`http://localhost:8000/api/announcements/${id}/`, {
                headers: { Authorization: `Bearer ${token}` }
            });

            setFormData({
                subject: response.data.subject,
                content: response.data.content,
                hourly_rate: response.data.hourly_rate.toString(),
            });
            setIsLoading(false);
        } catch (err) {
            setError("Błąd podczas pobierania danych ogłoszenia.");
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchAnnouncement();
    }, [id]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            const token = sessionStorage.getItem("access_token");
            if (!token) {
                navigate("/login");
                return;
            }

            await axios.put(`http://localhost:8000/api/announcements/edit/${id}/`, formData, {
                headers: { Authorization: `Bearer ${token}` }
            });

            navigate("/");
        } catch (err) {
            setError("Błąd podczas edytowania ogłoszenia.");
        } finally {
            setIsSubmitting(false);
        }
    };

    if (isLoading) return <p>Ładowanie...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="form-container">
            <h2 className="form-header">Edytuj Ogłoszenie</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label className="form-label">Przedmiot</label>
                    <input
                        type="text"
                        name="subject"
                        className="form-input"
                        value={formData.subject}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Opis</label>
                    <textarea
                        name="content"
                        className="form-input"
                        value={formData.content}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label className="form-label">Stawka za zajęcia (zł/h)</label>
                    <input
                        type="number"
                        name="hourly_rate"
                        className="form-input"
                        value={formData.hourly_rate}
                        onChange={handleChange}
                        required
                    />
                </div>

                {error && <p style={{ color: "red" }}>{error}</p>}

                <button type="submit" className="submit-button" disabled={isSubmitting}>
                    {isSubmitting ? "Zapisywanie..." : "Zapisz zmiany"}
                </button>
            </form>
        </div>
    );
};

export default EditAnnouncement;
