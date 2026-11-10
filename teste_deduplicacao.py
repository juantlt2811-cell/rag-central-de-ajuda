import re
t = "R$ 30,00. (fonte: a.md) (fonte: a.md) Outra frase. (fonte: a.md)"
print(re.sub(r"(\(fonte: [^)]*\))(?:\s*\1)+", r"\1", t))