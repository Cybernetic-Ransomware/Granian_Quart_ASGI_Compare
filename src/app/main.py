import asyncio
import time

from quart import Quart


app = Quart(__name__)

@app.route("/hello")
async def hello():
    start = time.time()
    await asyncio.sleep(0.05)
    return {"message": "Hello!", "response_time": time.time() - start}


if __name__ == "__main__":
    app.run()
