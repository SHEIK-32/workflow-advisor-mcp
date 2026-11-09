# workflow-advisor-mcp

An MCP server that diagnoses a repetitive workflow and returns an automation
plan grounded in a live web search, plus an exact time-saved calculator.

| Tool | What it does |
| --- | --- |
| `diagnose_workflow(workflow_description)` | Runs the inner decide -> execute -> respond loop (Groq + Tavily) and returns a plan |
| `estimate_time_saved(minutes_per_day, days_per_week)` | Hours lost per year, computed by code, not the model |

## Run locally
```bash
pip install -r requirements.txt
cp .env.example .env        # add GROQ_API_KEY and TAVILY_API_KEY, then export them
python diagnoser.py         # trace of the loop: read the gate line
fastmcp dev server.py       # MCP Inspector: both tools should be listed
python server.py            # http://localhost:8000/mcp
```

## Deploy on FastMCP Cloud
1. Push this folder to GitHub (the `.gitignore` keeps `.env` out).
2. On fastmcp.cloud, create a project from the repo.
3. Entrypoint: `server.py:mcp` (use `folder/server.py:mcp` if this lives in a subfolder).
4. Add `GROQ_API_KEY` and `TAVILY_API_KEY` in project settings.
5. Deploy. Your URL is `https://<project>.fastmcp.app/mcp`.

## Connect
- claude.ai: + -> Connectors -> Add custom connector -> paste the `/mcp` URL
- Claude Code: `claude mcp add --transport http workflow-advisor https://<project>.fastmcp.app/mcp`

Try: "Diagnose my morning Jira routine and tell me how many hours automating it
would save at 40 minutes a day, 5 days a week." Expect 173.3 hours.

## Protect your keys
Anyone with the URL can call this and spend your credits. A built-in cap
(`MAX_CALLS_PER_HOUR`, default 20) limits the damage, and you should check
FastMCP Cloud's project access settings, or take the demo down after sharing.
