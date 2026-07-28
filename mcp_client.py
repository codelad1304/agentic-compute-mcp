import os
import httpx
from typing import List
from fastmcp import FastMCP

# Core x402 & Web3 Imports moved to the global level
from eth_account import Account
from x402 import x402Client
from x402.http.clients.httpx import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

mcp = FastMCP("Agentic Compute Sandbox API")
private_key = os.getenv("EVM_PRIVATE_KEY")

async def make_request(url: str, payload: dict, cost: str, timeout: float = 60.0) -> str:
    """Helper function to handle x402 crypto payments or surface 402 errors to the agent."""
    if private_key:
        try:
            account = Account.from_key(private_key)
            client = x402Client()
            register_exact_evm_client(client, EthAccountSigner(account))
            
            async with x402HttpxClient(client, timeout=timeout) as http:
                response = await http.post(url, json=payload)
                response.raise_for_status()
                return str(response.json())
                
        except Exception as e:
            return f"Failed to execute with automatic payment: {str(e)}"
    else:
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return str(response.json())
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 402:
                return f"Payment Required: The server requested {cost} USDC. Please add an 'EVM_PRIVATE_KEY' to your MCP env config to enable automatic agent payments."
            return f"HTTP Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error connecting to sandbox: {str(e)}"

@mcp.tool()
async def execute_code_securely(code: str) -> str:
    """Executes Python code in the remote Azure sandbox, automatically handling x402 payments."""
    return await make_request(
        url="https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io/execute-code",
        payload={"code": code, "language": "python", "timeout_seconds": 5},
        cost="0.10"
    )

@mcp.tool()
async def sanitize_csv_securely(csv_content: str) -> str:
    """Cleans and normalizes raw CSV data in the remote Azure sandbox."""
    return await make_request(
        url="https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io/sanitize-csv",
        payload={"csv_content": csv_content},
        cost="0.25"
    )

@mcp.tool()
async def optimize_ga_securely(actuals: List[float], generations: int = 200, model_type: str = "polynomial") -> str:
    """Executes a Genetic Algorithm in the remote Azure sandbox to minimize MAPE. model_type can be 'polynomial', 'exponential', or 'logistic'."""
    return await make_request(
        url="https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io/optimize-ga",
        payload={"actuals": actuals, "generations": generations, "model_type": model_type},
        cost="0.50",
        timeout=120.0
    )

@mcp.tool()
async def generate_plot_securely(x: List[float], y: List[float], title: str = "Data Plot", chart_type: str = "line", x_label: str = "X", y_label: str = "Y") -> str:
    """Generates a visual chart (line or scatter) in the remote Azure sandbox."""
    return await make_request(
        url="https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io/generate-plot",
        payload={"x": x, "y": y, "title": title, "chart_type": chart_type, "x_label": x_label, "y_label": y_label},
        cost="0.30"
    )

if __name__ == "__main__":
    mcp.run()