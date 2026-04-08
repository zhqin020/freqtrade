import logging

import pandas as pd


logger = logging.getLogger(__name__)


def tripple_barrier(df_col, upper_pct, lower_pct, result):
    """Return label associated with first time crossing of vertical, upper or lower barrier

    upper_pct: % above close first cancle
    lower_pct: % below close first candle
    result: one of ["side", "value"]

    Example useage:
        window = 5
        params = {"upper_pct": 0.003, "lower_pct": 0.003}
        df["tripple_barrier"] = (
            df["close"]
            .shift(-window)
            .rolling(window + 1)
            .apply(tripple_barrier, kwargs=params)
        )
        tbm_map = {1: "upper", 0: "vertical", -1: "lower"}
        df["&tbm_target"] = df["tripple_barrier"].map(tbm_map)
    """

    initial_value = df_col.iat[0]
    upper_threshold = initial_value * (1 + upper_pct)
    lower_threshold = initial_value * (1 - lower_pct)

    # Get index position of first time upper & lower are crossed
    upper_idx = (df_col > upper_threshold).argmax() if (df_col > upper_threshold).any() else 99999
    lower_idx = (df_col < lower_threshold).argmax() if (df_col < lower_threshold).any() else 99999

    # Based on first crossing, assign appropriate label
    if upper_idx < lower_idx:
        side = 1
        value = df_col.iloc[upper_idx]
    elif lower_idx < upper_idx:
        side = -1
        value = df_col.iloc[lower_idx]
    else:
        side = 0
        value = df_col.iloc[-1]

    if result == "side":
        return side
    elif result == "value":
        return value


def max_extreme_value(df_col):
    """Identify max extreme value over future window and return value"""

    initial_value = df_col.iat[0]
    df_norm = df_col - initial_value

    # Get index position of first time upper & lower are crossed
    idx = df_norm.abs().argmax()

    return df_col.values[idx]


def nearby_extremes(df, threshold: float, forward_pass: bool, reverse_pass: bool):
    """Identify values beside peaks/valleys that are within a
    threshold distance and re-label them"""

    df.rename(columns={df.columns[1]: "raw_peaks"}, inplace=True)
    df_holder = []
    df_holder.append(df["raw_peaks"])

    # Forward Pass (avoid DataFrame.eval / numexpr to prevent object-dtype issues)
    if forward_pass:
        tmp = pd.concat(
            [
                df,
                df.mask(df["raw_peaks"] == 0).ffill().rename(columns=lambda n: "prev_" + n),
            ],
            axis=1,
        )

        # Compute within_threshold safely using pandas operations
        within_threshold = (tmp["close"].sub(tmp["prev_close"]).abs().div(tmp["prev_close"])) < threshold
        mask = within_threshold & (tmp["raw_peaks"] == 0)
        is_new_extreme = within_threshold.mask(mask).ffill()
        forward_extremes = tmp["prev_raw_peaks"].where(is_new_extreme).fillna(0).astype(int)

        df_holder.append(forward_extremes)

    # Reverse Pass
    if reverse_pass:
        rev = df.sort_index(ascending=False)
        tmp = pd.concat(
            [
                rev,
                rev.mask(rev["raw_peaks"] == 0).ffill().rename(columns=lambda n: "prev_" + n),
            ],
            axis=1,
        )

        within_threshold = (tmp["close"].sub(tmp["prev_close"]).abs().div(tmp["prev_close"])) < threshold
        mask = within_threshold & (tmp["raw_peaks"] == 0)
        is_new_extreme = within_threshold.mask(mask).ffill()
        reverse_extremes = tmp["prev_raw_peaks"].where(is_new_extreme).fillna(0).astype(int)

        df_holder.append(reverse_extremes.sort_index())

    # Merging
    merged_df = pd.concat(df_holder, axis=1)
    final_df = merged_df.sum(axis=1).clip(lower=-1, upper=1)

    return final_df
