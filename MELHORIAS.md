# Melhorias depois do TP

Este documento registra as melhorias feitas no projeto depois da entrega do TP da Aula 07. A versão entregue está na tag `v1-tp` (commit `d5b6bd8`) e o README descreve essa versão. Cada melhoria abaixo segue a mesma estrutura: problema medido, mudança, resultado antes e depois, e o que não melhorou.

Anotações dos tipos das variáveis e dos retorno das funções também foram adicionados

## v2: citação por número

### Problema medido

Os testes da rodada 2 devolviam as fontes mal formatadas, entregando com o final _md ao invés de .md que seria a indicação do tipo do arquivo. Nos testes 1 e 3, pelo menos uma fonte foi escrita mal formatada, enquanto no teste 4 todas foram terminadas com _md.

Para quem vai procurar essas fontes, vê-las com esse erro de escrita prejudica a análise dos documentos pelos usuários ou até mesmo por nós desenvolvedores.

### Ideia

Agora o modelo não escreve o nome todo do documento, ele apenas anota de forma numérica qual documento ele utilizou. Quem ficou responsável por escrever o documento é o código, trocando o número que o modelo escreveu pelo nome guardado nos metadados

### O que mudou no código

- `montar_contexto`: Adiciona os trechos recuperados a uma lista, numerando-os ao invés de escrevê-los diretamente.
- `REGRAS` (regra 1 e caminho 2): Agora pede para o modelo citar o trecho no formato [N] e não escrever o nome da fonte.
- `resolver_citacoes`: Pega os trechos numerados e escreve os nomes das fontes.
- `gerar_resposta`: As citações são escritas pela função resolver_citacoes e gerar_resposta fica responsável por chamar o modelo e pelo conteúdo.

### Como medi

Versões usadas são as mesmas das versões anteriores:
- Python: 3.14.10
- Ollama: 0.40.13
- Bibliotecas: `ollama` 0.6.3 e `chromadb` 1.5.9 (também fixadas no `requirements.txt`)
- Modelos: `phi4-mini` e `embeddinggemma`

As perguntas, a máquina, o modelo e os parâmetros permaneceram os mesmos. O que mudou foram as citações geradas na resposta, onde a citação por número resolve o formato do nome, mas a mudança de prompt e de contexto também pode ter alterado o comportamento do modelo, como no teste 5. Agora, as fontes são retornadas corretamente, com .md no final ao invés de _md ou de arquivo.md literal. 

Os testes 1, 2, 3, 5 e 6 foram feitos antes da deduplicação, enquanto que o teste 4 foi testado antes e depois dessa alteração.

### Resultado: antes e depois

| # | Pergunta | Antes (v4, `v1-tp`) | Depois (v5) |
|---|----------|---------------------|-------------|
| 1 | Qual é o prazo para reclamação após a entrega? | Pelo menos uma fonte vinha mal formada, escolheu trecho irrelevante e se contradisse ao dizer que não tinha a informação | Agora todas as fontes são retornadas corretamente, porém ainda escolhe alguns trechos irrelevantes e se contradiz da mesma forma |
| 2 | Qual é a taxa de entrega? | A única fonte retornada já aparecia com .md | Nada mudou |
| 3 | Eu ganho reembolso se a loja atrasar o meu pedido? | Mesmo caso do teste 1, onde pelo menos uma vinha com _md, se contradisse dizendo que a resposta não respondia diretamente a pergunta e passou o limite de três frases | Fontes aparecem bem formatadas e dessa vez não teve uma nota que cause contradição, porém o limite de três frases ainda está sendo passado |
| 4 | Qual é o valor mínimo de um pedido para usar cupom? | Fontes vinham mal formadas e duplicadas | Na primeira execução já apresentava o formato certo, porém com fontes duplicadas. Já na segunda execução, apresentou formato certo e sem fontes duplicadas |
| 5 | o restaurante desistiu do meu pedido, o que acontece com o dinheiro? | Formatação já era correta, além de estar no limite de três frases. O problema estava na incoerência com os documentos, dizendo que o restaurante reembolsa sendo que é a EntregaJá | Retornou cinco frases, ultrapassando o limite de três, sendo uma delas duplicada e uma de enchimento. Continua sem o aviso de 10 minutos e ainda mostra uma fonte errada junta ao texto do trecho 03_p2. Única melhoria na resposta, além dos documentos estarem formatados corretamente, foi o aviso de que o reembolso é feito automaticamente e não pelo restaurante |
| 6 | Qual é o telefone ou e-mail para falar com o atendimento? | Retornou corretamente que não tem a informação nas fontes | Retornou corretamente que não tem a informação nas fontes |

### O que melhorou

Agora todos os testes que possuem citações (1 a 5) mostraram que as fontes foram retornadas corretamente, com o nome real e bem formatado com .md no final. Nada de _md ou arquivo.md literal.

### O que não melhorou

De forma geral, o limite de três frases, posição da citação (deveria ser ao final da frase) e contradições continuaram aparecendo, o que era de se esperar já que não é responsabilidade do código atual garantir qualidade nesses quesitos.

Entretanto, o teste cinco apresentou uma piora no respeito ao limite de frases. A mudança do prompt e do contexto podem ter ocasionado isso.

### Uma falha do meu código que os testes revelaram

O teste 4 ainda duplicava as fontes, e isso aconteceu pois faltou um único trecho no meu código que retirava essa duplicação.  O modelo escreveu [1] [2] que são dois trechos diferentes do mesmo arquivo, e o antigo resolver_citacoes só evitava repetição dentro de um mesmo colchete.

Adicionei o trecho abaixo ao final do resolver_citacoes para resolver esse problema: 

```py
    texto = re.sub(r"\[(\d+(?:\s*,\s*\d+)*)\]", trocar, resposta)
    return re.sub(r"(\(fonte: [^)]*\))(?:\s*\1)+", r"\1", texto)
```

### Conclusão

Agora as citações estão bem formatadas e sem duplicatas vizinhas, facilitando leitura e curadoria dos documentos. Caso alguém queira ler o documento por conta própria, não vai se perder por conta de má formatação. Porém isso não melhorou a geração do phi4-mini, então ainda é necessário trabalhar o modelo para ele responder mais diretamente em perguntas fechadas e saber se comunicar dentro do limite de 3 frases em perguntas mais abertas.

### Referências

- Branch: `melhoria-citacoes`
- Pull request: <!-- link -->
- Tag: `v2`

## Próximas melhorias

- [x] Citação por número
- [ ] Começar por "Sim" ou "Não" em perguntas fechadas
- [ ] Limiar de distância para não enviar trechos ruidosos ao modelo
- [ ] Indexação incremental da base
- [ ] Script de avaliação automática com as seis perguntas, registrando tokens e latência
