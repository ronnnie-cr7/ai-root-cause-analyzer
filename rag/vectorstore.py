import json
import chromadb
from chromadb.utils import embedding_functions
from config.settings import CHROMA_DB_PATH, COLLECTION_NAME, PAST_INCIDENTS_PATH


def get_vectorstore():
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()
    
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )
    
    return collection


def seed_incidents():
    collection = get_vectorstore()
    
    # re-seed
    if collection.count() > 0:
        collection.delete(ids=collection.get()["ids"])
        print("Cleared old incidents. Re-seeding...")
    
    with open(PAST_INCIDENTS_PATH, "r") as f:
        incidents = json.load(f)
    
    documents = []
    metadatas = []
    ids = []
    
    for incident in incidents:
        # What we search against — combine key fields into one searchable string
        doc_text = f"""
        Title: {incident['title']}
        Symptoms: {incident['symptoms']}
        Root Cause: {incident['root_cause']}
        Fix: {incident['fix']}
        Tags: {', '.join(incident['tags'])}
        """
        
        documents.append(doc_text.strip())
        metadatas.append({
            "id": incident["id"],
            "title": incident["title"],
            "date": incident["date"],
            "root_cause": incident["root_cause"],
            "fix": incident["fix"]
        })
        ids.append(incident["id"])
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Seeded {len(incidents)} incidents into ChromaDB.")


def search_similar_incidents(query: str, n_results: int = 3):
    collection = get_vectorstore()
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    similar = []
    for i in range(len(results["ids"][0])):
        similar.append({
            "id": results["ids"][0][i],
            "title": results["metadatas"][0][i]["title"],
            "date": results["metadatas"][0][i]["date"],
            "root_cause": results["metadatas"][0][i]["root_cause"],
            "fix": results["metadatas"][0][i]["fix"],
            "similarity_score": round(1 - results["distances"][0][i], 2)
        })
    
    return similar


if __name__ == "__main__":
    seed_incidents()
    
    # Quick test
    print("\nTesting search...")
    results = search_similar_incidents("memory leak OOM container crash")
    for r in results:
        print(f"\n{r['id']} — {r['title']} (score: {r['similarity_score']})")
        print(f"Fix: {r['fix']}")