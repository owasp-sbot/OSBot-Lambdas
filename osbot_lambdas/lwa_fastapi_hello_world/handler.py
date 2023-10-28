import sys
sys.path.append('/opt/python')          # this needs to be done since LWA loses the path to the layers


def run():
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def root():
        print("in root method")
        return {"message": "Hello from lwa_fastapi_hello_world lambda"}

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    run()                                  # to be triggered from run.sh