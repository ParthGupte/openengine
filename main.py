from openengine.data.yahoo_connector import YahooFinanceConnector
from openengine.strategies.sample_strategy import SampleStrategy, MarubozuStrategy
from openengine.engine.backtester import Backtester
from openengine.utilities.config import INITIAL_CAPITAL

from datetime import datetime

def date_range_to_decimal_years(start_date: str, end_date: str) -> float:
    """
    Convert a date range in 'YYYY-MM-DD' format to a decimal number of years.
    
    Args:
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
    
    Returns:
        float: Decimal number of years between the two dates.
    """
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    
    days_difference = (end - start).days
    decimal_years = days_difference / 365.25  # account for leap years
    
    return decimal_years

def main():
    # Define parameters for data fetching
    ticker = "RELIANCE.NS"  # Example: Reliance Industries on NSE
    start_date = "2015-01-01"
    end_date = "2020-01-01"

    # Fetch historical data using the YahooFinanceConnector
    data_connector = YahooFinanceConnector()
    data = data_connector.fetch_data(ticker, start_date, end_date, interval="1d")
    
    # Initialize strategy
    strategy = MarubozuStrategy(0.005)
    # strategy = SampleStrategy()
    
    # Create and run the backtester
    backtester = Backtester(data, strategy, initial_capital=INITIAL_CAPITAL)
    portfolio = backtester.run()
    
    print("Backtesting complete. Final portfolio snapshot:")
    print(portfolio.tail())
    print("Annualised returns:",((portfolio.tail().iloc[-1]["total"]/INITIAL_CAPITAL)**(1/date_range_to_decimal_years(start_date,end_date))-1)*100)
    start_price = data.iloc[0]['Close'].item()
    end_price = data.iloc[-1]['Close'].item()
    print("Buy and Hold Returns:",(((end_price/start_price)**(1/date_range_to_decimal_years(start_date,end_date)))-1)*100)

if __name__ == "__main__":
    main()
