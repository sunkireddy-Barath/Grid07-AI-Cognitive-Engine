from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

bots = {
    "Bot_A": "I believe AI and crypto will solve all human problems. I am highly optimistic about technology, Elon Musk, and space exploration. I dismiss regulatory concerns.",
    "Bot_B": "I believe late-stage capitalism and tech monopolies are destroying society. I am highly critical of AI, social media, and billionaires. I value privacy and nature.",
    "Bot_C": "I strictly care about markets, interest rates, trading algorithms, and making money. I speak in finance jargon and view everything through the lens of ROI."
}

bot_names = list(bots.keys())
bot_descriptions = list(bots.values())

embeddings = model.encode(bot_descriptions)
faiss.normalize_L2(embeddings)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

def route_post_to_bots(post_content: str, threshold: float = 0.85):
    query = model.encode([post_content])
    faiss.normalize_L2(query)
    
    similarities, indices = index.search(query, 3)
    matched = []
    
    for i in range(len(bot_names)):
        score = np.dot(query[0], embeddings[i])
        print(f"Bot: {bot_names[i]}, Score: {score:.4f}")
        if score > threshold:
            matched.append(bot_names[i])
            
    return matched

if __name__ == "__main__":
    post = "OpenAI just released a new model that might replace junior developers."
    print("Matched Bots:", route_post_to_bots(post))
