import json
import chromadb
from chromadb.utils import embedding_functions
from config.settings import CHROMA_DB_PATH, COLLECTION_NAME, PAST_INCIDENTS_PATH


def get_vectorstore():
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    return collection


def seed_incidents():
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    try:
        client.delete_collection(COLLECTION_NAME)
        print("Cleared old collection.")
    except:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn
    )

    with open(PAST_INCIDENTS_PATH, "r") as f:
        incidents = json.load(f)

    documents = []
    metadatas = []
    ids = []

    for incident in incidents:
        doc_text = f"""
        Title: {incident['title']}
        Symptoms: {incident['symptoms']}
        Root Cause: {incident['root_cause']}
        Fix: {incident['fix']}
        Tags: {', '.join(incident['tags'])}
        """.strip()

        documents.append(doc_text)
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

    print(f"Seeded {len(incidents)} incidents with SentenceTransformer embeddings.")


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

    print("\nTesting search...")
    results = search_similar_incidents("memory leak OOM container crash")
    for r in results:
        print(f"\n{r['id']} — {r['title']} (score: {r['similarity_score']})")
        print(f"Fix: {r['fix']}")