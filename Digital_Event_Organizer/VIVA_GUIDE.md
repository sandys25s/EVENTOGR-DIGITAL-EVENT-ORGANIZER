# Digital Event Organizer - Viva Voce Guide

## Project Overview
The **Digital Event Organizer** is a web-based platform designed to streamline the process of managing and attending events. It provides a modern, intuitive interface for administrators to organize events and for users to discover and register for them.

### Key Objectives:
1.  **Centralization**: One platform for all campus/organization events.
2.  **Automation**: Automating registration and notification workflows.
3.  **Security**: Secure login and simulated payment processing.
4.  **Modern UI**: Using Liquid Glass (Glassmorphism) for a premium feel.

---

## Technical Stack (The "How")
-   **Frontend**: HTML5, CSS3 (Custom Glassmorphism), JavaScript (ES6+), Bootstrap 5.
-   **Backend**: Python 3 with Flask Framework.
-   **Database**: SQLite (built-in relational database).
-   **Authentication**: Werkzeug Password Hashing (SHA256).
-   **Architecture**: MVC (Model-View-Controller) inspired design.

---

## Module Explanations
1.  **Authentication**: Handles user sign-up and sign-in using sessions. Passwords are never stored in plain text.
2.  **Event Management (Admin)**: Allows creation, editing, and deletion of events. Tracks participant counts against limits.
3.  **Registration Workflow**: Users can browse events, view details, and register. For paid events, it triggers a mock payment gateway.
4.  **Notification System**: Real-time in-app alerts sent upon registration or payment success.
5.  **Payment Integration**: A simulated Secure Sandbox environment to demonstrate transaction flow.

---

## Common Viva Questions & Answers

**Q1: Why did you choose SQLite over MySQL?**
*A: SQLite is serverless and zero-configuration, making the project highly portable. For a college submission, it ensures the project runs on any evaluator's system without needing a complex MySQL server setup, while still providing full relational database capabilities.*

**Q2: How do you handle password security?**
*A: We use `werkzeug.security` to hash passwords before storing them in the MySQL database. We never store plain text passwords. During login, we use `check_password_hash` to verify the user.*

**Q3: What is "Glassmorphism" in your UI?**
*A: Glassmorphism is a design trend characterized by translucent backgrounds, background blur, and subtle borders. We implemented it using `backdrop-filter: blur()` and semi-transparent RGBA colors in CSS.*

**Q4: How does the registration limit work?**
*A: Each event has a `max_participants` field. Before a user registers, the system checks if `current_participants < max_participants`. If the limit is reached, it disables the registration button.*

**Q5: How is the notification system implemented?**
*A: It's a database-driven system. When a significant action occurs (like registration), a record is inserted into the `notifications` table. The user's dashboard fetches these records periodically (or on load).*

---

## Database Relationships
-   **One-to-Many**: One User can have many Registrations. One User can have many Notifications.
-   **One-to-Many**: One Event can have many Registrations.
-   **One-to-One**: One Registration corresponds to one Payment record.
