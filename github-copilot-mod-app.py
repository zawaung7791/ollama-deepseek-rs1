import streamlit as st
import ollama

st.set_page_config(layout="wide")
st.title("Ollama, DeepSeek R1 and Streamlit")

# CSS for scrolling
st.markdown(
    """
    <style>
    .response-area {
        overflow-y: auto;
        max-height: 600px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Enter your query:")
    user_input = st.text_area("Your Message", height=200)
    col1_buttons = st.columns([1, 1]) # Columns for buttons
    with col1_buttons[0]:
        send_button = st.button("Generate")
    with col1_buttons[1]:
        stop_button = st.button("Stop")

with col2:
    st.subheader("Response:")
    response_area = st.empty()

# Initialize session state for stop flag
if "stop_generating" not in st.session_state:
    st.session_state.stop_generating = False

if stop_button:
    st.session_state.stop_generating = True  # Set the flag if the Stop button is clicked

if send_button and user_input.strip():
    st.session_state.stop_generating = False  # Reset the flag when send is clicked
    try:
        response_stream = ollama.chat(
            model="deepseek-r1:14b",
            messages=[{"role": "user", "content": user_input}],
            stream=True,
        )

        full_response = ""
        for chunk in response_stream:
            if st.session_state.stop_generating:  # Check the flag in the loop
                break  # Exit the loop if Stop is clicked

            if "content" in chunk["message"]:
                content_chunk = chunk["message"]["content"]
                full_response += content_chunk
                response_area.markdown(f"<div class='response-area'>{full_response}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    if not user_input.strip():
        st.warning("Please enter some text.")