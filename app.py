import streamlit as st
import json
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Bid2Build Auction Console", layout="wide")

DATA_PATH = Path("data.json")

def load_data():
    if not DATA_PATH.exists():
        st.error("data.json not found. Create it in the same folder as app.py.")
        st.stop()
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

def save_data(d):
    DATA_PATH.write_text(json.dumps(d, indent=2), encoding="utf-8")

data = load_data()

# ---------------- Session ----------------
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

# ---------------- Login ----------------
def login_ui():
    st.title("Bid2Build — Auction Console")
    st.caption("Admin records the winning bids; teams see their own credits and items only.")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Admin Login")
        a_user = st.text_input("Username", key="a_user")
        a_pw = st.text_input("Password", type="password", key="a_pw")
        if st.button("Login as Admin"):
            if a_user == data["admin"]["username"] and a_pw == data["admin"]["password"]:
                st.session_state.user = a_user
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("Invalid admin credentials.")

    with col2:
        st.subheader("Team Login")
        t_user = st.text_input("Team username (exact)", key="t_user")
        t_pw = st.text_input("Team password", type="password", key="t_pw")
        if st.button("Login as Team"):
            teams = data["teams"]
            if t_user in teams and t_pw == teams[t_user]["password"]:
                st.session_state.user = t_user
                st.session_state.role = "team"
                st.rerun()
            else:
                st.error("Invalid team login (check username & password).")

# ---------------- Admin UI ----------------
def admin_ui():
    st.title("Admin Dashboard")
    st.success("You control recording: select winning team, item, price, and quantity. Credits auto-deduct.")

    # Global settings
    st.markdown("### Global Settings")
    colA, colB = st.columns(2)
    with colA:
        new_step = st.number_input("Bid step (points)", min_value=1, value=int(data.get("bid_step", 50)))
        if st.button("Save bid step"):
            data["bid_step"] = int(new_step)
            save_data(data)
            st.toast("Saved bid step.")
    with colB:
        new_start = st.number_input("Starting credits (for NEW teams)", min_value=1, value=int(data.get("starting_credits", 1000)))
        if st.button("Save starting credits"):
            data["starting_credits"] = int(new_start)
            save_data(data)
            st.toast("Saved starting credits.")

    st.divider()

    # Team management
    st.markdown("### Teams & Passwords")
    st.caption("Reset passwords/credits, mark registered, or remove teams. (Usernames are case-sensitive.)")
    teams = data["teams"]

    for name, info in teams.items():
        with st.expander(f"{name} — Credits: {info['credits']} — Items: {len(info['items'])} — Registered: {info.get('registered', True)}"):
            c1, c2, c3, c4 = st.columns([2,2,2,2])
            with c1:
                st.write("Password:", f"`{info['password']}`")
                if st.button(f"Reset Password [{name}]"):
                    import secrets, string
                    alpha = string.ascii_letters + string.digits
                    newpw = ''.join(secrets.choice(alpha) for _ in range(8))
                    info["password"] = newpw
                    save_data(data)
                    st.info(f"New password for {name}: {newpw}")
            with c2:
                if st.button(f"Reset Credits → {data['starting_credits']} [{name}]"):
                    info["credits"] = data["starting_credits"]
                    save_data(data)
                    st.success("Credits reset.")
            with c3:
                reg = st.checkbox("Registered", value=info.get("registered", True), key=f"reg_{name}")
                if reg != info.get("registered", True):
                    info["registered"] = reg
                    save_data(data)
                    st.info("Updated registration status.")
            with c4:
                if st.button(f"Remove Team [{name}]"):
                    del teams[name]
                    save_data(data)
                    st.warning(f"Removed team {name}.")
                    st.experimental_rerun()

            st.write("Items Won:")
            if info["items"]:
                for it in info["items"]:
                    st.write(f"- {it['qty']} × {it['name']} @ {it['price']} credits")
            else:
                st.caption("No items yet.")

    st.divider()

    # Add/Update team
    st.markdown("### Add / Update Team")
    new_name = st.text_input("Team username (no spaces recommended)")
    new_pw = st.text_input("Set password (leave blank to auto-generate)")
    if st.button("Add / Update Team"):
        if new_name.strip() == "":
            st.error("Team name required.")
        else:
            if new_name not in teams:
                teams[new_name] = {
                    "password": new_pw or "Temp1234",
                    "credits": data["starting_credits"],
                    "items": [],
                    "registered": True
                }
                save_data(data)
                st.success(f"Added team {new_name}. Password: {teams[new_name]['password']}")
            else:
                if new_pw:
                    teams[new_name]["password"] = new_pw
                    save_data(data)
                    st.info(f"Updated password for {new_name}.")

    st.divider()

    # Record auction result
    st.markdown("### Record Auction Result (Manual)")
    item_name = st.text_input("Item name (as shown in PPT)", placeholder="e.g., ESP32 DevKit V1")
    bid_price = st.number_input("Winning bid (credits per unit)", min_value=1, value=int(data.get("bid_step", 50)))
    qty = st.number_input("Quantity awarded", min_value=1, value=1, step=1)
    team_choice = st.selectbox("Winning Team", options=list(teams.keys()))
    if st.button("Assign Item to Team (Deduct Credits)"):
        total_cost = int(bid_price) * int(qty)
        if teams[team_choice]["credits"] < total_cost:
            st.error(f"Not enough credits. {team_choice} has {teams[team_choice]['credits']} credits.")
        else:
            teams[team_choice]["credits"] -= total_cost
            teams[team_choice]["items"].append({"name": item_name, "price": int(bid_price), "qty": int(qty)})
            data["log"].append(
                f"{datetime.now().isoformat(timespec='seconds')} — {team_choice} won {qty} × {item_name} @ {bid_price} (spent {total_cost})"
            )
            save_data(data)
            st.success(f"Awarded {qty} × {item_name} to {team_choice}. Remaining credits: {teams[team_choice]['credits']}")

    st.divider()

    # Export / Logs
    st.markdown("### Export / Logs")
    st.download_button(
        "Download current data.json",
        data=json.dumps(data, indent=2),
        file_name="data.json",
        mime="application/json"
    )
    st.write("Recent activity:")
    for line in data["log"][-20:]:
        st.code(line)

# ---------------- Team UI ----------------
def team_ui():
    name = st.session_state.user
    info = data["teams"][name]
    st.title(f"Team Console — {name}")
    st.metric("Credits Remaining", info["credits"])
    st.write("Items Won:")
    if info["items"]:
        for it in info["items"]:
            st.write(f"- {it['qty']} × {it['name']} @ {it['price']} credits")
    else:
        st.caption("No items yet. Keep bidding in the room!")
    st.info("Bidding is conducted live by the host. This page is your private ledger.")

# ---------------- Router ----------------
if st.session_state.user is None:
    login_ui()
else:
    if st.session_state.role == "admin":
        admin_ui()
    else:
        team_ui()
