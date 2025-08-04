"""Run the API server."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "langtools.main.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[
            "/workspace-root/langtools-main",
            "/workspace-root/langtools-ai",
            "/workspace-root/langtools-utils",
        ],
    )
