from  portfolioBuilder import portfolioBuilder
import pandas as pd

portfolio = PortfolioBuilder()
df_mean_reversion = protfolio.doMeanReversionTest('price_close')
df_rank = portfolio.rankMeanReversion(df_mean_reversion)
mean_reversion_codes = portfolio.buildUniverse(df_rank, 'rank', 0.8)

print mean_reversion_codes


