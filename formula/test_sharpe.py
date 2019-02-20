import sharpe

e_sharpe, pdf = sharpe.equity_sharpe ('GOOG')
mn_sharpe = sharpe.market_neutral_sharpe('GOOG', 'SPY')