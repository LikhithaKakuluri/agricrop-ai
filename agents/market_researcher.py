def get_top_market_crop(market_df):
    # Sort by demand index
    return market_df.sort_values(by="Demand_Index", ascending=False).iloc[0]
