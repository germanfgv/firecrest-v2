import uvicorn

# app
from firecrest import create_app

# plugins
from firecrest.plugins import settings

app = create_app(settings=settings)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
