import streamlit as st

def main():
    st.title("SQL Chat (LLM-powered)")

    st.write(
        "Ask a question about your data in natural language. "
        "The app will translate it into SQL and show the results."
    )

    question = st.text_area(
        "Your question:",
        placeholder="Example: Which customers placed the most orders last month?"
    )

    if st.button("Run"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            # For now, this is just a placeholder.
            st.info("Here is where the LLM-generated SQL will appear:")
            st.code("-- SQL will appear here", language="sql")

            st.info("And here is where the query results will be displayed.")
            st.write("(We will connect this to your database in the next step.)")


if __name__ == "__main__":
    main()