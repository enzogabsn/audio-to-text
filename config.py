import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configurações de API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurações de diretórios
INPUT_FOLDER = r"C:/Users/enzo/OneDrive/Documents/Projetos/Audio-Texto/audios"
OUTPUT_FOLDER = r"C:/Users/enzo/OneDrive/Documents/Projetos/Audio-Texto/texts"

# Configurações de reconhecimento de fala
LANGUAGE = "pt-BR"

# Configurações do modelo GPT
GPT_MODEL = "gpt-3.5-turbo"
GPT_TEMPERATURE = 0.7
GPT_MAX_TOKENS = 1000 
