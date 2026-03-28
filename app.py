import streamlit as st
import matplotlib.pyplot as plt

st.title("🧠 Cognitive Load Tracker")

# Store data
if "focus_levels" not in st.session_state:
    st.session_state.focus_levels = []
    st.session_state.time_points = []
    st.session_state.time = 0

# Input
focus = st.number_input("Enter Focus Level (1-5)", min_value=1, max_value=5)

# Add entry
if st.button("Add Entry"):
    st.session_state.focus_levels.append(focus)
    st.session_state.time_points.append(st.session_state.time)
    st.session_state.time += 10
    st.success("Entry added!")

#END SESSION
if st.button("End Session"):
    if st.session_state.focus_levels:
        avg = sum(st.session_state.focus_levels) / len(st.session_state.focus_levels)

        # Fatigue detection
        fatigue_point = None
        for i in range(1, len(st.session_state.focus_levels)):
            if st.session_state.focus_levels[i] < st.session_state.focus_levels[i-1]:
                fatigue_point = st.session_state.time_points[i]
                break

        # Peak
        max_focus = max(st.session_state.focus_levels)
        peak_time = st.session_state.time_points[st.session_state.focus_levels.index(max_focus)]

        # --- Recommendations ---
        if avg < 2:
            suggestion = "Very low focus detected. Improve environment, reduce distractions, and get proper rest."

        elif avg < 3:
            suggestion = "Focus is below average. Try shorter sessions and take regular breaks."

        elif fatigue_point is not None:
            suggestion = f"Your focus drops around {fatigue_point} minutes. Take a break before this time."

        elif avg >= 4:
            suggestion = "Excellent focus! Maintain your current study pattern."

        else:
            suggestion = "Good consistency. Minor improvements can further boost performance."

        # --- Display ---
        st.write(f"### Average Focus: {avg:.2f}")
        st.write(f"🔥 Peak Focus Time: {peak_time} mins")
        st.write(f"⚠️ Fatigue Point: {fatigue_point if fatigue_point else 'Not Detected'}")

        st.write("### 💡 Recommendation:")
        st.success(suggestion)

        # Graph
        plt.figure()
        plt.plot(st.session_state.time_points, st.session_state.focus_levels, marker='o')
        plt.xlabel("Time (minutes)")
        plt.ylabel("Focus Level")
        plt.title("Cognitive Load Tracker")
        st.pyplot(plt)