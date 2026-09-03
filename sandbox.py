import time
import requests
from azure.identity import DefaultAzureCredential

class AzureDynamicSandbox:
    def __init__(self, pool_endpoint: str, session_id: str = "agent-sandbox-1"):
        """Initialize the sandbox connection to Azure Container Apps."""
        self.pool_endpoint = pool_endpoint
        self.session_id = session_id
        self.credential = DefaultAzureCredential()

    def run_code_in_sandbox(self, code_str: str, timeout: int = 5) -> dict:
        """
        Sends Python code to the Azure serverless sandbox, returning a 
        deterministic schema with execution duration and audit state.
        """
        start_time = time.time()
        try:
            token = self.credential.get_token("https://acasessions.io/.default").token
        except Exception as e:
            return {
                "status": "error",
                "error_type": "AUTH_FAILURE",
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Failed to authenticate with Azure Session Pool: {str(e)}",
                "duration_ms": round((time.time() - start_time) * 1000, 2)
            }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "properties": {
                "codeInputType": "inline",
                "executionType": "synchronous",
                "code": code_str
            }
        }
        
        url = f"{self.pool_endpoint}/code/execute?api-version=2024-02-02-preview&identifier={self.session_id}"

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout + 2)
            response.raise_for_status()
            
            properties = response.json().get("properties", {})
            stdout = properties.get("stdout", "")
            stderr = properties.get("stderr", "")
            
            if not stdout and properties.get("result"):
                stdout = str(properties.get("result"))
            
            exit_code = 1 if stderr else 0
            status = "failed" if stderr else "success"
            
            return {
                "status": status,
                "error_type": "RUNTIME_ERROR" if stderr else None,
                "exit_code": exit_code,
                "stdout": stdout,
                "stderr": stderr,
                "duration_ms": round((time.time() - start_time) * 1000, 2)
            }
            
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "error_type": "EXECUTION_TIMEOUT",
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Execution exceeded bounded timeout limit of {timeout}s.",
                "duration_ms": round((time.time() - start_time) * 1000, 2)
            }
        except Exception as e:
            return {
                "status": "error",
                "error_type": "SANDBOX_INTERRUPT",
                "exit_code": -1,
                "stdout": "",
                "stderr": f"Sandbox security interruption: {str(e)}",
                "duration_ms": round((time.time() - start_time) * 1000, 2)
            }