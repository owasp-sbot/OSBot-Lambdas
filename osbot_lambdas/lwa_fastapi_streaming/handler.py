import sys
sys.path.append('/opt/python')          # this needs to be done since LWA loses the path to the layers


def run():
    from osbot_utils.utils.Misc import str_to_bytes
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse


    app = FastAPI()

    async def streamer():
        for i in range(10):
            #import asyncio
            #await asyncio.sleep(0.1)                       # for the tests there is no need to wait
            yield str_to_bytes(f"[#{i}] This is streaming from Lambda \n")

    @app.get("/")
    async def index():
        return StreamingResponse(streamer(), media_type="text/plain; charset=utf-8")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == '__main__':
    run()                                  # to be triggered from run.sh