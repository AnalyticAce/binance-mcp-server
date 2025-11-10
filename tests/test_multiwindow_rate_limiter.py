import time

from binance_mcp_server.utils import MultiWindowRateLimiter


def test_multiwindow_rate_limiter_basic():
    # 6 per minute (~0.1 per sec), 2 per sec
    rl = MultiWindowRateLimiter(per_minute=6, per_second=2)

    # First second: allow up to 2 weight
    assert rl.try_consume(1) is True
    assert rl.try_consume(1) is True
    assert rl.try_consume(1) is False  # second bucket exhausted

    time.sleep(1.05)  # next second
    # minute budget remaining: 6 - 2 = 4
    assert rl.try_consume(2) is True
    assert rl.try_consume(3) is False  # minute budget would exceed (only 2 left)
