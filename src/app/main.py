import asyncio
import time

from dataclasses import dataclass

from quart import Quart
from quart_schema import QuartSchema, validate_response

app = Quart(__name__)

QuartSchema(app)

@dataclass
class PerformanceResponse:
    message: str
    response_time: float


@app.route("/hello", methods=["GET"])
async def hello() -> PerformanceResponse:
    start = time.time()
    await asyncio.sleep(0.05)
    duration = time.time() - start

    response = PerformanceResponse(
        message="Hello!",
        response_time=duration
    )

    return response


if __name__ == "__main__":
    app.run()
