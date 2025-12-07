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

import streamlit as st
from openai import OpenAI  # nuevo import para usar el LLM

# Cliente usando tu API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Aquí luego pondrás tu esquema real
SCHEMA_DESCRIPTION = """
TABLE customers (customer_id, name, email, city)
TABLE orders (order_id, customer_id, order_date, total_amount)
"""

SYSTEM_PROMPT = """
You are an assistant that translates natural-language questions into safe MySQL queries.

Rules:
- Use only the tables and columns that exist in this schema.
- Never use SELECT *.
- Assume user input is untrusted and avoid SQL injection.
- Prefer simple SELECT queries with JOINs where needed.
- Add LIMIT 50 when the query could return many rows.
- If the question cannot be answered with this schema, say so.
Return ONLY the SQL query, nothing else.
"""

def generate_sql_from_question(question: str) -> str:
    user_message = f"Schema:\n{SCHEMA_DESCRIPTION}\n\nUser question:\n{question}"

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )

    sql = response.choices[0].message.content.strip()
    return sql