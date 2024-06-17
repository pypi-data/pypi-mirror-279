# bnrxrate

Python3 utility for easily accessing and parsing XML documents containing the exchange rates published by BNR (Romanian National Bank / Banca Națională a României) on their website.

## Features

- Fetch XML documents from https://www.bnr.ro with simple function calls.
- Parse XML into a Pythonic format (a dict).
- Cache retrieved data in an object property (a dict).

## Installation
`pip install bnrxrate`

## Usage

```
from bnrxrate import Xrates

bnrxr = Xrates()

# Get the listed exchange rates for all symbols for today:
bnrxr.get_xrate()

# Get the exchange rate for EUR and USD for today:
bnrxr.get_xrate(['EUR', 'USD'])

# Get the exchange rate for EUR and USD for specific date:
date = datetime.date(2024, 2, 22)
bnrxr.get_xrate(['EUR', 'USD'], date)

# Get the symbols available at a specific date:
date = datetime.date(2024, 6, 1)
bnrxr.list_symbols(date)

# Get the exchange rates for all symbols in a specific period:
start_date = datetime.date(2024, 1, 1)
end_date = datetime.date.today()
all_xrates = bnrxr.get_xrate([], start_date, end_date)

# Get the exchange rates for specific symbols in a specific period:
start_date = datetime.date(2024, 1, 1)
end_date = datetime.date.today()
all_xrates = bnrxr.get_xrate(['EUR', 'usd'], start_date, end_date)

# Check if a specific date is a banking day:
date = datetime.date(2024, 4, 1)
bnrxr.is_banking_day(date)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.