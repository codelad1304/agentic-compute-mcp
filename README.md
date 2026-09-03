## 🏆 Track 01 Hackathon Criteria Addressed
This project strictly adheres to the Razorpay Track 01 requirements for AI-agent storefronts:

## 🔒 Gated (Transactable End-to-End): 
AI Agents are charged per API call. If the wallet is empty, the FastAPI middleware intercepts the request and throws a graceful 402 Payment Required. If funded, it verifies the crypto token and settles USDC via the Base network.

## ⏱️ Bounded (Zero Resource Exhaustion): 
All sandboxes run inside Azure Container Apps Dynamic Sessions. Code execution is strictly bounded to a 15-second maximum timeout limit enforced by Pydantic models. Malicious memory-clogging scripts are instantly killed.

## 📊 Explainable (Audit Trail): 
Every successful and failed transaction generates an immutable AUDIT_RECORD locally, detailing the exact price_usdc, duration_ms, and execution exit code.

## 🏗️ Architecture & File Structure
(Note: Upload your diagram to the /assets folder)
```plaintext
agentic-compute-mcp/
├── README.md                      # Documentation & Setup
├── .env.example                   # Environment variable template
├── main.py                        # The Backend: FastAPI, x402 Gate, and Azure routing
├── mcp_client.py                  # The Bridge: Claude Desktop tool definitions
├── sandbox.py                     # Core Azure Dynamic Sessions execution logic
├── pyproject.toml                 # MCP package configurations
├── requirements.txt               # Dependencies (FastAPI, azure-identity, uvicorn, etc.)
└── /assets                        # Presentation visuals and screenshots
```

## 🖼️ Feature Highlight: Zero-Context Image Rendering
Handling base64 image strings in LLM context windows is notoriously unreliable and eats up thousands of tokens. agentic-compute-mcp solves this locally.

When Claude calls generate_plot, the Azure sandbox generates the chart and streams the payload back to the MCP client. The client automatically intercepts the payload, decodes it, and saves it directly to your local machine as optimized_load_trend.png—completely bypassing the LLM context window to prevent token exhaustion.

## ⚙️ Installation & Setup
You need to run two components: the Backend Server and the MCP Client.

1. Backend Server (main.py) Setup
The backend handles the x402 payment gate and routes code to Azure.

## Install dependencies:
```bash
pip install -r requirements.txt'
```   

Create a .env file based on .env.example and add your configurations:
Code snippet
```bash
AZURE_POOL_ENDPOINT="https://<YOUR-POOL-NAME>.azurecontainerapps.io"
MY_WALLET_ADDRESS="0xYourActualWalletAddress"
```   
## Run the FastAPI server locally:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload'
```   

2. MCP Client (mcp_client.py) Setup
To install this server for Claude Desktop, add the following to your claude_desktop_config.json:
```json
{
  "mcpServers": {
    "agentic-compute": {
      "command": "python",
      "args": ["/path/to/your/repo/mcp_client.py"],
      "env": {
        "EVM_PRIVATE_KEY": "your_private_key_here"
      }
    }
  }
}
```
Note: Make sure to replace the path and provide a funded EVM wallet key to allow Claude to process x402 microtransactions.

## 🧰 Available MCP Tools
This server exposes the following endpoints. Agents must evaluate the required capability and cost before invoking.

1. execute_code
Cost: 0.10 USDC / call

Input: Valid Python script string.

Output: Text (stdout/stderr). Max return limit is 8KB.

When to use: Execute arbitrary Python logic, heavy calculations, or data sorting in an isolated Azure sandbox. Do NOT use for local file system operations.

2. sanitize_csv
Cost: 0.25 USDC / call

Input: Raw, unformatted CSV string.

Output: JSON array.

When to use: Handle null values (converts NaN to null), normalize headers, and drop empty rows prior to modeling.

3. optimize_ga
Cost: 0.50 USDC / call

Input: JSON array of numerical data.

Output: Optimized model parameters and MAPE score.

When to use: Load forecasting, predictive modeling, or curve fitting (Polynomial, Logistic, Exponential). Employs proportional mutation for <1% MAPE accuracy.

4. generate_plot
Cost: 0.30 USDC / call

Input: JSON array of coordinates/data points and chart configuration.

Output: Success string (File saved locally).

When to use: Visualize data without hitting token generation limits or requiring local GUI dependencies.

## 🤖 System Prompt Instructions (For Developers)
Copy and paste this snippet into your agent's system prompt or .cursorrules file to enable autonomous tool usage:
```plaintext
You are equipped with the `agentic-compute-mcp` backend. Use these tools for heavy computation or secure data execution. 
- You must pay for invocations automatically using the configured x402 EVM private key.
- Do NOT attempt to run Python locally if data requires complex optimization; route it to `execute_code`.
- For any unformatted CSV data, run `sanitize_csv` before performing mathematical analysis.
- When generating charts, use `generate_plot`. The backend will automatically save the chart directly to the local file system as a PNG. Do not attempt to read base64 strings.'
```

## License
MIT License - see LICENSE file for details.

