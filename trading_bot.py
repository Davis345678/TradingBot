import json
import time
import logging
import os
import subprocess
import random
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Simulate price data for BTC/USD
def simulate_price():
    # Simulate a price between $25,000 and $35,000 with some randomness
    base_price = 30000
    fluctuation = random.uniform(-1000, 1000)  # Random fluctuation of ±$1000
    return base_price + fluctuation

# Main trading loop with simulated data
def trading_loop():
    trades = []
    # Load existing trades if trades.json exists
    if os.path.exists('trades.json'):
        try:
            with open('trades.json', 'r') as f:
                trades = json.load(f)
        except json.JSONDecodeError:
            logging.warning("trades.json is corrupted, starting with an empty list")
            trades = []

    while True:
        try:
            price = simulate_price()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            trade_type = random.choice(['buy', 'sell'])
            trade = {
                'timestamp': timestamp,
                'symbol': 'BTC/USD',
                'type': trade_type,
                'price': round(price, 2)
            }
            trades.append(trade)

            # Save trades to trades.json
            with open('trades.json', 'w') as f:
                json.dump(trades, f, indent=4)

            logging.info(f"New trade: {trade}")

            # Update trades on GitHub
            update_trades_on_github()

            # Wait for 60 seconds before the next trade
            time.sleep(60)

        except Exception as e:
            logging.error(f"Error in trading loop: {e}")
            time.sleep(60)

# Function to update trades.json on GitHub
def update_trades_on_github():
    try:
        # Ensure we're in the correct directory
        os.chdir("C:/TradingBot")
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if "trades.json" in status.stdout:
            subprocess.run(["git", "add", "trades.json"])
            subprocess.run(["git", "commit", "-m", "Update trades.json"])
            subprocess.run(["git", "push", "origin", "main"])
            logging.info("Successfully updated trades.json on GitHub")
        else:
            logging.info("No changes to trades.json to commit")
    except Exception as e:
        logging.error(f"Error updating trades on GitHub: {e}")

# Main function to start the bot
def main():
    logging.info("Starting trading bot in paper trading mode...")
    trading_loop()

if __name__ == "__main__":
    main()