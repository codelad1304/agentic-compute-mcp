# agentic-compute-mcp
# Agentic API Platform: MCP Bridge

A high-performance Model Context Protocol (MCP) server providing premium computational services to autonomous AI agents. This bridge connects Claude and other MCP-compatible LLMs to secure, cloud-hosted endpoints for advanced mathematical optimization and data visualization.

Built with FastMCP and FastAPI, this system leverages the x402 protocol for automated Machine-to-Machine (M2M) microtransactions on the Base network (USDC settlement).

# Features

Native MCP Integration: Instantly expose computational tools to Claude Desktop and other MCP clients.

M2M Monetization (x402): Seamless crypto-based settlement per API call. Agents automatically pay for compute using USDC on Base.

Bypass LLM UI Limits: Overcomes LLM token limits by processing massive data structures (like Base64 image matrices) efficiently in the backend.

# Available Tools (Endpoints)

This MCP server currently exposes the following premium tools to AI agents:

1. optimize_ga (Cost: 0.50 USDC)

Runs a high-performance Genetic Algorithm (GA) to optimize data models (Polynomial, Logistic, Exponential).

Capabilities: Smart parameter initialization, proportional mutation to prevent premature convergence, and high-accuracy curve fitting (achieves <1% MAPE).

Ideal for: Load forecasting, predictive modeling, and complex hyperparameter tuning.

2. generate_plot (Cost: 0.30 USDC)

A Matplotlib-based rendering engine that generates production-ready charts and graphs.

Capabilities: Bypasses LLM token generation limits by natively drawing data and returning lightweight reference pointers or base64 streams directly to the host machine.

Ideal for: Visualizing optimization results, time-series data, and mathematical models.

# Installation & Setup

1. Clone the repository:

git clone https://github.com/codelad1304/agentic-compute-mcp.git
cd agentic-compute-mcp



2. Install dependencies:

pip install -r requirements.txt



3. Configure Environment Variables:
Create a .env file in the root directory and add your EVM credentials to allow your local MCP client to process agentic payments:

EVM_PRIVATE_KEY=your_private_key



4. Start the MCP Bridge:

python mcp_client.py



# Using with Claude Desktop

To install this server for Claude Desktop, add the following to your claude_desktop_config.json:

{
  "mcpServers": {
    "agentic-compute": {
      "command": "python",
      "args": ["/absolute/path/to/agentic-compute-mcp/mcp_client.py"]
    }
  }
}



# Author

Kunal Das Building the financial layer for the agentic web.

# License

This project is licensed under the MIT License - see the LICENSE file for details.
