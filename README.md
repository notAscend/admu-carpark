# Ateneo Parking System

A web-based parking management system for Ateneo de Manila University. This application helps students manage their vehicle registrations and track their active parking sessions on campus.

## ✨ Features

* **User Authentication:** Secure user registration and login with Ateneo Student ID and email validation.
* **Parking Zone Management:** Admins can define and manage various parking zones on campus.
* **Live Parking Sessions:** Users can start and end parking sessions in a designated zone.
* **Real-time Duration Tracker:** A live counter on the user's dashboard shows how long they have been parked.

## 🛠️ Technologies Used

* **Backend:** Python, Django
* **Database:** SQLite (default)
* **Frontend:** HTML5, Bootstrap 5, Vanilla JavaScript
* **Development:** Git, GitHub

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites

* Python 3.8+
* pip

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/NotAscend/admu-carpark.git
    cd your-repo-name
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install Django
    ```
    (Note: It's recommended to create a `requirements.txt` file and install from there.)

4.  **Run database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create an admin user:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

The application will now be running on `http://127.0.0.1:8000/`.

## 📌 Usage

* Navigate to the login/registration page to create an account using your Ateneo Student ID and email.
* Once logged in, go to the "My Account" page to register a car pass.
* If you have an active parking session, the page will show your current parking details and a live timer.
* You can use the "Enter Parking System" button to start a new session or the "Exit Parking" button to end it.
