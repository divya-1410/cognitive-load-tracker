import streamlit as st
import matplotlib.pyplot as plt
import json
import os
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Cognitive Load Tracker", layout="wide")

# ---------------- FORCE BACKGROUND (BULLETPROOF) ----------------
st.markdown("""
<style>

/* FULL SCREEN BACKGROUND LAYER */
.background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;

    background: linear-gradient(
        135deg,
        #F1EDE1,
        #E4F0E2,
        #D6E8D4
    );

    z-index: -999;
}

/* Remove default white */
[data-testid="stAppViewContainer"] {
    background: transparent;
}

/* Remove header */
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    background: transparent;
}

/* MAIN CARD */
.block-container {
    background: rgba(255, 255, 255, 0.55);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(10px);
}

/* TEXT */
h1 {
    color: #344E41;
    text-align: center;
}
h2, h3 {
    color: #588157;
}

/* BUTTON */
.stButton>button {
    background-color: #A3B18A;
    color: white;
    border-radius: 10px;
    height: 3em;
}

/* FONT */
html, body, [class*="css"] {
    font-family: Georgia, serif;
}

</style>

<div class="background"></div>
""", unsafe_allow_html=True)

# ---------------- LOGO ----------------
def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "logo.png")

logo_base64 = get_base64_image(logo_path)

if logo_base64:
    st.markdown(f"""
    <style>
    .logo-container {{
        position: fixed;
        top: 20px;
        right: 25px;
        z-index: 9999;
    }}
    .logo-container img {{
        width: 65px;
    }}
    </style>

    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    """, unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🌿 Cognitive Load Tracker")
st.markdown("#### Study calmly. Grow steadily. 🤍")

# ---------------- LOGIN ----------------
user = st.text_input("Enter your name")

if user:
    filename = f"{user}.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = {"sessions": [], "planner": []}

    st.success(f"Welcome, {user} 🌸")

    tab1, tab2, tab3 = st.tabs(["📊 Tracker", "📈 Progress", "📚 Planner"])

    # ================= TRACKER =================
    with tab1:
        st.subheader("Track Your Focus 🌿")

        if "focus_levels" not in st.session_state:
            st.session_state.focus_levels = []
            st.session_state.time_points = []
            st.session_state.time = 0

        mood = st.selectbox("Mood", ["😊 Calm", "😐 Neutral", "😣 Stressed"])

        focus = st.slider("Focus Level", 1, 5, 3)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("➕ Add Entry"):
                st.session_state.focus_levels.append(focus)
                st.session_state.time_points.append(st.session_state.time)
                st.session_state.time += 10

        with col2:
            if st.button("⏹ End Session"):
                if st.session_state.focus_levels:

                    avg = sum(st.session_state.focus_levels) / len(st.session_state.focus_levels)

                    fatigue = None
                    for i in range(1, len(st.session_state.focus_levels)):
                        if st.session_state.focus_levels[i] < st.session_state.focus_levels[i-1]:
                            fatigue = st.session_state.time_points[i]
                            break

                    data["sessions"].append(avg)
                    with open(filename, "w") as f:
                        json.dump(data, f)

                    st.metric("Average Focus", f"{avg:.2f}")

                    if fatigue:
                        st.warning(f"Fatigue at {fatigue} mins")
                    else:
                        st.success("No fatigue detected")

                    if avg < 3:
                        st.info("Try shorter sessions with breaks")
                    else:
                        st.info("You're doing great")

                    # Graph
                    plt.figure()
                    plt.plot(st.session_state.time_points, st.session_state.focus_levels, marker='o')
                    plt.xlabel("Time")
                    plt.ylabel("Focus")
                    st.pyplot(plt)

    # ================= PROGRESS =================
    with tab2:
        if data["sessions"]:
            st.line_chart(data["sessions"])
        else:
            st.info("No data yet")

    # ================= PLANNER =================
    with tab3:
        subjects = st.text_input("Subjects (comma separated)")

        if st.button("Generate Plan"):
            subject_list = subjects.split(",")

            plan = []
            time = 30

            for sub in subject_list:
                plan.append(f"{sub.strip()} - {time} mins")
                time += 10

            data["planner"] = plan

            with open(filename, "w") as f:
                json.dump(data, f)

        if data["planner"]:
            for p in data["planner"]:
                st.write(p)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Made with calm energy 🌿")