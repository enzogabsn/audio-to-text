import os
import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
from config import INPUT_FOLDER, OUTPUT_FOLDER
from audio_processor import AudioProcessor
from text_processor import TextProcessor
from file_manager import FileManager

# Carrega variáveis de ambiente do arquivo .env (contendo OPENAI_API_KEY)
load_dotenv()

# Inicializa o cliente OpenAI com a chave da API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cria a pasta de saída se não existir
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def reescrever_chatgpt(texto_original: str, nome_arquivo_sem_extensao: str, nome_pasta: str) -> str:
    """
    Pede ao ChatGPT para, mesmo que o texto pareça correto,
    adicionar pontuação, separar em parágrafos bem definidos,
    incluir o nome da pasta e do arquivo no topo no formato "# Nome da pasta - Nome do arquivo Texto da IA"

    Args:
        texto_original: O texto a ser reescrito
        nome_arquivo_sem_extensao: O nome do arquivo de áudio sem a extensão
        nome_pasta: O nome da pasta onde está o arquivo
    """
    prompt_text = (
        "Corrija, melhore e adicione pontuação ao texto em português, "
        "mesmo que já pareça correto. Separe em pelo menos dois parágrafos distintos, "
        "adicione vírgulas, pontos finais e interrogações onde possível. "
        "Certifique-se de que o texto tenha uma estrutura de parágrafos clara, "
        "com cada parágrafo separado por uma linha em branco. "
        f"Comece o texto com a linha '# {nome_pasta} - {nome_arquivo_sem_extensao} Texto Final Revisado', "
        "sem nenhuma linha adicional antes desse título. "
        "Exemplo de formatação desejada:\n\n"
        f"# {nome_pasta} - {nome_arquivo_sem_extensao}\n\n"
        "Este é o primeiro parágrafo com várias frases. "
        "Cada frase tem pontuação adequada. "
        "O parágrafo termina com um ponto final.\n\n"
        "Este é o segundo parágrafo. "
        "Ele também tem várias frases com pontuação adequada. "
        "O objetivo é ter um texto bem formatado e de fácil leitura.\n\n"
        f"Texto a ser reescrito: {texto_original}"
    )

    print("[DEBUG] Chamando ChatGPT com o prompt:\n", prompt_text)

    try:
        # Utiliza a nova estrutura da API do OpenAI
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente de escrita em português que melhora, "
                        "pontua e formata textos. Reescreva o texto fornecido dividindo-o "
                        "em parágrafos claros e bem definidos, separados por linhas em branco. "
                        "Use pontuação adequada e mantenha o texto bem estruturado."
                        "Escreva somente, SOMENTE o texto e mais nada."
                    )
                },
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # A estrutura da resposta é diferente na nova API
        texto_reescrito = resposta.choices[0].message.content.strip()

        print("[DEBUG] ChatGPT concluiu o processo com sucesso.")
        return texto_reescrito
    except Exception as e:
        print(f"[ERRO] Falha ao chamar a API do ChatGPT: {e}")
        # Em caso de erro, retorna um texto formatado manualmente com o nome da pasta e do arquivo
        return f"# {nome_pasta} - {nome_arquivo_sem_extensao}\n\n{texto_original}"


def processar_arquivo_audio(audio_path, output_folder):
    """
    Processa um único arquivo de áudio WAV, extraindo texto e reescrevendo-o.
    
    Args:
        audio_path: Caminho completo para o arquivo de áudio
        output_folder: Pasta onde o texto será salvo
    """
    # Extrai o nome do arquivo sem a extensão
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    
    # Determina a pasta pai do arquivo
    parent_folder = os.path.basename(os.path.dirname(audio_path))
    
    # Cria o caminho para o arquivo de texto de saída
    text_file_path = os.path.join(output_folder, base_name + ".txt")
    
    # Garante que a pasta de saída exista
    os.makedirs(os.path.dirname(text_file_path), exist_ok=True)
    
    print(f"[INFO] Processando arquivo: {audio_path}")
    
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            texto_bruto = recognizer.recognize_google(audio_data, language="pt-BR")
            print(f"[PASSO 1] Áudio transcrito: {os.path.basename(audio_path)}")
    except sr.UnknownValueError:
        texto_bruto = "Não foi possível entender o áudio."
        print(f"[AVISO] Não foi possível entender o áudio: {os.path.basename(audio_path)}")
    except sr.RequestError:
        texto_bruto = "Erro ao conectar ao serviço de reconhecimento de fala."
        print(f"[ERRO] Falha no serviço de reconhecimento: {os.path.basename(audio_path)}")
    except Exception as e:
        texto_bruto = f"Erro ao processar o áudio: {str(e)}"
        print(f"[ERRO] Falha ao processar o áudio '{os.path.basename(audio_path)}': {e}")
        return

    # Salva transcrição bruta
    try:
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(texto_bruto)
        print(f"[PASSO 2] Transcrição criada: {text_file_path}")
    except Exception as e:
        print(f"[ERRO] Falha ao salvar '{text_file_path}': {e}")
        return

    # Ler o texto e enviar ao ChatGPT
    try:
        with open(text_file_path, "r", encoding="utf-8") as f:
            texto_original = f.read()
    except Exception as e:
        print(f"[ERRO] Falha ao ler '{text_file_path}': {e}")
        return

    # Passa o nome do arquivo sem extensão e o nome da pasta para a função de reescrita
    texto_reescrito = reescrever_chatgpt(texto_original, base_name, parent_folder)

    # Comparar e mostrar no console
    print("------ COMPARAÇÃO DE TEXTO ------")
    print("ORIGINAL:\n", texto_original)
    print("REESCRITO:\n", texto_reescrito)
    print("---------------------------------\n")

    # Sobrescrever o arquivo .txt com a versão reescrita
    try:
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(texto_reescrito)
        print(f"[PASSO 3] Arquivo reescrito: {text_file_path}\n")
    except Exception as e:
        print(f"[ERRO] Falha ao sobrescrever '{text_file_path}': {e}")


def percorrer_pastas_recursivamente(input_folder, output_folder):
    """
    Percorre recursivamente todas as pastas e subpastas em busca de arquivos WAV.
    
    Args:
        input_folder: Pasta de entrada a ser percorrida
        output_folder: Pasta de saída para os arquivos de texto
    """
    
    arquivos_wav_encontrados = False
    
    # Percorre arquivos e pastas no diretório atual
    for item in os.listdir(input_folder):
        caminho_completo = os.path.join(input_folder, item)
        
        # Se for um arquivo WAV, processa
        if os.path.isfile(caminho_completo) and item.lower().endswith(".wav"):
            # Determina o caminho relativo desde a pasta de entrada principal
            caminho_relativo = os.path.relpath(os.path.dirname(caminho_completo), INPUT_FOLDER)
            
            # Cria o caminho correspondente na pasta de saída
            pasta_saida_correspondente = os.path.join(OUTPUT_FOLDER, caminho_relativo)
            os.makedirs(pasta_saida_correspondente, exist_ok=True)
            
            # Processa o arquivo de áudio
            processar_arquivo_audio(caminho_completo, pasta_saida_correspondente)
            arquivos_wav_encontrados = True
        
        # Se for uma pasta, percorre recursivamente
        elif os.path.isdir(caminho_completo):
            print(f"[INFO] Entrando na pasta: {caminho_completo}")
            
            # Determina o caminho relativo desde a pasta de entrada principal
            caminho_relativo = os.path.relpath(caminho_completo, INPUT_FOLDER)
            
            # Cria o caminho correspondente na pasta de saída
            pasta_saida_correspondente = os.path.join(OUTPUT_FOLDER, caminho_relativo)
            os.makedirs(pasta_saida_correspondente, exist_ok=True)
            
            # Chama recursivamente para a subpasta
            subpasta_encontrou_arquivos = percorrer_pastas_recursivamente(
                caminho_completo, pasta_saida_correspondente
            )
            
            arquivos_wav_encontrados = arquivos_wav_encontrados or subpasta_encontrou_arquivos
    
    if not arquivos_wav_encontrados:
        print(f"[INFO] Nenhum arquivo WAV encontrado em: {input_folder}")
    
    return arquivos_wav_encontrados


def executar_fluxo():
    """
    Executa o fluxo principal do programa, percorrendo a pasta de entrada
    e todas as suas subpastas em busca de arquivos WAV para processar.
    """
    print(f"[INFO] Iniciando processamento recursivo a partir de: {INPUT_FOLDER}")
    encontrou_arquivos = percorrer_pastas_recursivamente(INPUT_FOLDER, OUTPUT_FOLDER)
    
    if encontrou_arquivos:
        print("[INFO] Fluxo concluído com sucesso!")
    else:
        print("[AVISO] Nenhum arquivo WAV foi encontrado em nenhuma pasta!")


class AudioTextConverter:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.text_processor = TextProcessor()
        self.file_manager = FileManager()

    def process_audio_file(self, audio_path: str) -> None:
        """
        Processa um único arquivo de áudio.

        Args:
            audio_path: Caminho do arquivo de áudio
        """
        # Obtém informações do arquivo
        base_name, parent_folder = self.file_manager.get_file_info(audio_path)
        output_path = self.file_manager.get_output_path(audio_path, INPUT_FOLDER, OUTPUT_FOLDER)

        print(f"[INFO] Processando arquivo: {audio_path}")

        # Transcreve o áudio
        texto_bruto = self.audio_processor.transcribe_audio(audio_path)

        # Salva a transcrição bruta
        self.file_manager.save_text(texto_bruto, output_path)

        # Reescreve o texto usando GPT
        texto_reescrito = self.text_processor.rewrite_text(texto_bruto, base_name, parent_folder)

        # Mostra comparação
        print("\n------ COMPARAÇÃO DE TEXTO ------")
        print("ORIGINAL:\n", texto_bruto)
        print("\nREESCRITO:\n", texto_reescrito)
        print("---------------------------------\n")

        # Salva o texto reescrito
        self.file_manager.save_text(texto_reescrito, output_path)

    def process_all_files(self) -> None:
        """Processa todos os arquivos WAV encontrados."""
        print(f"[INFO] Iniciando processamento em: {INPUT_FOLDER}")
        
        # Encontra todos os arquivos WAV
        wav_files = self.file_manager.find_wav_files(INPUT_FOLDER)
        
        if not wav_files:
            print("[AVISO] Nenhum arquivo WAV encontrado!")
            return

        # Processa cada arquivo
        for audio_path in wav_files:
            self.process_audio_file(audio_path)

        print("[INFO] Processamento concluído com sucesso!")


def main():
    """Função principal do programa."""
    converter = AudioTextConverter()
    converter.process_all_files()


if __name__ == "__main__":
    main()
