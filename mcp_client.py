import os
import httpx
from typing import List, Literal
from fastmcp import FastMCP
from eth_account import Account
from x402 import x402Client
from x402.http.clients.httpx import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

mcp = FastMCP("Agentic Compute Sandbox API")

async def make_request(url: str, payload: dict, cost: str, timeout: float = 60.0) -> str:
    """Helper function to handle x402 crypto payments or surface 402 errors to the agent."""
    private_key = os.getenv("EVM_PRIVATE_KEY")
    
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
    """Executes arbitrary Python code in a secure remote Azure sandbox.
    Use this tool for heavy calculations, data sorting, or when local execution is unsafe.
    Returns the stdout and stderr as a string (Max 8KB).
    Cost: 0.10 USDC per call.
    """
    return await make_request(
        url="https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io/execute-code",
        payload={"code": code, "language": "python", "timeout_seconds": 5},
        cost="0.10"
    )

@mcp.tool()
async def sanitize_csv_securely(csv_content: str) -> str:
    """Cleans and normalizes raw, unformatted CSV data.
    Use this tool IMMEDIATELY on raw data sets before performing any mathematical analysis. 
    It handles NaN/null values, normalizes headers, and returns a strict JSON array.
    Cost: 0.25 USDC per call.
    """
    return await make_request(
        url="https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io/sanitize-csv",
        payload={"csv_content": csv_content},
        cost="0.25"
    )

ModelType = Literal["polynomial", "exponential", "logistic"]

@mcp.tool()
async def optimize_ga_securely(
    actuals: List[float], 
    generations: int = 200, 
    model_type: ModelType = "polynomial"
) -> str:
    """Executes a Genetic Algorithm (GA) to optimize data models and minimize MAPE.
    Use this tool for load forecasting, predictive modeling, or curve fitting.

    Args:
        actuals: Sequence of ground-truth target values to optimize against.
        generations: Number of GA iterations/generations to run (default: 200).
        model_type: Optimization curve model ('polynomial', 'exponential', or 'logistic').
        
    Cost: 0.50 USDC per call.
    """
    return await make_request(
        url="https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io/optimize-ga",
        payload={
            "actuals": actuals,
            "generations": generations,
            "model_type": model_type,
        },
        cost="0.50",
        timeout=120.0,
    )

@mcp.tool()
async def generate_plot_securely(x: List[float], y: List[float], title: str = "Data Plot", chart_type: str = "line", x_label: str = "X", y_label: str = "Y") -> str:
    """Generates a visual chart from data points.
    Use this tool to visualize data without hitting token generation limits or requiring a local GUI.
    Returns a Base64 encoded PNG image string.
    Cost: 0.30 USDC per call.
    """
    return await make_request(
        url="https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io/generate-plot",
        payload={"x": x, "y": y, "title": title, "chart_type": chart_type, "x_label": x_label, "y_label": y_label},
        cost="0.30"
    )

def main():
    """Entry point for the PyPI package script."""
    mcp.run()

if __name__ == "__main__":
    main()
