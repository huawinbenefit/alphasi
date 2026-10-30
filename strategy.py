"""AlphaSI educational, long-only trend decision example. No broker integration."""
from dataclasses import dataclass, asdict
import json
import math


@dataclass(frozen=True)
class Decision:
    signal: str
    reason: str
    fast_average: float
    slow_average: float
    suggested_shares: int


def decide(closes, equity=10000.0, fast=5, slow=20,
           risk_fraction=0.01, stop_fraction=0.05, max_allocation=0.20):
    """Use completed bars only; signal is a target stance, not a trade order.

    Position limit = min(stop-based risk budget, allocation cap). A stop is
    hypothetical: gaps and execution costs can cause losses above the budget.
    """
    if not (isinstance(fast, int) and isinstance(slow, int) and 1 <= fast < slow):
        raise ValueError("Require integer windows 1 <= fast < slow")
    prices = tuple(float(x) for x in closes)
    if len(prices) < slow or any(not math.isfinite(x) or x <= 0 for x in prices):
        raise ValueError("Require enough finite positive completed close prices")
    params = (equity, risk_fraction, stop_fraction, max_allocation)
    if any(not math.isfinite(x) for x in params) or equity <= 0:
        raise ValueError("Require positive finite equity and finite risk parameters")
    if not all(0 < x <= 1 for x in params[1:]):
        raise ValueError("Fractions must be in (0, 1]")
    short = sum(prices[-fast:]) / fast
    long = sum(prices[-slow:]) / slow
    if short <= long:
        return Decision("FLAT", "Fast average is not above slow average", short, long, 0)
    price = prices[-1]
    shares = math.floor(min(equity * risk_fraction / (price * stop_fraction),
                            equity * max_allocation / price))
    return Decision("LONG" if shares else "FLAT", "Trend and position-size limits", short, long, shares)


if __name__ == "__main__":
    # Deterministic synthetic prices; these are not security market data.
    simulated_closes = [100 + i * 0.5 for i in range(40)]
    print(json.dumps(asdict(decide(simulated_closes)), indent=2))
