import numpy as np
from openai import OpenAI

class Embedder:
    def __init__(self, client: OpenAI | None = None, model: str = "text-embedding-3-small"):
        self._client = client or OpenAI()
        self._model = model

    def embed(self, text: str) -> bytes:
        response = self._client.embeddings.create(model=self._model, input=text)
        vector = np.array(response.data[0].embedding, dtype=np.float32)
        return vector.tobytes()
