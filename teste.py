import ollama

# Parte 1: embedding
frase = "Oi?"

resposta_emb = ollama.embed(model="embeddinggemma", input=frase)
vetor = resposta_emb["embeddings"][0]

print("Tamanho do vetor:", len(vetor))
print("Primeiros 5 números:", vetor[:5])

# Parte 2: geração
resposta_chat = ollama.chat(
    model="phi4-mini",
    messages=[{"role": "user", "content": "Explique em uma frase o que é um banco de dados vetorial."}],
)

print("Resposta do modelo:", resposta_chat["message"]["content"])