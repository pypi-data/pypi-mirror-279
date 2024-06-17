import numpy as np
import pandas as pd
from numba import njit

from finter.backtest.results import SimulatorResult

# Todo
# - volcap
# - buy & hold frequency


class Simulator:
    def __init__(
        self,
        position: pd.DataFrame,
        price: pd.DataFrame,
        initial_cash: np.float64,
        buy_fee_tax: np.float64,
        sell_fee_tax: np.float64,
        slippage: np.float64,
    ) -> None:

        self.weight, self.price, self.dates, self.common_columns = self.preprocess_data(
            position, price
        )
        self.initial_cash = initial_cash

        # Todo: matrix fee
        self.buy_fee_tax = buy_fee_tax / 10000
        self.sell_fee_tax = sell_fee_tax / 10000

        # Todo: matrix slipage
        self.slippage = slippage / 10000

        # Todo: user set buy price, sell price
        self.buy_price = self.price * (1 + self.slippage)
        self.sell_price = self.price * (1 - self.slippage)

        self.num_assets = self.weight.shape[1]
        self.num_days = self.weight.shape[0]

        self.initialize_variables()

        self._results = SimulatorResult(self)

    def preprocess_data(self, position: pd.DataFrame, price: pd.DataFrame) -> tuple:
        weight = position / 1e8

        common_columns = weight.columns.intersection(price.columns)

        weight = weight[common_columns]
        price = price[common_columns]

        first_position_index = weight.index[0]
        price_index_pos = price.index.get_loc(first_position_index)

        if price_index_pos == 0:
            price_index_pos = 1

        price = price.iloc[price_index_pos - 1 : price_index_pos + len(weight)]
        weight = weight.reindex(price.index)

        return weight.to_numpy(), price.to_numpy(), weight.index, common_columns

    def initialize_variables(self) -> None:
        shape = (self.num_days, self.num_assets)

        self.actual_holding_volume = np.full(shape, np.nan, dtype=np.float64)
        self.target_volume = np.full(shape, np.nan, dtype=np.float64)
        self.target_buy_volume = np.full(shape, np.nan, dtype=np.float64)
        self.target_sell_volume = np.full(shape, np.nan, dtype=np.float64)
        self.actual_sell_volume = np.full(shape, np.nan, dtype=np.float64)
        self.actual_sell_amount = np.full(shape, np.nan, dtype=np.float64)
        self.available_buy_amount = np.full(
            (self.num_days, 1), np.nan, dtype=np.float64
        )
        self.target_buy_amount = np.full(shape, np.nan, dtype=np.float64)
        self.target_buy_amount_sum = np.full(
            (self.num_days, 1), np.nan, dtype=np.float64
        )
        self.available_buy_volume = np.full(shape, np.nan, dtype=np.float64)
        self.actual_buy_volume = np.full(shape, np.nan, dtype=np.float64)
        self.actual_buy_amount = np.full(shape, np.nan, dtype=np.float64)
        self.valuation = np.full(shape, np.nan, dtype=np.float64)
        self.cash = np.full((self.num_days, 1), np.nan, dtype=np.float64)
        self.nav = np.full((self.num_days, 1), np.nan, dtype=np.float64)

        self.actual_holding_volume[0] = 0
        self.cash[0] = self.initial_cash
        self.nav[0] = self.initial_cash

    def backtest(self):
        for i in range(1, self.num_days):
            # Todo: use base price
            self.target_volume[i] = update_target_volume(
                self.weight[i], self.nav[i - 1, 0], self.price[i - 1]
            )

            (
                self.target_buy_volume[i],
                self.target_sell_volume[i],
                self.actual_sell_volume[i],
            ) = calculate_buy_sell_volumes(
                self.target_volume[i], self.actual_holding_volume[i - 1]
            )

            (
                self.actual_sell_amount[i],
                self.available_buy_amount[i, 0],
                self.actual_buy_volume[i],
                self.actual_buy_amount[i],
            ) = execute_transactions(
                self.actual_sell_volume[i],
                self.buy_price[i],
                self.buy_fee_tax,
                self.sell_price[i],
                self.sell_fee_tax,
                self.cash[i - 1, 0],
                self.target_buy_volume[i],
            )

            self.actual_holding_volume[i], self.valuation[i], self.cash[i, 0] = (
                update_valuation_and_cash(
                    self.actual_holding_volume[i - 1],
                    self.actual_buy_volume[i],
                    self.actual_sell_volume[i],
                    self.price[i],
                    self.available_buy_amount[i, 0],
                    self.actual_buy_amount[i],
                )
            )
            self.nav[i, 0] = update_nav(self.cash[i, 0], self.valuation[i])

    @property
    def result(self):
        return self._results

    @property
    def summary(self):
        return self._results.summary


@njit
def update_target_volume(
    weight: np.ndarray, prev_nav: np.float64, prev_price: np.ndarray
) -> np.ndarray:
    return np.nan_to_num(weight * prev_nav / prev_price)


@njit
def calculate_buy_sell_volumes(
    target_volume: np.ndarray, actual_holding_volume: np.ndarray
) -> tuple:
    target_buy_volume = np.maximum(target_volume - actual_holding_volume, 0)
    target_sell_volume = np.maximum(actual_holding_volume - target_volume, 0)
    actual_sell_volume = target_sell_volume
    return target_buy_volume, target_sell_volume, actual_sell_volume


@njit
def execute_transactions(
    actual_sell_volume: np.ndarray,
    buy_price: np.ndarray,
    buy_fee_tax: np.float64,
    sell_price: np.ndarray,
    sell_fee_tax: np.float64,
    prev_cash: np.float64,
    target_buy_volume: np.ndarray,
) -> tuple:
    actual_sell_amount = np.nan_to_num(
        actual_sell_volume * sell_price * (1 - sell_fee_tax)
    )
    available_buy_amount = prev_cash + actual_sell_amount.sum()
    target_buy_amount = np.nan_to_num(target_buy_volume * buy_price * (1 + buy_fee_tax))
    target_buy_amount_sum = target_buy_amount.sum()
    if target_buy_amount_sum > 0:
        available_buy_volume = np.nan_to_num(
            (target_buy_amount / target_buy_amount_sum)
            * (available_buy_amount / (buy_price * (1 + buy_fee_tax)))
        )
        actual_buy_volume = np.minimum(available_buy_volume, target_buy_volume)
        actual_buy_amount = np.nan_to_num(
            actual_buy_volume * buy_price * (1 + buy_fee_tax)
        )
    else:
        actual_buy_volume = np.zeros_like(target_buy_volume)
        actual_buy_amount = np.zeros_like(target_buy_volume)
    return (
        actual_sell_amount,
        available_buy_amount,
        actual_buy_volume,
        actual_buy_amount,
    )


@njit
def update_valuation_and_cash(
    prev_actual_holding_volume: np.ndarray,
    actual_buy_volume: np.ndarray,
    actual_sell_volume: np.ndarray,
    price: np.ndarray,
    available_buy_amount: np.float64,
    actual_buy_amount: np.ndarray,
) -> tuple:
    actual_holding_volume = (
        prev_actual_holding_volume + actual_buy_volume - actual_sell_volume
    )
    valuation = np.nan_to_num(actual_holding_volume * price)
    cash = available_buy_amount - actual_buy_amount.sum()
    return actual_holding_volume, valuation, cash


@njit
def update_nav(cash: np.float64, valuation: np.ndarray) -> np.float64:
    return cash + valuation.sum()


if __name__ == "__main__":

    from finter.data import ContentFactory, ModelData

    cf = ContentFactory("kr_stock", 20000101, 20230101)
    price = cf.get_df("price_close")
    position = ModelData.load("portfolio.krx.krx.stock.ldh0127.bb_3")
    price = price.reindex(position.index)

    self = Simulator(
        position, price, initial_cash=1e6, buy_fee_tax=0, sell_fee_tax=0, slippage=0
    )
    self.backtest()
    result = pd.DataFrame(
        {
            "nav": self.nav.flatten(),
            "cash": self.cash.flatten(),
            "valuation": self.valuation.sum(axis=1),
        },
        index=self.dates,
    )
