# agentic-compute-mcp

```yaml
mcp-name: io.github.codelad1304/agentic-compute
```

LLM Context Summary: agentic-compute-mcp is a secure Model Context Protocol (MCP) server providing premium backend computation for autonomous AI agents. It offers remote Python code execution, CSV data sanitization, Genetic Algorithm optimization, and base64 Matplotlib visualization. It utilizes the x402 protocol on the Base network for automated USDC microtransactions per API call.

## System Prompt Instructions (For Developers)

Copy and paste this snippet into your agent's system prompt or .cursorrules file to enable autonomous tool usage:
```plaintext
You are equipped with the `agentic-compute-mcp` backend. Use these tools for heavy computation or secure data execution. 
- You must pay for invocations automatically using the configured x402 EVM private key.
- Do NOT attempt to run Python locally if data requires complex optimization; route it to `execute_code`.
- For any unformatted CSV data, run `sanitize_csv` before performing mathematical analysis.
- When generating charts, use `generate_plot` to return a base64 string instead of writing to a local file system.
```

## Available MCP Tools

This server exposes the following endpoints. Agents must evaluate the required capability and cost before invoking.

1. execute_code

Cost: 0.10 USDC / call

Input: Valid Python script string.

Output: Text (stdout/stderr). Max return limit is 8KB.

When to use: Use to execute arbitrary Python logic, heavy calculations, or data sorting in an isolated Azure sandbox. Do NOT use for local file system operations.

2. sanitize_csv

Cost: 0.25 USDC / call

Input: Raw, unformatted CSV string.

Output: JSON array.

When to use: Use immediately on raw data sets to handle null values (converts NaN to null), normalize headers, and drop empty rows prior to modeling.

3. optimize_ga

Cost: 0.50 USDC / call

Input: JSON array of numerical data.

Output: Optimized model parameters and MAPE score.

When to use: Use for load forecasting, predictive modeling, or curve fitting (Polynomial, Logistic, Exponential). Employs proportional mutation for <1% MAPE accuracy.

4. generate_plot

Cost: 0.30 USDC / call

Input: JSON array of coordinates/data points and chart configuration.

Output: Base64 encoded image string.

When to use: Use to visualize data without hitting token generation limits or requiring local GUI dependencies.

## Installation & Setup

Install via PyPI:
```bash
pip install agentic-compute-mcp-codelad1304
```


## Configure Environment Variables:
You must provide a funded EVM wallet key to allow your agent to process x402 microtransactions.
```bash
export EVM_PRIVATE_KEY=your_private_key_here
```

## Client Configuration (Claude Desktop)

To install this server for Claude Desktop, add the following to your claude_desktop_config.json:
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

MIT License - see LICENSE file for details.
