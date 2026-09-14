from unittest.mock import MagicMock
import numpy as np
from runbook.memory.embedder import Embedder

def test_embed_returns_packed_float32_bytes():
    client = MagicMock()
    client.embeddings.create.return_value = MagicMock(
        data=[MagicMock(embedding=[0.1, 0.2, 0.3])]
    )
    embedder = Embedder(client=client)

    result = embedder.embed("some text")
    vector = np.frombuffer(result, dtype=np.float32)

    assert vector.shape == (3,)
    assert np.allclose(vector, [0.1, 0.2, 0.3], atol=1e-6)
