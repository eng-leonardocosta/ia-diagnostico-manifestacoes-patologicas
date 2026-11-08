# Livro de códigos

O gabarito é sempre o diagnóstico registrado na ficha PATORREB (`dados/fichas_selecionadas.csv`). Vale o mecanismo, não a palavra: termos equivalentes contam como acerto (ex.: "mofo" = "bolor"; "ausência de pingadeira" = "deficiente configuração do peitoril"; "ascensão capilar" = "umidade ascensional").

## Campos de `dados/codificacao.csv`

| Campo | Valores | Regra |
|---|---|---|
| `mpos` | 1, 2, 0 | Posição da **manifestação** da ficha na resposta: 1 = é a manifestação principal descrita; 2 = aparece como secundária ou em termo genérico do mesmo tipo; 0 = não aparece |
| `cpos` | 1, 2, 0 | Posição da **causa** da ficha: 1 = é o primeiro mecanismo da causa mais provável; 2 = aparece entre as alternativas, como fator associado ou de forma genérica; 0 = não aparece |
| `grupo_ia` | 12 grupos + "Outra" | Grupo a que pertence a causa **mais provável** apontada pela ferramenta |
| `confianca` | A, M, B | Grau de confiança declarado pela própria ferramenta (alto, médio, baixo) |
| `nota` | texto | Justificativa curta dos casos-limite |

**Pontos:** posição 1 = 1; posição 2 = 0,5; ausente = 0.
**Indicadores:** manifestação exata = `mpos` 1; causa exata = `cpos` 1; causa entre as hipóteses = `cpos` 1 ou 2.

## Casos-limite

- **Causa combinada** ("A combinada com B" como causa principal): conta como posição 1 o mecanismo citado primeiro; o segundo conta como 2.
- **Causa genérica** ("umidade" sem mecanismo): não confirma condensação, ascensão capilar ou infiltração; posição 0 para o mecanismo específico, salvo se ele aparecer nas alternativas.
- **Elemento trocado** (ex.: fachada tomada por piso): pontua-se o que foi dito sobre a manifestação e a causa, e registra-se o erro em `nota`.

## Grupos de causa

Umidade – condensação; Umidade – ascensional; Umidade – infiltração / água; Movimentação térmica / higrotérmica; Eflorescência / sais solúveis; Falha de projeto ou execução; Envelhecimento / ação ambiental; Deformação / instabilidade do suporte; Retração (argamassa / suporte); Corrosão (armaduras / metais); Ação mecânica (choque / desgaste); Vazamento de instalações; Outra.

## Quem pontuou: desenho agente × agente

A pontuação das 60 respostas foi feita por um **agente avaliador**: o modelo Claude Opus 5.5 (Anthropic), em plano pago e com esforço de raciocínio alto, operando com acesso às respostas, às fichas e a estas regras. Ele aplicou o mesmo critério a cada resposta, tendo como gabarito o diagnóstico da ficha PATORREB, e registrou em `nota` uma justificativa para os casos-limite.

O desenho é, portanto, **agente × agente**: o que um agente pago conclui sobre as respostas de agentes gratuitos, ancorado em diagnósticos validados por especialistas. Os autores definiram as regras e o gabarito, mas não revisaram a pontuação linha a linha nesta versão.

Como o agente avaliador pertence à mesma família de uma das ferramentas avaliadas (G – Claude), há risco de viés de afinidade. Por isso:

- as respostas originais estão completas em `dados/respostas_brutas.md`, para que qualquer leitor refaça a pontuação;
- a aba *Conferência* da planilha tem colunas para registrar concordância ou correção linha a linha, e a aba *Resultado* recalcula tudo automaticamente;
- a próxima etapa prevista é a **pontuação humana e a correlação com o agente**: dois avaliadores independentes, sem saber qual ferramenta produziu cada resposta, pontuarão as 60 respostas, e será medida a concordância entre eles e entre eles e o agente avaliador. O resultado indicará se o agente reproduz o julgamento de especialistas e pode ser usado para reavaliar novas versões em escala.
