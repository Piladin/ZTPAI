import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Header from "./components/Header";
import Login from "./components/Login";
import Register from "./components/Register";
import Profile from "./components/Profile";
import Add from "./components/Add";
import Announcements from "./components/Announcements";
import EditAnnouncement from "./components/EditAnnouncement";

const App = () => {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Header />
        <Routes>
          <Route path="" element={<Navigate to="/announcements" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/add" element={<Add />} />
          <Route path="/announcements" element={<Announcements />} />
          <Route path="/edit/:id" element={<EditAnnouncement />} /> {/* Nowa trasa */}
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;