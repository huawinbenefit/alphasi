# AlphaSI

A small, standalone open-source example of quantitative strategy decisions.
一个独立的量化策略决策示例，展示趋势信号与风险仓位约束。

## Included

- Completed-close fast/slow moving-average trend filter (long or flat).
- Whole-share sizing constrained by a hypothetical stop-risk budget and maximum allocation.
- Deterministic synthetic data demo; no API keys, dependencies or broker connections.
- Unit tests for trend states, invalid prices and position limits.

## Run

Python 3.10+:

```sh
python3 strategy.py
python3 -m unittest -v
```

`LONG` is a target stance, not an executed order or a crossover event. Existing
positions must be reconciled separately. Input bars must be completed and in
chronological order. A historical simulation must execute after the signal bar
and include slippage, fees, corporate actions and appropriate currency handling.

The position calculation uses price and equity in the same currency. It does
not implement Hong Kong board lots, exchange tick rules, FX conversion, order
execution, portfolio risk aggregation, or stop orders. Stops cannot guarantee
the stated risk budget during gaps. No investment returns are claimed.

这是研究与教学代码，不是生产交易系统或投资建议。本仓库为独立编写的公开示例，
不包含 AlphaSI 网站、管理后台、生产策略、账户资料或其他专有组件。

## License

MIT. See [LICENSE](LICENSE).
