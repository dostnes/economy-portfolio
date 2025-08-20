"""
Reads a list of tickers from tickers.txt, adds the .OL suffix,
and fetches the latest price for each from yfinance.
"""
import yfinance as yf

def main():
    try:
        with open("tickers.txt", "r", encoding="utf-8") as f:
            # Read all lines and strip whitespace/newlines from each
            stocks = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("❌ Error: tickers.txt not found.")
        print("Please run get_tickers.py first to create the file.")
        return

    if not stocks:
        print("No tickers found in tickers.txt.")
        return

    print(f"✅ Found {len(stocks)} stocks in tickers.txt. Fetching prices...")
    print("---")

    suffix = ".OL"
    for stock in stocks:
        ticker_for_yfinance = stock + suffix
        try:
            yf_ticker = yf.Ticker(ticker_for_yfinance)
            hist = yf_ticker.history(period="1mo")
            
            if not hist.empty:
                latest_price = hist['Close'].iloc[-1]
                print(f"  - {ticker_for_yfinance}: ${latest_price:.2f}")
            else:
                print(f"  - {ticker_for_yfinance}: No data found")
        except Exception as e:
            print(f"  - Could not get data for {ticker_for_yfinance}: {e}")

if __name__ == "__main__":
    main()