# Pastas

Para o código funcionar, precisamos definir 2 variáveis: **INPUT_FOLDER** e **OUTPUT_FOLDER**. A variável **INPUT_FOLDER** será o caminho da pasta dos seus áudios .mp3, e a variável **OUTPUT_FOLDER** será o caminho
da pasta da onde irá ficar todos os textos dos áudios que foram transcrevidos. Na linha 14 do código podemos definir isso, observe:

```py
import os
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (contendo OPENAI_API_KEY)
load_dotenv()

# Inicializa o cliente OpenAI com a chave da API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Caminhos
INPUT_FOLDER = r"C:/SUA/PASTA/DE/AUDIOS"
OUTPUT_FOLDER = r"C:/SUA/PASTA/ONDE/IRÁ/OS/TEXTOS/TRANSCREVIDOS"
```

No caso, é só você colocar o caminho dos áudios em `INPUT_FOLDER` e onde vai ficar os textos em `OUTPUT_FOLDER`, entre as aspas duplas.

**Ass: Enzin Coda**
