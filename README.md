# TP Aula 07: consulta de documentos com busca vetorial e RAG

## 1. Identificação

- Nome: Juan Tadeu
- Curso / disciplina / turma: Análise e Desenvolvimento de Sistemas / IA / A
- Data: 02/11/2026

## 2. Tema e finalidade

A base responde, citando os documentos, perguntas sobre a EntregaJá, um serviço de delivery fictício, que os clientes usam para pedir suas compras, almoços, lanches e afins.

## 3. Documentos da base

Todos ficam na pasta `documentos/` e abordam aspectos diferentes do mesmo tema.

| Arquivo | Assunto |
|---|---|
| `01_atraso_na_entrega.md` | Definição de atraso e reembolso por faixa de minutos, com cupom |
| `02_item_faltando_ou_errado.md` | Reembolso de item ausente ou trocado em pedido entregue |
| `03_pedido_cancelado_pela_loja.md` | Reembolso total quando o restaurante cancela, e cupom de desculpas |
| `04_prazo_para_reclamar.md` | Prazo de 24 horas e o que acontece depois dele |
| `05_entregue_mas_nao_recebido.md` | Pedido marcado como entregue que o cliente diz não ter recebido |
| `06_limite_de_reembolso_automatico.md` | Teto por solicitação e limite mensal do atendimento automático |
| `07_pagamento_e_estorno.md` | Formas de pagamento e prazos de estorno |
| `08_cupons_e_promocoes.md` | Validade, pedido mínimo e acúmulo de cupons |
| `09_taxa_de_entrega_e_gorjeta.md` | Cálculo da taxa de entrega, frete grátis e gorjeta |
| `10_privacidade_e_dados_da_conta.md` | Acesso aos próprios dados, retenção e exclusão da conta |

## 4. Origem dos textos e uso de IA


- **Conteúdo fictício.** A EntregaJá não existe. Todos os documentos têm o aviso de documento fictício logo abaixo do título e não contêm dados pessoais.
- **Textos dos documentos.** O tema relacionado ao mundo de delivery foi definido por mim, em conjunto com o Claude, para que o projeto servisse de portfólio para o estágio de genai do Ifood. O primeiro documento foi escrito por mim, porém reescrito pelo Claude (que também escreveu por completo os outros documentos), para que ficassem diretos, coerentes e gramaticalmente corretos.
- **Apoio ao código.** Os códigos foram fornecidos pelo Claude, etapa a etapa, para que eu pudesse escrever, entender e questionar pedaço por pedaço para agregar ao estudo.
- **Fontes públicas.** Nenhuma.
- **README e análise dos testes.** Claude estruturou o esqueleto do README e participou das análises dos testes me questionando, levantando sugestões e me fazendo pensar nas respostas e melhorias. Ele organizou os comentários a partir das minhas observações e dos resultados dos testes que foram executados por mim. As perguntas, as respostas esperadas e os documentos de referência também foram escolhidos por mim.
## 5. Instalação e execução

Versões usadas:

- Python: 3.14.10
- Ollama: 0.40.13
- Bibliotecas: `ollama` 0.6.3 e `chromadb` 1.5.9 (também fixadas no `requirements.txt`)
- Modelos: `phi4-mini` e `embeddinggemma`

Passos (Windows, PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

ollama pull phi4-mini
ollama pull embeddinggemma

python tp_aula7_rag_vetorial.py
```

O Ollama precisa estar em execução. Na primeira execução o programa cria a base vetorial, o que leva alguns segundos. Depois ele pede perguntas no terminal; digite `sair` para encerrar.



## 6. Chunking e preservação das fontes

Carregar um documento por completo toda vez que você precisa responder ou entender algo é muito pesado e desnecessário. Para evitar isso, a gente quebra o documento
em pedaços menores, sem tirar o contexto desses pedaços, para que as respostas fiquem coerentes e rápidas. Esses pedaços são o que chamamos de chunks. Nesse projeto, os documentos foram divididos por parágrafos, criando os chunks a cada linha em branco.

Ao todo, a base tem 10 documentos e 30 chunks.

Cada chunk é armazenado com Id, Arquivo de Origem, Título do Documento e o Texto do Parágrafo. Para formar o Id, pegamos o nome do arquivo e adicionamos _p e o número do parágrafo, assim ele fica único e já mostra de onde o trecho veio. O título não vira chunk, mas é guardado como metadado (não serve como evidência).

A fonte é guardada para rastreamento da origem, assim podendo verificar de onde a resposta veio. Ela não participa da busca.

Ao perguntar, o Chroma compara o vetor da pergunta com os vetores guardados e devolve o Id, o Texto, a Fonte e a Distância dos trechos mais próximos. O programa mostra o Id, a Fonte e a Distância no terminal. Ao phi4-mini, porém, envia só o texto de cada trecho, numerado como [1], [2] e [3], sem o nome do arquivo. O modelo cita o número do trecho que usou, e o código troca cada número pelo nome real do arquivo, guardado como metadado.

## 7. Papel de cada componente

- **embeddinggemma:** Responsável por transformar os textos em vetores
- **Chroma:** Compara os vetores e retorna os mais próximos
- **phi4-mini:** Llm local responsável por responder as dúvidas baseando-se no que tem nos trechos recuperados
- **O código (Python):** Define as regras da resposta da llm, a regra da divisão dos chunks, o como usa o banco, numera os trechos enviados ao modelo e troca os números citados pelos nomes dos arquivos.

Como modelos de embeddings geram vetores diferentes, utilizar modelos diferentes criariam contextos diferentes e a comparação ficaria errada. 


## 8. Criação, reutilização e atualização da base vetorial

A base fica gravada em uma pasta chroma_db com uma assinatura hash SHA-256 que marca os ids, os textos e o modelo. Essa assinatura 
serve para o código verificar se o modelo ou alguma palavra no documento mudou. Se a assinatura for igual, reutiliza sem recalcular os embeddings dos documentos.
Se for uma assinatura diferente, apaga a coleção anterior e recria com as novas alterações. Como a coleção antiga é apagada antes de gravar a nova, rodar de novo não duplica registros.

A pasta `chroma_db` é criada pelo próprio programa a partir de `documentos/`, por isso não vai no ZIP: se for apagada, a próxima execução a recria.

**Limitação:** qualquer mudança, mesmo uma vírgula, reindexa todos os 30 chunks.

## 9. Testes e análise dos resultados

Os testes abaixo são os da segunda rodada, feita com o prompt v4, quando o modelo ainda escrevia o nome do arquivo. Os resultados depois da melhoria “citação por número” estão em MELHORIAS.md.

Configuração dos testes: embeddinggemma, `phi4-mini` com `temperature` 0 e `num_predict` 200, 3 trechos recuperados por pergunta, distância de cosseno e "Lembre-se: no máximo 3 frases, só com base nos trechos." em gerar_resposta().

**Sobre as distâncias:** a distância mostra quanto um trecho está próximo da pergunta, e serve para ordenar os trechos de uma mesma consulta. Não é um percentual de certeza, e não deve ser comparada entre perguntas diferentes. O trecho mais próximo também pode não conter a resposta.

### Teste 1

- **Pergunta:** Qual é o prazo para reclamação após a entrega?

- **Esperado e documento de referência:** O cliente tem até 24h após o pedido ser marcado como entregue no aplicativo (04_prazo_para_reclamar.md).

- **Recuperado (ids, fontes e distâncias):** 
  - [04_prazo_para_reclamar_p1] fonte: 04_prazo_para_reclamar.md (distancia 0.406)
  - [02_item_faltando_ou_errado_p1] fonte: 02_item_faltando_ou_errado.md (distancia 0.422)
  - [05_entregue_mas_nao_recebido_p1] fonte: 05_entregue_mas_nao_recebido.md (distancia 0.439)

- **Resposta gerada:** O cliente tem até 24 horas após a entrega para solicitar reembolso por atraso, item faltando ou item errado (fonte: 04_prazo_para_reclamar.md). O prazo conta a partir do horário em que o pedido foi marcado como entregue no aplicativo (fonte: 04_prazo_para_reclamar_md). O cliente pode solicitar reembolso pela tela do pedido no aplicativo, dentro do prazo geral de reclamação (fonte: 02_item_faltando_ou_errado.md). O prazo geral de reclamação não é explicitamente mencionado nos trechos fornecidos. (fonte: 02_item_faltando_ou_errado_md)

- **Comentário:**
  - Busca: encontrou evidência suficiente. O trecho 04_prazo_para_reclamar_p1 ficou em 1º (0.406) e contém o fato esperado (24 horas, contadas da marcação como entregue). Os outros dois trechos (02 e 05) não eram necessários.

  - Resposta: o conteúdo esperado aparece nas duas primeiras frases, mas a resposta tem 4 frases (limite: 3) e a última contradiz as anteriores ("o prazo geral de reclamação não é explicitamente mencionado" logo depois de informar as 24 horas). Usou também o trecho do doc 02, apesar da regra de ignorar trechos que não tratam da pergunta. A primeira fonte veio com o nome correto, mas as outras saíram malformadas ("_md" no lugar de ".md"). Na rodada 1 todas as citações eram o literal "arquivo.md".

  - Problema em (chunking, recuperação ou geração): geração. A recuperação funcionou.

### Teste 2

- **Pergunta:** Qual é a taxa de entrega?
- **Esperado e documento de referência:** A taxa de entrega é de R$ 4,90 para distâncias de até 3km. Distâncias maiores soma-se R$ 1,50 por km adicional. (09_taxa_de_entrega_e_gorjeta.md)

- **Recuperado:** 
  - [09_taxa_de_entrega_e_gorjeta_p1] fonte: 09_taxa_de_entrega_e_gorjeta.md (distancia 0.362)
  - [09_taxa_de_entrega_e_gorjeta_p2] fonte: 09_taxa_de_entrega_e_gorjeta.md (distancia 0.396)
  - [09_taxa_de_entrega_e_gorjeta_p3] fonte: 09_taxa_de_entrega_e_gorjeta.md (distancia 0.547)


- **Resposta gerada:** A taxa de entrega da EntregaJá é de R$ 4,90 para distâncias de até 3 km, com R$ 1,50 por quilômetro adicional para distâncias maiores. (fonte: 09_taxa_de_entrega_e_gorjeta.md)

- **Comentário:** 
  - Busca: suficiente. O trecho 09_taxa_de_entrega_e_gorjeta_p1 ficou em 1º (0.362) e traz R$ 4,90 até 3 km e R$ 1,50 por km adicional. Os trechos p2 e p3 (gorjeta) não eram necessários.

  - Resposta: respeitou a evidência e a pergunta. Uma frase, direta, só com o que foi perguntado, fonte com o nome e o formato corretos. Na rodada 1 a resposta trazia informação sobre gorjeta que ninguém perguntou. Foi o melhor resultado da rodada 2.

  - Problema em: nenhum na rodada 2 (na rodada 1, geração: resposta fora do tema).

### Teste 3

- **Pergunta:** Eu ganho reembolso se a loja atrasar o meu pedido?
- **Esperado e documento de referência:** Sim. Para atrasos de até 10 minutos, você recebe até 15% do valor total. Se for entre 11 a 25 minutos, o reembolso é de até 35%. Para 26 minutos ou mais, o reembolso é de até 50% do valor total. (01_atraso_na_entrega.md)
- **Recuperado:** 
  - [01_atraso_na_entrega_p2] fonte: 01_atraso_na_entrega.md (distancia 0.312)

  - [01_atraso_na_entrega_p1] fonte: 01_atraso_na_entrega.md (distancia 0.335)

  - [02_item_faltando_ou_errado_p3] fonte: 02_item_faltando_ou_errado.md (distancia 0.359)

- **Resposta gerada:** Se o atraso for de 1 a 10 minutos, você tem direito a até 15% do valor total do pedido (fonte: 01_atraso_na_entrega.md). Se o atraso for de 11 a 25 minutos, o reembolso é de até 35% do valor total (fonte: 01_atraso_na_entrega_md). Se o atraso for de 26 minutos ou mais, o reembolso é de até 50% do valor total (fonte: 01_atraso_na_entrega_md). Pedidos entregues no horário previsto não têm direito a reembolso por atraso (fonte: 01_atraso_na_entrega_md). (Nota: O trecho fornecido não responde diretamente à pergunta sobre o reembolso se a loja atrasar o pedido, mas fornece informações sobre os percentuais de reembolso com base no tempo de atraso.)


- **Comentário:** 
  - Busca: suficiente. O trecho 01_atraso_na_entrega_p2 ficou em 1º (0.312) com as três faixas; o p1 define atraso e a base de cálculo. O 3º trecho (doc 02, p3) não é relevante. A distância se manteve igual à da rodada 1.

  - Resposta: as três faixas estão corretas, com "até" em cada uma. Mas a resposta tem 4 frases mais uma "Nota" (limite: 3), e a nota diz que o trecho "não responde diretamente à pergunta", o que contradiz o conteúdo informado. Não começa com "Sim", que seria a resposta direta para uma pergunta fechada (poderia confirmar que há reembolso e depois dar os percentuais). Primeira fonte correta, demais malformadas ("_md"). A frase irrelevante sobre pedidos em preparo, que existia na rodada 1, desapareceu.

  - Problema em: geração.

### Teste 4

- **Pergunta:** Qual é o valor mínimo de um pedido para usar cupom?
- **Esperado e documento de referência:** O valor dos itens do pedido deve ser de pelo menos R$ 30,00 (08_cupons_e_promocoes.md)
- **Recuperado:** 
  - [08_cupons_e_promocoes_p1] fonte: 08_cupons_e_promocoes.md (distancia 0.414)

  - [08_cupons_e_promocoes_p2] fonte: 08_cupons_e_promocoes.md (distancia 0.448)

  - [09_taxa_de_entrega_e_gorjeta_p3] fonte: 09_taxa_de_entrega_e_gorjeta.md (distancia 0.457)

- **Resposta gerada:** O valor mínimo de um pedido para usar um cupom é R$ 30,00 (fonte: 08_cupons_e_promocoes_md). (fonte: 08_cupons_e_promocoes_md)
- **Comentário:** 
  - Busca: suficiente. O trecho 08_cupons_e_promocoes_p1 ficou em 1º (0.414) e contém o mínimo de R$ 30,00 sobre o valor dos itens. A distância é maior que a do teste 3 (0.312), mas a distância só serve para ordenar os trechos de uma mesma consulta, e não para comparar perguntas diferentes nem como medida de certeza.

  - Resposta: o valor está correto (R$ 30,00), mas perde o detalhe de que o mínimo vale para o valor dos itens do pedido. A fonte saiu malformada ("08_cupons_e_promocoes_md") e repetida duas vezes. A resposta é idêntica à da rodada 1, o que é esperado com temperature 0, embora o determinismo não seja garantido (ver Reprodutibilidade).

  - Problema em: geração (formato da citação e pequena perda de precisão).

### Teste 5 (paráfrase)

- **Pergunta:** o restaurante desistiu do meu pedido, o que acontece com o dinheiro?
- **Esperado e documento de referência:** A EntregaJá reembolsa 100% do valor do pedido e avisa o cliente sobre o cancelamento pelo aplicativo em até 10 minutos. (03_pedido_cancelado_pela_loja.md)

- **Recuperado:** 
  - [03_pedido_cancelado_pela_loja_p1] fonte: 03_pedido_cancelado_pela_loja.md (distancia 0.337)
  
  - [04_prazo_para_reclamar_p3] fonte: 04_prazo_para_reclamar.md (distancia 0.408)

  - [02_item_faltando_ou_errado_p3] fonte: 02_item_faltando_ou_errado.md (distancia 0.448)
- **Resposta gerada:** O restaurante reembolsa 100% do valor do pedido, incluindo a taxa de entrega, se cancelar por falta de ingrediente, problema na cozinha ou encerramento do expediente. O reembolso é feito automaticamente sem necessidade de reclamação do cliente. (fonte: 03_pedido_cancelado_pela_loja.md)
- **Comentário:** 
  - Busca: suficiente, e a paráfrase funcionou. O trecho 03_pedido_cancelado_pela_loja_p1 ficou em 1º (0.337) mesmo sem as palavras "cancelado" ou "reembolso" na pergunta. O 2º (doc 04, p3) é relevante, porque diz que cancelamentos da loja são reembolsados automaticamente. O 3º (doc 02, p3) é ruído.

  - Resposta: informa corretamente o reembolso de 100% do valor, incluindo a taxa de entrega, em 2 frases, com a fonte no formato certo. Problemas: (1) diz "O restaurante reembolsa", mas quem reembolsa é a EntregaJá; (2) falta o aviso ao cliente em até 10 minutos, que fazia parte do esperado; (3) a informação de reembolso automático vem do doc 04, mas só o doc 03 é citado. Melhorou bastante em relação à rodada 1, que citava três fontes no formato "arquivo.md|id:" e incluía uma frase irrelevante sobre item faltando.

  - Problema em: geração.

### Teste 6 (informação ausente)

- **Pergunta:** Qual é o telefone ou e-mail para falar com o atendimento?
- **Esperado:** Por não ter essa informação em nenhum dos documentos, a Llm deve retornar que não possui isso na base de dados. O quase-acerto, no qual ela identifica que não bate com a pergunta, seria o primeiro trecho do documento 10, que fala sobre o assistente nunca revelar endereço, telefone ou pedidos de outros clientes (Único documento em que a palavra telefone aparece)
- **Recuperado:** 
  - [10_privacidade_e_dados_da_conta_p1] fonte: 10_privacidade_e_dados_da_conta.md (distancia 0.521) 

  - [06_limite_de_reembolso_automatico_p1] fonte: 06_limite_de_reembolso_automatico.md (distancia 0.544)

  - [05_entregue_mas_nao_recebido_p1] fonte: 05_entregue_mas_nao_recebido.md (distancia 0.560)

- **Resposta gerada:** Não encontrei essa informação nos documentos.
- **Comentário:** 
  - Busca: não existe evidência nos documentos, como esperado. O trecho mais próximo (doc 10, p1, 0.521) menciona "telefone" apenas no contexto de privacidade (o assistente não revela telefone de outros clientes), então é um quase-acerto. As distâncias (0.521 a 0.560) ficaram acima das do 1º trecho dos testes respondíveis (0.312 a 0.414), mas são poucos exemplos para definir um limiar.

  - Resposta: informa exatamente o que foi definido como regra (se não tiver a informação em nenhum documento, fale que não encontrou essa informação).

  - Problema em: nada

### Evolução do prompt

As duas primeiras versões do prompt (v1 e v2) sequer chegaram a ser testadas com as seis perguntas descritas nos testes acima, pois com outros testes diretos, foram notadas a contradição e confusão. 
  Erros: O modelo citava fontes aleatórias mesmo quando dizia que não havia encontrado nada nos documentos. Em outro caso, se contradisse ao falar sobre as taxas de entrega de até 3km e depois disse que não haviam informações sobre isso nos documentos. 

Para a versão 3 do prompt, tivemos dois caminhos para resposta (um com evidência e outro sem), mostrando um exemplo de frase fixa para o caso sem resposta. 
  Erros: O modelo trouxe frases fora do tema, copiou a formatação exemplo do prompt (arquivo.md) como se fosse o nome real e passou do limite de 3 frases.

A versão 4 (usada nos testes mostrados acima) já apresentou uma melhoria, acertando o nome do documento na primeira citação nos testes 1, 2, 3 e 5 (o teste 4 veio errado em todas as citações) e obteve um foco mais direto em alguns testes (teste 2 e 5).
  Erros: Após a primeira citação, o modelo retornou _md ao invés de .md e passou de 3 frases (4 frases com contradições) nos testes 1 e 3.




### Análise geral

As buscas encontraram os trechos certos e os chunks foram separados corretamente por parágrafos.

O sistema sempre vai mandar três trechos ao modelo mesmo que apenas um seja útil. Isso pode causar ruído em alguns casos.

A maior parte das falhas se encontrou na geração, onde o modelo não escrevia o formato certo do nome do arquivo, se contradisse várias vezes e extrapolou o limite de três frases. 

A paráfrase funcionou muito bem, retornando o trecho esperado e com uma distância parecida com a das perguntas diretas (0,337).

O teste 6, no qual verificamos a resposta caso não tenha documentos na base, retornou exatamente o esperado mesmo tendo um quase-acerto no doc 10 que poderia confundir um pouco o modelo.


### Reprodutibilidade

Ao rodar o programa de novo em uma instalação limpa (ZIP extraído, ambiente virtual novo e base recriada), os trechos recuperados no teste 1 foram os mesmos, com distâncias que variaram só na terceira casa decimal (0,405 e 0,421 contra 0,406 e 0,422). A resposta, porém, variou: a quarta frase mudou e o modelo acrescentou “Não encontrei essa informação nos documentos.” depois de já ter respondido, misturando os dois caminhos do prompt. Isso mostra que temperature 0 reduz a variação, mas não garante respostas idênticas, e reforça que a geração é o ponto mais frágil do sistema.

## 10. Uma dificuldade e melhorias

**Dificuldade encontrada:** 
Entender como fazer a llm respeitar os limites, responder adequadamente e não ficar mesclando documentos sem necessidade. Não só mudanças no prompt, mas fatores como garantias de limite no código precisam estar favoráveis para que o modelo fique mais preciso.

**Melhorias implementadas:** 
Para evitar que o README fique extenso demais e mudando constantemente a cada melhoria, optei por desenvolver um documento novo chamado [MELHORIAS.md](MELHORIAS.md).

Citação por número: os trechos enviados ao modelo são numerados ([1], [2], [3]) e o modelo cita só o número do trecho que usou. O código converte cada número no nome real do arquivo, guardado nos metadados, então o nome não depende do que o modelo escreve. Isso não garante que ele cite o trecho certo.