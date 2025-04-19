# 🧠 API Chunk Processor

Uma API inteligente para transformar transcrições brutas (.txt) em conteúdo revisado e acessível, utilizando modelos da OpenAI e síntese de voz da ElevenLabs.

---

## 🚀 Funcionalidades

- 📤 Upload de arquivos `.txt` com transcrições
- 🔬 Divisão do conteúdo em chunks e revisão com OpenAI `gpt-4o`
- 📄 Retorno do texto final em Markdown
- 🔊 Geração de áudio com ElevenLabs (pt-BR)
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



Crie um arquivo .env na raiz com:
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_VOICE_ID=xxxxxxxxxxxxxxxxxxxxxxxx
ELEVENLABS_MODEL_ID=eleven_multilingual_v2

Você pode usar o script audio/listar_vozes.py para descobrir o VOICE_ID desejado

▶️ Executando o projeto
uvicorn main:app --reload --timeout-keep-alive 300

Abra no navegador:

Documentação Swagger: http://localhost:8000/docs

Página inicial: http://localhost:8000/

Listagem de arquivos: http://localhost:8000/processar/listar-arquivos

🛠️ Endpoints disponíveis
POST /processar/upload
Envia um arquivo .txt para processamento.

Retorna um arquivo_id.

GET /processar/resultado/{arquivo_id}
Retorna o texto completo processado em Markdown.

POST /processar/audio
Envia o .txt, processa e retorna:

link para o texto .txt

link para o áudio .mp3 (com os 400 primeiros caracteres do resultado)

GET /processar/listar-arquivos
Painel web simples listando os arquivos .mp3 e .txt disponíveis para download.

🧪 Testes (em breve)
Testes automatizados podem ser criados com pytest para validar:

Upload de arquivos

Processamento com OpenAI

Geração de áudio

Respostas da API

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
│   └── logger.py
├── audio/
│   ├── gerar_audio.py
│   └── listar_vozes.py
├── storage/
│   ├── uploads/
│   └── public/


📢 Observações
O áudio gerado usa apenas os primeiros 400 caracteres do texto final para garantir velocidade e compatibilidade.

O projeto é modular e facilmente expansível para outras funções, como:

Tradução

Geração de resumo

PDF ou slides a partir da transcrição

✨ Autor
Desenvolvido por Vinicius Terna Machado