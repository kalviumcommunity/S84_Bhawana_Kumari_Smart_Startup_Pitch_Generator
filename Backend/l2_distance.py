import numpy as np

def l2_distance(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.linalg.norm(vec1 - vec2)

# Example usage
if __name__ == "__main__":
    embedding1 = [0.1] * 384
    embedding2 = [0.2] * 384
    distance = l2_distance(embedding1, embedding2)
    print("L2 (Euclidean) distance:", distance)