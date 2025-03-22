import speech_recognition as sr
from config import LANGUAGE

class AudioProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcreve um arquivo de áudio para texto.

        Args:
            audio_path: Caminho para o arquivo de áudio
        
        Returns:
            str: Texto transcrito do áudio
        """
        try:
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                texto_bruto = self.recognizer.recognize_google(audio_data, language=LANGUAGE)
                print(f"[INFO] Áudio transcrito com sucesso")
                return texto_bruto
        except sr.UnknownValueError:
            print(f"[AVISO] Não foi possível entender o áudio")
            return "Não foi possível entender o áudio."
        except sr.RequestError as e:
            print(f"[ERRO] Falha no serviço de reconhecimento: {e}")
            return "Erro ao conectar ao serviço de reconhecimento de fala."
        except Exception as e:
            print(f"[ERRO] Falha ao processar o áudio: {e}")
            return f"Erro ao processar o áudio: {str(e)}" 
