# 🏐 Southside JO Interactive Tracker

This is a **Streamlit app** that lets you follow Southside's path through the 18U Men’s Championship bracket at Junior Olympics.  
You can click **Win** or **Lose** after each game to see exactly when and where their next game will be, all the way through the tournament.  

It includes the Platinum and Gold bracket reassignments and updates automatically based on your choices.

---

## 📦 Features
- Shows **current game info** (date, time, pool)
- Click **Win** or **Lose** to follow the path
- **Reset** button to start over at Southside’s first game
- Tracks **Platinum/Gold bracket reassignments** automatically
- Works on **desktop or mobile**

---

## 📁 Files
- `app.py` – the Streamlit app
- `2025_Public_Sched_S3.xlsx` – schedule file (must be in same folder)
- `README.md` – this file

---

## 🖥 Run Locally

### 1️⃣ Install Python
Make sure you have Python 3.9+ installed.

### 2️⃣ Install required libraries
```bash
pip install streamlit pandas openpyxl
