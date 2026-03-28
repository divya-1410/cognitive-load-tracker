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

        # Graph
        plt.figure()
        plt.plot(st.session_state.time_points, st.session_state.focus_levels, marker='o')
        plt.xlabel("Time (minutes)")
        plt.ylabel("Focus Level")
        plt.title("Cognitive Load Tracker")
        st.pyplot(plt)