import sys
sys.path.append('/opt/python')          # this needs to be done since LWA loses the path to the layers


def run():
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello from docked_playwright lambda!!"}


    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    run()                                  # to be triggered from run.sh