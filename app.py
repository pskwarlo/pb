import streamlit as st

from main import get_response


def chat_with_user(session_id):
    st.title("DokuWiki Chat")
    st.write("Aplikacja może popełniać błędy. Weryfikuj ważne infromacje!")
    user_input = st.text_input("Ty: ", "")

    if user_input:
        response = get_response(session_id, user_input)
        st.write(f"AI: {response}")


if __name__ == "__main__":
    chat_with_user("session_1")
