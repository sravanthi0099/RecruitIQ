import faiss
import numpy as np


class FAISSService:

    def __init__(self):
        self.dimension = 384

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        self.candidate_ids = []

    def add_candidate(
        self,
        candidate_id,
        embedding
    ):
        vector = np.array(
            [embedding],
            dtype=np.float32
        )

        self.index.add(vector)

        self.candidate_ids.append(
            candidate_id
        )

    def search(
        self,
        embedding,
        k=5
    ):
        vector = np.array(
            [embedding],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            vector,
            k
        )

        results = []

        for distance, idx in zip(
            distances[0],
            indices[0]
        ):

            if idx < len(self.candidate_ids):

                results.append(
                    {
                        "candidate_id":
                            self.candidate_ids[idx],

                        "distance":
                            float(distance)
                    }
                )

        return results


faiss_service = FAISSService()