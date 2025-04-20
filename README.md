# 🧠 API Chunk Processor

Uma API inteligente para transformar transcrições brutas (.txt) em conteúdo revisado e acessível, utilizando modelos da OpenAI e síntese de voz da ElevenLabs.

---

## 🚀 Funcionalidades

- 📤 Upload de arquivos `.txt` com transcrições
- 🔬 Divisão do conteúdo em chunks e revisão com OpenAI `gpt-4o`
- 📄 Retorno do texto final em Markdown
- 🔊 Geração de áudio com ElevenLabs (pt-BR)
- 🛡️ Proteção das rotas com `X-API-KEY`
- 🌐 Painel web simples para download de arquivos gerados

---

## 📦 Requisitos

- Python 3.10+
- Conta com API Key da [OpenAI](https://platform.openai.com/)
- Conta com API Key da [ElevenLabs](https://elevenlabs.io/)

---

## ⚙️ Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/api_chunk_processor.git
cd api_chunk_processor

# Crie e ative um ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # macOS/Linux

# Instale as dependências
pip install -r requirements.txt

---------

Crie um arquivo .env na raiz com:
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_VOICE_ID=xxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
API_KEY=xxxxxxx

Você pode usar o script audio/listar_vozes.py para descobrir o VOICE_ID desejado

--------


🔐 Autenticação
Todas as rotas exigem uma chave de API via header:

X-API-KEY: 
No Swagger, clique em "Authorize" e insira esse valor no campo X-API-KEY.

--------

▶️ Executando o projeto
uvicorn main:app --reload --timeout-keep-alive 300
Abra no navegador:

🧪 Documentação Swagger: http://localhost:8000/docs

🏠 Página inicial: http://localhost:8000/

📂 Arquivos gerados: http://localhost:8000/v1/processar/listar-arquivos

--------

🛠️ Endpoints disponíveis (v1)

POST /v1/processar/upload
Envia um arquivo .txt para processamento com OpenAI

Retorna um arquivo_id

GET /v1/processar/resultado/{arquivo_id}
Retorna o texto final (concatenado) gerado para o arquivo enviado

POST /v1/processar/audio
Processa o .txt e gera:

link para o texto .txt

link para o áudio .mp3 (com os primeiros 400 caracteres)

GET /v1/processar/listar-arquivos
Gera um painel web listando todos os arquivos gerados


📁 Estrutura do projeto (resumo)

api_chunk_processor/
├── main.py
├── .env
├── requirements.txt
├── routers/
│   ├── processamento_router.py
│   └── audio_router.py
├── services/
│   └── processador.py
├── utils/
│   ├── logger.py
│   └── auth.py
├── audio/
│   ├── gerar_audio.py
│   └── listar_vozes.py
├── storage/
│   ├── uploads/
│   └── public/



📢 Observações
O áudio gerado usa apenas os primeiros 400 caracteres do texto final para garantir velocidade, a título de exemplo.

O projeto é modular e facilmente expansível para outras funções, como:

Tradução
Geração de resumo
PDF ou slides a partir da transcrição

✨ Autor
Desenvolvido por Vinicius Terna Machado
Projeto para disciplina de Construção de APIs para IA - Pós-graduação