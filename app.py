import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import time

st.set_page_config(page_title="Bid2Build Auction Console", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card Styles */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Header Styles */
    .main-title {
        font-size: 4em;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        letter-spacing: -2px;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.3em;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .metric-value {
        font-size: 3em;
        font-weight: 800;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1em;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }
    
    /* Small Metric Cards */
    .small-metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .small-metric-value {
        font-size: 2em;
        font-weight: 700;
        color: #667eea;
        margin: 0;
    }
    
    .small-metric-label {
        font-size: 0.85em;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Progress Bar */
    .progress-container {
        background: #e5e7eb;
        border-radius: 50px;
        height: 30px;
        overflow: hidden;
        position: relative;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        transition: width 0.5s ease;
    }
    
    .progress-label {
        font-size: 0.9em;
        color: #374151;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Leaderboard */
    .leaderboard-item {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }
    
    .leaderboard-item:hover {
        transform: translateX(5px);
    }
    
    .leaderboard-rank {
        font-size: 1.5em;
        font-weight: 800;
        color: #667eea;
        margin-right: 1rem;
        min-width: 40px;
    }
    
    .leaderboard-name {
        flex-grow: 1;
        font-weight: 600;
        color: #1f2937;
    }
    
    .leaderboard-value {
        font-weight: 700;
        color: #667eea;
    }
    
    .current-team {
        border: 3px solid #667eea;
        background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
    }
    
    .medal {
        font-size: 1.5em;
        margin-right: 0.5rem;
    }
    
    /* Item List Styles */
    .item-card {
        background: #f8fafc;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .item-name {
        font-weight: 600;
        font-size: 1.1em;
        color: #1f2937;
    }
    
    .item-price {
        color: #667eea;
        font-weight: 700;
        font-size: 1.1em;
    }
    
    /* Button Styles */
    .stButton > button {
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Team Expander */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        border-left: 4px solid #667eea;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Login Container */
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    
    /* Stats Badge */
    .stat-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85em;
        margin-left: 0.5rem;
    }
    
    .status-success {
        background: #10b981;
        color: white;
    }
    
    .status-warning {
        background: #f59e0b;
        color: white;
    }
    
    .status-danger {
        background: #ef4444;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

DATA_PATH = Path("data.json")

def load_data():
    if not DATA_PATH.exists():
        st.error("data.json not found. Create it in the same folder as app.py.")
        st.stop()
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

def save_data(d):
    DATA_PATH.write_text(json.dumps(d, indent=2), encoding="utf-8")

data = load_data()

# Session state management
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None
# Restore session from URL (only if session is empty)
if st.session_state.user is None:
    user = st.query_params.get("user")
    role = st.query_params.get("role")

    if user and role:
        if role == "admin" and user == data["admin"]["username"]:
            st.session_state.user = user
            st.session_state.role = "admin"
        elif role == "team" and user in data["teams"]:
            st.session_state.user = user
            st.session_state.role = "team"
# Browser back/forward is not working, researched and found this is a known limitation of Streamlit.
# ---------------- Login UI ----------------
def login_ui():
    st.markdown('<h1 class="main-title">Bid2Build</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">🔨 Tech Auction | Build Your Product</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Team Login Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Team Login")
        t_user = st.text_input("Team Username", placeholder="Enter your team username", key="t_user_login")
        t_pw = st.text_input("Password", type="password", placeholder="Enter your password", key="t_pw_login")
        
        if st.button("Login as Team", use_container_width=True):
            teams = data["teams"]
            if t_user in teams and t_pw == teams[t_user]["password"]:
                st.session_state.user = t_user
                st.session_state.role = "team"
                st.query_params["user"] = t_user
                st.query_params["role"] = "team"
                st.success(f"Welcome, {t_user}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials. Please check your username and password.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Admin Login Expander
        with st.expander("Admin Access"):
            a_user = st.text_input("Admin Username", key="admin_user")
            a_pw = st.text_input("Admin Password", type="password", key="admin_pw")
            if st.button("Login as Admin", key="admin_login_btn", use_container_width=True):
                if a_user == data["admin"]["username"] and a_pw == data["admin"]["password"]:
                    st.session_state.user = a_user
                    st.session_state.role = "admin"
                    st.query_params["user"] = a_user
                    st.query_params["role"] = "admin"
                    st.success("Admin access granted.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(" Invalid admin credentials.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #6b7280; font-size: 0.9em;">IEEE SPS BNMIT</div>', unsafe_allow_html=True)

# ---------------- Logout UI ----------------
def logout_ui():
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.session_state.role = None
            st.query_params.clear()
            st.rerun()

# ---------------- Admin UI ----------------
def admin_ui():
    st.markdown('<h1 style="color: white;">⚙️ Admin Dashboard</h1>', unsafe_allow_html=True)
    logout_ui()
    
    st.success("✅ You control recording: select winning team, item, price, and quantity. Credits auto-deduct.")
    
    # Global Settings in cards
    st.markdown("### 🌐 Global Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Bid Step (points)")
        new_step = st.number_input("Bid step value", min_value=1, value=int(data.get("bid_step", 50)), key="bid_step")
        if st.button("💾 Save Bid Step", use_container_width=True):
            data["bid_step"] = int(new_step)
            save_data(data)
            st.toast("✅ Saved bid step.")
    
    with col2:
        st.markdown("#### Starting Credits")
        new_start = st.number_input("Starting credits value", min_value=1, value=int(data.get("starting_credits", 1000)), key="start_credits")
        if st.button("💾 Save Starting Credits", use_container_width=True):
            data["starting_credits"] = int(new_start)
            save_data(data)
            st.toast("✅ Saved starting credits.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Teams Management
    st.markdown("### 👥 Teams & Management")
    teams = data["teams"]
    
    # Team stats overview
    total_teams = len(teams)
    total_items = sum(len(info['items']) for info in teams.values())
    avg_credits = sum(info['credits'] for info in teams.values()) // total_teams if total_teams > 0 else 0
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.markdown(f'<div class="metric-card"><p class="metric-value">{total_teams}</p><p class="metric-label">Total Teams</p></div>', unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f'<div class="metric-card"><p class="metric-value">{total_items}</p><p class="metric-label">Items Awarded</p></div>', unsafe_allow_html=True)
    with stat_col3:
        st.markdown(f'<div class="metric-card"><p class="metric-value">{avg_credits}</p><p class="metric-label">Avg Credits Left</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    for name, info in teams.items():
        with st.expander(f"🏆 {name} — 💰 {info['credits']} credits — 📦 {len(info['items'])} items — ✓ Registered: {info.get('registered', True)}"):
            c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
            with c1:
                st.markdown(f"**Password:** `{info['password']}`")
                if st.button(f"🔄 Reset Password", key=f"reset_pw_{name}"):
                    import secrets, string
                    alpha = string.ascii_letters + string.digits
                    newpw = ''.join(secrets.choice(alpha) for _ in range(8))
                    info["password"] = newpw
                    save_data(data)
                    st.info(f"New password: {newpw}")
            with c2:
                if st.button(f"💳 Reset Credits", key=f"reset_cred_{name}"):
                    info["credits"] = data["starting_credits"]
                    info["items"] = []
                    save_data(data)
                    st.success(f"✅ Reset complete!")
            with c3:
                reg = st.checkbox("Registered", value=info.get("registered", True), key=f"reg_{name}")
                if reg != info.get("registered", True):
                    info["registered"] = reg
                    save_data(data)
            with c4:
                if st.button(f"🗑️ Remove", key=f"rm_team_{name}"):
                    del teams[name]
                    save_data(data)
                    st.warning(f"Removed {name}")
                    st.rerun()
            
            st.markdown("**Items Won:**")
            if info["items"]:
                for idx, it in enumerate(info["items"]):
                    col_i, col_r = st.columns([5, 1])
                    with col_i:
                        st.markdown(f'<div class="item-card"><span class="item-name">{it["qty"]} × {it["name"]}</span><span class="item-price">@ {it["price"]} credits</span></div>', unsafe_allow_html=True)
                    with col_r:
                        if st.button("❌", key=f"rm_item_{name}_{idx}"):
                            refund = it["price"] * it.get("qty", 1)
                            info["credits"] += refund
                            del info["items"][idx]
                            save_data(data)
                            st.warning(f"Refunded {refund} credits")
                            st.rerun()
            else:
                st.caption("No items yet.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add/Update Team
    st.markdown("### ➕ Add / Update Team")
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("Team Username", placeholder="e.g., team_alpha")
    with col2:
        new_pw = st.text_input("Password", placeholder="Leave blank to auto-generate", type="password")
    
    if st.button("➕ Add / Update Team", use_container_width=True):
        if new_name.strip() == "":
            st.error("❌ Team name required.")
        else:
            if new_name not in teams:
                teams[new_name] = {
                    "password": new_pw or "Temp1234",
                    "credits": data["starting_credits"],
                    "items": [],
                    "registered": True
                }
                save_data(data)
                st.success(f"✅ Added {new_name}. Password: {teams[new_name]['password']}")
            else:
                if new_pw:
                    teams[new_name]["password"] = new_pw
                    save_data(data)
                    st.info(f"✅ Updated password for {new_name}.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Record Auction
    st.markdown("### 🎯 Record Auction Result")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        item_name = st.text_input("Item Name", placeholder="e.g., ESP32 DevKit")
    with col2:
        bid_price = st.number_input("Price per Unit", min_value=1, value=int(data.get("bid_step", 50)))
    with col3:
        qty = st.number_input("Quantity", min_value=1, value=1, step=1)
    with col4:
        team_choice = st.selectbox("Winning Team", options=list(teams.keys()))
    
    if st.button("🏆 Assign Item to Team", use_container_width=True):
        total_cost = int(bid_price) * int(qty)
        current_credits = teams[team_choice]["credits"]
        starting_credits = data.get("starting_credits", 1000)
        new_remaining = current_credits - total_cost
        total_spent = starting_credits - new_remaining
        
        if total_cost > current_credits:
            st.error(f"❌ {team_choice} doesn't have enough credits ({current_credits} remaining).")
        elif total_spent > starting_credits:
            st.error(f"⚠️ {team_choice} would exceed the {starting_credits}-credit limit.")
        else:
            teams[team_choice]["credits"] = new_remaining
            teams[team_choice]["items"].append({
                "name": item_name,
                "price": int(bid_price),
                "qty": int(qty)
            })
            data["log"].append(
                f"{datetime.now().isoformat(timespec='seconds')} — {team_choice} won {qty} × {item_name} @ {bid_price} (spent {total_cost})"
            )
            save_data(data)
            st.success(f"✅ Awarded {qty} × {item_name} to {team_choice}. Remaining: {new_remaining} credits")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export / Logs
    st.markdown("### 📊 Export & Logs")
    st.download_button(
        "📥 Download data.json",
        data=json.dumps(data, indent=2),
        file_name="data.json",
        mime="application/json",
        use_container_width=True
    )
    
    st.markdown("**Recent Activity:**")
    for line in data["log"][-20:]:
        st.code(line, language=None)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Reset
    st.markdown("### ⚠️ Danger Zone")
    st.warning("This will clear all team items, restore full credits, and delete the event log.")
    if st.button("🧹 Reset All Teams & Logs", type="secondary"):
        for name, info in teams.items():
            info["credits"] = data["starting_credits"]
            info["items"] = []
        data["log"] = []
        save_data(data)
        st.success("✅ Reset complete!")
        st.rerun()

# ---------------- Team UI ----------------
def team_ui():
    name = st.session_state.user
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    info = data["teams"][name]
    starting_credits = data.get("starting_credits", 1000)
    
    st.markdown(f'<h1 style="color: white;">🏆 Team Console — {name}</h1>', unsafe_allow_html=True)
    logout_ui()
    
    # Calculate stats
    total_spent = starting_credits - info["credits"]
    total_items = len(info["items"])
    avg_price = total_spent // total_items if total_items > 0 else 0
    credit_percentage = (info["credits"] / starting_credits) * 100
    
    # Determine status
    if credit_percentage > 60:
        status = "Healthy"
        status_class = "status-success"
    elif credit_percentage > 30:
        status = "Moderate"
        status_class = "status-warning"
    else:
        status = "Low Credits"
        status_class = "status-danger"
    
    # Main Credits Display with Status
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<div class="metric-card"><p class="metric-value">{info["credits"]}<span class="status-badge {status_class}">{status}</span></p><p class="metric-label">Credits Remaining</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Credit Usage Progress Bar
    st.markdown('<p class="progress-label">💰 Credit Usage</p>', unsafe_allow_html=True)
    spent_percentage = (total_spent / starting_credits) * 100
    st.markdown(f'''
    <div class="progress-container">
        <div class="progress-bar" style="width: {spent_percentage}%;">
            {total_spent} / {starting_credits} ({spent_percentage:.0f}%)
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Statistics Cards
    st.markdown("### 📊 Your Statistics")
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.markdown(f'''
        <div class="small-metric-card">
            <p class="small-metric-value">{total_spent}</p>
            <p class="small-metric-label">Total Spent</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown(f'''
        <div class="small-metric-card">
            <p class="small-metric-value">{total_items}</p>
            <p class="small-metric-label">Items Won</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown(f'''
        <div class="small-metric-card">
            <p class="small-metric-value">{avg_price}</p>
            <p class="small-metric-label">Avg Price</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Items Won
    st.markdown("### 📦 Your Items Won")
    if info["items"]:
        for it in info["items"]:
            st.markdown(f'<div class="item-card"><span class="item-name">{it["qty"]} × {it["name"]}</span><span class="item-price">@ {it["price"]} credits</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">🎯 No items yet. Keep bidding in the auction to build your product!</div>', unsafe_allow_html=True)
    
    st.info("💡 Bidding is conducted live by the host. This page is your private ledger with real-time updates.")
    
    # Auto-refresh
    st.caption("🔄 Auto-refreshing every 10 seconds for live updates...")
    time.sleep(10)
    st.rerun()

# ---------------- Router ----------------  
if st.session_state.user is None:
    login_ui()
else:
    if st.session_state.role == "admin":
        admin_ui()
    else:
        team_ui()