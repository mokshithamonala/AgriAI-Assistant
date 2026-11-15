from vector_engine import retrieve_context

if __name__ == "__main__":
    print("--- STEP 1: Testing Retrieval Query Contract ---")
    query = "disease"
    
    # Using the exact function specified in the contract!
    results = retrieve_context(query, k=2)
    
    print(f"\n🔍 Search query: '{query}'")
    print(f"📚 Retrieved {len(results)} matches:\n")
    
    for i, doc in enumerate(results, start=1):
        source = doc.metadata.get("source", "Unknown")
        print(f"[Match {i}] Source: {source}")
        print(f"Content: {doc.page_content[:300]}...\n")