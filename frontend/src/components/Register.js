import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [username, setUsername] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [age, setAge] = useState('');
  const [otp, setOtp] = useState('');
  const [message, setMessage] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes in seconds
  const [timerId, setTimerId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (otpSent && timeLeft > 0) {
      const id = setTimeout(() => {
        setTimeLeft(timeLeft - 1);
      }, 1000);
      setTimerId(id);
      return () => clearTimeout(id);
    } else if (timeLeft === 0 && timerId) {
      setMessage('OTP expired.');
      setOtpSent(false);
      setOtp(''); // Clear OTP when expired
      clearTimeout(timerId);
      setTimerId(null);
    }
  }, [otpSent, timeLeft]);

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/register', {
        username,
        phone_number: phoneNumber,
        age,
        otp_code: otp,
      });
      setMessage(response.data.data.message);
      console.log(response.data.data.token)
      if (response.data.data.token) {
        console.log("Token Set ! ")
        localStorage.setItem('token', response.data.data.token);
        navigate('/'); // Redirect to home page
      }
      else{
        setMessage("Registration unsuccessful");
      }
    } catch (error) {
      setMessage(error.response.data.data.message || 'Registration failed.');
    }
  };

  const handleSendOtp = async () => {
    try {
      const response = await axios.post('http://localhost:5000/send_otp', {
        phone_number: phoneNumber,
      });
      setMessage('OTP sent. It will expire in 5 minutes.');
      setOtpSent(true);
      setTimeLeft(300); // Reset timer to 5 minutes
    } catch (error) {
      console.log(error.response)
      setMessage(error.response.data.data.message || 'Failed to send OTP.');
    }
  };

  return (
    <div className="form-container">
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Phone Number:</label>
          <input
            type="text"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            required
          />
        </div>
        <button type="button" onClick={handleSendOtp} disabled={otpSent && timeLeft > 0}>Send OTP</button>
        {otpSent && timeLeft > 0 && (
          <p>Time left: {Math.floor(timeLeft / 60)}:{('0' + (timeLeft % 60)).slice(-2)}</p>
        )}
        <div>
          <label>Age:</label>
          <input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            required
          />
        </div>
        <div>
          <label>OTP Code:</label>
          <input
            type="number"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            required
            maxLength="6"
          />
        </div>
        {message && <p>{message}</p>}
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register; 