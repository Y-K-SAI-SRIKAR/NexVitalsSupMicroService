import uvicorn
import os

if __name__ == "__main__":
    uvicorn.run(
        "NVChatBot.api:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 7766)),
        reload=True
    )