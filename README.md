# Login-System Assignment

## Description
This is a login app, where users can login/ register using their Phone number by verifying WhatsApp OTP code.

## Instructions to Run

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd login-system/backend
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv env
    ```
3.  **Activate the virtual environment:**
    ```bash
    .\env\Scripts\activate
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Set environment variables:**
    Create a `.env` file in the `login-system/backend` directory and add the following (replace with your actual keys):
    ```
    SECRET_KEY='secret_key_here'
    TWILIO_ACCOUNT_SID='twilio_account_sid'
    TWILIO_AUTH_TOKEN='twilio_auth_token'
    TWILIO_WHATSAPP_NUMBER='twilio_whatsapp_number'
    ```
6.  **Set Flask App environment variable (Windows PowerShell):**
    ```bash
    $env:FLASK_APP='app.py'
    ```
    
7.  **Run the backend application:**
    ```bash
    flask run
    ```
    This will start the backend server at http://localhost:5000/.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd login-system/frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run the frontend application:**
    ```bash
    npm start
    ```
    This will start your React app at http://localhost:3000/.

