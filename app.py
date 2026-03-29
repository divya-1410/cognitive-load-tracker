import streamlit as st
import matplotlib.pyplot as plt
import json
import os
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Cognitive Load Tracker", layout="centered")

# ---------------- SAFE LOGO LOADING ----------------
def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "logo.png.png")
logo_base64 = get_base64_image(logo_path)

# ---------------- STYLING ----------------
st.markdown("""
<style>
@keyframes float {
  0% { transform: translateY(0px); opacity: 0.8; }
  50% { transform: translateY(-20px); opacity: 0.4; }
  100% { transform: translateY(0px); opacity: 0.8; }
}

.sparkle {
  position: fixed;
  width: 10px;
  height: 10px;
  background: #ffffff;
  border-radius: 50%;
  opacity: 0.6;
  animation: float 6s infinite ease-in-out;
}

.sparkle:nth-child(1) { top: 20%; left: 10%; animation-delay: 0s; }
.sparkle:nth-child(2) { top: 50%; left: 80%; animation-delay: 2s; }
.sparkle:nth-child(3) { top: 70%; left: 30%; animation-delay: 4s; }
.sparkle:nth-child(4) { top: 30%; left: 60%; animation-delay: 1s; }
</style>

<div class="sparkle"></div>
<div class="sparkle"></div>
<div class="sparkle"></div>
<div class="sparkle"></div>
""", unsafe_allow_html=True)
.stButton>button {
    background-color: #E0BBE4;
    color: black;
    border-radius: 12px;
    height: 3em;
    font-size: 15px;
    border: none;
    transition: 0.3s ease;
}

.stButton>button:hover {
    background-color: #D291BC;
    transform: scale(1.05);
}
.block-container {
    background: rgba(255, 255, 255, 0.5);
    padding: 2rem;
    border-radius: 25px;
    backdrop-filter: blur(15px);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.1);
}

# Show logo ONLY if exists (no error)
if logo_base64:
    st.markdown(f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    """, unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🌸 Cognitive Load Tracker")
st.markdown("#### Study softly. Grow deeply. 💭")
st.markdown("#### 🌙 Little steps today, big dreams tomorrow")

# ---------------- LOGIN ----------------
user = st.text_input("Enter your name")

if user:
    filename = f"{user}.json"

    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = {"sessions": [], "planner": []}

    st.success(f"Welcome, {user} 💖")

    tab1, tab2, tab3 = st.tabs(["📊 Tracker", "📈 Progress", "📚 Planner"])

    # ================= TRACKER =================
    with tab1:
        st.subheader("Track Your Focus 🌷")

        if "focus_levels" not in st.session_state:
            st.session_state.focus_levels = []
            st.session_state.time_points = []
            st.session_state.time = 0

        mood = st.selectbox("How are you feeling today?", ["😊 Calm", "😐 Neutral", "😣 Stressed"])

        if mood == "😣 Stressed":
            st.info("Take it slow today. You're doing enough 💗")

        focus = st.slider("Focus Level", 1, 5, 3)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("➕ Add Entry"):
                st.session_state.focus_levels.append(focus)
                st.session_state.time_points.append(st.session_state.time)
                st.session_state.time += 10
                st.success("Added 💫")

        with col2:
            if st.button("⏹ End Session"):
                if st.session_state.focus_levels:

                    avg = sum(st.session_state.focus_levels) / len(st.session_state.focus_levels)

                    fatigue = None
                    for i in range(1, len(st.session_state.focus_levels)):
                        if st.session_state.focus_levels[i] < st.session_state.focus_levels[i-1]:
                            fatigue = st.session_state.time_points[i]
                            break

                    max_focus = max(st.session_state.focus_levels)
                    peak_time = st.session_state.time_points[
                        st.session_state.focus_levels.index(max_focus)
                    ]

                    # Save session
                    data["sessions"].append(avg)
                    with open(filename, "w") as f:
                        json.dump(data, f)

                    st.markdown("## 📊 Session Summary")

                    st.metric("Average Focus", f"{avg:.2f}")
                    st.metric("Peak Time", f"{peak_time} mins")

                    if fatigue:
                        st.error(f"Fatigue detected at {fatigue} mins")
                    else:
                        st.success("No fatigue detected 💖")

                    # Recommendation
                    if avg < 2:
                        suggestion = "Rest well. Start with 15 min sessions 🌸"
                    elif avg < 3:
                        suggestion = "Try 25 min sessions with breaks 💭"
                    elif fatigue:
                        suggestion = f"Take a break before {fatigue} mins ⏳"
                    else:
                        suggestion = "You're doing amazing. Keep going 💜"

                    st.info(suggestion)

                    # Study Plan Suggestion
                    if avg < 3:
                        plan = "Light study + frequent breaks"
                    elif avg < 4:
                        plan = "Moderate sessions with revision"
                    else:
                        plan = "Deep work sessions for difficult topics"

                    st.markdown("### 📚 Suggested Study Plan")
                    st.success(plan)

                    # Graph
                    plt.figure()
                    plt.plot(st.session_state.time_points, st.session_state.focus_levels, marker='o')
                    plt.xlabel("Time (minutes)")
                    plt.ylabel("Focus Level")
                    plt.title("Focus Trend")
                    plt.grid()
                    st.pyplot(plt)

    # ================= PROGRESS =================
    with tab2:
        st.subheader("Your Progress 🌷")

        if data["sessions"]:
            st.line_chart(data["sessions"])
        else:
            st.info("No sessions recorded yet 💭")

    # ================= PLANNER =================
    with tab3:
        st.subheader("Plan Your Day 🌸")

        subjects = st.text_input("Enter subjects (comma separated)")

        if st.button("Generate Plan"):
            subject_list = subjects.split(",")

            plan = []
            time = 30

            for sub in subject_list:
                plan.append(f"✨ {sub.strip()} - {time} mins")
                time += 10

            data["planner"] = plan

            with open(filename, "w") as f:
                json.dump(data, f)

        if data["planner"]:
            st.markdown("### Your Plan 💖")
            for p in data["planner"]:
                st.write(p)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Made with calm energy 🌷")