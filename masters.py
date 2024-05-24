from bs4 import BeautifulSoup
import requests
import chromadb
import uuid

def scrape_masters():

    holes = []

    # URL of the webpage to scrape
    url = "https://www.golfpass.com/travel-advisor/articles/augusta-national-golf-club-hole-by-hole-guide-masters-tournament"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the div elements with class "Enhancement"
    enhancements = soup.find_all("div", class_="Enhancement")

    # Iterate over the enhancements
    for enhancement in enhancements:
        # Find the h2 element within the enhancement
        h2 = enhancement.find("h2")
        # Check if the h2 element exists and its text starts with "Hole"
        if h2 and h2.text.startswith("Hole"):
            # Print the text of the h2 element
            cur_hole = ""
            cur_hole = cur_hole + h2.text
            # Find the adjacent p element containing the hole description
            description = enhancement.find_next_sibling("p")
            # Check if the description exists
            if description:
                # Print the text of the description
                cur_hole = cur_hole + " " + description.text.strip()
                #print(cur_hole)
                holes.append(cur_hole)
            #print()  # Add a newline for better readability
            

    return holes

def extract_hole_data(raw_data):
    parts = raw_data.split(' - ')

    # Extract hole number, par, and length
    hole_info = parts[0].split(': ')
    hole_number = hole_info[0].split()[1]
    par = parts[1].split(',')[0].split('Par')[1]
    length = parts[1].split('yards')[0].split(',')[1]
    
    # Extract description
    description = parts[1].split('yards')[1]
    
    return {
        "hole_number": hole_number,
        "par": par,
        "length": length,
        "description": description
    }

def populate_db(docs):

    # Initialize ChromaDB connection
    chroma_client = chromadb.Client()

    # Create a collection for the hole descriptions
    collection_name = "masters1"

    # Function to check if a collection exists
    def collection_exists(client, name):
        collections = client.list_collections()
        return any(collection.name == name for collection in collections)

    # Check if the collection exists
    if collection_exists(chroma_client, collection_name):
        collections = chroma_client.get_collection(name=collection_name)
        print("collection exists")
    else: 
        # Collection does not exist, create it
        collections = chroma_client.create_collection(collection_name)
        print("collection created")


    # Insert data into the collection
    hole_ids = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18"]

    collections.add(documents=docs, ids=hole_ids)

    return collection_name



def main():

    holes = scrape_masters()

    # docs = []

    # for i in holes:
    #     docs.append(extract_hole_data(i))

    # for i in docs:
    #     print(i)


    col = populate_db(holes)
    print(col)
    chroma_client = chromadb.Client()
    collection = chroma_client.get_collection(name=col)
    results = collection.query(
        query_texts=["What club should I hit on Hole 1: Tea Olive"], # Chroma will embed this for you
        n_results=2 # how many results to return
    )
    print(results)

    



if __name__ == "__main__":
    main()