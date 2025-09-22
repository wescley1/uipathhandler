from src.uipath_manager import UiPathProcess
import os

if __name__ == '__main__':
    # Cria uma instância da classe. Ela irá ler os valores do .env.
    uipath_proc = UiPathProcess()
    args = {"in_text": "Hello from Python!"}
    # Inicia o processo
    uipath_proc.start_process(input_arguments=args)

    # Aguarda a conclusão
    return_code = uipath_proc.wait_for_completion()
    
    print("\n--- Logs da Execução do UiPath ---")
    for log_line in uipath_proc.get_logs():
        print(log_line)

    if return_code == 0:
        print("Automação do UiPath executada com sucesso!")
    else:
        print(f"A automação falhou com o código de erro: {return_code}")
