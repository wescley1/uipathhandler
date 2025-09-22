import subprocess
import json
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class UiPathProcess:
    def __init__(self, process_name=None, uipath_robot_path=None):
        self.process_name = process_name or os.getenv('UIPATH_PROCESS_NAME')
        self.uipath_robot_path = uipath_robot_path or os.getenv('UIPATH_ROBOT_PATH')
        self.process = None
        self.logs = [] # Lista para armazenar os logs

    def start_process(self, input_arguments=None):
        """
        Inicia a execução do processo UiPath e captura a saída.
        """
        if not self.process_name or not self.uipath_robot_path:
            raise ValueError("O nome do processo ou o caminho do UiRobot não foi fornecido ou não está no .env")

        print(f"Iniciando o processo UiPath: {self.process_name}")
        
        command_list = [self.uipath_robot_path, 'execute', f'--file "{self.process_name}"']
        
        if input_arguments:
            args_json = json.dumps(input_arguments)
            #command_list.append(f'--input "{args_json}"')
            command_list.append(f'--input "{str(input_arguments)}"')
            #command_list.append("""--input "{'in_text': 'Hello from Python!'}" """)

        command = ' '.join(command_list)

        try:
            # Redireciona stdout e stderr para PIPE para capturar a saída
            self.process = subprocess.Popen(
                ['powershell', '-NoProfile', '-Command', command],
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True # Decodifica a saída como texto
            )
            print(f"Processo '{self.process_name}' iniciado com sucesso.")
        except FileNotFoundError:
            print("Erro: Verifique se o caminho para o UiRobot.exe está correto.")
            self.process = None
        except Exception as e:
            print(f"Erro ao iniciar o processo: {e}")
            self.process = None
            
    def wait_for_completion(self, timeout=3600):
        """
        Espera a conclusão do processo e captura os logs.
        """
        if self.process is None:
            print("O processo não foi iniciado.")
            return -1
            
        print(f"Aguardando a conclusão do processo '{self.process_name}'...")
        try:
            # O .communicate() espera o processo terminar e retorna stdout e stderr
            stdout, stderr = self.process.communicate(timeout=timeout)
            
            # Divide os logs em linhas e armazena na lista
            self.logs = (stdout + stderr).splitlines()
            
            print(f"Processo '{self.process_name}' concluído com código de retorno: {self.process.returncode}")
            return self.process.returncode
        except subprocess.TimeoutExpired:
            print(f"Tempo limite de {timeout} segundos atingido. O processo pode ainda estar em execução.")
            self.process.kill()
            return -2

    def get_logs(self):
        """
        Retorna a lista de logs capturados.
        """
        return self.logs
