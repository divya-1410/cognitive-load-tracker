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

# End session
if st.button("End Session"):
    if st.session_state.focus_levels:
        avg = sum(st.session_state.focus_levels) / len(st.session_state.focus_levels)

        st.write(f"### Average Focus: {avg:.2f}")

        # Detect fatigue
        fatigue_point = None
        for i in range(1, len(st.session_state.focus_levels)):
            if st.session_state.focus_levels[i] < st.session_state.focus_levels[i-1]:
                fatigue_point = st.session_state.time_points[i]
                break

        # Graph
        plt.figure()
        plt.plot(st.session_state.time_points, st.session_state.focus_levels, marker='o')

        # Highlight fatigue point
        if fatigue_point:
            plt.axvline(x=fatigue_point, linestyle='--')

        plt.xlabel("Time (minutes)")
        plt.ylabel("Focus Level")
        plt.title("Cognitive Performance Analyzer")

        st.pyplot(plt)

        # Insight message
        if fatigue_point:
            st.warning(f"⚠️ Fatigue starts around {fatigue_point} minutes")
        else:
            st.success("✅ No fatigue detected")