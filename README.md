# ProMetric Tutoring System

Welcome to **ProMetric** — a user-friendly platform for managing tutoring operations, capturing improvement suggestions, and streamlining workflows for students, tutors, and managers.

---

## Motivation

Education deserves to be data-driven and responsive.  
The motivation behind building ProMetric was to empower tutoring centers with tools to gather and analyze data for better decision-making. The goal was to create a single platform to manage:

- Student and tutor registrations
- Centralized navigation through a professional dashboard
- Collecting user-driven suggestions to improve services

---

## What Problem Does ProMetric Solve?

- **Student Engagement:** Many students hesitate to give feedback verbally. ProMetric provides a private and accessible way for them to share suggestions.
- **Operational Efficiency:** Streamlines registration, login, and staff management.
- **Continuous Improvement:** Enables management to collect and review ideas directly from users.

---

## What Does ProMetric Do?

ProMetric offers:

- Student registration and login
- Employee (tutor) registration and login
- Manager login
- Centralized dashboard for navigating the system
- **Suggest Improvement module**:
  - Allows students, tutors, and managers to submit ideas or suggestions for improving services

*Note:* The original Tutor Feedback feature is paused for a future redesign. The new `improvements` feature is active and working.

---

## Technologies Used

- **Programming Language:** Python
- **GUI Framework:** Tkinter
- **Database:** MySQL
- **DB Driver:** mysql-connector-python
- **Image Handling:** Pillow (PIL)

These technologies were chosen because:

- Python allows rapid development and has strong community support.
- Tkinter is lightweight and comes bundled with Python.
- MySQL is a robust and reliable relational database.
- Pillow supports flexible image processing for GUI applications.

---

## Features

- Clean and modern Tkinter GUI
- Background images for a professional appearance
- Modular structure with separate files for Views (UI) and Models (Database Logic)
- Suggest Improvement module:
  - User-friendly interface for submitting suggestions
  - Stores suggestions in MySQL for management review
- Integrated dashboard with quick access to various user portals

---

## SQL Table Definition

The `improvements` table stores all submitted suggestions:

```sql
CREATE TABLE improvements (
    improvement_id INT AUTO_INCREMENT PRIMARY KEY,
    user_type VARCHAR(50),
    user_id INT,
    suggestion_text TEXT,
    submitted_on DATETIME
);

## Challenges Faced

- Maintaining a modern, attractive UI using only Tkinter
- Managing database connections and ensuring reliable error handling
- Deciding to pause certain features (such as the original Tutor Feedback system) for future improvements

## Future Features

- Re-introduce tutor-specific feedback, integrated with subject mappings
- Analytics dashboard for managers to track improvement suggestions
- User authentication security enhancements
- Advanced reporting features with export options

## Proud Of

- Creating a modular, maintainable code structure
- Successfully integrating MySQL with a Tkinter GUI
- Building a simple yet effective system to collect improvement suggestions

## Lessons Learned

- Practical experience in designing relational databases
- Tkinter’s flexibility in handling complex layouts
- The importance of user-centered design in educational software
- Keeping code modular and readable for future updates

## What next?

- Deploying the system on a larger scale
- Enhancing the UI with modern frameworks (e.g., custom Tkinter themes or migration  to web technologies)
- Implementing real-time notifications for management when new suggestions are submitted

## Tech Stack

- **Languages:** Python
- **GUI Framework:** Tkinter
- **Database:** MySQL
- **ORM/Queries:** MySQL Connector for Python
- **Image Processing:** Pillow

## Deployment

Currently designed for desktop execution. No online deploy link is available yet.

## Contact

For any queries or contributions, please reach out to:
neilbarot5@gmail.com


Thank you for your interest in ProMetric.
