import streamlit as st
import pandas as pd

# Load the schedule
schedule = pd.read_excel("2025_Public_Sched_S3.xlsx", sheet_name="18U_M_Champ")

# Convert Game # to string for consistent matching
schedule['Game'] = schedule['Game'].astype(str)

# Define first game for Southside
SOUTHSIDE_FIRST_GAME = "13"

# Initialize session state
if "current_game" not in st.session_state:
    st.session_state.current_game = SOUTHSIDE_FIRST_GAME
    st.session_state.path = []

st.title("🏐 Southside JO Interactive Tracker")
st.write("Click **Win** or **Lose** to follow Southside’s path through the tournament.")

# Find the current game details
current_game_row = schedule[schedule['Game'] == st.session_state.current_game]

if not current_game_row.empty:
    date = current_game_row['Date'].values[0]
    time = current_game_row['Time'].values[0]
    pool = current_game_row['Pool'].values[0]
else:
    date, time, pool = None, None, None

st.subheader(f"Game {st.session_state.current_game}")
st.write(f"**Date:** {date}")
st.write(f"**Time:** {time}")
st.write(f"**Pool:** {pool}")

# Buttons for win/lose
col1, col2, col3 = st.columns(3)

def update_game(result):
    # Record result in path
    st.session_state.path.append((st.session_state.current_game, date, time, pool, result))
    
    # Get next game based on win or loss
    if result == "Win":
        next_game = current_game_row['If Win'].values[0]
    else:
        next_game = current_game_row['If Lose'].values[0]
    
    if pd.isna(next_game):
        st.session_state.current_game = None
    else:
        st.session_state.current_game = str(next_game)

with col1:
    if st.button("✅ Win"):
        update_game("Win")

with col2:
    if st.button("❌ Lose"):
        update_game("Lose")

with col3:
    if st.button("🔄 Reset"):
        st.session_state.current_game = SOUTHSIDE_FIRST_GAME
        st.session_state.path = []

st.subheader("Path so far")
for game, g_date, g_time, g_pool, result in st.session_state.path:
    st.write(f"Game {game} ({g_date} {g_time} {g_pool}) → {result}")
