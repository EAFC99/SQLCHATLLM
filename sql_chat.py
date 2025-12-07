import streamlit as st
from openai import OpenAI

# Cliente con key desde secrets.toml
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Ejemplo de esquema - luego reemplázalo con tus tablas reales
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
- Add LIMIT 50 when appropriate.
- If the question cannot be answered with this schema, say so.
Return ONLY the SQL query, nothing else.
"""


def generate_sql_from_question(question: str) -> str:
    """Call the LLM and return SQL from the user's question."""
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


def main():
    st.title("SQL Chat (LLM-powered)")

    st.write(
        "Ask a question about your data in natural language. "
        "The app will translate it into SQL and display the generated query."
    )

    question = st.text_area(
        "Your question:",
        placeholder="Example: Which customers placed the most orders last month?"
    )

    if st.button("Run"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Asking the LLM to generate SQL..."):
                sql = generate_sql_from_question(question)

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            if not sql.lower().startswith("select"):
                st.warning(
                    "The LLM did not return a SELECT query.\n"
                    "It may be explaining why the question cannot be answered with this schema."
                )


if __name__ == "__main__":
    main()