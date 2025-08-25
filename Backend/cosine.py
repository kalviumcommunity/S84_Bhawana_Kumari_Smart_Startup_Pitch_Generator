import numpy as np

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

# Example usage
if __name__ == "__main__":
    embedding1 = [0.1] * 384
    embedding2 = [0.2] * 384
    similarity = cosine_similarity(embedding1, embedding2)
    print("Cosine similarity:", similarity)