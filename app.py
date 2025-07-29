import streamlit as st
import pandas as pd

# --------------------------
# CONFIG
# --------------------------
EXCEL_FILE = "2025_Public_Sched_S3.xlsx"
SHEET_NAME = "18U_M_Champ-27 teams DE auRR"
SOUTHSIDE_START_GAME = 13
DAY1_ROWS = (0, 60)        # Bracket range
TYPE_SECTION_START = 82    # "type" column start row for Platinum/Gold

# --------------------------
# LOAD EXCEL
# --------------------------
@st.cache_data
def load_schedule():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, header=None)

    # Build game map from Day 1
    games_map = {}
    for idx, row in df.iloc[DAY1_ROWS[0]:DAY1_ROWS[1]].iterrows():
        try:
            game_num = int(str(row[0]).strip())
        except:
            continue
        games_map[game_num] = {
            "date": str(row[1]).strip() if pd.notna(row[1]) else None,
            "time": str(row[2]).strip() if pd.notna(row[2]) else None,
            "pool": str(row[3]).strip() if pd.notna(row[3]) else None,
            "win": str(row[4]).strip() if pd.notna(row[4]) else None,
            "lose": str(row[5]).strip() if pd.notna(row[5]) else None
        }

    # Parse Platinum/Gold type section
    type_map = {}
    for idx, row in df.iloc[TYPE_SECTION_START:].iterrows():
        if pd.isna(row[1]):
            continue
        type_val = str(row[1]).strip()
        if "/" in type_val:
            try:
                game_num = int(str(row[0]).strip())
            except:
                continue
            left, right = type_val.replace("W/L", "").strip().split("/")
            left = left.strip()
            right = right.strip()
            type_map[left] = game_num
            type_map[right] = game_num
            games_map[game_num] = {
                "date": str(row[2]).strip() if pd.notna(row[2]) else None,
                "time": str(row[3]).strip() if pd.notna(row[3]) else None,
                "pool": str(row[4]).strip() if pd.notna(row[4]) else None,
                "win": str(row[5]).strip() if pd.notna(row[5]) else None,
                "lose": str(row[6]).strip() if pd.notna(row[6]) else None
            }

    return games_map, type_map

games_map, type_map = load_schedule()

# --------------------------
# GET NEXT GAME FUNCTION
# --------------------------
def get_game_info(node):
    """Return game info for a game number or type code."""
    if isinstance(node, str) and not node.isdigit():
        if node in type_map:
            node = type_map[node]
        else:
            return {"game": node, "date": None, "time": None, "pool": None, "win": None, "lose": None}
    try:
        node = int(node)
    except:
        return {"game": node, "date": None, "time": None, "pool": None, "win": None, "lose": None}

    if node not in games_map:
        return {"game": node, "date": None, "time": None, "pool": None, "win": None, "lose": None}

    info = games_map[node].copy()
    info["game"] = node
    return info

# --------------------------
# STREAMLIT UI
# --------------------------
st.title("🏐 Southside JO Tracker")
st.write("Click **Win** or **Lose** to follow Southside’s path through the tournament.")

if "current_node" not in st.session_state:
    st.session_state.current_node = SOUTHSIDE_START_GAME
if "history" not in st.session_state:
    st.session_state.history = []

current_info = get_game_info(st.session_state.current_node)

# Show current game
st.subheader(f"Game {current_info['game']}")
st.write(f"**Date:** {current_info['date']}")
st.write(f"**Time:** {current_info['time']}")
st.write(f"**Pool:** {current_info['pool']}")

# Action buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✅ Win"):
        st.session_state.history.append((current_info, "Win"))
        st.session_state.current_node = current_info["win"]
with col2:
    if st.button("❌ Lose"):
        st.session_state.history.append((current_info, "Lose"))
        st.session_state.current_node = current_info["lose"]
with col3:
    if st.button("🔄 Reset"):
        st.session_state.history = []
        st.session_state.current_node = SOUTHSIDE_START_GAME

# Show history
if st.session_state.history:
    st.markdown("### Path so far")
    for game, result in st.session_state.history:
        st.write(f"Game {game['game']} ({game['date']} {game['time']} {game['pool']}) → {result}")
