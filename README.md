# Monitor de mudanças de liderança em marketing

Pipeline semanal que busca notícias sobre contratação/promoção/saída de CMOs e diretores
de marketing em empresas médias/grandes, filtra com IA, extrai os dados e grava em uma
planilha do Google Sheets.

## Fluxo

1. GitHub Actions dispara toda segunda-feira (`when:7d` cobre a semana anterior)
2. `src/fetch_news.py` busca o RSS do Google News (pt-BR e en-US)
3. `src/dedupe.py` remove itens já vistos (banco SQLite versionado em `data/seen.sqlite3`)
4. `src/classify.py` usa Claude para (a) classificar relevância e (b) extrair os campos estruturados
5. `src/sheets_writer.py` grava as linhas relevantes no Google Sheets
6. O workflow comita o banco de dedup atualizado de volta no repositório

## Setup

### 1. Criar a planilha Google Sheets

Crie uma planilha em branco e copie o ID dela (está na URL, entre `/d/` e `/edit`).

### 2. Criar uma Service Account do Google

1. No Google Cloud Console, crie um projeto (ou use um existente)
2. Ative a API do Google Sheets
3. Crie uma Service Account e gere uma chave JSON
4. Compartilhe a planilha (botão "Compartilhar") com o e-mail da service account
   (algo como `nome@projeto.iam.gserviceaccount.com`), com permissão de Editor

### 3. Configurar os Secrets no GitHub

No repositório, vá em Settings > Secrets and variables > Actions e crie:

- `ANTHROPIC_API_KEY`: sua chave da API da Anthropic
- `GOOGLE_SERVICE_ACCOUNT_JSON`: o conteúdo completo do arquivo JSON da service account (cole o JSON inteiro)
- `GOOGLE_SHEET_ID`: o ID da planilha

### 4. Rodar manualmente para testar

Vá na aba "Actions" do repositório, escolha o workflow "Busca semanal..." e clique em
"Run workflow" (o gatilho `workflow_dispatch` permite isso sem esperar a segunda-feira).

### 5. Testar localmente (opcional)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="..."
export GOOGLE_SERVICE_ACCOUNT_JSON="$(cat caminho/para/service-account.json)"
export GOOGLE_SHEET_ID="..."
python src/main.py
```

## Aba "Configurações" na planilha

O robô cria automaticamente uma aba chamada **"Configurações"** na primeira execução,
com dois campos editáveis (sem precisar tocar em código):

- **País (gl)**: sigla do país a buscar (ex: `BR`). Para mais de um país, separe por
  vírgula (ex: `BR,US`). Cada sigla precisa ter um preset correspondente em
  `COUNTRY_PRESETS` (arquivo `src/config.py`) — hoje já existem presets para `BR`, `US`
  e `PT`. Para adicionar um novo país, basta criar uma nova entrada nesse dicionário.
- **Data de busca inicial (opcional, formato DD/MM/AAAA)**: deixe vazio para o robô
  buscar sempre os últimos 7 dias (padrão). Preencha apenas quando quiser fazer uma
  carga inicial maior (ex: últimos 60 dias) — depois da execução, **limpe o campo de
  volta** para o robô voltar a usar a janela padrão de 7 dias nas próximas execuções
  semanais.

## Ajustando as buscas (termos de pesquisa)

Edite `src/config.py`, dicionário `COUNTRY_PRESETS`, para adicionar/remover termos por
país. O período (`when:Nd`) é calculado automaticamente a partir da aba
"Configurações" e não precisa ser editado no código.

## Ajustando o filtro de relevância

Os prompts que decidem o que entra ou não na planilha estão em `src/config.py`:
`CLASSIFY_SYSTEM_PROMPT` (sim/não) e `EXTRACT_SYSTEM_PROMPT` (extração estruturada).
