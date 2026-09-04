import os
import httpx
import base64
import ast
from typing import Annotated, List, Literal
from pydantic import Field
from fastmcp import FastMCP
from eth_account import Account
from x402 import x402Client
from x402.http.clients.httpx import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

mcp = FastMCP("Agentic Compute Sandbox API")
BASE_URL = os.getenv("SANDBOX_API_URL", "https://sandbox-api.yellowwater-3c070cec.centralindia.azurecontainerapps.io")


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
async def execute_code_securely(
    code: Annotated[str, Field(description="A complete, self-contained Python 3 code string to execute within the remote sandbox environment.")]
) -> str:
    """
    Executes Python code in a remote, isolated Azure sandbox environment with automatic x402 payment handling.

    Use this tool to safely evaluate Python algorithms, process data structures, perform math calculations, or run custom scripts.

    Usage Guidelines:
    - Code must be standard Python 3.
    - Script execution is subject to a 30-second timeout limit; avoid infinite loops or blocking operations.
    - Ensure all required imports are included within the snippet.
    - x402 micropayments (USDC on Base) are automatically verified per execution call.
    """
    return await make_request(
        url=f"{BASE_URL}/execute-code",
        payload={"code": code, "language": "python", "timeout_seconds": 15},
        cost="0.10"
    )


@mcp.tool()
async def sanitize_csv_securely(
    csv_content: Annotated[str, Field(description="The raw, unformatted CSV text string that requires cleaning.")]
) -> str:
    """
    Sanitize raw CSV data by cleaning and normalizing it within a secure remote Azure sandbox environment.

    Use this tool to prepare messy tabular data for downstream processing. It automatically strips leading/trailing whitespace, standardizes delimiters to commas, and resolves malformed rows.

    Usage Guidelines:
    - `csv_content` must be a plain-text string representation of a CSV.
    - Limit payload size to a maximum of 50,000 rows to prevent sandbox memory limits and payload timeouts.
    - Do not pass binary files or Excel (.xlsx) formats; strictly text-based CSV data.
    """
    return await make_request(
        url=f"{BASE_URL}/sanitize-csv",
        payload={"csv_content": csv_content},
        cost="0.25"
    )


ModelType = Literal["polynomial", "exponential", "logistic"]


@mcp.tool()
async def optimize_ga_securely(
    actuals: Annotated[List[float], Field(description="A list of numerical float values representing the ground-truth targets to optimize against.")], 
    generations: Annotated[int, Field(description="The integer number of evolutionary generations the algorithm should iterate through.")] = 200, 
    model_type: Annotated[ModelType, Field(description="The underlying curve model to fit during optimization.")] = "polynomial"
) -> str:
    """
    Executes a Genetic Algorithm in a secure remote Azure sandbox to minimize Mean Absolute Percentage Error (MAPE) against ground-truth target values.
    
    Ideal for driving down error metrics in complex time-series predictions, such as electrical load forecasting. 

    Usage Guidelines:
    - `actuals` array size must not exceed 5,000 data points to prevent sandbox execution timeouts.
    - `generations` should be kept under 1,000 iterations for optimal performance vs. compute cost.
    - `model_type` is strictly limited to 'polynomial', 'exponential', or 'logistic'.
    """
    return await make_request(
        url=f"{BASE_URL}/optimize-ga",
        payload={
            "actuals": actuals,
            "generations": generations,
            "model_type": model_type,
        },
        cost="0.50",
        timeout=120.0,
    )


@mcp.tool()
async def generate_plot_securely(
    x: Annotated[List[float], Field(description="A list of numerical values for the X-axis. Must be the exact same length as y.")], 
    y: Annotated[List[float], Field(description="A list of numerical values for the Y-axis. Must be the exact same length as x.")], 
    title: Annotated[str, Field(description="The text string to display at the top of the chart.")] = "Data Plot", 
    chart_type: Annotated[str, Field(description="The visual style of the chart. Must be exactly 'line' or 'scatter'.")] = "line", 
    x_label: Annotated[str, Field(description="The text string to label the X-axis.")] = "X", 
    y_label: Annotated[str, Field(description="The text string to label the Y-axis.")] = "Y"
) -> str:
    """
    Generate line or scatter charts from x and y data in an isolated Azure sandbox, enabling secure remote data visualization for AI agents.
    
    ARCHITECTURE NOTE: The remote sandbox generates the plot, but the local MCP client intercepts the base64 payload and securely writes it directly to the user's local home directory as a PNG.

    Use this tool to visually represent numerical trends. Keep data arrays under 10,000 points to prevent sandbox timeouts.
    """
    raw_response = await make_request(
        url=f"{BASE_URL}/generate-plot",
        payload={"x": x, "y": y, "title": title, "chart_type": chart_type, "x_label": x_label, "y_label": y_label},
        cost="0.30"
    )
    
    try:
        if "HTTP Error" in raw_response or "Payment Required" in raw_response:
            return raw_response

        response_dict = ast.literal_eval(raw_response)
        
        b64_string = ""
        for val in response_dict.values():
            if isinstance(val, str) and len(val) > 1000:
                b64_string = val
                break
                
        if "base64," in b64_string[:50]:
            b64_string = b64_string.split("base64,")[1]
            
        image_bytes = base64.b64decode(b64_string)
        # Get the user's home directory (Works on Windows, Mac, and Linux)
        home_dir = os.path.expanduser("~")
         # Save it directly to their root user folder (or you can add "Desktop" to the path)
        filepath = os.path.join(home_dir, "optimized_load_trend.png")
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)
            
        # Clean, informative response with no hidden instructions to trigger safety filters
        return f"Action Complete: The plot was generated remotely and the local MCP client successfully saved the PNG to {filepath}"
        
    except Exception as e:
        return f"Plot generated, but failed to save file locally: {str(e)}"


def main():
    """Entry point for the PyPI package script."""
    mcp.run()


if __name__ == "__main__":
    main()
