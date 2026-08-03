# agentic-compute-mcp

## Agentic API Platform: MCP Bridge
<!-- mcp-name: io.github.codelad1304/agentic-compute -->

A high-performance Model Context Protocol (MCP) server providing premium computational services to autonomous AI agents. This bridge connects Claude and other MCP-compatible LLMs to secure, cloud-hosted endpoints for advanced mathematical optimization and data visualization.

Built with FastMCP and FastAPI, this system leverages the x402 protocol for automated Machine-to-Machine (M2M) microtransactions on the Base network (USDC settlement).

## Features

**Native MCP Integration**: Instantly expose computational tools to Claude Desktop and other MCP clients.

**M2M Monetization (x402)**: Seamless crypto-based settlement per API call. Agents automatically pay for compute using USDC on Base.

**Bypass LLM UI Limits**: Overcomes LLM token limits by processing massive data structures (like Base64 image matrices) efficiently in the backend.

## Available Tools (Endpoints)

This MCP server currently exposes the following premium tools to AI agents:

1. **execute_code** (Cost: 0.10 USDC)

* Executes arbitrary, agent-generated Python code in a highly secure, isolated remote Azure sandbox.

* **Capabilities**: Protects the host machine from untrusted code execution while returning standard output (stdout) and standard error (stderr) directly to the agent.

2. **sanitize_csv** (Cost: 0.25 USDC)

* Cleans and normalizes raw, unstructured CSV data into strict JSON arrays.

* **Capabilities**: Automatically normalizes headers, handles null values, and drops empty rows, preparing messy data for immediate mathematical modeling.

3. **optimize_ga** (Cost: 0.50 USDC)

* Runs a high-performance Genetic Algorithm (GA) to optimize data models (Polynomial, Logistic, Exponential).

* **Capabilities**: Smart parameter initialization, proportional mutation to prevent premature convergence, and high-accuracy curve fitting (achieves <1% MAPE).

* **Ideal for**: Load forecasting, predictive modeling, and complex hyperparameter tuning.

4. **generate_plot** (Cost: 0.30 USDC)

* A Matplotlib-based rendering engine that generates production-ready charts and graphs.

* **Capabilities**: Bypasses LLM token generation limits by natively drawing data and returning lightweight base64 image streams directly to the host machine.

* **Ideal for**: Visualizing optimization results, time-series data, and mathematical models.

## Installation & Setup

1. **Install via PyPI**:

```bash
pip install agentic-compute-mcp-codelad1304
```


2. **Configure Environment Variables**:
Create a .env file or export the following variable in your terminal to allow your local MCP client to process agentic payments:

```bash
export EVM_PRIVATE_KEY=your_private_key_here
```


## Using with Claude Desktop

* To install this server for Claude Desktop, add the following to your claude_desktop_config.json:
```json
{
  "mcpServers": {
    "agentic-compute": {
      "command": "agentic-compute-mcp",
      "args": [],
      "env": {
        "EVM_PRIVATE_KEY": "your_private_key_here"
      }
    }
  }
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
