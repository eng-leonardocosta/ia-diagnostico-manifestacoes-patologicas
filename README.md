# IA ao alcance de todos: dados e protocolo

Repositório de verificação do artigo **"Inteligência artificial ao alcance de todos: o que ferramentas gratuitas acertam no diagnóstico de manifestações patológicas por fotografia"**, apresentado no V Simpósio Internacional do NDAE (Tucuruí – PA, 25 e 26 de novembro de 2026).

Autores: Leonardo Costa dos Santos, Vanessa da Silva de Azevedo e Otávio Noura Teixeira.

## O que o estudo fez

Três ferramentas de IA multimodal em versão gratuita (Claude, ChatGPT e Gemini) receberam a fotografia de 20 casos do catálogo PATORREB (Universidade do Porto), cujos diagnósticos foram validados por especialistas. As 60 respostas foram pontuadas por uma ferramenta de IA, com regras fixas e o diagnóstico da ficha como gabarito (avaliação de IA por IA, ancorada em diagnósticos validados por especialistas). A concordância foi medida pelo coeficiente Kappa de Cohen.

## O que está aqui

| Pasta / arquivo | Conteúdo |
|---|---|
| `dados/fichas_selecionadas.csv` | As 20 fichas: elemento, manifestação (original e adaptada), causa e grupo de causa de referência |
| `dados/respostas_brutas.csv` e `.md` | As 60 respostas **na íntegra**, sem edição, com ferramenta, modelo exibido e data |
| `dados/codificacao.csv` | A pontuação de cada resposta (manifestação, causa, grupo e confiança) |
| `protocolo/comando.txt` | O comando enviado, idêntico para as três ferramentas |
| `protocolo/condicoes_de_coleta.md` | Data, planos, modelos, modo anônimo e regras de envio |
| `protocolo/livro_de_codigos.md` | As regras de pontuação e os casos-limite |
| `planilha/` | Planilha com as 60 respostas, a codificação e o cálculo de todos os indicadores **por fórmulas editáveis** |
| `scripts/analise.py` | Recalcula todos os números do artigo |
| `scripts/figura_dispersao.py` | Gera a Figura 1 |
| `resultados/` | Saídas dos scripts (tabelas CSV, `resultados.json` e a figura) |

As fotografias **não** estão aqui: pertencem ao catálogo PATORREB e podem ser consultadas em www.patorreb.com pelo número da ficha.

## Como conferir

**Sem programar:** abra a planilha. A aba *Conferência* traz cada resposta ao lado do diagnóstico da ficha e da pontuação; a aba *Resultado* recalcula sozinha os indicadores e o Kappa. Se discordar de alguma pontuação, altere-a e veja o efeito nos resultados.

**Com Python:**

```bash
pip install -r requirements.txt
python scripts/analise.py
python scripts/figura_dispersao.py
```

Os números esperados são:

| Ferramenta | Manifestação exata | Causa exata | Causa entre hipóteses | Kappa (IC 95%) |
|---|---|---|---|---|
| G – Claude | 70,0% | 65,0% | 95,0% | 0,66 (0,43–0,88) |
| H – ChatGPT | 70,0% | 50,0% | 70,0% | 0,49 (0,26–0,70) |
| I – Gemini | 75,0% | 55,0% | 85,0% | 0,55 (0,32–0,76) |
| Conjunto (n = 60) | 71,7% | 56,7% | 83,3% | 0,57 (0,38–0,73) |

Também são calculados: McNemar exato entre acertar a manifestação e acertar a causa (p = 0,093), Q de Cochran entre as ferramentas (Q = 1,75; p = 0,42), pi de Scott, alfa de Krippendorff e AC1 de Gwet. Os intervalos de confiança vêm de 2.000 reamostragens das fichas, com semente fixa (2026).

## Como medimos

- **Pontuação:** manifestação e causa recebem 1 (acerto pleno), 0,5 (parcial) ou 0 (erro), conforme o livro de códigos.
- **Kappa de Cohen:** compara o grupo de causa indicado em primeiro lugar com o da ficha e desconta os acertos que ocorreriam ao acaso: κ = (po − pe) / (1 − pe). Exemplo: a ferramenta G acertou o grupo em 14 de 20 casos (po = 0,70); o acaso explicaria pe = 0,105; κ = (0,70 − 0,105) / (1 − 0,105) = 0,66.
- **Leitura:** 0,41–0,60 moderada; 0,61–0,80 substancial (Landis e Koch, 1977). Patamar adotado para uso como apoio: κ ≥ 0,61.

## Reaplicar o protocolo

As ferramentas mudam com frequência, então os números valem para a data da coleta (23/10/2026). Para avaliar outra versão ou outra ferramenta, mantenha fixos as 20 fichas, o comando, o modo anônimo e o livro de códigos. Registre data, plano e modelo exibido, codifique as novas respostas no mesmo formato de `dados/codificacao.csv` e rode `scripts/analise.py`.

## Uso de IA

A pontuação das 60 respostas foi feita por ferramenta de IA (Claude, Anthropic), seguindo as regras e o gabarito definidos pelos autores, e **não foi revisada linha a linha por humanos nesta versão** (ver `protocolo/livro_de_codigos.md`, seção "Quem pontuou"). A organização dos dados, os scripts e a revisão de texto também tiveram apoio dessa ferramenta. As versões gratuitas de Claude, ChatGPT e Gemini foram o **objeto** da pesquisa.

**Validação humana (próxima etapa):** dois avaliadores independentes, às cegas quanto à ferramenta, pontuarão as respostas, e a concordância entre eles e com a IA será publicada em nova versão. Leitores que quiserem contribuir podem usar a aba *Conferência* da planilha e abrir uma *issue* com suas divergências.

## Licença e citação

Dados e textos sob CC BY 4.0; código sob MIT (ver `LICENSE.md`). Para citar, use `CITATION.cff`.

## Versões

- **v1.0** (nov/2026): versão submetida ao V Simpósio Internacional do NDAE, com pontuação feita por IA.
- **Próximas:** validação humana da pontuação; inclusão das versões pagas (9 configurações) do artigo completo.
