Installation
============

Install via pip
---------------

Install PyRice package (the newest version) with :command:`pip`::

    $ pip install pyrice


To choose older version of Pyrice package using :command:`pip`::

    $ pip install pyrice==0.2.0


Now there are 2 versions available (should use the latest version):
    - Version 0.2.0: Update reference for gene from Oryzabase. Add 2 new databases PlantTFDB for PyRice
        - If you install PyRice on your local machine, please follow these steps:

            + Please check carefully the current version of Chrome on your computer before downloading
            + Download the `Chrome driver <https://chromedriver.chromium.org/downloads>`_

            + After downloading, fill the file path lead to Chrome driver before querying::

                >>> from pyrice import utils
                >>> utils.chrome_path = "the path of your Chrome driver"


    - Version 0.1.9: PyRice on Google Colab or other cloud platform. Updating the change output format.

    - Version 0.1.8: Addition of crawling JavaScript data with Selenium.

    - Version 0.1.5: Crawl data without Selenium (unsupported).

    **IN PROCESS**: If you want to install the newest demo of PyRice using :command:`pip`::

    $ pip install -i https://test.pypi.org/simple/ pyrice

Install via Github
------------------

Clone project on PyRice (the newest version) with :command:`git`::

  $ git clone https://github.com/SouthGreenPlatform/PyRice.git

To choose older version of Pyrice package, choose release pyrice-0.1.8:

Download package
----------------

Download and extract the `compressed archive from PyPI`_.

.. _compressed archive from PyPI: https://pypi.org/project/pyrice/

