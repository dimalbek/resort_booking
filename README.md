# resort_booking

**Resort Booking** is a comprehensive booking management system for resorts, allowing administrators to manage guest records, room availability, and user accounts efficiently. It includes user authentication, stay record management, guest count tracking, and intuitive forms for adding, editing, and removing records.

---
## Project Overview

Resort Booking provides::

- **User Management:**: Register, login, and manage user accounts with approval workflows for admins.
- **Stay Record Management**: Add, edit, and delete stay records for guests with room numbers.
- **Room Management**: Track room availability and stay durations.
- **Guest Count**: View current and historical guest counts.
- **Responsive Design**: Modern UI for intuitive user interactions.
- **Role-Based Access**: Resorts and Admins with distinct permissions.


---

## Features

1. **User Management**  
   - Secure user authentication with hashed passwords.
   - Admin approval system for user registrations.

2. **Stay Record Management**  
   - Add, edit, and delete stay records.
   - Manage room numbers and guest counts.
   - Automatic time zone handling for accurate record keeping.

3. **Room Management**  
   - Track available rooms.
   - Manage room numbers and stay durations.

4. **Guest Count Tracking**  
   - View current and historical guest counts based on stay records. 

5. **Modern UI**  
   - Clean, responsive design for easy navigation.
   - Intuitive forms for managing stay records and user accounts.


---

## Technology Stack
- **FastAPI**: Backend framework for building RESTful APIs.
- **SQLAlchemy & Alembic**: Database ORM and schema migrations.
- **PostgreSQL**: Production-grade relational database.
- **Jinja2**: Templating engine for HTML pages.
- **Pytest**: Test suite for verifying application functionality.

---

## Project Structure

```plaintext
.
├── README.md
├── alembic
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── <migrations>
├── alembic.ini
├── app
│   ├── config.py
│   ├── database
│   │   ├── base.py
│   │   └── models.py
│   ├── main.py
│   ├── repositories
│   │   ├── stay_records.py
│   │   └── users.py
│   ├── routers
│   │   ├── admin.py
│   │   ├── auth.py
│   │   └── stay_records.py
│   ├── schemas
│   │   └── schemas.py
│   ├── templates
│   │   └── <HTML templates>
│   └── utils
│       ├── security.py
│       └── timezone.py
├── requirements.txt
├── .env
└── tests
    ├── <tests>
    └── conftest.py
```
## **Installation**

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/dimalbek/resort_booking.git
    cd resort_booking
    ```

2. **Set up a Virtual Environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```


4. **Create .env File in the root directory and fill it with the following content**:
    ```
    DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_DAYS=7
    ```

5. **Initialize the Database**:
    ```bash
    alembic upgrade head
    ```

6. **Run the Application**:
    ```bash
    uvicorn app.main:app --reload
    ```

The API will now be accessible at http://127.0.0.1:8000 .
index page wtih main page template at http://127.0.0.1:8000/templated .
You may check endpoints at http://127.0.0.1:8000/docs .


## API Endpoints

Below is a brief overview of available endpoints. Refer to [`/docs`](../docs) in your local environment for additional details.

---

### **Auth & User Routes**

- **POST** `/auth/users/register/initiate`  
  Initiate user registration, sending a verification code to the email.

- **POST** `/auth/users/register/confirm`  
  Complete registration by confirming the code.

- **POST** `/auth/users/login/initiate`  
  Begin a 2FA login flow by sending a verification code via email.

- **POST** `/auth/users/login/confirm`  
  Finalize login with the code; receive a JWT.

- **POST** `/auth/users/password-reset/initiate`  
  Start the password reset process; a reset code is emailed to the user.

- **POST** `/auth/users/password-reset/confirm`  
  Complete the reset with the provided code and new password.

- **GET** `/auth/users/me`  
  Fetch details for the currently authenticated user.

- **PATCH** `/auth/users/me`  
  Update personal information (fullname, email, phone, etc.).

---

### **Auth Routes**

- **POST** `/auth/register` - Register a new user.

- **POST** `/auth/login` - Authenticate a user.

- **GET** `/templated/auth/register` - Get Register Form

- **POST** `/templated/auth/register` - Register

- **GET** `/templated/auth/login` - Get Login Form

- **POST** `/templated/auth/login` - Login

- **POST** `/templated/auth/logout` - Logout

### **Admin Routes**

- **GET** `/admin/users/pending` - Get Pending Users

- **POST** `/admin/users/{user_id}/approve` - Approve User

- **POST** `/admin/users/{user_id}/reject` - Reject User

- **GET** `/templated/admin/users/pending` - Get Pending Users

- **GET** `/templated/admin/users/approved` - Get Approved Users

- **POST** `/templated/admin/users/{user_id}/approve` - Approve User

- **POST** `/templated/admin/users/{user_id}/reject` - Reject User

- **POST** `/templated/admin/users/{user_id}/revoke` - Revoke User Approval

- **POST** `/templated/admin/cleanup` - Delete Expired Records

### **Stay Record Routes**

- **GET** `/templated/stay_records/add` - Get Add Stay Record Form

- **POST** `/templated/stay_records/add` - Add Stay Record

- **GET** `/templated/stay_records/current_count` - Current Count Page

- **GE** `/templated/stay_records/guest_count` - Guest Count Form

- **POST** `/templated/stay_records/guest_count` - Guest Count Result

- **GET** `/templated/stay_records/users/{user_id}/stay_records` - Get User Stay Records

- **POST** `/templated/stay_records/users/{user_id}/stay_records/{record_id}/delete` - Delete Stay Record

- **GET** `/templated/stay_records/users/{user_id}/stay_records/{record_id}/edit` - Edit Stay Record Form

- **POST** `/templated/stay_records/users/{user_id}/stay_records/{record_id}/update` - Update Stay Record




## Author ##

Developed by Dinmukhamed Albek