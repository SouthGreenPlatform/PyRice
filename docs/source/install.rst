Installation
============

Install via pip
---------------

Install PyRice package (the newest version) with :command:`pip`::

    $ pip install pyrice


To choose older version of Pyrice package using :command:`pip`::

    $ pip install pyrice==0.1.5


Now there are 2 versions available:

    - Version 0.1.7: Addition of crawling JavaScript data with Selenium.

        - If you want to use Selenium, please follow these steps

            + Please check carefully the current version of Chrome on your computer before downloading
            + Download the `Chrome driver <https://chromedriver.chromium.org/downloads>`_

            + After downloading, fill the file path lead to Chrome driver before querying::

                >>> from pyrice import utils
                >>> utils.chrome_path = "the path of your Chrome driver"
    - Version 0.1.5: Crawl data without Selenium.

Install via Github
------------------

Clone project on PyRice (the newest version) with :command:`git`::

  $ git clone https://github.com/SouthGreenPlatform/PyRice.git

To choose older version of Pyrice package, choose release pyrice-0.1.5:

Download package
----------------

Download and extract the `compressed archive from PyPI`_.

.. _compressed archive from PyPI: https://pypi.org/project/pyrice/

