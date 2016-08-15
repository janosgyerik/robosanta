`_fetch_sede_soup` is doing too much, try to decompose:

- fetch url
- create bs4 object
- cache content if bs4 contains result sets

Track the order of arguments (like `--naruto`, `--ripe-zombie`, `--message`) and post in that order.
See: http://stackoverflow.com/questions/9027028/argparse-argument-order
