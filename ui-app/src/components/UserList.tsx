import { useEffect, useState } from "react";
import axios from "axios";
import "./UserList.css";

interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone_number?: string;
  is_staff: boolean;
}

const UserList = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchUsers = async () => {
    const token = sessionStorage.getItem("access_token");
    if (!token) {
      setError("Unauthorized access. Please log in.");
      return;
    }

    try {
      const response = await axios.get("http://localhost:8000/api/users/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(response.data);
    } catch (err) {
      setError("Failed to fetch users. You might not have permission.");
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return;

    const token = sessionStorage.getItem("access_token");
    if (!token) {
      setError("Unauthorized access. Please log in.");
      return;
    }

    try {
      await axios.delete(`http://localhost:8000/api/users/delete/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(users.filter((user) => user.id !== id));
      alert("User deleted successfully.");
    } catch (err) {
      setError("Failed to delete user. You might not have permission.");
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  if (error) return <p className="error-message">{error}</p>;

  return (
    <div className="user-list-container">
      <h1>User List</h1>
      <div className="user-list">
        {users.map((user) => (
          <div key={user.id} className="user-card">
            <div className="user-info">
              <p>
                <strong>Name:</strong> {user.first_name} {user.last_name}
              </p>
              <p>
                <strong>Email:</strong> {user.email}
              </p>
              {user.phone_number && (
                <p>
                  <strong>Phone:</strong> {user.phone_number}
                </p>
              )}
              <p>
                <strong>Role:</strong> {user.is_staff ? "Admin" : "User"}
              </p>
            </div>
            {user.is_staff ? null : (
              <button
                className="delete-button"
                onClick={() => handleDelete(user.id)}
              >
                Delete User
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default UserList;