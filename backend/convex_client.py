import os
from typing import Any, Dict, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

# Try to use real ConvexClient, fall back to mock if needed
USE_MOCK_CONVEX = os.getenv("USE_MOCK_CONVEX", "false").lower() == "true"


class ConvexClient:
    """
    Minimal Convex HTTP API client for FastAPI backend.

    Uses the Functions HTTP API:
      - POST {CONVEX_URL}/api/query
      - POST {CONVEX_URL}/api/mutation

    Auth:
      - For this app we use public functions, so the Authorization header
        is optional. If CONVEX_API_KEY is set, it will be sent as
        `Authorization: Convex <CONVEX_API_KEY>`.
    """

    def __init__(
        self,
        deployment_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        # Prefer the Convex URL written by `npx convex dev` into env
        self.deployment_url = deployment_url or os.getenv("CONVEX_URL")
        self.api_key = api_key or os.getenv("CONVEX_API_KEY")
        if not self.deployment_url:
            raise RuntimeError("CONVEX_URL is not configured in backend/.env")

        self._client = httpx.AsyncClient(timeout=10.0)

    @property
    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
        }
        # Only send admin key if configured.
        if self.api_key:
            headers["Authorization"] = f"Convex {self.api_key}"
        return headers

    async def query(self, path: str, args: Dict[str, Any]) -> Any:
        url = f"{self.deployment_url.rstrip('/')}/api/query"
        payload = {"path": path, "args": args, "format": "json"}
        resp = await self._client.post(url, headers=self._headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "success":
            # Surface Convex error to FastAPI instead of generic 500
            error_msg = data.get("errorMessage", "Unknown Convex query error")
            raise RuntimeError(f"Convex query error for {path}: {error_msg}")
        return data.get("value")

    async def mutation(self, path: str, args: Dict[str, Any]) -> Any:
        url = f"{self.deployment_url.rstrip('/')}/api/mutation"
        payload = {"path": path, "args": args, "format": "json"}
        resp = await self._client.post(url, headers=self._headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "success":
            error_msg = data.get("errorMessage", "Unknown Convex mutation error")
            raise RuntimeError(f"Convex mutation error for {path}: {error_msg}")
        return data.get("value")


async def get_convex_client() -> ConvexClient:
    """
    FastAPI dependency to lazily construct the Convex client.
    Falls back to mock if real backend is unavailable.
    """
    if USE_MOCK_CONVEX:
        from mock_convex import MockConvexClient
        return MockConvexClient()
    
    try:
        return ConvexClient()
    except Exception as e:
        print(f"[CONVEX] Failed to connect to real backend: {e}")
        print("[CONVEX] Falling back to mock client")
        from mock_convex import MockConvexClient
        return MockConvexClient()


