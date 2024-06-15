# backtest.py

from typing import Sequence
import datetime as dt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from market_break.labels import (
    ENTRY, EXIT, LONG, SHORT, TYPE, RETURNS
)

__all__ = [
    "Report",
    "Trades",
    "Plot"
]

class Trades:

    EMPTY = -1

    @staticmethod
    def adjust(trades: pd.DataFrame) -> pd.DataFrame:

        trades = trades[trades[EXIT] != Trades.EMPTY]
        trades = trades[trades[ENTRY] != Trades.EMPTY]

        return trades

    @staticmethod
    def generate(
            up: Sequence[bool] | bool,
            down: Sequence[bool] | bool,
            adjust: bool = False
    ) -> pd.DataFrame:

        if len(up) != len(down):
            raise ValueError(
                'up and down must have the same length, '
                f'but {len(up)} and {len(down)} where given.'
            )

        long = []
        short = []
        data = []

        for i in range(len(up)):
            long_signal = up[i]
            short_signal = down[i]

            if len(long) == len(short) == 0:
                if long_signal:
                    long.append(i)
                    data.append((short[-1] if short else Trades.EMPTY, long[-1], SHORT))

                elif short_signal:
                    short.append(i)
                    data.append((long[-1] if long else Trades.EMPTY, short[-1], LONG))

            elif len(long) == len(short):
                if (long[0] < short[0]) and long_signal:
                    long.append(i)
                    data.append((short[-1] if short else Trades.EMPTY, long[-1], SHORT))

                elif (long[0] > short[0]) and short_signal:
                    short.append(i)
                    data.append((long[-1] if long else Trades.EMPTY, short[-1], LONG))

            elif (len(long) > 0) and (len(short) > 0):
                if (long[-1] < short[-1]) and long_signal:
                    long.append(i)
                    data.append((short[-1] if short else Trades.EMPTY, long[-1], SHORT))

                elif (long[-1] > short[-1]) and short_signal:
                    short.append(i)
                    data.append((long[-1] if long else Trades.EMPTY, short[-1], LONG))

            else:
                if (len(long) < len(short)) and long_signal:
                    long.append(i)
                    data.append((short[-1] if short else Trades.EMPTY, long[-1], SHORT))

                elif (len(long) > len(short)) and short_signal:
                    short.append(i)
                    data.append((long[-1] if long else Trades.EMPTY, short[-1], LONG))

        if Trades.EMPTY not in data[-1]:
            if data[-1][2] == SHORT:
                data.append((data[-1][1], Trades.EMPTY, LONG))

            elif data[-1][2] == LONG:
                data.append((data[-1][1], Trades.EMPTY, SHORT))

        data = np.array(data)

        trades = pd.DataFrame(
            {
                ENTRY: data[:, 0].astype(int),
                EXIT: data[:, 1].astype(int),
                TYPE: data[:, 2].astype(str)
            }
        )

        if adjust:
            trades = Trades.adjust(trades)

        return trades

    @staticmethod
    def returns(
            trades: pd.DataFrame,
            bid: pd.Series,
            ask: pd.Series,
            fee: float = 0.0
    ) -> pd.Series:

        if len(bid) != len(ask):
            raise ValueError(
                'bid and ask must have the same length, '
                f'but {len(bid)} and {len(ask)} where given.'
            )

        trades = Trades.adjust(trades)
        flip_short = trades[TYPE] == SHORT

        returns = bid.iloc[trades[EXIT]].values / ask.iloc[trades[ENTRY]].values
        returns[flip_short] = 1 / returns[flip_short]

        return pd.Series((returns - 1) * (1 - fee), index=trades[EXIT], name=RETURNS)

type Index = int | float | pd.Timestamp | dt.datetime | dt.date

class Report:

    @staticmethod
    def generate[I: Index](
            index: Sequence[I],
            returns: Sequence[float],
            long: Sequence[int],
            short: Sequence[int],
            balance: Sequence[float] = None
    ) -> dict[str, dict[str, float | I]]:

        if not isinstance(index, pd.Series):
            index = pd.Series(index)

        if not isinstance(returns, np.ndarray):
            returns = np.array(returns)

        if balance is None:
            balance = np.cumsum(returns)

        if not isinstance(balance, np.ndarray):
            balance = np.array(balance)

        tick_time = (index.iloc[1:] - index.values[:-1])
        mean_tick_time = tick_time.mean()
        min_tick_time = tick_time.min()
        max_tick_time = tick_time.max()
        tuw = (index.iloc[short] - index.iloc[long].values)
        mean_tuw = tuw.mean()
        max_tuw = tuw.max()
        min_tuw = tuw.min()

        gains = returns[returns > 0]
        losses = returns[returns < 0]

        return {
            'index': {
                'start': index.iloc[0],
                'end': index.iloc[-1],
                'total duration': index.iloc[-1] - index.iloc[0],
                'min. tick duration': (
                    min_tick_time.to_pytimedelta()
                    if isinstance(min_tick_time, pd.Timedelta) else
                    min_tick_time
                ),
                'max. tick duration': (
                    max_tick_time.to_pytimedelta()
                    if isinstance(max_tick_time, pd.Timedelta) else
                    max_tick_time
                ),
                'avg. tick duration': (
                    mean_tick_time.to_pytimedelta()
                    if isinstance(mean_tick_time, pd.Timedelta) else
                    mean_tick_time
                ),
                'ticks': len(index)
            },
            'trades': {
                'long trades': len(long),
                'short trades': len(short),
                'min. TUW': (
                    min_tuw.to_pytimedelta()
                    if isinstance(min_tuw, pd.Timedelta) else
                    min_tuw
                ),
                'max. TUW': (
                    max_tuw.to_pytimedelta()
                    if isinstance(max_tuw, pd.Timedelta) else
                    max_tuw
                ),
                'avg. TUW': (
                    mean_tuw.to_pytimedelta()
                    if isinstance(mean_tuw, pd.Timedelta) else
                    mean_tuw
                )
            },
            'gains': {
                '[%] min. gain': gains.min() * 100,
                '[%] max. gain': gains.max() * 100,
                '[%] avg. gain': gains.mean() * 100,
                '[%] total gains': gains.sum() * 100,
                'winning trades': len(gains)
            },
            'losses': {
                '[%] min. loss': losses.max() * 100,
                '[%] max. loss': losses.min() * 100,
                '[%] avg. loss': losses.mean() * 100,
                '[%] total losses': losses.sum() * 100,
                'losing trades': len(losses)
            },
            'performance': {
                'PnL factor': (gains.sum() / -losses.sum()),
                'avg. profit factor': (1 + returns.mean()),
                '[%] win rate': (len(gains) / len(returns)) * 100,
                '[%] total profit': balance[-1] * 100
            }
        }

    @staticmethod
    def repr[I: Index](
            data: dict[str, dict[str, float | I]],
            padding: int = 23,
            precision: int = 4
    ) -> str:

        output = []

        for title, values in data.items():
            output.append(f"{'\n' if output else ''}[{title.title()}]")

            for key, value in values.items():
                if isinstance(value, (int, float, np.number)):
                    value = round(value, precision)

                elif isinstance(value, (dt.datetime, dt.timedelta, pd.Timedelta, pd.Timestamp)):
                    value = str(value)[:-4]

                output.append(f"{key:<{padding}}{value:>{padding}}")

        return "\n".join(output)

class Plot:

    plt.style.use('fivethirtyeight')

    @staticmethod
    def style(style: str) -> None:

        plt.style.use(style)

    @staticmethod
    def returns_histogram(returns: pd.Series, bins: int = 50) -> None:

        returns_pct = returns * 100

        gains_pct = returns_pct[returns_pct > 0]
        losses_pct = returns_pct[returns_pct < 0]

        returns_pct_average = returns_pct.mean()
        gains_pct_average = gains_pct.mean()
        losses_pct_average = losses_pct.mean()

        y, x = np.histogram(returns_pct, bins=bins)
        y = np.concatenate([y, np.array([0])])
        curve = np.poly1d(np.polyfit(x, y, 7))(x)

        plt.figure(figsize=(14, 4))
        plt.title('Transaction Returns Histogram')
        plt.xlabel('Returns (%)')
        plt.ylabel('Count')
        plt.axvline(0, color='blue', label='zero', lw=1.5, linestyle='dashed')
        plt.axvline(
            returns_pct_average, color='orange',
            label=f'mean return {returns_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axvline(
            gains_pct_average, color='green',
            label=f'mean gain {gains_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axvline(
            losses_pct_average, color='red',
            label=f'mean loss {losses_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.hist(returns_pct, bins=bins, alpha=0.85, label=f'returns ({bins} bins)')
        plt.plot(x, curve, alpha=1, lw=2.5, c="cyan")
        plt.legend()
        plt.show()

    @staticmethod
    def returns_signals(returns: pd.Series, index: np.ndarray | pd.Series = None) -> None:

        returns_pct = returns * 100

        if index is None:
            index = returns.index

        else:
            index = index[returns.index]

        gains_pct = returns_pct[returns_pct > 0]
        losses_pct = returns_pct[returns_pct < 0]

        returns_pct_average = returns_pct.mean()
        gains_pct_average = gains_pct.mean()
        losses_pct_average = losses_pct.mean()

        x = np.array(list(range(len(returns_pct))))
        curve = np.poly1d(np.polyfit(x, returns_pct, 7))(x)

        plt.figure(figsize=(14, 4))
        plt.title('Transaction Returns')
        plt.xlabel('Date-Time')
        plt.ylabel('Returns (%)')
        plt.scatter(
            index[gains_pct.index], gains_pct,
            c='green', s=15, alpha=0.875
        )
        plt.scatter(
            index[losses_pct.index], losses_pct,
            c='red', s=15, alpha=0.875
        )
        plt.plot(
            index, returns_pct,
            lw=1.5, label='returns', alpha=0.85
        )
        plt.axhline(
            returns_pct_average, color='orange',
            label=f'mean {returns_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axhline(
            gains_pct_average, color='green',
            label=f'mean gain {gains_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axhline(
            losses_pct_average, color='red',
            label=f'mean loss {losses_pct_average:.5f}%', lw=1.5, linestyle='dashed'
        )
        plt.axhline(0, color='blue', label=f'zero', lw=1.5, linestyle='dashed')
        plt.plot(index, curve, alpha=1, lw=2.5, c="cyan")
        plt.legend()
        plt.show()

    @staticmethod
    def returns_pie(returns: pd.Series) -> None:

        # noinspection PyUnresolvedReferences
        returns_counts = (returns > 0).value_counts()
        returns_sizes = pd.Series(
            [returns[returns > 0].sum(), -1 * returns[returns < 0].sum()]
        ) * 100

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        fig.suptitle('Transaction Returns')
        ax1.pie(returns_counts, explode=[0, 0.06], startangle=90, autopct='%1.2f%%')
        ax1.legend(labels=[f'Wins {returns_counts[True]}', f'Losses {returns_counts[False]}'])
        ax2.pie(returns_sizes, explode=[0, 0.1], startangle=90, autopct='%1.2f%%')
        ax2.legend(labels=[f'Gains {returns_sizes[0]:.3f}%', f'Losses {returns_sizes[1]:.3f}%'])
        plt.show()

    @staticmethod
    def returns_balance(returns: pd.Series, index: np.ndarray | pd.Series = None) -> None:

        returns_pct = returns * 100

        if index is None:
            index = returns.index

        else:
            index = index[returns.index]

        gains_pct = returns_pct[returns_pct > 0]
        losses_pct = returns_pct[returns_pct < 0]

        balance_pct = returns_pct.cumsum()
        total_gains_pct = gains_pct.cumsum()
        total_losses_pct = losses_pct.cumsum()

        plt.figure(figsize=(14, 4))
        plt.title('Transaction Balance')
        plt.xlabel('Date-Time')
        plt.ylabel('Returns (%)')
        plt.plot(
            index[balance_pct.index], balance_pct,
            lw=4, label=f'cumulative returns {balance_pct.iloc[-1]:.3f}%'
        )
        plt.plot(
            index[total_gains_pct.index], total_gains_pct,
            lw=2, c='green', linestyle='dashed',
            label=f'cumulative gains {total_gains_pct.iloc[-1]:.3f}5'
        )
        plt.plot(
            index[total_losses_pct.index], -total_losses_pct,
            lw=2, c='red', linestyle='dashed',
            label=f'cumulative losses {-total_losses_pct.iloc[-1]:.3f}%'
        )
        plt.legend()
        plt.show()

    @staticmethod
    def price_signals(
            bid: pd.Series,
            ask: pd.Series,
            long: Sequence[int] = None,
            short: Sequence[int] = None,
            index: np.ndarray | pd.Series = None
    ) -> None:

        if len(bid) != len(ask):
            raise ValueError(
                'bid and ask must have the same length, '
                f'but {len(bid)} and {len(ask)} where given.'
            )

        if index is None:
            index = bid.index

        else:
            index = index[bid.index]

        mid = ask / 2 + bid / 2

        plt.figure(figsize=(14, 4))
        plt.title('Strategy Actions')
        plt.xlabel('Date-Time')
        plt.ylabel('Price')

        if (long is not None) and (short is not None):
            new_long = long[long != short]
            new_short = short[short != long]

            long = new_long
            short = new_short

        if long is not None:
            plt.scatter(
                index[long], bid[long],
                marker='^', color='green', s=35, label='long'
            )

        if short is not None:
            plt.scatter(
                index[short], ask[short],
                marker='v', color='red', s=35, label='short'
            )

        plt.plot(
            index[bid.index], bid,
            lw=1, label=f'bid {bid.iloc[-1]}', alpha=0.875
        )
        plt.plot(
            index[ask.index], ask,
            lw=1, label=f'ask {ask.iloc[-1]}', alpha=0.875
        )
        plt.plot(
            index[ask.index], mid,
            lw=0.75, label=f'mid {round(mid.iloc[-1], 5)}', alpha=0.75
        )

        plt.legend()
        plt.show()
