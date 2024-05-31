# OWASP Demo

This is a Django-based web application that is designed to be deliberately vulnerable to introduce some of the top ten vulnerabilities from the OWASP Top Ten 2021 list. The purpose of this project is to demonstrate both vulnerabilities and their fixes within a controlled environment. It is part of Cyber Security Base 2024 course series by University of Helsinki.

The vulnerable version of the app is here in the `main` branch, and the secure version is on the branch `secure-version`. Please see them both for comparison. In the `main` branch, the specific vulnerabilities, and where they are on the backend code, have been commented so you can easily find where exactly the flaw is. The flaws you can find in this project are the following:

- A01:2021-Broken Access Control
- A02:2021-Cryptographic Failures
- A03:2021-Injection
- A05:2021-Security Misconfiguration
- A07:2021-Identification and Authentication Failures
- A09:2021-Security Logging and Monitoring Failures

## Installation Instructions

To get this project up and running on your local machine for development and testing purposes, follow these steps:

### Prerequisites

Make sure you have Python and Django installed. If you need to install these, please refer to the [official Python installation page](https://www.python.org/downloads/) and [Django installation guide](https://docs.djangoproject.com/en/stable/intro/install/).

### Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/AaroKoinsaari/django-owasp-demo.git
    cd django-owasp-demo
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Initialize the Database**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Run the Server**

    ```bash
    python manage.py runserver
    ```

    Visit `http://127.0.0.1:8000/` in your browser to view the application.

## Testing

To make sure the vulnerabilities are playing their part perfectly:

```bash
python manage.py test
```

## Application Usage

The application is just a simple user management system where you can create a profile, edit your personal information, and view other users' information if their profiles are public.

### Registration and Login

1. **Registration**: Navigate to the registration page and create a new user account by providing a username, password, email, and phone number. Note that in the vulnerable version, passwords are stored in plain text and weak passwords are permitted.

2. **Login**: Use the login page to authenticate with your username and password. Successful login redirects you to your profile page. In the vulnerable version, informative error messages reveal whether the username or password was incorrect.

### User Profile

After logging in, you can view and update your profile information, including email, phone number, bio, and the visibility of your profile (public/private).

### User Search

Use the search functionality to look up other users by username if they have set their profile public. In the vulnerable version, this feature is susceptible to SQL injection attacks.

### Viewing Other User Profiles

You can view the profile information of other users by clicking on their usernames in the search results. In the vulnerable version, there are no access control checks, allowing users to access any profile directly.

### Logging and Error Handling

The application has minimal logging for registration and login activities. In the vulnerable version, detailed stack traces are displayed to the user in case of errors.

## Contact Information

For any inquiries, please reach out to [aaro.koinsaari@proton.me](mailto:aaro.koinsaari@proton.me).
