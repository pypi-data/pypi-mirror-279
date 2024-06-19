import logging
import os

import pandas as pd
from dotenv import load_dotenv
from py_alpaca_api import PyAlpacaAPI

from alpaca_daily_losers.close_positions import ClosePositions
from alpaca_daily_losers.global_functions import (
    get_ticker_data,
    send_message,
    send_position_messages,
)
from alpaca_daily_losers.liquidate import Liquidate
from alpaca_daily_losers.openai import OpenAIAPI
from alpaca_daily_losers.statistics import Statistics

# get a custom logger & set the logging level
py_logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.WARNING if os.getenv("PRODUCTION") == "True" else logging.INFO,
    format="%(name)s %(asctime)s %(levelname)s %(message)s",
)

load_dotenv()

api_key = str(os.getenv("API_KEY"))
api_secret = str(os.getenv("API_SECRET"))
api_paper = True if os.getenv("API_PAPER") == "True" else False


class DailyLosers:
    def __init__(self):
        self.alpaca = PyAlpacaAPI(api_key=api_key, api_secret=api_secret, api_paper=api_paper)
        self.production = True if os.getenv("PRODUCTION") == "True" else False
        self.liquidate = Liquidate(trading_client=self.alpaca.trading, py_logger=py_logger)
        self.close = ClosePositions(
            trading_client=self.alpaca.trading,
            stock_client=self.alpaca.stock,
            py_logger=py_logger,
        )
        self.statistics = Statistics(account=self.alpaca.trading.account, py_logger=py_logger)

    def run(self, buy_limit: int = 6, article_limit: int = 4) -> None:
        """
        Executes the main logic of the program.

        This method performs the following steps:
        1. Attempts to sell positions based on certain criteria.
        2. Attempts to liquidate positions for capital.
        3. Checks for new buy opportunities.

        If any of the steps encounter an error, it logs the error and
        continues to the next step.
        """
        try:
            self.close.sell_positions_from_criteria()
        except Exception as e:
            py_logger.error(f"Error selling positions from criteria. Error {e}")
            pass
        try:
            self.liquidate.liquidate_positions()
        except Exception as e:
            py_logger.error(f"Error liquidating positions for capital. Error: {e}")
            pass
        try:
            self.check_for_buy_opportunities(buy_limit=buy_limit, article_limit=article_limit)
        except Exception as e:
            py_logger.error(f"Error entering new positions. Error {e}")

    ########################################################
    # Define the check_for_buy_opportunities method
    ########################################################
    def check_for_buy_opportunities(self, buy_limit: int = 6, article_limit: int = 4) -> None:
        """
        Checks for buy opportunities based on daily losers and opens positions if any are found.

        Returns:
            None
        """
        losers = self.get_daily_losers()
        tickers = self.filter_tickers_with_news(
            losers, filter_ticker_limit=buy_limit, article_limit=article_limit
        )

        if len(tickers) > 0:
            print(f"Found {len(tickers)} buy opportunities.")
            self.open_positions(tickers=tickers, ticker_limit=buy_limit)
        else:
            print("No buy opportunities found")

    ########################################################
    # Define the open_positions method
    ########################################################
    def open_positions(self, tickers: list, ticker_limit: int = 6) -> None:
        """
        Opens buying orders based on buy opportunities and openai sentiment.
        Limits the number of stocks to buy to 8 by default.

        Args:
            tickers (list): A list of ticker symbols to buy.
            ticker_limit (int, optional): The maximum number of tickers to buy. Defaults to 8.

        Returns:
            None
        """

        available_cash = self.alpaca.trading.account.get().cash

        if len(tickers) == 0:
            send_message("No tickers to buy.")
            return
        else:
            notional = (available_cash / len(tickers[:ticker_limit])) - 1

        bought_positions = []

        for ticker in tickers[:ticker_limit]:
            try:
                self.alpaca.trading.orders.market(symbol=ticker, notional=notional)
            except Exception as e:
                py_logger.warning(f"Error entering new position for {ticker}. Error: {e}")
                send_message(message=f"Error buying {ticker}: {e}")
                continue
            else:
                bought_positions.append({"symbol": ticker, "notional": round(notional, 2)})

        send_position_messages(positions=bought_positions, pos_type="buy")

    ########################################################
    # Define the update_or_create_watchlist method
    ########################################################
    def update_or_create_watchlist(self, name, symbols) -> None:
        """
        Updates an existing watchlist with the given name and symbols,
        or creates a new watchlist if it doesn't exist.

        Args:
            name (str): The name of the watchlist.
            symbols (List[str]): A list of symbols to be added to the watchlist.

        Returns:
            None

        Raises:
            Exception: If the watchlist cannot be updated or created.

        """
        try:
            self.alpaca.trading.watchlists.update(watchlist_name=name, symbols=symbols)
        except Exception as e:
            py_logger.info(
                f"Watchlist could not be updated: {e}:\nTrying to create new watchlist with \
                    name: {name}"
            )
            try:
                self.alpaca.trading.watchlists.create(name=name, symbols=symbols)
            except Exception as e:
                py_logger.error(f"Could not create or update the watchlist {name}.\nError: {e}")

    ########################################################
    # Define the filter_tickers_with_news method
    ########################################################
    def filter_tickers_with_news(
        self, tickers: list, article_limit: int = 4, filter_ticker_limit: int = 6
    ) -> list:
        """
        Filters a list of tickers based on news sentiment analysis.

        Args:
            tickers (list): A list of tickers to filter.
            article_limit (int, optional): The maximum number of articles to retrieve for each
            ticker. Defaults to 4.
            filter_ticker_limit (int, optional): The maximum number of tickers to include
            in the filtered list. Defaults to 8.

        Returns:
            list: The filtered list of tickers based on news sentiment analysis.
        """

        openai = OpenAIAPI()
        filtered_tickers = []

        for i, ticker in enumerate(tickers):
            if len(filtered_tickers) >= filter_ticker_limit:
                break
            try:
                articles = self.alpaca.trading.news.get_news(
                    symbol=ticker, limit=article_limit, content_length=4000
                )
            except Exception as e:
                py_logger.warning(f"Error getting articles for {ticker}. Error {e}")
                continue

            if len(articles) >= article_limit and len(articles) > 0:
                if len(filtered_tickers) >= filter_ticker_limit:
                    break
                py_logger.info(f"Found {len(articles)} articles for {ticker}")
                bullish = 0
                bearish = 0
                for art in articles[:article_limit]:
                    sentiment = openai.get_sentiment_analysis(
                        title=art["title"],
                        symbol=art["symbol"],
                        article=art["content"],
                    )
                    if sentiment == "BULLISH":
                        bullish += 1
                    else:
                        bearish += 1

                if bullish > bearish:
                    filtered_tickers.append(ticker)

        self.update_or_create_watchlist(name="DailyLosers", symbols=filtered_tickers)

        return self.alpaca.trading.watchlists.get_assets(watchlist_name="DailyLosers")

    ########################################################
    # Define the get_daily_losers method
    ########################################################
    def get_daily_losers(self) -> list:
        """
        Retrieves the daily losers from Alpaca stock predictor,
        filters them based on buy criteria,
        and updates the watchlist with the filtered losers.

        Returns:
            A list of assets in the DailyLosers watchlist.
        """
        losers = self.alpaca.stock.predictor.get_losers_to_gainers()
        losers = get_ticker_data(
            tickers=losers, stock_client=self.alpaca.stock, py_logger=py_logger
        )
        losers = self.buy_criteria(losers)

        if len(losers) == 0:
            send_message("No daily losers found.")
            return []

        for i, ticker in enumerate(losers):
            try:
                sentiment = self.alpaca.trading.recommendations.get_sentiment(ticker)
            except Exception as e:
                py_logger.info(f"Error getting sentiment from Yahoo. Error: {e}")
                sentiment = "NEUTRAL"

            if sentiment == "NEUTRAL" or sentiment == "BEARISH":
                losers.remove(ticker)

        if len(losers) == 0:
            send_message("No daily losers found.")
            return []

        print(f"Found {len(losers)} daily losers with BULLISH recommendations.")

        self.update_or_create_watchlist(name="DailyLosers", symbols=losers)

        return self.alpaca.trading.watchlists.get_assets(watchlist_name="DailyLosers")

    ########################################################
    # Define the buy_criteria method
    ########################################################
    def buy_criteria(self, data: pd.DataFrame) -> list:
        """
        Applies buy criteria to the given DataFrame and returns a
        list of symbols that meet the criteria.

        Parameters:
        - data (pd.DataFrame): The DataFrame containing the data
        to apply the buy criteria on.

        Returns:
        - list: A list of symbols that meet the buy criteria.

        Raises:
        - None

        Example usage:
        ```
        data = pd.DataFrame(...)
        symbols = buy_criteria(data)
        print(symbols)
        ```

        Note:
        - The buy criteria is based on two conditions:
            1. RSI (Relative Strength Index) values in the columns
            'rsi14', 'rsi30', 'rsi50', 'rsi200' should be less than or equal to 30.
            2. BBLO (Bollinger Bands Lower Indicator) values in the
            columns 'bblo14', 'bblo30', 'bblo50', 'bblo200' should be equal to 1.
        - If no symbols meet the buy criteria, an empty list is returned.
        - The watchlist named 'DailyLosers' is updated or created with
        the symbols that meet the buy criteria.
        - The assets in the 'DailyLosers' watchlist are returned.

        """

        RSI_COLUMNS = ["rsi14", "rsi30", "rsi50", "rsi200"]
        BBLO_COLUMNS = ["bblo14", "bblo30", "bblo50", "bblo200"]

        criterion1 = data[RSI_COLUMNS] <= 30
        criterion2 = data[BBLO_COLUMNS] == 1
        buy_criteria = criterion1.any(axis=1) | criterion2.any(axis=1)

        buy_filtered_data = data[buy_criteria]

        filtered_data = list(buy_filtered_data["symbol"])

        if len(filtered_data) == 0:
            print("No tickers meet the buy criteria")
            return []

        print(f"Found {len(filtered_data)} tickers that meet the buy criteria.")

        self.update_or_create_watchlist(name="DailyLosers", symbols=filtered_data)

        return self.alpaca.trading.watchlists.get_assets(watchlist_name="DailyLosers")
