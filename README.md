# Real-time Chat Application

A modern, dynamic real-time chat application built using Django. This project features user authentication, instant messaging interfaces, and a clean, user-friendly UI for seamless communication.

---

## 📸 Preview

<p align="center">
  <img src="Screenshot%202026-06-12%20154208.png" alt="Real-time Chat Application Preview" width="100%">
</p>

---

## 🚀 Features

*   **Real-time Messaging:** Chat updates instantly without needing to refresh the page.
*   **User Authentication:** Secure user management including admin configuration.
*   **Clean UI/UX:** Sleek dark-themed interface designed for optimal readability and modern aesthetics.
*   **Presence Tracking:** Visual indication of online status.

---

## 🛠️ Getting Started

Follow these steps to set up and run the project locally on your machine.

### Prerequisites

Make sure you have Python 3 installed on your system.

### Setup with pip

#### 1. Create Virtual Environment

Choose the command matching your operating system:

**On macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate

**On Windows:**

PowerShell
python3 -m venv .venv
.\venv\Scripts\Activate.ps1
2. Install Dependencies
Upgrade your package installer and pull in all required Python modules:

Bash
pip install --upgrade pip
pip install -r requirements.txt
3. Database Migration & Admin Setup
Initialize the database schema and create your initial admin credentials:

Bash
python manage.py migrate
python manage.py createsuperuser
4. Run the Application
Start the local development server:

Bash
python manage.py runserver
Once running, navigate to your web browser and open:
👉 http://localhost:8000

📂 Project Structure Note
To ensure the preview image loads correctly on your GitHub repository page, keep the image file named exactly Screenshot 2026-06-12 154208.png in the root directory of your project alongside this README file.

---

### 💡 Quick Tips for You:
1. **Image Path:** The file name in the HTML `<img>` tag is URL-encoded (`%20` replacing the spaces) to prevent broken links on GitHub, so you don't have to rename your file. Just make sure the file `Screenshot 2026-06-12 154208.png` is uploaded to the same main directory as this `README.md`.
2. **Customization:** Feel free to update the **Features** list if you are using specific technologies under the hood (like Django Channels, WebSockets, or Tailwind CSS)!
