# 🚗 BluePark - ADMU Parking System
A web-based parking management system designed for Ateneo de Manila University. This application provides a streamlined way for students to register their vehicles and manage their parking sessions across campus.

## ✨ Features
* **Secure User Authentication:** Students can register and log in using their Ateneo Student ID, with a secure, email-validated authentication process.
* **Real-Time Parking Management** Start and end parking sessions from a user-friendly dashboard that provides live updates on your current session.
* **Live Parking Sessions:** A dynamic counter shows exactly how long your vehicle has been parked, giving you real-time visibility.
* **Vehicle Registration:** A simple, intuitive form lets users register their vehicles and generate a unique car pass number.

## 🛠️ Technologies 
* **Backend:** Python, Django
* * **Frontend:** HTML5, Bootstrap 5, Vanilla JavaScript
* **Database:** SQLite 
* **Development:** Git, GitHub

## 🚀 Getting Started
Follow these simple steps to get the project running on your local machine.

### Prerequisites
* Python 3.8+
* pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/NotAscend/admu-carpark.git
    cd admu-carpark
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the database:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py loaddata parking_zones.json
    ```
    
5.  **Create an admin user:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will now be live at `http://127.0.0.1:8000/`.

## 📌 How to Use

* **Register:** Navigate to the registration page and sign up using your Ateneo Student ID and email.
* **Register a Vehicle:** Log in and go to "My Account" to register your car. This generates a unique car pass number you can use for parking.
* **Start a Session:** Click "Enter Parking System," choose an available parking zone, and begin your session. The dashboard will show a live timer for your parking duration.
* **End a Session:** When you're ready to leave, simply use the "Exit Parking" button on your dashboard to end your session.
