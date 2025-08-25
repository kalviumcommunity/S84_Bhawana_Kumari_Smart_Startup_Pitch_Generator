import numpy as np

def dot_product_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2)

# Example usage
if __name__ == "__main__":
    embedding1 = [0.1] * 384
    embedding2 = [0.2] * 384
    similarity = dot_product_similarity(embedding1, embedding2)
    print("Dot product similarity:", similarity)