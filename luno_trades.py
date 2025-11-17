#!/usr/bin/env python3

# Parse .env file.
# If any of the .env is missing halt, output error and exit

import os
import csv
import json
import base64
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime


def load_env_file(filepath=".env"):
    """Load environment variables from a .env file and validate required variables"""
    if not os.path.exists(filepath):
        return

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            # Split on first '=' only
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                os.environ[key] = value

    # Validate required environment variables
    required_vars = [
        "LUNO_API_KEY",
        "LUNO_API_SECRET",
        "TOKENS",
        "CURRENCY",
        "START_DATE",
        "END_DATE",
    ]

    empty_vars = []

    for var_name in required_vars:
        env_value = os.getenv(var_name)

        if not env_value or not env_value.strip():
            empty_vars.append(var_name)

    if empty_vars:
        print(
            f"Error: The following required environment variables are empty: {', '.join(empty_vars)}"
        )
        exit(1)


def parse_date_to_timestamp(date):
    # Parse the input date (returns seconds, convert to milliseconds)
    parsed_timestamp = int(datetime.strptime(date, "%Y-%m-%d").timestamp() * 1000)

    # Get current date (without time for fair comparison) - convert to milliseconds
    current_timestamp = int(datetime.now().timestamp() * 1000)

    # Get historical date - convert to milliseconds
    earliest_timestamp = int(
        datetime.strptime("2009-01-09", "%Y-%m-%d").timestamp() * 1000
    )

    if parsed_timestamp <= earliest_timestamp or parsed_timestamp > current_timestamp:
        print(
            f"Error: The date {date} is not within the valid range. Please check that your dates are correct and follow the yyyy-mm-dd format."
        )
        exit(1)

    return parsed_timestamp


def make_luno_api_call(params):
    """Make authenticated API call to Luno using urllib"""

    """Format Luno API URL with proper parameter encoding"""
    base_url = "https://api.luno.com/api/1/listtrades"
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"

    # DEBUG: Print the URL and params
    print(f"DEBUG - URL: {url}")
    print(f"DEBUG - Params: {params}")

    # Get credentials
    api_key = os.getenv("LUNO_API_KEY")
    api_secret = os.getenv("LUNO_API_SECRET")

    if not api_key or not api_secret:
        raise Exception(
            "LUNO_API_KEY and LUNO_API_SECRET environment variables are required"
        )

    # Create request
    request = urllib.request.Request(url)

    # Add authentication header (HTTP Basic Auth)
    credentials = f"{api_key}:{api_secret}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("ascii")
    auth_header = f"Basic {encoded_credentials}"
    request.add_header("Authorization", auth_header)

    try:
        # Make the request
        with urllib.request.urlopen(request) as response:
            response_data = response.read().decode("utf-8")
            return json.loads(response_data)

    except urllib.error.HTTPError as e:
        # DEBUG: Print raw error response
        print(f"DEBUG - HTTP Error: {e.code} {e.reason}")
        error_body = e.read().decode("utf-8")
        print(f"DEBUG - Error body: {error_body}")

        try:
            error_data = json.loads(error_body)
            raise Exception(f"API Error: {error_data.get('message', error_body)}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise Exception(f"HTTP {e.code}: {e.reason}\nResponse: {error_body}")
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {e.reason}")


def request_trades(token, currency, start_date, end_date):
    params = {
        "pair": f"{token}{currency}",
        "since": start_date,
        "before": end_date,
        "limit": 1000,
    }

    # Make API call using urllib
    response = make_luno_api_call(params)

    if "trades" not in response:
        raise Exception("No trades found in response")

    trades = response["trades"]

    return trades


def parse_tokens(tokens_str):
    tokens = tokens_str.split(",")
    return [token.strip() for token in tokens]


def append_to_csv(trades, filename):
    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write headers only if file is new
        if not file_exists:
            writer.writerow(
                [
                    "base",
                    "client_order_id",
                    "counter",
                    "fee_base",
                    "fee_counter",
                    "is_buy",
                    "order_id",
                    "pair",
                    "price",
                    "sequence",
                    "timestamp",
                    "type",
                    "volume",
                ]
            )

        # Write trade data
        for trade in trades:
            writer.writerow(
                [
                    trade.get("base"),
                    trade.get("client_order_id"),
                    trade.get("counter"),
                    trade.get("fee_base"),
                    trade.get("fee_counter"),
                    trade.get("is_buy"),
                    trade.get("order_id"),
                    trade.get("pair"),
                    trade.get("price"),
                    trade.get("sequence"),
                    trade.get("timestamp"),
                    trade.get("type"),
                    trade.get("volume"),
                ]
            )


def fetch_trades():
    tokens = parse_tokens(os.getenv("TOKENS"))
    currency = os.getenv("CURRENCY")
    start_date = parse_date_to_timestamp(os.getenv("START_DATE"))
    end_date = parse_date_to_timestamp(os.getenv("END_DATE"))
    current_time = int(datetime.now().timestamp())

    # Format parameters for API call
    for token in tokens:
        # break down requests to weekly
        start_date_copy = start_date
        while start_date_copy < end_date:
            end_date_weekly = min(start_date_copy + (604800 * 1000), end_date)
            historical_trades = request_trades(
                token, currency, start_date_copy, end_date_weekly
            )
            append_to_csv(historical_trades, f"luno_trades_{current_time}.csv")
            start_date_copy = end_date_weekly + 1


# Usage
if __name__ == "__main__":
    load_env_file(".env")
    fetch_trades()