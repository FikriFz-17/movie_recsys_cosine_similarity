# Movie Recommendation Using Cosine Similarity

## Formula
### 1. Cosine Similarity
Cosine Similarity measures the cosine of the angle between two vectors, representing their similarity:

$$
\text{Cosine Similarity} (A, B) = \frac{A \cdot B}{\|\|A\|\| \cdot \|\|B\|\|}
$$

Where:
- $$\( A \cdot B \)$$ is the dot product of vectors A and B
- $$\( \|\|A\|\|)$$ is the Euclidean norm (magnitude) of vector A
- $$\( \|\|B\|\|)$$ is the Euclidean norm (magnitude) of vector B


### 2. Term Frequency-Inverse Document Frequency (TF-IDF)
TF-IDF is used to weigh terms based on their importance in a document relative to a collection of documents.

$$
\text{TF-IDF} (t, d) = \text{TF} (t, d) \times \text{IDF} (t)
$$


