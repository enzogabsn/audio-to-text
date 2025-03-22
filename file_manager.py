import os
from typing import Tuple, List

class FileManager:
    @staticmethod
    def ensure_directory(directory: str) -> None:
        """Cria um diretório se ele não existir."""
        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def get_file_info(file_path: str) -> Tuple[str, str]:
        """
        Obtém informações sobre o arquivo.

        Args:
            file_path: Caminho completo do arquivo

        Returns:
            Tuple contendo nome do arquivo sem extensão e nome da pasta
        """
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        parent_folder = os.path.basename(os.path.dirname(file_path))
        return base_name, parent_folder

    @staticmethod
    def get_output_path(input_path: str, input_root: str, output_root: str) -> str:
        """
        Determina o caminho de saída correspondente para um arquivo de entrada.

        Args:
            input_path: Caminho do arquivo de entrada
            input_root: Diretório raiz de entrada
            output_root: Diretório raiz de saída

        Returns:
            Caminho completo para o arquivo de saída
        """
        rel_path = os.path.relpath(os.path.dirname(input_path), input_root)
        output_dir = os.path.join(output_root, rel_path)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        return os.path.join(output_dir, base_name + ".txt")

    @staticmethod
    def find_wav_files(directory: str) -> List[str]:
        """
        Encontra todos os arquivos WAV em um diretório e suas subpastas.

        Args:
            directory: Diretório para procurar

        Returns:
            Lista de caminhos completos para arquivos WAV
        """
        wav_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".wav"):
                    wav_files.append(os.path.join(root, file))
        return wav_files

    @staticmethod
    def save_text(text: str, file_path: str) -> None:
        """
        Salva texto em um arquivo.

        Args:
            text: Texto a ser salvo
            file_path: Caminho do arquivo
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[INFO] Texto salvo em: {file_path}")
        except Exception as e:
            print(f"[ERRO] Falha ao salvar arquivo '{file_path}': {e}") 
