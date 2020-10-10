# pyPremiumSIM
[![Build Status](https://travis-ci.org/skhg/pypremiumsim.svg?branch=main)](https://travis-ci.org/skhg/pypremiumsim) [![PyPI](https://img.shields.io/pypi/v/pypremiumsim.svg)](https://pypi.python.org/pypi/pypremiumsim/) [![Codecov](https://img.shields.io/codecov/c/github/skhg/pypremiumsim.svg)](https://codecov.io/gh/skhg/pypremiumsim)

A Python API for accessing your [PremiumSIM.de](https://www.premiumsim.de/) account balance &amp; usage stats. This is an unoffical API and the author/contributors are in no way connected to PremiumSIM or Drillisch. The API provides a method to:
* Get your current month's data balances (consumed and remaining GB)

## Installation
`pip install pypremiumsim`

## Usage
It's very easy to use. Try the following to get your balance data:
```python
from pypremiumsim import *
from pprint import pprint

session = pypremiumsim.PremiumSimSession()
session.try_login("<username>", "<password>")
data_used = session.current_month_data_usage()

pprint(vars(data_used))
```
returns:
```python
{'consumed_data_gb': 0.735859375,
 'tariff_total_data_gb': 20.0,
 'used_percentage': 3.7}
 ```
 
 ## Tests
 `python ./tests/tests.py`
 
 ## Contributing
 Fork this repo, make some changes and create a new pull request!
