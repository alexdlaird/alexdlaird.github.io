---
title: "amazon-orders for Python"
date: 2024-01-31
tags: 
  - "amazon"
  - "python"
  - "education"
coverImage: "Screenshot-2024-03-03-at-7.22.55 PM.png"
---

[![amazon-orders - A Python libray (and CLI) for Amazon order history](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Famazon-orders.readthedocs.io%2F_images%2Flogo.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Famazon-orders.readthedocs.io%2F_images%2Flogo.png)

`amazon-orders` is an unofficial library that provides a Python API (and CLI) for Amazon order history.

This package works by parsing data from Amazon's consumer-facing website. A periodic build validates functionality to ensure its stability, but as Amazon provides no official API to use, this package may break at any time. Pin the [minor version](https://semver.org/) with a wildcard (ex. `==4.0.*`, not `==4.0.7`)—or reinstall with the `--upgrade` (as shown below) often—to ensure you always get the latest stable release.

This package only officially supports the English, `.com` version of Amazon.

## [](https://dev.to/alexdlaird/amazon-orders-python-library-2cnj#installation)Installation

`amazon-orders` is available on [PyPI](https://pypi.org/project/amazon-orders/) and can be installed using `pip`:

```bash
pip install amazon-orders --upgrade
```

That's it! `amazon-orders` is now available as a package to your Python projects and from the command line.

## [](https://dev.to/alexdlaird/amazon-orders-python-library-2cnj#basic-usage)Basic Usage

You'll use [`AmazonSession`](https://amazon-orders.readthedocs.io/api.html#amazonorders.session.AmazonSession) to authenticate your Amazon account, then [`AmazonOrders`](https://amazon-orders.readthedocs.io/api.html#amazonorders.orders.AmazonOrders) and [`AmazonTransactions`](https://amazon-orders.readthedocs.io/api.html#amazonorders.transactions.AmazonTransactions) to interact with account data. [`get_order_history`](https://amazon-orders.readthedocs.io/api.html#amazonorders.orders.AmazonOrders.get_order_history) and [`get_order`](https://amazon-orders.readthedocs.io/api.html#amazonorders.orders.AmazonOrders.get_order) are good places to start.

```python
from amazonorders.session import AmazonSession
from amazonorders.orders import AmazonOrders

amazon_session = AmazonSession("<AMAZON_EMAIL>",
                               "<AMAZON_PASSWORD>")
amazon_session.login()

amazon_orders = AmazonOrders(amazon_session)
orders = amazon_orders.get_order_history(year=2023)

for order in orders:
    print(f"{order.order_number} - {order.grand_total}")
```

If the fields you're looking for aren't populated with the above, set `full_details=True` (or pass `--full-details` to the `history` CLI command), since by default it is `False` (enabling it slows down querying, since an additional request for each order is necessary). Have a look at the [Order](https://amazon-orders.readthedocs.io/api.html#amazonorders.entity.order.Order) entity's docs to see what fields are only populated with full details.

### [](https://dev.to/alexdlaird/amazon-orders-python-library-2cnj#command-line-usage)Command Line Usage

You can also run any command available to the main Python interface from the command line:

```bash
amazon-orders login
amazon-orders history --year 2023
```

### [](https://dev.to/alexdlaird/amazon-orders-python-library-2cnj#automating-authentication)Automating Authentication

Authentication can be automated by (in order of precedence) storing credentials in environment variables, passing them to [`AmazonSession`](https://amazon-orders.readthedocs.io/api.html#amazonorders.session.AmazonSession), or storing them in [`AmazonOrdersConfig`](https://amazon-orders.readthedocs.io/api.html#amazonorders.conf.AmazonOrdersConfig). The environment variables `amazon-orders` looks for are:

- `AMAZON_USERNAME`

- `AMAZON_PASSWORD`

- `AMAZON_OTP_SECRET_KEY` (see [docs for usage](https://amazon-orders.readthedocs.io/api.html#amazonorders.session.AmazonSession.otp_secret_key))

## [](https://dev.to/alexdlaird/amazon-orders-python-library-2cnj#documentation)Documentation

For more advanced usage, `amazon-orders`'s official documentation is available at [http://amazon-orders.readthedocs.io](http://amazon-orders.readthedocs.io/).

## [](https://dev.to/alexdlaird/amazon-orders-python-library-2cnj#contributing)Contributing

If you would like to get involved, be sure to review the [Contribution Guide](https://github.com/alexdlaird/amazon-orders/blob/main/CONTRIBUTING.rst).

Want to contribute financially? If you've found `amazon-orders` useful, [sponsorship](https://github.com/sponsors/alexdlaird) would also be greatly appreciated!
