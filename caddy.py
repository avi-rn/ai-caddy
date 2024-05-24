import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from masters import populate_db, scrape_masters
import streamlit as st

def query_ai_caddy(question):
  holes = scrape_masters()
  col = populate_db(holes)

  client = chromadb.Client()


  collection = client.get_collection("masters1")

  results = collection.query(
      query_texts=[question], # Chroma will embed this for you
      n_results=3# how many results to return
  )
  # Extract documents from the data
  documents_list = results['documents']

  # Convert the list of documents into a single string
  documents_string = '\n'.join(documents_list[0])

  query = f"""Use the below info on the relevant holes at Augusta National Golf Course to answer the subsequent question. If the answer cannot be found, write "I don't know."

  Info:
  \"\"\"
  {documents_string}
  \"\"\"

  Question: {question}"""

  load_dotenv()

  client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Act as a golf caddy to minimize a player's strokes on Augusta National Golf Course. Be decisive in your advice. Push back against risky shots."},
      {"role": "user", "content": query}
    ]
  )

  return completion.choices[0].message.content

# Inject custom CSS for background color
page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #036635;
    color: #FFCC00;
}

[data-testid="stHeader"] {
    background-color: #036635;
    color: #FFCC00;
}

[data-testid="stSidebar"] {
    background-color: #036635;
    color: #FFCC00;
}

h2, h3, p, div {
    color: #FFCC00;
}

/* Update button styling */
button.streamlit-button {
    background-color: #FFCC00 !important; /* Yellow background */
    color: #036635 !important; /* Green text */
}

/* Update button hover styling */
button.streamlit-button:hover {
    background-color: #FFCC00 !important; /* Yellow background */
    color: #036635 !important; /* Green text */
}

/* Update button active styling */
button.streamlit-button:active {
    background-color: #FFCC00 !important; /* Yellow background */
    color: #036635 !important; /* Green text */
}

/* Update button focus styling */
button.streamlit-button:focus {
    background-color: #FFCC00 !important; /* Yellow background */
    color: #036635 !important; /* Green text */
}
</style>
"""

# Add the JavaScript and CSS code to the Streamlit app
st.markdown(page_bg_css, unsafe_allow_html=True)

# Streamlit UI
st.title("AI Caddy @ Augusta National")
st.write("Ask for advice on any shot about Augusta National Golf Course and hear from our AI Caddy. The more information you provide, the better the response will be.")
st.write("Example: I am teeing off on Hole 1 - Tea Olive, what club should I hit? I am a 15 handicapper who tends to slice it.")

# User input
user_input = st.text_input("Ask your question here:", key="user_input")
prev_qry = ""


try:

  if st.button("Ask") or (prev_qry != user_input):
    if user_input:
        prev_query = user_input
        response = query_ai_caddy(user_input)
        st.markdown("**AI Caddy's Advice**")
        st.write(response)

except Exception as e:
    st.error("An error occurred while processing your request. Please try again later.")
    st.write(e)  # Optionally, write the error details for debugging

