import numpy as np
import pandas as pd

from finter.backtest.simulator import Simulator


class SimulatorResult:
    def __init__(self, simulator: Simulator) -> None:
        self.simulator = simulator

    @property
    def nav(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.simulator.nav, index=self.simulator.dates, columns=["nav"]
        )

    @property
    def cash(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.simulator.cash, index=self.simulator.dates, columns=["cash"]
        )

    @property
    def valuation(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.simulator.valuation.sum(axis=1),
            index=self.simulator.dates,
            columns=["valuation"],
        )

    @property
    def cost(self) -> pd.DataFrame:
        cost = np.nansum(
            (
                self.simulator.actual_buy_volume
                * self.simulator.buy_price
                * self.simulator.buy_fee_tax
            )
            + (
                self.simulator.actual_sell_volume
                * self.simulator.sell_price
                * self.simulator.sell_fee_tax
            ),
            axis=1,
        )
        return pd.DataFrame(
            cost,
            index=self.simulator.dates,
            columns=["cost"],
        )

    # Additional features
    # - average buy price
    # - realized pnl
    # - unrealized pnl

    @property
    def summary(self) -> pd.DataFrame:

        # Todo: Calculate with realized pnl, unrealized pnl
        pnl = self.nav.diff().fillna(0) - self.cost.values
        pnl.name = "pnl"

        result = pd.concat(
            [self.nav, self.cash, self.valuation, self.cost, pnl], axis=1
        )
        return result
