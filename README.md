# workflow-advisor-mcp

An MCP server with no inner LLM and no API keys. The host model (Claude, ChatGPT,
Cursor) does the reasoning and the web search. The server supplies what a model
should not improvise.

| Piece | What it does |
| --- | --- |
| `get_diagnosis_framework()` | Returns the method and reply format the host should follow |
| `estimate_time_saved(minutes_per_day, days_per_week)` | Hours lost per year, computed by code, validated before it runs |
| `diagnose_my_workflow` (prompt) | One-click starter in hosts that surface MCP prompts |

## Run locally
```bash
pip install -r requirements.txt
python -m fastmcp dev server.py   # MCP Inspector: both tools should be listed
                                  # (use `python -m` if `fastmcp` is not found on Windows)
python server.py            # http://localhost:8000/mcp
```

## Deploy on Prefect Horizon (formerly FastMCP Cloud)
1. Push this folder to GitHub.
2. On horizon.prefect.io, sign in with GitHub and select the repo.
3. Entrypoint: `server.py:mcp` (prefix the folder if it lives in a subfolder).
4. Deploy. No environment variables needed. Your URL is `https://<project>.fastmcp.app/mcp`.

## Connect
- claude.ai: + -> Connectors -> Add custom connector -> paste the `/mcp` URL
- Claude Code: `claude mcp add --transport http workflow-advisor https://<project>.fastmcp.app/mcp`

Try: "Diagnose my morning Jira routine. How many hours would automating it save
at 40 minutes a day, 5 days a week?" Expect the host to call
`get_diagnosis_framework`, search the web, then call `estimate_time_saved` for 173.3 hours.
Then drop the numbers and check that the host asks for them instead of guessing.

## Cost and security
Nothing here spends credits, so there is no rate limit to maintain. The tools are
read-only and deterministic. Anyone with the URL can call them, which is
harmless today but worth revisiting if you add tools that touch real data.