import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# List of charts to display
def generate_chart(chart_index):
    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    
    if chart_index == 0:
        ax.plot(x, np.sin(x), label='Sine Wave')
        ax.set_title("Sine Wave")
    elif chart_index == 1:
        ax.plot(x, np.cos(x), label='Cosine Wave', color='r')
        ax.set_title("Cosine Wave")
    elif chart_index == 2:
        ax.plot(x, np.tan(x), label='Tangent Wave', color='g')
        ax.set_ylim(-5, 5)
        ax.set_title("Tangent Wave (Limited)")
    
    ax.legend()
    st.pyplot(fig)

# Initialize session state
if 'chart_index' not in st.session_state:
    st.session_state.chart_index = 0

# Layout for buttons and chart
col1, col2, col3 = st.columns([1, 5, 1])
with col1:
    if st.session_state.chart_index > 0:
        if st.button("⬅ Previous"):
            st.session_state.chart_index -= 1
            st.rerun()
with col2:
    generate_chart(st.session_state.chart_index)
with col3:
    if st.session_state.chart_index < 2:
        if st.button("Next ➡"):
            st.session_state.chart_index += 1
            st.rerun()
