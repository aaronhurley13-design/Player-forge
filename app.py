import random
import streamlit as st

# ==========================================
# PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="Player Forge | GOAT Builder",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for dark-mode sports card styling & animations
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .slot-card {
        background-color: #1e293b;
        border: 2px dashed #475569;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .slot-card.filled {
        border: 2px solid #3b82f6;
        background: linear-gradient(135deg, #1e3a8a 0%, #1e293b 100%);
    }
    .badge-safe {
        background-color: #065f46;
        color: #34d399;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# DATABASE & ATHLETE POOLS (4 LEAGUES)
# ==========================================
LEAGUES_DATA = {
    "🏀 Pro Basketball": {
        "attributes": [
            "Scoring / Inside",
            "Shooting / Range",
            "Playmaking / IQ",
            "Perimeter Defense",
            "Rebounding / Motor",
            "Clutch / Takeover",
        ],
        "athletes": [
            # GOATs & Superstars
            {
                "name": "His Airness",
                "safe": "The 23 Air",
                "team": "CHI",
                "vals": [99, 90, 93, 98, 88, 99],
            },
            {
                "name": "King James",
                "safe": "The Akron Engine",
                "team": "LA",
                "vals": [98, 89, 99, 92, 94, 97],
            },
            {
                "name": "Chef Curry",
                "safe": "The 30 Sharpshooter",
                "team": "GSW",
                "vals": [92, 99, 95, 84, 76, 98],
            },
            {
                "name": "The Joker",
                "safe": "Sombor Maestro",
                "team": "DEN",
                "vals": [96, 93, 99, 83, 96, 95],
            },
            {
                "name": "Wemby",
                "safe": "The Alien Center",
                "team": "SAS",
                "vals": [90, 85, 82, 99, 98, 88],
            },
            {
                "name": "Black Mamba",
                "safe": "The 24 Legend",
                "team": "LAL",
                "vals": [99, 91, 90, 95, 78, 99],
            },
            {
                "name": "The Diesel",
                "safe": "Big Cactus",
                "team": "ORL",
                "vals": [99, 52, 75, 84, 99, 90],
            },
            {
                "name": "Greek Freak",
                "safe": "The 34 Engine",
                "team": "MIL",
                "vals": [98, 70, 88, 95, 98, 92],
            },
            {
                "name": "The Beard",
                "safe": "Stepback Maestro",
                "team": "HOU",
                "vals": [95, 94, 97, 78, 75, 88],
            },
            # Traps / Specialists
            {
                "name": "Kwame B.",
                "safe": "Rookie Bust #1",
                "team": "WAS",
                "vals": [58, 42, 50, 62, 60, 45],
            },
            {
                "name": "White Mamba",
                "safe": "Victory Cigar #1",
                "team": "BOS",
                "vals": [68, 78, 70, 60, 58, 72],
            },
        ],
    },
    "🏈 Pro Football": {
        "attributes": [
            "Passing Accuracy",
            "Arm Strength",
            "Rushing & Agility",
            "Catching / Hands",
            "Pass Protection / IQ",
            "Clutch Drive Gen",
        ],
        "athletes": [
            {
                "name": "Tom Terrific",
                "safe": "The 7-Ring Icon",
                "team": "NE",
                "vals": [97, 91, 72, 80, 98, 99],
            },
            {
                "name": "Mahomes Magic",
                "safe": "No-Look Wizard",
                "team": "KC",
                "vals": [96, 98, 92, 82, 94, 98],
            },
            {
                "name": "Megatron",
                "safe": "The 6-5 Deep Threat",
                "team": "DET",
                "vals": [85, 75, 88, 99, 70, 93],
            },
            {
                "name": "The Minister of Defense",
                "safe": "92 Edge Terror",
                "team": "PHI",
                "vals": [72, 60, 78, 85, 99, 95],
            },
            {
                "name": "Lamar Action",
                "safe": "Gridiron Sprinter",
                "team": "BAL",
                "vals": [90, 89, 99, 83, 85, 92],
            },
            {
                "name": "Jettas",
                "safe": "Griddy Receiver",
                "team": "MIN",
                "vals": [88, 70, 91, 98, 74, 94],
            },
            {
                "name": "Peyton",
                "safe": "The Sheriff 18",
                "team": "IND",
                "vals": [99, 94, 65, 82, 99, 96],
            },
            {
                "name": "The Assassin",
                "safe": "Safety 20",
                "team": "OAK",
                "vals": [65, 55, 70, 75, 92, 98],
            },
            # Traps
            {
                "name": "JaMarcus",
                "safe": "Purple Jam",
                "team": "OAK",
                "vals": [60, 99, 52, 65, 48, 50],
            },
            {
                "name": "Punt God",
                "safe": "Eighty-Yard Boot",
                "team": "BUF",
                "vals": [50, 85, 60, 60, 70, 70],
            },
        ],
    },
    "⚽ World Soccer": {
        "attributes": [
            "Finishing / Striking",
            "Dribbling / Agility",
            "Vision & Passing",
            "Defensive Workrate",
            "Stamina & Pace",
            "Big Match Clutchness",
        ],
        "athletes": [
            {
                "name": "La Pulga",
                "safe": "The 10 Magician",
                "team": "ARG",
                "vals": [98, 99, 99, 65, 88, 99],
            },
            {
                "name": "CR7",
                "safe": "The 7 Apex Striker",
                "team": "POR",
                "vals": [99, 93, 86, 74, 96, 99],
            },
            {
                "name": "King Pelé",
                "safe": "The 10 Eternal",
                "team": "BRA",
                "vals": [99, 97, 95, 78, 94, 99],
            },
            {
                "name": "El Fenômeno",
                "safe": "R9 Strike Force",
                "team": "BRA",
                "vals": [99, 98, 85, 55, 92, 97],
            },
            {
                "name": "Zizou",
                "safe": "The Maestro 5",
                "team": "FRA",
                "vals": [91, 95, 99, 82, 84, 98],
            },
            {
                "name": "Mbappé",
                "safe": "Turtle Speed 7",
                "team": "FRA",
                "vals": [97, 97, 85, 64, 99, 94],
            },
            {
                "name": "VVD",
                "safe": "The Rock Center-Back",
                "team": "NED",
                "vals": [70, 75, 82, 99, 90, 92],
            },
            # Traps
            {
                "name": "Lord Bendtner",
                "safe": "The Danish Legend",
                "team": "DEN",
                "vals": [72, 65, 60, 52, 68, 80],
            },
            {
                "name": "Adama",
                "safe": "Baby-Oiled Winger",
                "team": "ESP",
                "vals": [68, 90, 64, 75, 99, 65],
            },
        ],
    },
    "🎾 Pro Tennis": {
        "attributes": [
            "Forehand Power",
            "Backhand Precision",
            "Serve / Aces",
            "Volley & Net IQ",
            "Court Coverage / Speed",
            "Tiebreak Mental Toughness",
        ],
        "athletes": [
            {
                "name": "King Roger",
                "safe": "Basel Maestro",
                "team": "SUI",
                "vals": [94, 98, 96, 99, 92, 95],
            },
            {
                "name": "Rafa Clay",
                "safe": "Mallorca Bull",
                "team": "ESP",
                "vals": [99, 92, 90, 88, 99, 99],
            },
            {
                "name": "Novak GOAT",
                "safe": "Belgrade Wall",
                "team": "SRB",
                "vals": [96, 97, 95, 90, 99, 99],
            },
            {
                "name": "Serena Queen",
                "safe": "Compton Apex Serve",
                "team": "USA",
                "vals": [99, 94, 99, 89, 93, 99],
            },
            {
                "name": "Alcaraz",
                "safe": "Murcia Rocket",
                "team": "ESP",
                "vals": [98, 93, 92, 91, 98, 96],
            },
            # Traps
            {
                "name": "Tomic the Tank",
                "safe": "Matchday Mystery",
                "team": "AUS",
                "vals": [65, 60, 78, 55, 50, 40],
            },
        ],
    },
}

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "league" not in st.session_state:
    st.session_state.league = "🏀 Pro Basketball"
if "safe_mode" not in st.session_state:
    st.session_state.safe_mode = False
if "assigned_slots" not in st.session_state:
    st.session_state.assigned_slots = {
        i: None for i in range(6)
    }  # slot_idx -> athlete_dict
if "current_spun_athlete" not in st.session_state:
    st.session_state.current_spun_athlete = None
if "skip_tokens" not in st.session_state:
    st.session_state.skip_tokens = 1
if "best_fit_tokens" not in st.session_state:
    st.session_state.best_fit_tokens = 1
if "player_name" not in st.session_state:
    st.session_state.player_name = "Apex Rookie"

# ==========================================
# SIDEBAR CONTROLS
# ==========================================
st.sidebar.title("⚙️ Forge Control Center")

new_league = st.sidebar.selectbox(
    "Select Sport League", list(LEAGUES_DATA.keys())
)
if new_league != st.session_state.league:
    st.session_state.league = new_league
    st.session_state.assigned_slots = {i: None for i in range(6)}
    st.session_state.current_spun_athlete = None
    st.rerun()

st.sidebar.markdown("---")
st.session_state.safe_mode = st.sidebar.checkbox(
    "🛡️ Safe Names Mode (Parody/No IRL Names)",
    value=st.session_state.safe_mode,
)

st.sidebar.markdown("### 🎴 Custom Player Name")
st.session_state.player_name = st.sidebar.text_input(
    "Name your forged star", value=st.session_state.player_name
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Forge", use_container_width=True):
    st.session_state.assigned_slots = {i: None for i in range(6)}
    st.session_state.current_spun_athlete = None
    st.session_state.skip_tokens = 1
    st.session_state.best_fit_tokens = 1
    st.rerun()

# ==========================================
# MAIN APP HEADER
# ==========================================
st.title("⚡ PLAYER FORGE")
st.markdown(
    "**Spin random athletes from history, then strategically assign them to build your ultimate 6-tool GOAT!**"
)

league_info = LEAGUES_DATA[st.session_state.league]
attributes = league_info["attributes"]
athletes_pool = league_info["athletes"]

# ==========================================
# CENTRAL SPINDLE & STAGE
# ==========================================
st.markdown("### 🎯 Player Spin Stage")

col_spin1, col_spin2, col_spin3 = st.columns([2, 2, 2])

with col_spin1:
    if st.button("🎲 SPIN PLAYER", type="primary", use_container_width=True):
        st.session_state.current_spun_athlete = random.choice(athletes_pool)
        st.rerun()

with col_spin2:
    if st.session_state.skip_tokens > 0 and st.session_state.current_spun_athlete:
        if st.button(
            f"⏭️ Skip Token ({st.session_state.skip_tokens} left)",
            use_container_width=True,
        ):
            st.session_state.current_spun_athlete = random.choice(
                athletes_pool
            )
            st.session_state.skip_tokens -= 1
            st.rerun()
    else:
        st.markdown(
            "<div style='text-align:center; color:#64748b; padding-top:8px;'>No Skips Left</div>",
            unsafe_allow_html=True,
        )

with col_spin3:
    if (
        st.session_state.best_fit_tokens > 0
        and st.session_state.current_spun_athlete
    ):
        if st.button(
            f"⚡ Auto-Best Fit ({st.session_state.best_fit_tokens} left)",
            use_container_width=True,
        ):
            # Find best open slot
            ath = st.session_state.current_spun_athlete
            best_val = -1
            best_idx = None
            for idx, attr in enumerate(attributes):
                if st.session_state.assigned_slots[idx] is None:
                    if ath["vals"][idx] > best_val:
                        best_val = ath["vals"][idx]
                        best_idx = idx
            if best_idx is not None:
                st.session_state.assigned_slots[best_idx] = ath
                st.session_state.current_spun_athlete = None
                st.session_state.best_fit_tokens -= 1
                st.rerun()
    else:
        st.markdown(
            "<div style='text-align:center; color:#64748b; padding-top:8px;'>No Auto-Fits Left</div>",
            unsafe_allow_html=True,
        )

# Display Current Spun Athlete Card
curr_ath = st.session_state.current_spun_athlete
if curr_ath:
    display_name = (
        curr_ath["safe"] if st.session_state.safe_mode else curr_ath["name"]
    )
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #312e81 0%, #1e1b4b 100%); border: 2px solid #6366f1; padding: 20px; border-radius: 12px; text-align: center; margin-top: 15px; margin-bottom: 25px;">
            <h2 style="margin: 0; color: #a5b4fc;">🌟 SPUN ATHLETE: {display_name} ({curr_ath['team']})</h2>
            <p style="margin: 5px 0 15px 0; color: #cbd5e1; font-size: 14px;">Select an open attribute slot below to lock in their rating!</p>
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
        """,
        unsafe_allow_html=True,
    )

    cols_vals = st.columns(6)
    for i, attr in enumerate(attributes):
        with cols_vals[i]:
            st.metric(label=attr[:10], value=curr_ath["vals"][i])

    st.markdown("</div></div>", unsafe_allow_html=True)
else:
    st.info(
        "👆 Click **SPIN PLAYER** above to draw an athlete into the forge stage!"
    )

st.markdown("---")

# ==========================================
# FORGED PLAYER BUILDER BOARD (6 SLOTS)
# ==========================================
st.markdown(
    f"### 🛡️ Forged Board: {st.session_state.player_name}'s Skill DNA"
)

board_cols = st.columns(3)
for idx, attr in enumerate(attributes):
    col_idx = idx % 3
    with board_cols[col_idx]:
        assigned = st.session_state.assigned_slots[idx]

        if assigned is not None:
            a_name = (
                assigned["safe"]
                if st.session_state.safe_mode
                else assigned["name"]
            )
            val = assigned["vals"][idx]
            st.markdown(
                f"""
                <div class="slot-card filled">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: bold;">{attr.upper()}</span>
                    <h3 style="margin: 5px 0; color: #60a5fa;">{val} / 99</h3>
                    <p style="margin: 0; font-size: 13px; color: #e2e8f0;">Source: {a_name} ({assigned['team']})</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Clear Slot {idx+1}", key=f"clear_{idx}"):
                st.session_state.assigned_slots[idx] = None
                st.rerun()
        else:
            st.markdown(
                f"""
                <div class="slot-card">
                    <span style="font-size: 12px; color: #94a3b8; font-weight: bold;">{attr.upper()}</span>
                    <h3 style="margin: 5px 0; color: #64748b;">EMPTY</h3>
                    <p style="margin: 0; font-size: 12px; color: #64748b;">Awaiting Assignment</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if curr_ath is not None:
                if st.button(f"Assign to Slot {idx+1}", key=f"assign_{idx}y"):
                    st.session_state.assigned_slots[idx] = curr_ath
                    st.session_state.current_spun_athlete = None
                    st.rerun()

# ==========================================
# CALCULATIONS & CAREER SIMULATION
# ==========================================
st.markdown("---")
st.markdown("### 📈 Career Simulation & Scouting Report")

filled_count = sum(
    1 for v in st.session_state.assigned_slots.values() if v is not None
)

if filled_count == 6:
    vals_list = [
        st.session_state.assigned_slots[i]["vals"][i] for i in range(6)
    ]
    ovr = sum(vals_list) // 6

    # Determine Tier & Hall of Fame Probability
    if ovr >= 95:
        tier = "👑 GOAT TIER LEGEND"
        hof_prob = "99.9%"
        rings = random.randint(5, 8)
        mvps = random.randint(3, 6)
    elif ovr >= 90:
        tier = "⚡ SUPERSTAR ICON"
        hof_prob = "95.0%"
        rings = random.randint(2, 4)
        mvps = random.randint(1, 3)
    elif ovr >= 85:
        tier = "🌟 ALL-STAR STARTER"
        hof_prob = "78.4%"
        rings = random.randint(0, 2)
        mvps = 0
    else:
        tier = "🧢 BENCH SPECIALIST"
        hof_prob = "22.1%"
        rings = 0
        mvps = 0

    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    with col_res1:
        st.metric("Composite OVR", f"{ovr} OVR")
    with col_res2:
        st.metric("Career Tier", tier)
    with col_res3:
        st.metric("Championships / Titles", f"{rings} Rings")
    with col_res4:
        st.metric("HOF Probability", hof_prob)

    st.success(
        f"🎉 **{st.session_state.player_name}** is fully forged! Ready to dominate the league history books."
    )
else:
    st.warning(
        f"⚠️ Complete all 6 attribute slots to unlock the career simulation and Hall of Fame projection! ({filled_count}/6 filled)"
    )

# ==========================================
# FOOTER & LEGAL DISCLAIMER
# ==========================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 12px; padding-bottom: 20px;">
        <p><strong>Player Forge</strong> is an independent fan-made sports attribute drafting simulation game.</p>
        <p>Not affiliated with, endorsed by, or licensed by any professional sports league, player association, or governing body. All athlete names in Safe Mode are purely parodic.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
