import pandas as pd

def smooth_trial_outcomes(df, window_size=10):

    smoothed = pd.DataFrame()

    for trial_number, g in df.groupby('trial_number'):
        sg = g.copy()
        for col in ['return_ratio', 'observed_returns', 'optimal_returns']:
            sg[col] = g[col].rolling(window_size).mean()
        smoothed = smoothed.append(sg)

    return smoothed
