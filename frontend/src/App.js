import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css';

import Login from './components/Login';
import Register from './components/Register';

function Home({ setIsLoggedIn, setUsername, username }) {
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUsername = async () => {
      const token = localStorage.getItem('token');
      if (token == null) {
        setUsername("Please login or register to start");
        setIsLoggedIn(false);
        return;
      }

      try {
        const response = await axios.get('http://localhost:5000/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setUsername(response.data.data.username);
        setIsLoggedIn(true);
      } catch (error) {
        localStorage.removeItem('token');
        setUsername("Please login or register to start");
        setIsLoggedIn(false);
      }
    };
    fetchUsername();
  }, [navigate, setIsLoggedIn, setUsername]);

  return (
    <div className="home-container">
      <h2>Welcome, {username}!</h2>
    </div>
  );
}

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");

  const handleLogout = () => {
    console.log("Logout");
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    setUsername("Please login or register to start");
  };

  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            {!isLoggedIn && (
              <li>
                <Link to="/login">Login</Link>
              </li>
            )}
            {!isLoggedIn && (
              <li>
                <Link to="/register">Register</Link>
              </li>
            )}
            {isLoggedIn && (
              <li>
                <button onClick={handleLogout} className="nav-button">Logout</button>
              </li>
            )}
            <li>
              <Link to="/">Home</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Home setIsLoggedIn={setIsLoggedIn} setUsername={setUsername} username={username} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
