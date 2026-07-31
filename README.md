# 💬 Gemini Chatbot (Streamlit + Google AI Studio)

An interactive chatbot built with **Streamlit** and **Google AI Studio (Gemini models)**.  
This project demonstrates **OOP design**, **model switching**, and **quota tracking** — making it a strong portfolio piece for showcasing AI/ML and full‑stack skills.

---

## 🚀 Features
- **Model switching** → Seamlessly switch between Gemini models (Flash, Flash‑Lite, Pro) during a conversation.
- **Per‑model token tracking** → Logs prompt, output, and total tokens separately for each model.
- **Quota monitoring** → Displays request counts, per‑model totals, and grand totals in the sidebar.
- **Visual dashboards** → Bar chart visualization of token usage across models.
- **Conversation history** → Preserves chat context when switching models.
- **OOP design** → Encapsulated `Chatbot` class with properties and helper methods.

---

## 📂 Project Structure
```
general-purpose-chatbot/
│── main.py        # Streamlit UI
│── chatbot.py     # Chatbot class (model switching + token tracking)
│── logs.log       # Debug logs
│── .env           # API key storage (local dev)
│── .streamlit/secrets.toml # API key storage (production)
│── README.md      # Project documentation
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/general-purpose-chatbot.git
   cd general-purpose-chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv projectvenv
   source projectvenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**
   - For local dev: create a `.env` file in the project root:
     ```
     API_KEY=your_google_ai_studio_api_key_here
     ```
   - For Streamlit Cloud: add it to `.streamlit/secrets.toml` or via **Settings → Secrets**.

5. **Run the app**
   ```bash
   streamlit run main.py
   ```

---

## 📊 Sidebar Dashboard
- **Requests Used Today** → Tracks API calls.  
- **Current Model Tokens** → Shows usage for the active model.  
- **Per‑Model Token Usage** → Lists token totals for each model used.  
- **Total Tokens (All Models)** → Aggregated usage across all models.  
- **Bar Chart** → Visual comparison of token consumption per model.  

---

## 🛠️ Tech Stack
- **Python** (OOP design, logging, environment management)  
- **Streamlit** (UI + visualization)  
- **Google AI Studio** (Gemini models API)  
- **dotenv** (secure API key management)  

---

## 🎯 Portfolio Value
This project demonstrates:
- Practical **AI/ML integration** with real APIs.  
- **End‑to‑end design**: backend logic + frontend visualization.  
- **Robust quota handling** (per‑model tracking, fallback readiness).  
- Recruiter‑friendly UI with clear metrics and charts.  

---

## 📌 Next Steps
- Add **line chart visualization** for token usage per turn.  
- Implement **automatic fallback** when a model’s quota is exhausted.  
- Extend to support **multi‑modal inputs** (images, audio).  

---

## 📝 License
MIT License — free to use and adapt.
```

---

Drop this into `README.md` and commit it.  

Yuri, do you want me to also generate a **requirements.txt** file so anyone cloning your repo can install dependencies in one step? That’s usually the next thing recruiters look for.