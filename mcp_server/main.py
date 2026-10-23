"""
OmniCare Autonomous – Self-hosted MCP Server
Implements MCP Spec 2025-11-25 over Streamable HTTP.
Primary track: Alexa+
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import json
import uuid
from typing import Any, Dict, List, Optional

from .tools import TOOLS, execute_tool
from .agent_orchestrator import run_agent

app = FastAPI(
    title="OmniCare Autonomous MCP Server",
    description="Self-hosted MCP server for Alexa+ – Amazon Developer Hackathon 2026",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (for demo)
sessions: Dict[str, Dict[str, Any]] = {}


def mcp_response(id: Any, result: Any = None, error: Any = None) -> Dict:
    payload = {"jsonrpc": "2.0", "id": id}
    if error is not None:
        payload["error"] = error
    else:
        payload["result"] = result
    return payload


@app.post("/")
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Streamable HTTP MCP transport endpoint."""
    body = await request.json()
    method = body.get("method")
    req_id = body.get("id")
    params = body.get("params", {})

    # ---- initialize ----
    if method == "initialize":
        session_id = str(uuid.uuid4())
        sessions[session_id] = {"initialized": True}
        return JSONResponse(
            content=mcp_response(
                req_id,
                {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {
                        "tools": {"listChanged": False},
                        "resources": {},
                        "prompts": {},
                    },
                    "serverInfo": {
                        "name": "omnicare-autonomous",
                        "version": "1.0.0",
                    },
                },
            ),
            headers={"Mcp-Session-Id": session_id},
        )

    # ---- tools/list ----
    if method == "tools/list":
        return JSONResponse(
            content=mcp_response(req_id, {"tools": TOOLS})
        )

    # ---- tools/call ----
    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        try:
            result = await execute_tool(tool_name, arguments)
            return JSONResponse(
                content=mcp_response(
                    req_id,
                    {
                        "content": [
                            {"type": "text", "text": json.dumps(result, indent=2)}
                        ],
                        "isError": False,
                    },
                )
            )
        except Exception as e:
            return JSONResponse(
                content=mcp_response(
                    req_id,
                    {
                        "content": [{"type": "text", "text": str(e)}],
                        "isError": True,
                    },
                )
            )

    # ---- notifications/initialized ----
    if method == "notifications/initialized":
        return Response(status_code=204)

    # ---- ping ----
    if method == "ping":
        return JSONResponse(content=mcp_response(req_id, {}))

    return JSONResponse(
        content=mcp_response(
            req_id,
            error={"code": -32601, "message": f"Method not found: {method}"},
        )
    )


@app.get("/health")
async def health():
    return {"status": "ok", "server": "omnicare-autonomous", "protocol": "2025-11-25"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp_server.main:app", host="0.0.0.0", port=8000, reload=True)
