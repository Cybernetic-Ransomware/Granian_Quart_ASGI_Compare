import asyncio
import math
import time
from pathlib import Path

import httpx
import pytest
from decouple import AutoConfig

ROOT_DIR = Path(__file__).resolve().parent.parent
config = AutoConfig(search_path=str(ROOT_DIR))

BASE_URL = config("LOADTEST_BASE_URL", default="http://localhost:8080")
TOTAL_REQUESTS = config("LOADTEST_REQUESTS", cast=int, default=10000)
CONCURRENCY = config("LOADTEST_CONCURRENCY", cast=int, default=200)
RUN_LOAD_TESTS = config("RUN_LOAD_TESTS", cast=bool, default=False)

pytestmark = pytest.mark.skipif(
    not RUN_LOAD_TESTS,
    reason="Set RUN_LOAD_TESTS=1 in .env (or env var) to enable the 10k request load test.",
)

async def _run_load(client: httpx.AsyncClient, url: str):
    semaphore = asyncio.Semaphore(CONCURRENCY)
    durations: list[float] = []

    async def hit():
        async with semaphore:
            start = time.perf_counter()
            resp = await client.get(url)
            resp.raise_for_status()
            await resp.aread()
            durations.append(time.perf_counter() - start)

    started = time.perf_counter()
    await asyncio.gather(*(hit() for _ in range(TOTAL_REQUESTS)))
    return durations, time.perf_counter() - started


def _percentile(values: list[float], percentile: float) -> float:
    idx = max(0, min(len(values) - 1, math.ceil(percentile * len(values)) - 1))
    return values[idx]


def _summaries_to_text(results: dict[str, dict[str, float]]) -> str:
    lines = [
        "Load test results (requests: "
        f"{TOTAL_REQUESTS}, concurrency: {CONCURRENCY}, target: {BASE_URL})"
    ]
    for name, stats in results.items():
        lines.append(
            f"- {name}: avg={stats['avg']:.4f}s p95={stats['p95']:.4f}s "
            f"max={stats['max']:.4f}s rps={stats['rps']:.1f}"
        )
    return "\n".join(lines)


@pytest.mark.asyncio
async def test_load_comparison():
    endpoints = {
        "granian": f"{BASE_URL}/granian",
        "hypercorn": f"{BASE_URL}/hypercorn",
    }
    results: dict[str, dict[str, float]] = {}

    async with httpx.AsyncClient(timeout=None) as client:
        for name, url in endpoints.items():
            durations, total_time = await _run_load(client, url)
            assert len(durations) == TOTAL_REQUESTS
            sorted_durations = sorted(durations)
            results[name] = {
                "avg": sum(sorted_durations) / TOTAL_REQUESTS,
                "p95": _percentile(sorted_durations, 0.95),
                "max": sorted_durations[-1],
                "rps": TOTAL_REQUESTS / total_time,
            }

    print(_summaries_to_text(results))
