import pandas as pd
import numpy as np
import gym
from gym import spaces
from typing import List, Tuple, Any, Optional, Dict
from tradegym.rewards import all_rewards_func

class TradingEnv(gym.Env):
    """Trading environment for reinforcement learning.

    This environment is for training trading algorithms using reinforcement learning.
    It allows the agent to take actions representing portfolio weights for different assets.

    Attributes:
        metadata (dict): Metadata for the environment rendering.
    """
    metadata = {"render.modes": ["human"]}

    def __init__(self,
                 data: pd.DataFrame,
                 window: int = 1,
                 features_list: Optional[List[str]] = None,
                 mode_train: bool = False,
                 random_start_step: bool = False,
                 reward_type: str = "tanh_rew",
                 reward_settings: dict = {'alpha': 0.19, 'beta': 0.145},
                 risk_free_rate: float = 0.0005,
                 reward_metric_window: int = 24,
                 initial_balance: float = 10_000,
                 verbose: int = 0,
                 random_seed: int = 10,
                 buy_commission_pct: float = 0.03,  # in percentage
                 sell_commission_pct: float = 0.03,  # in percentage
                 obs_type: str = 'np',
                 rebalance_threshold_pct: float = 0.0):  # in percentage
        """
        Initializes the trading environment.

        Args:
            data (pd.DataFrame): Historical market data.
            window (int): Window size for observation.
            features_list (Optional[List[str]]): List of feature names to be used.
            mode_train (bool): Flag for training mode.
            random_start_step (bool): Flag for random start step.
            reward_type (str): Type of reward function.
            reward_settings (dict): Settings for the reward function.
            risk_free_rate (float): Risk-free rate for reward calculation.
            reward_metric_window (int): Window size for reward metric.
            initial_balance (float): Initial balance for the agent.
            verbose (int): Verbosity level.
            random_seed (int): Random seed for reproducibility.
            buy_commission_pct (float): Commission for buying.
            sell_commission_pct (float): Commission for selling.
            obs_type (str): Type of observation ('np' или 'pd').
            rebalance_threshold_pct (float): Threshold for rebalancing the portfolio in percentage.

        Raises:
            ValueError: If data is None or empty, or if window size is less than or equal to 0.
        """
        # Проверка корректности данных
        if data is None or data.empty:
            raise ValueError("Data cannot be None or empty.")
        
        # Проверка корректности размера окна
        if window <= 0:
            raise ValueError("Window size must be greater than 0.")

        # Инициализация параметров среды
        self.data = data
        self.window = window
        self.features_list = features_list if features_list else ['open', 'high', 'low', 'close', 'volume']
        self.reward_settings = reward_settings
        self.mode_train = mode_train
        self.random_start_step = random_start_step
        self.reward_type = reward_type
        self.risk_free_rate = risk_free_rate
        self.reward_metric_window = reward_metric_window
        self.initial_balance = initial_balance
        self.verbose = verbose
        self.random_seed = random_seed
        self.buy_commission_pct = buy_commission_pct
        self.sell_commission_pct = sell_commission_pct
        self.obs_type = obs_type
        self.rebalance_threshold = rebalance_threshold_pct / 100  # Convert to decimal

        # Предобработка данных
        self.data = self.data.sort_values(['date', 'symbol'])
        self.data.reset_index(drop=True, inplace=True)
        self.data.ffill(inplace=True)
        self.data.fillna(0, inplace=True)

        # Проверка на корректность дат
        self._check_dates(self.data)

        # Формирование списка фичей
        feature_columns = self.features_list.copy()
        feature_columns.extend(['date', 'symbol'])

        # Преобразование данных в 3D тензор для numpy или pandas
        if self.obs_type == 'np':
            self.fe_data = self._data_to_3d_tensor(self.data[feature_columns])
            self.close_prices = self._data_to_3d_tensor(self.data[['date', 'symbol', 'close']].copy())[:, :, 0]
        elif self.obs_type == 'pd':
            self.fe_data = self.data.copy()
            self.close_prices = self._data_to_3d_tensor(self.data[['date', 'symbol', 'close']].copy())[:, :, 0]
        else:
            raise ValueError("Invalid observation type. Use 'pd' or 'np'.")

        # Уникальные даты и символы
        self.all_dates = np.array(self.data.date.unique())
        self.total_dates = len(self.all_dates)

        self.symbols = list(self.data.symbol.unique())
        self.num_assets = len(self.symbols)

        if self.window > self.total_dates:
            raise ValueError("Window size is larger than the number of dates.")

        # Определение пространства наблюдений и действий
        if self.obs_type == 'np':
            if self.window > 1:
                self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                                    shape=(self.window, self.fe_data.shape[1], self.fe_data.shape[2]),
                                                    dtype=np.float32)
            else:
                self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                                    shape=(self.fe_data.shape[1], self.fe_data.shape[2]))
        elif self.obs_type == 'pd':
            if self.window > 1:
                self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                                    shape=(self.window, len(self.features_list), self.num_assets))
            else:
                self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                                    shape=(len(self.features_list), self.num_assets))

        self.action_space = spaces.Box(low=-1, high=1, shape=(self.num_assets,))

        # Установка seed для воспроизводимости
        self.seed(self.random_seed)

        # Инициализация структур памяти
        self.reset()

    def _check_dates(self, df: pd.DataFrame):
        """Check that the number of dates for each symbol matches.
        
        Args:
            df (pd.DataFrame): Input data.
            
        Raises:
            ValueError: If the number of dates for each symbol does not match.
        """
        symbol_counts = df.groupby('symbol')['date'].count()
        if symbol_counts.std() != 0:
            raise ValueError('The number of dates for each symbol does not match.')

    def _data_to_3d_tensor(self, data: pd.DataFrame) -> np.array:
        """
        Convert input data to 3D tensor.

        Args:
            data (pd.DataFrame): Input data.

        Returns:
            np.array: Transformed 3D tensor.
        """
        df = data.sort_values(['date', 'symbol']).copy()
        df = df.set_index(['date', 'symbol'])
        dates = df.index.get_level_values('date').unique()
        data_3d = np.array([df.loc[date].values for date in dates])
        return data_3d

    def reset(self) -> np.array:
        """
        Reset the state of the environment to an initial state.

        Returns:
            np.array: The initial state.
        """
        # Инициализация структур памяти
        self.actions_memory = [np.zeros(self.num_assets),]
        self.total_commission = 0
        self.total_commission_memory = [0,]
        self.balance = self.initial_balance
        self.balance_memory = [self.initial_balance,]
        self.finish_portfolio_value = 0
        self.portfolio_value_memory = [0,]
        self.date_memory = [self.all_dates[0],]
        self.portfolio_weights = np.zeros(self.num_assets)
        self.portfolio_weights_memory = [self.portfolio_weights,]
        self.asset_prices = np.zeros(self.num_assets)
        self.asset_prices_memory = [self.asset_prices,]
        self.positions = np.zeros(self.num_assets)
        self.positions_memory = [np.zeros(self.num_assets),]
        self.total_profit_memory = [0,]
        self.reward_memory = [0,]
        self.trades = 0
        self.reward = 0
        self.episode = 0
        self.current_step = 0
        self.total_step_profit = 0
        self.done = False

        # Начальная позиция в данных
        self.data_step = self.window + 1
        self.current_date = self.all_dates[self.data_step]
        self.date_memory = [self.current_date,]

        # Получение начального состояния
        state = self.get_state(self.data_step)
        return state

    def get_state(self, data_step: int) -> np.array:
        """
        Retrieve the current state of the environment.

        Args:
            data_step (int): The current step in the data.

        Returns:
            np.array: The current state.
        """
        if self.obs_type == 'np':
            if self.window > 1:
                obs = self.fe_data[(data_step - self.window + 1):data_step + 1]
            else:
                obs = np.array(self.fe_data[data_step])
        elif self.obs_type == 'pd':
            obs = self.fe_data[((data_step - self.window + 1) * len(self.symbols)):(data_step + 1) * len(self.symbols)].copy()
        self.current_date = self.all_dates[data_step]
        self.asset_prices = self.close_prices[data_step]
        return obs

    def seed(self, seed: int = 1) -> list:
        """
        Set the random seed for the environment.

        Args:
            seed (int, optional): The random seed value.

        Returns:
            list: The random seed.
        """
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def render(self, mode: str = "human"):
        """
        Render the environment.

        Args:
            mode (str, optional): The mode for rendering.
        """
        print(
            f"Date: {self.date_memory[-1]}, Balance: {self.balance:.2f}, "
            f"Portfolio Value: {self.finish_portfolio_value:.2f}, "
            f"Profit: {self.total_step_profit:.2f}, "
            f"Trades: {self.trades}, "
            f"Total Commission: {self.total_commission:.5f}"
        )

    def _calculate_commission(self, balance, new_weights, old_weights, positions, asset_prices, buy_commission_pct, sell_commission_pct):
        """
        Calculate commission for the trading.

        Args:
            balance: Current balance.
            new_weights: New portfolio weights.
            old_weights: Old portfolio weights.
            positions: Current positions.
            asset_prices: Current asset prices.
            buy_commission_pct: Buy commission rate.
            sell_commission_pct: Sell commission rate.

        Returns:
            float: Total commission cost.
        """
        changes_in_quantity = (np.divide(new_weights, old_weights, out=np.zeros_like(new_weights), where=old_weights != 0) * positions) - positions
        changes_in_quantity[old_weights == 0] = (balance * new_weights / asset_prices)[old_weights == 0]
        buy_cost = np.sum(np.maximum(changes_in_quantity * asset_prices, 0))
        sell_cost = np.sum(np.abs(np.minimum(changes_in_quantity * asset_prices, 0)))
        total_buy_commission = buy_cost * (buy_commission_pct / 100)
        total_sell_commission = sell_cost * (sell_commission_pct / 100)
        total_commission = total_buy_commission + total_sell_commission
        if np.isfinite(total_commission):
            total_commission = round(total_commission, 10)
        if np.isnan(total_commission):
            total_commission = 0
        return total_commission

    def _normalize_weights(self, actions):
        """
        Normalize portfolio weights.

        Args:
            actions: Actions representing raw portfolio weights.

        Returns:
            np.array: Normalized portfolio weights.
        """
        total_action = np.sum(np.abs(actions))
        if total_action > 1:
            normalized_weights = actions / total_action if total_action != 0 else np.zeros(self.num_assets)
        else:
            normalized_weights = actions
        normalized_weights = np.clip(normalized_weights, -1, 1)
        normalized_weights = np.round(normalized_weights, 4)
        return normalized_weights

    def _get_reward(self):
        """
        Calculate the reward based on the selected reward type.
        """
        if self.reward_type in ["sharpe", "sortino", 'mean_return', 'alpha_penalize']:
            if self.current_step < self.reward_metric_window or len(self.balance_memory) < self.reward_metric_window:
                self.reward = 0
            else:
                self.reward_settings['balances'] = self.balance_memory[(self.current_step - self.reward_metric_window) - 1: self.current_step]
                self.reward_settings['returns'] = np.diff(self.reward_settings['balances']) / self.reward_settings['balances'][:-1]
                self.reward_settings['risk_free_rate'] = self.risk_free_rate
                self.reward_settings['total_commission'] = self.total_commission
                self.reward = all_rewards_func[self.reward_type](**self.reward_settings)
        else:
            self.reward_settings['asset_prices'] = self.asset_prices
            self.reward_settings['old_asset_prices'] = self.old_asset_prices
            self.reward_settings['portfolio_weights'] = self.portfolio_weights
            self.reward_settings['total_step_profit'] = self.total_step_profit
            self.reward = all_rewards_func[self.reward_type](**self.reward_settings)
        if not np.isfinite(self.reward):
            self.reward = 0

    def _calculate_positions(self, weights: np.array, balance: float, prices: np.array) -> np.array:
        """
        Calculate positions based on portfolio weights and current balance.

        Args:
            weights (np.array): Portfolio weights.
            balance (float): Current balance.
            prices (np.array): Current asset prices.

        Returns:
            np.array: Positions.
        """
        positions = (weights * balance) / prices
        return positions

    def _calculate_portfolio_value(self, positions: np.array, prices: np.array) -> float:
        """
        Calculate portfolio value based on positions and current asset prices.

        Args:
            positions (np.array): Current positions.
            prices (np.array): Current asset prices.

        Returns:
            float: Portfolio value.
        """
        portfolio_value = np.round(np.sum(np.abs(positions) * prices), 4)
        return portfolio_value

    def _calculate_weights(self, balance: float, positions: np.array, prices: np.array) -> np.array:
        """
        Calculate portfolio weights based on current positions and asset prices.

        Args:
            balance (float): Current balance.
            positions (np.array): Current positions.
            prices (np.array): Current asset prices.

        Returns:
            np.array: Portfolio weights.
        """
        asset_values = positions * prices
        total_portfolio_value = np.sum(np.abs(asset_values))
        cash_allocation = (balance - total_portfolio_value) / balance
        full_weights = np.zeros(len(prices))
        if total_portfolio_value > 0:
            weights = (asset_values / total_portfolio_value) * (1 - cash_allocation)
            full_weights = weights
        return np.round(full_weights, 4)

    def _calculate_step_profit(self, prices: np.array, old_prices: np.array, positions: np.array) -> float:
        """
        Calculate the total profit or loss from the current step.

        Args:
            prices (np.array): Current asset prices.
            old_prices (np.array): Asset prices from the previous step.
            positions (np.array): Current positions.

        Returns:
            float: Total profit.
        """
        price_change = prices - old_prices
        long_profit_loss = np.sum(np.where(positions > 0, positions * price_change, 0))
        short_profit_loss = np.sum(np.where(positions < 0, positions * -price_change, 0))
        step_profit = (long_profit_loss - short_profit_loss)
        return step_profit

    def _update_memory(self):
        """
        Update the memory structures with the latest values.
        """
        self.portfolio_value = self._calculate_portfolio_value(self.positions, self.asset_prices)
        self.portfolio_weights = self._calculate_weights(self.balance, self.positions, self.asset_prices)
        self.portfolio_value_memory.append(self.portfolio_value)
        self.total_profit_memory.append(self.total_step_profit)
        self.portfolio_weights_memory.append(self.portfolio_weights.copy())
        self.asset_prices_memory.append(self.asset_prices.copy())
        self.reward_memory.append(self.reward)
        self.balance_memory.append(self.balance)
        self.total_commission_memory.append(self.total_commission)
        self.date_memory.append(self.current_date)

    def step(self, actions: np.array) -> Tuple[np.array, float, bool, Dict[str, Any]]:
        """
        Execute one time step within the environment.

        Args:
            actions (np.array): An array of actions to execute in the environment.

        Returns:
            Tuple[np.array, float, bool, Dict[str, Any]]: A tuple containing the next state, reward, done, and info.
        """
        self.actions_memory.append(actions.copy())
        self.old_portfolio_weights = self.portfolio_weights.copy()
        self.old_asset_prices = self.asset_prices.copy()
        self.new_portfolio_weights = self._normalize_weights(actions)
        
        # Calculate the change in weights directly
        weight_change = np.abs(self.old_portfolio_weights - self.new_portfolio_weights)

        if np.any(weight_change > self.rebalance_threshold):
            # If change exceeds the threshold, apply commissions and update positions
            self.total_commission = self._calculate_commission(
                balance=self.balance,
                new_weights=self.new_portfolio_weights,
                old_weights=self.old_portfolio_weights,
                positions=self.positions,
                asset_prices=self.asset_prices,
                buy_commission_pct=self.buy_commission_pct,
                sell_commission_pct=self.sell_commission_pct,
            )
            self.balance -= self.total_commission
            #if self.total_commission > 0:
            self.trades += 1

            self.positions = self._calculate_positions(self.new_portfolio_weights, self.balance, self.asset_prices)
            self.portfolio_weights = self.new_portfolio_weights.copy()
            self.total_commission_memory.append(self.total_commission)
        else:
            #self.total_commission_memory.append(0)
            self.total_commission = 0
            
            #self.positions = self._calculate_positions(self.new_portfolio_weights, self.balance, self.asset_prices)

        self.current_step += 1
        self.data_step += 1

        state = self.get_state(self.data_step)
        self.step_profit = self._calculate_step_profit(self.asset_prices, self.old_asset_prices, self.positions)
        self.total_step_profit = self.step_profit - self.total_commission
        self.balance += self.step_profit
        self._get_reward()

        if self.data_step == self.total_dates - 1 or self.balance <= 0:
            self.done = True

        self._update_memory()
        info = {}
        return state, self.reward, self.done, info

    def save_balance_memory(self) -> pd.DataFrame:
        """
        Save the balance memory to a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the balance memory.
        """
        df_memory = pd.DataFrame({"date": self.date_memory, "account_value": self.balance_memory})
        return df_memory

    def save_memory(self) -> pd.DataFrame:
        """
        Save the memory to a DataFrame.

        Returns:
            pd.DataFrame: DataFrame containing the memory.
        """
        df_memory = pd.DataFrame(
            {
                "date": self.date_memory,
                "account_value": self.balance_memory,
                "actions": self.actions_memory,
                "portfolio_weights": self.portfolio_weights_memory,
                "portfolio_value": self.portfolio_value_memory,
                "reward": self.reward_memory,
            }
        )
        return df_memory

    def save_action_memory(self, action_list=None) -> pd.DataFrame:
        """
        Save the action memory to a DataFrame.

        Args:
            action_list (list, optional): List of actions.

        Returns:
            pd.DataFrame: DataFrame containing the action memory.
        """
        if self.num_assets > 1:
            date_list = self.date_memory
            df_date = pd.DataFrame(date_list)
            df_date.columns = ["date"]

            if action_list is None:
                action_list = self.actions_memory

            df_actions = pd.DataFrame(action_list)
            df_actions.columns = self.symbols
            df_actions.index = df_date.date
        else:
            date_list = self.date_memory[:-1]
            action_list = self.actions_memory
            df_actions = pd.DataFrame({"date": date_list, "actions": action_list})
            
        return df_actions
