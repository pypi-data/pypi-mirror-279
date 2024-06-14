import os
import pandas as pd
import numpy as np
import quantstats as qs
import vectorbt as vbt
from typing import Any, Dict, List, Optional, Type
from .plots import Plotter

vbt.settings.plotting['layout']['template'] = 'vbt_dark'


class BackTest:
    """
    Backtest Agent. This class is used to backtest the model.
    """

    def __init__(self,
                 env: Type,
                 agent: Type,
                 verbose: int = 1,
                 verbose_step: int = 1000,
                 benchmark_coin_name: str = 'BTC-USDT-PERP',
                 report_folder: str = './backtest_reports/'):
        """
        Initialize the BackTest class.

        Args:
            env (Type): The environment to use.
            agent (Type): The agent to use.
            verbose (int, optional): Verbosity level. Defaults to 1.
            verbose_step (int, optional): Verbosity step. Defaults to 1000.
            benchmark_coin_name (str, optional): Benchmark coin name. Defaults to 'BTC-USDT-PERP'.
            report_folder (str, optional): Folder to save reports. Defaults to './backtest_reports/'.
        """
        self.verbose = verbose
        self.verbose_step = verbose_step
        self.benchmark_coin_name = benchmark_coin_name
        self.env = env
        self.agent = agent
        self.pf = None

        self.report_folder = report_folder
        self.plotter = Plotter(report_folder=report_folder)

    def print_metrics(self, metrics: Dict[str, Any]) -> None:
        """Print backtest metrics."""
        print(
            f'> Model Agent Total Profit: {metrics["profit_$"]:<6}$'
            f' | Cumulative Return: {metrics["return_%"]:<4}%'
            f' | Sharpe: {metrics["sharpe"]:<5.2f}'
            f' | Sortino: {metrics["sortino"]:<5.2f}'
            f' | Max Drawdown: {metrics["max_drawdown"]}%'
            f' | Total Commission: {metrics["commission_$"]}$'
        )
        print('_' * 120)

    def render(self, deterministic: bool = True) -> None:
        """Render the environment."""
        obs = self.env.reset()
        i = 0
        while not self.env.done:
            action, _states = self.agent.predict(obs, deterministic=deterministic)
            obs, rewards, done, info = self.env.step(action)
            i += 1
            if self.verbose > 1 and i % self.verbose_step == 0:
                self.env.render()
        if self.verbose > 0:
            metrics = self.get_metrics()
            self.print_metrics(metrics)

    def get_balance_df(self) -> pd.DataFrame:
        """Get the balance DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the balance history.
        """
        if len(self.env.balance_memory) <= 1:
            raise ValueError('You must  .render() the backtest first!')
        return self.env.save_balance_memory().set_index('date')

    def get_benchmark_df(self) -> pd.DataFrame:
        """Get the benchmark DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the benchmark data.
        """
        strategy = self.get_balance_df()
        bench = self.env.data.pivot_table(index='date', columns='symbol', values='close')
        bench['Strategy'] = strategy['account_value']
        bench.dropna(inplace=True)
        return bench

    def get_profit_benchmark_df(self) -> pd.DataFrame:
        """Get the profit benchmark DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the profit benchmark data.
        """
        bench = self.get_benchmark_df()
        profit_benchmark = (bench.divide(bench.iloc[0]) * self.env.initial_balance) - self.env.initial_balance
        return profit_benchmark

    def get_portfolio_weights_memory(self) -> List[Dict[str, Any]]:
        """Get the portfolio weights memory.

        Returns:
            list: List of portfolio weights.
        """
        if len(self.env.portfolio_weights_memory) <= 1:
            raise ValueError('You must  .render() the backtest first!')
        return self.env.portfolio_weights_memory

    def get_action_memory_df(self, action_list: Optional[List[Dict[str, Any]]] = None) -> pd.DataFrame:
        """Get the action memory DataFrame.

        Args:
            action_list (list, optional): List of actions to use. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame containing the action memory.
        """
        if len(self.env.actions_memory) <= 1:
            raise ValueError('You must  .render() the backtest first!')
        return self.env.save_action_memory(action_list=action_list)
    
    def get_portfolio_weights_memory_df(self,) -> pd.DataFrame:
        """Get the portfolio_weights memory DataFrame.

        Args:
            action_list (list, optional): List of memoty to use. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame containing the action memory.
        """
        if len(self.env.actions_memory) <= 1:
            raise ValueError('You must  .render() the backtest first!')
        return self.env.save_action_memory(action_list=self.env.portfolio_weights_memory)

    def get_metrics(self, mode: str = 'base') -> Dict[str, Any]:
        """Get the metrics of the backtest.

        Args:
            mode (str, optional): Mode for calculating metrics. Defaults to 'base'.

        Returns:
            dict: Dictionary containing the metrics.
        """
        bench = self.get_benchmark_df()
        metrics = {
            'start_date': bench.index[0].strftime('%Y-%m-%d %H:%M'),
            'end_date': bench.index[-1].strftime('%Y-%m-%d %H:%M'),
            'trade_days': (bench.index[-1] - bench.index[0]).days,
            'trades': self.env.trades,
            'initial_balance_$': np.round(self.env.initial_balance, 2),
            'final_balance_$': np.round(self.env.balance, 2),
            'profit_$': np.round(self.env.balance - self.env.initial_balance, 2),
            'commission_$': np.round(np.sum(self.env.total_commission_memory), 2),
            'return_%': np.round((self.env.balance - self.env.initial_balance) / self.env.initial_balance * 100, 2),
            'max_drawdown': 0,
            'sharpe': 0,
            'sortino': 0,
            'calmar': 0,
            'profit_factor': 0,
            'value_at_risk': 0,
        }
        if metrics['trades'] != 0:
            metrics['max_drawdown'] = np.round(qs.stats.max_drawdown(bench['Strategy']) * 100, 2)
            metrics['sharpe'] = np.round(qs.stats.sharpe(bench['Strategy']), 3)
            metrics['sortino'] = np.round(qs.stats.sortino(bench['Strategy']), 3)
            metrics['calmar'] = np.round(qs.stats.calmar(bench['Strategy']), 3)
            metrics['profit_factor'] = np.round(qs.stats.profit_factor(bench['Strategy']), 2)
            metrics['value_at_risk'] = np.round(qs.stats.value_at_risk(bench['Strategy']), 2)
            if mode == 'full':
                metrics['tail_ratio'] = np.round(qs.stats.tail_ratio(bench['Strategy']), 2)
                metrics['common_sense_ratio'] = np.round(qs.stats.common_sense_ratio(bench['Strategy']), 2)
                metrics['conditional_value_at_risk'] = np.round(qs.stats.conditional_value_at_risk(bench['Strategy']), 2)
                metrics['information_ratio'] = np.round(qs.stats.information_ratio(bench['Strategy'], bench[self.benchmark_coin_name]), 2)
                metrics['gain_to_pain_ratio'] = np.round(qs.stats.gain_to_pain_ratio(bench['Strategy']), 2)
                metrics['ulcer_index'] = np.round(qs.stats.ulcer_index(bench['Strategy']), 2)
        return metrics

    def check_total_trades(self) -> bool:
        """Check if there are any trades made.

        Returns:
            bool: True if there are trades, False otherwise.
        """
        metrics = self.get_metrics()
        if metrics['trades'] == 0:
            print('!!! No trades were made! Nothing to plot')
            return False
        return True

    def plot_qs_report(self, bench_symbol: str = 'BTC-USDT-PERP', mode: str = 'full') -> None:
        """Plot the quantstats report.

        Args:
            bench_symbol (str, optional): Benchmark symbol. Defaults to 'BTC-USDT-PERP'.
            mode (str, optional): Mode for the report. Defaults to 'full'.
        """
        if self.check_total_trades():
            bench = self.get_benchmark_df()
            qs.reports.plots(bench['Strategy'], benchmark=bench[bench_symbol], periods_per_year=365, mode=mode)

    def save_qs_report(self, bench_symbol: str = 'BTC-USDT-PERP', mode: str = 'full', filename: str = 'quantstats-report.html') -> None:
        """Save the quantstats report.

        Args:
            bench_symbol (str, optional): Benchmark symbol. Defaults to 'BTC-USDT-PERP'.
            mode (str, optional): Mode for the report. Defaults to 'full'.
            filename (str, optional): Filename for the report. Defaults to 'quantstats-report.html'.
        """
        if self.check_total_trades():
            bench = self.get_benchmark_df()
            qs.reports.html(bench['Strategy'], benchmark=bench[bench_symbol], periods_per_year=365, mode=mode, output=os.path.join(self.report_folder, filename))

    def plot_profit_benchmark(self, plot_png: bool = True, save_report: bool = False, filename: str = 'profit_benchmark') -> None:
        """Plot and save the profit benchmark.

        Args:
            plot_png (bool, optional): Whether to save the plot as PNG. Defaults to True.
            save_report (bool, optional): Whether to save the plot as HTML. Defaults to False.
            filename (str, optional): Filename for the plot. Defaults to 'profit_benchmark'.
        """
        profit_benchmark = self.get_profit_benchmark_df()
        fig = self.plotter.get_plot_profit_benchmark(profit_benchmark=profit_benchmark)
        self.plotter.plot_and_save(fig, plot_png, save_report, filename, width=1200, height=600, dpi=100)

    def plot_drawdowns_benchmark(self, plot_png: bool = True, save_report: bool = False, filename: str = 'drawdowns_benchmark') -> None:
        """Plot and save the drawdowns benchmark.

        Args:
            plot_png (bool, optional): Whether to save the plot as PNG. Defaults to True.
            save_report (bool, optional): Whether to save the plot as HTML. Defaults to False.
            filename (str, optional): Filename for the plot. Defaults to 'drawdowns_benchmark'.
        """
        profit_benchmark = self.get_profit_benchmark_df()
        fig = self.plotter.get_plot_drawdowns_benchmark(profit_benchmark=profit_benchmark)
        self.plotter.plot_and_save(fig, plot_png, save_report, filename, width=1200, height=600, dpi=100)

    def plot_actions(self, plot_png: bool = True, save_report: bool = False, filename: str = 'actions') -> None:
        """Plot and save the actions.

        Args:
            plot_png (bool, optional): Whether to save the plot as PNG. Defaults to True.
            save_report (bool, optional): Whether to save the plot as HTML. Defaults to False.
            filename (str, optional): Filename for the plot. Defaults to 'actions'.
        """
        df = self.get_action_memory_df()
        fig = self.plotter.get_plot_actions(df)
        self.plotter.plot_and_save(fig, plot_png, save_report, filename, width=1200, height=600, dpi=100)

    def plot_portfolio_weights(self, plot_png: bool = True, save_report: bool = False, filename: str = 'portfolio_weights') -> None:
        """Plot and save the portfolio weights.

        Args:
            plot_png (bool, optional): Whether to save the plot as PNG. Defaults to True.
            save_report (bool, optional): Whether to save the plot as HTML. Defaults to False.
            filename (str, optional): Filename for the plot. Defaults to 'portfolio_weights'.
        """
        df = self.get_portfolio_weights_memory_df()
        fig = self.plotter.get_plot_portfolio_weights(df)
        self.plotter.plot_and_save(fig, plot_png, save_report, filename, width=1200, height=600, dpi=100)

    ################################### VectorBT ###################################
    @staticmethod
    def _get_avg_trades_per_day(df: pd.DataFrame) -> float:
        """Calculate the average number of trades per day.

        Args:
            df (pd.DataFrame): DataFrame containing trade records with a 'Timestamp' column.

        Returns:
            float: The average number of trades per day.
        """
        trades_df = df.copy()
        trades_df['Timestamp'] = pd.to_datetime(trades_df['Timestamp'])
        trades_df['Date'] = trades_df['Timestamp'].dt.date
        daily_trades = trades_df.groupby('Date').size()
        return np.round(daily_trades.mean(), 1)
    
    @staticmethod
    def _get_avg_trades_per_week(df: pd.DataFrame) -> float:
        """Calculate the average number of trades per week.

        Args:
            df (pd.DataFrame): DataFrame containing trade records with a 'Timestamp' column.

        Returns:
            float: The average number of trades per week.
        """
        trades_df = df.copy()
        trades_df['Timestamp'] = pd.to_datetime(trades_df['Timestamp'])
        trades_df['Week'] = trades_df['Timestamp'].dt.to_period('W').apply(lambda r: r.start_time)
        weekly_trades = trades_df.groupby('Week').size()
        return np.round(weekly_trades.mean(), 1)
    
    def get_vbt_backtest_by_symbol(self, symbol: str, lot: float = 0.1, freq: str = '1h') -> Optional[vbt.Portfolio]:
        """Run a backtest using vectorbt's Portfolio.from_orders method.

        Args:
            symbol (str): Trading symbol.
            lot (float, optional): Lot size for each trade. Defaults to 0.1.
            freq (str, optional): Frequency of data. Defaults to '1h'.

        Returns:
            Optional[vbt.Portfolio]: The Portfolio object or None if an error occurs.
        """
        signals = self.get_action_memory_df()[symbol]
        order_sizes = signals.diff().fillna(signals)
        # signals < th 0.01 = 0
        order_sizes = order_sizes.apply(lambda x: 0 if abs(x) < self.env.rebalance_threshold else x)
        
        try:
            pf = vbt.Portfolio.from_orders(
                close=self.get_benchmark_df()[symbol],
                size=order_sizes,
                size_type='amount',
                direction='both',
                fees=self.env.buy_commission_pct / 100,
                freq=freq,
                init_cash=self.env.initial_balance,
                cash_sharing=False
            )
        except Exception as e:
            print(f'No stat error for {symbol}: {e}')
            pf = None
        return pf
    
    def get_stats_by_symbol_df(self, lot: float = 0.1, freq: str = '1h') -> pd.DataFrame:
        """Generate a DataFrame with statistics for each trading symbol.

        Args:
            lot (float, optional): Lot size for each trade. Defaults to 0.1.
            freq (str, optional): Frequency of data. Defaults to '1h'.

        Returns:
            pd.DataFrame: DataFrame containing statistics for each symbol, sorted by total return.
        """
        select_metrics = [
            'End Value', 
            'Total Return [%]', 
            'Benchmark Return [%]', 
            'Max Drawdown [%]', 
            'Max Drawdown Duration', 
            'Total Trades', 
            'Avg Trades by Day',
            'Avg Trades by Week',
            'Win Rate [%]', 
            'Best Trade [%]', 
            'Worst Trade [%]', 
            'Avg Winning Trade [%]', 
            'Avg Losing Trade [%]', 
            'Avg Winning Trade Duration', 
            'Avg Losing Trade Duration', 
            'Profit Factor', 
            'Expectancy', 
            'Sharpe Ratio', 
            'Calmar Ratio', 
            'Sortino Ratio'
        ]

        total_stat: Dict[str, Dict[str, Any]] = {}

        for symbol in self.env.symbols:
            pf = self.get_vbt_backtest_by_symbol(symbol=symbol, lot=lot, freq=freq)
            if pf is not None:
                stats = pf.stats()
                stats['Avg Trades by Day'] = self._get_avg_trades_per_day(pf.orders.records_readable)
                stats['Avg Trades by Week'] = self._get_avg_trades_per_week(pf.orders.records_readable)
                #stats['Total Trades'] = len(pf.trades.records)
                total_stat[symbol] = stats.to_dict()

        bench_metrics_symbols = pd.DataFrame(total_stat).T.sort_values(by='Total Return [%]', ascending=False)[select_metrics]
        float_columns = bench_metrics_symbols.T.select_dtypes(include=['float64'])
        float_columns_ls = list(float_columns.index)
        bench_metrics_symbols = bench_metrics_symbols[float_columns_ls].fillna(0).round(2)
        return bench_metrics_symbols

    def plot_vbt_report_by_symbol(self, plot_png: bool = True, symbol: str = 'BTC-USDT-PERP', lot: float = 0.1, freq: str = '1h', width: int = 1200, height: int = 3500, dpi: int = 100, save_report: bool = False, filename: str = 'vbt-report') -> None:
        """Generate a detailed report plot for a specific trading symbol.

        Args:
            plot_png (bool, optional): Whether to save the plot as PNG. Defaults to True.
            symbol (str, optional): Trading symbol. Defaults to 'BTC-USDT-PERP'.
            lot (float, optional): Lot size for each trade. Defaults to 0.1.
            freq (str, optional): Frequency of data. Defaults to '1h'.
            width (int, optional): Width of the plot. Defaults to 1200.
            height (int, optional): Height of the plot. Defaults to 3500.
            dpi (int, optional): DPI of the plot. Defaults to 100.
            save_report (bool, optional): Whether to save the plot as HTML. Defaults to False.
            filename (str, optional): Filename for the plot. Defaults to 'vbt-report'.
        """
        pf = self.get_vbt_backtest_by_symbol(symbol=symbol, lot=lot, freq=freq)
        fig = pf.plot(subplots=['cum_returns', 'orders', 'trades', 'trade_pnl', 'gross_exposure', 'net_exposure', 'underwater', 'drawdowns', 'assets', 'asset_value', 'cash'])
        fig.update_layout(width=width)
        self.plotter.plot_and_save(fig, plot_png, save_report, filename, width, height, dpi)

    def get_vbt_backtest(self, close: pd.DataFrame, weights: pd.DataFrame, leverage: float = 1, freq: str = '1H') -> vbt.Portfolio:
        """Run a futures market backtest using vectorbt.

        Args:
            close (pd.DataFrame): DataFrame containing closing prices with datetime index.
            weights (pd.DataFrame): DataFrame containing portfolio weights with datetime index.
            leverage (float, optional): Leverage for the futures contracts. Defaults to 1.
            freq (str, optional): Frequency of the data (e.g., '1H' for hourly). Defaults to '1H'.

        Returns:
            vbt.Portfolio: Resulting portfolio from the backtest.
        """
        size = weights * leverage
        # szie to orders
        order_sizes = size.diff().fillna(size)
        #order_sizes = order_sizes.apply(lambda x: 0 if abs(x) < self.env.rebalance_threshold else x)
        
        pf = vbt.Portfolio.from_orders(
            close=close,
            size=order_sizes,
            size_type='targetpercent',
            group_by=True,
            cash_sharing=True,
            init_cash=self.env.initial_balance,
            fees=self.env.buy_commission_pct / 100,
            freq=freq
        )
        self.pf = pf
        return pf
    
    def get_vbt_report(self, freq: str = '1h', leverage: float = 1) -> vbt.Portfolio:
        """Generate a backtest report using vectorbt.

        Args:
            freq (str, optional): Frequency of data. Defaults to '1h'.
            leverage (float, optional): Leverage for the futures contracts. Defaults to 1.

        Returns:
            vbt.Portfolio: Resulting portfolio from the backtest.
        """
        weights_data = self.get_action_memory_df(action_list=self.env.portfolio_weights_memory)
        prices_data = self.env.data.pivot(index='date', columns='symbol', values='close').copy()
        prices_data = prices_data[prices_data.index >= weights_data.index[0]].copy()
        portfolio = self.get_vbt_backtest(prices_data, weights_data, freq=freq, leverage=leverage)
        return portfolio
    
    def plot_vbt_report(self, freq: str = '1h', leverage: float = 1, plots: bool = True, plot_png: bool = True, width: int = 1200, height: int = 600, dpi: int = 100, save_report: bool = False, filename: str = 'vbt-report') -> None:
        """Generate and plot a backtest report using vectorbt.

        Args:
            freq (str, optional): Frequency of data. Defaults to '1h'.
            leverage (float, optional): Leverage for the futures contracts. Defaults to 1.
            plots (bool, optional): Whether to plot the results. Defaults to True.
            plot_png (bool, optional): Whether to save the plot as PNG. Defaults to True.
            width (int, optional): Width of the plot. Defaults to 1200.
            height (int, optional): Height of the plot. Defaults to 600.
            dpi (int, optional): DPI of the plot. Defaults to 100.
            save_report (bool, optional): Whether to save the plot as HTML. Defaults to False.
            filename (str, optional): Filename for the plot. Defaults to 'vbt-report'.
        """
        portfolio = self.get_vbt_report(freq=freq, leverage=leverage)
        stats = portfolio.stats()
        print(stats)
        if plots:
            fig = portfolio.plot()
            self.plotter.plot_and_save(fig, plot_png, save_report, filename, width, height, dpi)
