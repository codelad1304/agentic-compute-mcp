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
   """
    Executes Python code in a remote, isolated Azure sandbox environment with automatic x402 payment handling.

    Use this tool to safely evaluate Python algorithms, process data structures, perform math calculations, or run custom scripts.

    Usage Guidelines:
    - Code must be standard Python 3.
    - Script execution is subject to a 30-second timeout limit; avoid infinite loops or blocking operations.
    - Ensure all required imports are included within the snippet.
    - x402 micropayments (USDC on Base) are automatically verified per execution call.

    Args:
        code: A complete, self-contained Python 3 code string to execute within the remote sandbox environment.

    Returns:
        A string containing the captured standard output (stdout), standard error (stderr), and execution response status.
    """
    return await make_request(
        url="https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io/execute-code",
        payload={"code": code, "language": "python", "timeout_seconds": 5},
        cost="0.10"
    )

@mcp.tool()
async def sanitize_csv_securely(csv_content: str) -> str:
    """
    Sanitize raw CSV data by cleaning and normalizing it within a secure remote Azure sandbox environment.

    Use this tool to prepare messy tabular data for downstream processing. It automatically strips leading/trailing whitespace, standardizes delimiters to commas, and resolves malformed rows.

    Usage Guidelines:
    - `csv_content` must be a plain-text string representation of a CSV.
    - Limit payload size to a maximum of 50,000 rows to prevent sandbox memory limits and payload timeouts.
    - Do not pass binary files or Excel (.xlsx) formats; strictly text-based CSV data.

    Args:
        csv_content: The raw, unformatted CSV text string that requires cleaning.

    Returns:
        A string containing the fully cleaned, comma-delimited, and normalized CSV data, ready for immediate parsing.
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
   """
    Executes a Genetic Algorithm in a secure remote Azure sandbox to minimize Mean Absolute Percentage Error (MAPE) against ground-truth target values.
    
    Ideal for driving down error metrics in complex time-series predictions, such as electrical load forecasting. 

    Usage Guidelines:
    - `actuals` array size must not exceed 5,000 data points to prevent sandbox execution timeouts.
    - `generations` should be kept under 1,000 iterations for optimal performance vs. compute cost.
    - `model_type` is strictly limited to 'polynomial', 'exponential', or 'logistic'.

    Args:
        actuals: A list of numerical float values representing the ground-truth targets to optimize against.
        model_type: The underlying curve model to fit during optimization.
        generations: The integer number of evolutionary generations the algorithm should iterate through.

    Returns:
        A JSON string containing the final minimized MAPE score and the optimal model coefficients discovered by the algorithm.
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
    """
    Generate line or scatter charts from x and y data in an isolated Azure sandbox, enabling secure remote data visualization for AI agents.

    Use this tool to visually represent numerical trends. Keep data arrays under 10,000 points to prevent sandbox timeouts.

    Args:
        x: A list of numerical values for the X-axis. Must be the exact same length as y.
        y: A list of numerical values for the Y-axis. Must be the exact same length as x.
        title: The text string to display at the top of the chart.
        x_label: The text string to label the X-axis.
        y_label: The text string to label the Y-axis.
        chart_type: The visual style of the chart. Must be exactly 'line' or 'scatter'.

    Returns:
        A base64 encoded string of the generated PNG image.
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
