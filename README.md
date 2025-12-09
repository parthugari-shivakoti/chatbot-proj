# 🎓 College Inquiry Chatbot (AI + Django + MongoDB)

This is an AI-powered College Inquiry Chatbot built using **Django**, **Google Gemini AI**, and **MongoDB**.  
The chatbot understands user queries and provides information about different colleges such as:
- Available Courses
- District Location
- Fees Structure
- Scholarship / Concession Availability

---

## 🚀 Features
✔ Conversational interface like a real chatbot  
✔ Smart AI understanding using Google Gemini  
✔ MongoDB used for storing all college data  
✔ Real-time chat using JavaScript (Fetch API)  
✔ Can filter data by **district**, **course**, **fees**, etc.  
✔ Easy to extend with more college records

## 🏗️ Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Django (Python) |
| Database | MongoDB Atlas |
| AI Model | Google Gemini API |
| Frontend | HTML, CSS, JavaScript |
| Communication | Fetch API (AJAX) |

## 📂 Project Structure

myproject/
│── myproject/
│ ├── settings.py
│ ├── urls.py
│ └── views.py
│
│── chatbot/
│ ├── views.py
│ ├── urls.py
│ ├── templates/
│ │ └── home.html
│ ├── static/
│ │ ├── style.css
│ │ └── script.js
│ └── mongodb_connection.py
│
└── manage.py

## 🧠 How It Works

1️⃣ User sends a message through chat UI  
2️⃣ JavaScript calls Django using `fetch()`  
3️⃣ Django sends message to Gemini model  
4️⃣ Gemini returns a JSON query format  
5️⃣ Django extracts filter conditions  
6️⃣ MongoDB is queried and results are returned  
7️⃣ Chatbot displays college details to the user  

---

## ⚙️ Setup Guide

### 1️⃣ Clone the project
git clone <https://github.com/parthugari-shivakoti/chatbot-proj/>
cd college_chatbot

### 2️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate (Windows))

shell

### 3️⃣ Install Dependencies
pip install -r requirements.txt

bash
Copy code

### 4️⃣ Add your API Key (Google Gemini)
Inside `chatbot/views.py`:
```python
api_key = "YOUR_GEMINI_API_KEY"
5️⃣ Setup MongoDB Atlas Connection
Inside mongodb_connection.py:

python
Copy code
MONGO_URI = "YOUR_MONGO_ATLAS_URI"
DB_NAME = "your_db_name"
COLLECTION_NAME = "colleges"
6️⃣ Run Server
nginx
Copy code
python manage.py runserver
Open in browser: 👉 http://127.0.0.1:8000/

🔍 Example Queries You Can Ask
"give me faculty details?"

"give me textbooks for CSE"

The chatbot understands real language 🔥

📦 Sample Data
20+ real-like Gujarati college entries included in MongoDB.
(You can add more anytime.)

🔮 Future Enhancements (Optional)
Add login & admin panel

Ranking & placement information

Provide direct Apply Now buttons

Voice interaction with microphone

🧑‍💻 Author
P Shivakoti
College Inquiry Chatbot Project Using AI
If you like this project, ⭐ star the repo!
