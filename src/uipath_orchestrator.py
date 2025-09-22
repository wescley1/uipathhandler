import requests
import json
import os
from dotenv import load_dotenv

class UiPathOrchestrator:
    def __init__(self, env_file=".env"):
        """
        Inicializa a conexão lendo do .env
        """
        load_dotenv(env_file)

        self.url = os.getenv("UIPATH_URL", "").rstrip('/')
        self.organization = os.getenv("UIPATH_ORGANIZATION", "")
        self.tenant = os.getenv("UIPATH_TENANT", "")
        self.client_id = os.getenv("UIPATH_CLIENT_ID", "")
        self.user_key = os.getenv("UIPATH_USER_KEY", "")
        self.folder_id = os.getenv("UIPATH_FOLDER_ID", "")
        self.app_id = os.getenv("APP_ID", "")
        self.app_secret = os.getenv("APP_SECRET", "")
        self.token = None

        if not all([self.url, self.tenant, self.client_id, self.user_key, self.folder_id]):
            raise ValueError("Alguma variável obrigatória não foi encontrada no .env")

    def authenticate(self):
        """Autentica no Orchestrator e guarda o token"""
        auth_url = f"{self.url}/identity_/connect/token"
        #auth_url = f"{self.url}/api/Account/Authenticate"

        payload = f'grant_type=client_credentials&client_id={self.app_id}&client_secret={self.app_secret}&scope=OR.Default'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(auth_url, data=payload, headers=headers)
        response.raise_for_status()
        print(str(response))
        self.token = response.json()["access_token"]

    def start_job(self, process_name, robot_count=1, strategy="ModernJobsCount"):
        """
        Dispara um job de um processo no Orchestrator.
        :param process_name: Nome do processo publicado no Orchestrator
        :param robot_count: Quantidade de robôs a serem alocados
        :param strategy: Estratégia de execução (ModernJobsCount ou Specific)
        """
        if not self.token:
            self.authenticate()

        jobs_url = f"{self.url}/{self.tenant}/orchestrator_/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-UIPATH-OrganizationUnitId": str(self.folder_id),
            "Content-Type": "application/json"
        }

        payload = {
            "startInfo": {
                "ReleaseKey": self._get_release_key(process_name),
                "Strategy": strategy,
                "JobsCount": robot_count,
                "Source": "Manual"
            }
        }

        response = requests.post(jobs_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()

    def _get_release_key(self, process_name):
        """Busca a ReleaseKey de um processo pelo nome"""
        if not self.token:
            self.authenticate()

        releases_url = f"{self.url}/{self.tenant}/orchestrator_/odata/Job?$filter=Name eq '{process_name}'"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(releases_url, headers=headers)
        response.raise_for_status()
        results = response.json().get("value", [])
        if not results:
            raise ValueError(f"Processo '{process_name}' não encontrado.")
        return results[0]["Key"]
