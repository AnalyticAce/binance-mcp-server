import os
import math
import time

from binance_mcp_server.utils import (
    WeightedRateLimiter,
    rate_limited,
    estimate_weight_for_depth,
)


def test_weighted_rate_limiter_basic():
    rl = WeightedRateLimiter(capacity=10, refill_per_minute=60)  # 1 token/sec
    assert rl.try_consume(5) is True
    assert rl.try_consume(6) is False  # only 5 left
    time.sleep(1.1)
    assert rl.try_consume(1) is True


def test_rate_limited_decorator_cost():
    rl = WeightedRateLimiter(capacity=3, refill_per_minute=60)

    calls = {"count": 0}

    @rate_limited(rl, cost=2)
    def f():
        calls["count"] += 1
        return {"ok": True}

    r1 = f()
    r2 = f()  # should fail due to insufficient tokens (3 capacity, first consumed 2, second wants 2)
    assert r1.get("ok") is True
    assert r2.get("success") is False
    assert r2.get("error", {}).get("type") == "rate_limit_exceeded"


def test_estimate_weight_for_depth():
    assert estimate_weight_for_depth(None) in (2, 5, 10, 20, 50, 5)
    assert estimate_weight_for_depth(5) == 2
    assert estimate_weight_for_depth(100) == 5
    assert estimate_weight_for_depth(500) == 10
    assert estimate_weight_for_depth(1000) == 20
    assert estimate_weight_for_depth(5000) == 50

