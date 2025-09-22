from src.uipath_orchestrator import UiPathOrchestrator

def main():
    try:
        # Inicializa a classe lendo as configs do .env
        uipath = UiPathOrchestrator()

        # Nome do processo publicado no Orchestrator
        process_name = "test_handler"

        # Dispara o job
        result = uipath._get_release_key(process_name)
        #result = uipath.start_job(process_name, robot_count=1)

        print("✅ Job iniciado com sucesso!")
        print(result)

    except Exception as e:
        print("❌ Erro ao iniciar o job:", str(e))

if __name__ == "__main__":
    main()
