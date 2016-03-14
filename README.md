# Collector Test #

## Installation ##

pip install .

## Usage ##

First fetch some random articles:

    collector_test -f 50

This fetch 50 times 100 articles

Build books and upload to pediapress:

    collector_test -m 100

The above commands builds 100 books.

Multiple browser instances can be launched at the same time:

    collector_test -m 100 -n 2

Complete list of command line switches:

    collector_test -h




# Authors #
* Volker Haas <volker.haas@pediapress.com>
