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

  client = OpenAI()

  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Act as a golf caddy to minimize a player's strokes on Augusta National Golf Course"},
      {"role": "user", "content": query}
    ]
  )

  return completion.choices[0].message.content


# Streamlit UI
st.title("AI Golf Caddy @ Augusta National")
st.write("Ask for advice on any shot about Augusta National Golf Course and get advice from our AI Caddy.\nExample: I am teeing off on Hole 1 - Tea Olive, what club should I hit?")

# User input
user_question = st.text_input("Enter your question here:")

if st.button("Ask"):
    # Query AI Caddy and display response
    response = query_ai_caddy(user_question)
    st.write(response)