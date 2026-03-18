# SaaS Subscription Tracker

A web-based application built using Flask that helps users efficiently manage and monitor their recurring subscriptions.

---

## 🚀 Overview

With the increasing number of digital subscriptions (OTT platforms, software tools, etc.), it becomes difficult to track expenses and renewal dates. This project provides a simple and structured solution to manage subscriptions, track billing cycles, and receive timely reminders.

---

## ✨ Features

- Add, edit, and delete subscriptions
- Track billing cycles (monthly/yearly)
- Automatic calculation of upcoming billing dates
- Categorization: Active, Due Soon, Overdue
- Interactive dashboard with expense insights
- Category-wise spending analysis
- Monthly and yearly cost overview
- CSV export functionality
- Automated email reminders for upcoming payments
- Secure user authentication system

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Migrations:** Flask-Migrate
- **Authentication:** Flask-Login
- **Email Service:** Flask-Mail
- **Frontend:** HTML, CSS, Bootstrap
- **Templating:** Jinja2

---

## 📊 Dashboard Insights

- Total monthly and yearly subscription cost
- Upcoming renewals
- Category-wise spending distribution
- Monthly spending trends

---

## 📂 Project Structure

```
/project
│── app/
│   ├── auth/           # Authentication routes
│   ├── main/           # Main dashboard routes
│   ├── subscriptions/  # Subscription management
│   ├── models.py       # Database models
│   ├── __init__.py     # App factory
│── migrations/         # Database migrations
│── config.py           # Configuration settings
│── run.py              # Entry point
```

---

## ⚙️ Installation & Setup

1. Clone the repository
```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Create a virtual environment
```
python -m venv venv
source venv/bin/activate  (Linux/Mac)
venv\Scripts\activate     (Windows)
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Set environment variables
```
FLASK_APP=run.py
FLASK_ENV=development
MAIL_USERNAME=your_email
MAIL_PASSWORD=your_password
```

5. Run the application
```
flask run
```

---

## 📧 Email Notifications

The application sends automated email reminders for subscriptions that are due within a specified timeframe, helping users avoid missed payments.

---

## 📚 Learning Outcomes

- Understanding relational database design and ORM relationships
- Handling forms and validation in Flask
- Debugging backend issues (null constraints, imports, etc.)
- Working with date and time logic for recurring events
- Integrating third-party services like email
- Structuring scalable applications using blueprints

---

## 🔮 Future Improvements

- Advanced analytics and visualizations
- Improved UI/UX design
- Payment integration
- Multi-user collaboration features
- Mobile responsiveness enhancements

---

## 🤝 Contributors

- Aditi M Jambha 
- Samarth H Rao

---

## 📌 License

This project is for educational purposes.

---

## 💬 Feedback

Feel free to share your suggestions or feedback to help improve this project!

