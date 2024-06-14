import numpy as np
import empyrical as ep

def reward_sortino(returns, risk_free_rate: float = 0.0005, **kwargs):
    reward = ep.sortino_ratio(returns, risk_free_rate)
    return np.round(reward, 3)

def reward_sharpe(returns, risk_free_rate: float = 0.0005, **kwargs):
    reward = ep.sharpe_ratio(returns, risk_free_rate)
    return np.round(reward, 3)

def reward_mean_return(returns, **kwargs):
    reward = np.tanh(np.mean(returns))
    return np.round(reward, 3)

def reward_tanh(total_step_profit, **kwargs):
    reward = np.tanh(total_step_profit)
    return np.round(reward, 3)

def reward_alpha_penalize(alpha, beta, returns, total_commission, **kwargs):
    if len(returns) < 2:
        reward = 0
    else:
        reward = (1+alpha)*np.min(returns) + (1-alpha)*np.mean(returns)  - beta*total_commission
    return np.round(reward, 3)

def reward_max_possible_return(asset_prices, old_asset_prices, portfolio_weights, **kwargs) -> float:
        """Calculate the reward based on the maximum possible return at the current step.

        The reward is calculated as the ratio of the actual return achieved by the current
        portfolio allocation to the maximum possible return. The maximum return is defined 
        as the absolute sum of the price changes for each asset.

        Returns:
            reward: The calculated reward.

        Raises:
            ZeroDivisionError: If the maximum possible return is zero.
        """
        # Calculate the price change
        price_change_percent = (asset_prices - old_asset_prices) / old_asset_prices

        # Calculate the maximum possible return if all capital was invested in the asset with the largest price change,
        max_rew = np.max(np.abs(price_change_percent))

        # Calculate the return you actually achieved with your portfolio
        current_rew = np.sum((portfolio_weights * price_change_percent))

        if max_rew == 0 or np.sum(np.abs(portfolio_weights)) == 0:
            reward = 0.0
        else:
            reward = np.round(current_rew / max_rew, 3)
        
        return np.round(reward, 3)


##########################################################################################################################

all_rewards_func = {
    'mean_return': reward_mean_return,
    'sortino': reward_sortino,
    'sharpe': reward_sharpe,
    'tanh_rew': reward_tanh,
    'alpha_penalize': reward_alpha_penalize,
    'max_possible_return': reward_max_possible_return,
}