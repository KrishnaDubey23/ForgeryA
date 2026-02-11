"""Mock Convex client for testing when real backend is unavailable."""

import os
from typing import Any, Dict, Optional
import uuid

class MockConvexClient:
    """Mock Convex client that returns test data without hitting real backend."""
    
    def __init__(self, deployment_url: Optional[str] = None, api_key: Optional[str] = None):
        self.deployment_url = deployment_url or os.getenv("CONVEX_URL", "http://mock")
        self.api_key = api_key or os.getenv("CONVEX_API_KEY")
        print(f"[MOCK CONVEX] Using mock backend (real URL: {self.deployment_url})")
    
    async def query(self, path: str, args: Dict[str, Any]) -> Any:
        """Mock query - returns test data."""
        print(f"[MOCK CONVEX] query({path}, {args})")
        
        if "getUserByEmail" in path:
            email = args.get("email")
            if email == "demo@forgerydetection.ai":
                return {
                    "_id": f"demo_user_{uuid.uuid4().hex[:8]}",
                    "email": email,
                    "passwordHash": "$2b$12$test",
                    "isAdmin": True,
                    "_creationTime": 1234567890,
                }
            return None
        
        if "getUserById" in path:
            return {
                "_id": args.get("userId"),
                "email": f"user@example.com",
                "isAdmin": False,
            }
        
        return {"result": "ok"}
    
    async def mutation(self, path: str, args: Dict[str, Any]) -> Any:
        """Mock mutation - returns test data."""
        print(f"[MOCK CONVEX] mutation({path}, {args})")
        
        if "createUser" in path:
            return {
                "_id": f"user_{uuid.uuid4().hex[:8]}",
                "email": args.get("email"),
                "passwordHash": args.get("passwordHash"),
                "isAdmin": args.get("isAdmin", False),
                "_creationTime": 1234567890,
            }
        
        if "createUpload" in path:
            return {
                "_id": f"upload_{uuid.uuid4().hex[:8]}",
                "userId": args.get("userId"),
                "imagePath": args.get("imagePath"),
                "createdAt": args.get("createdAt"),
                "_creationTime": 1234567890,
            }
        
        if "createPrediction" in path:
            return {
                "_id": f"prediction_{uuid.uuid4().hex[:8]}",
                "uploadId": args.get("uploadId"),
                "densenetScore": args.get("densenetScore"),
                "mobilenetScore": args.get("mobilenetScore"),
                "ensembleScore": args.get("ensembleScore"),
                "severity": args.get("severity"),
                "tamperedRatio": args.get("tamperedRatio"),
                "heatmapPaths": args.get("heatmapPaths", []),
                "createdAt": args.get("createdAt"),
                "_creationTime": 1234567890,
            }
        
        return {"_id": f"result_{uuid.uuid4().hex[:8]}", "success": True}
