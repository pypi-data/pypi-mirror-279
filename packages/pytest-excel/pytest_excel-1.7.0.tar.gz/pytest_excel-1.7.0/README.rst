pytest-excel
================


pytest-excel is a plugin for `py.test <http://pytest.org>`_ that allows to 
to create excel report for test results.


Requirements
------------

You will need the following prerequisites in order to use pytest-excel:

- Python 3.9, 3.10, 3.11 and 3.12
- pytest 
- pandas


Installation
------------

To install pytest-excel::

    $�pip install pytest-excel

Then run your tests with::

    $ py.test --excelreport=report.xls

If you would like more detailed output (one test per line), then you may use the verbose option::

    $ py.test --verbose

If you would like to run tests without execution to collect test doc string::

    $ py.test --excelreport=report.xls --collect-only


If you would like to get timestamp in the as filename::

    $ py.test --excelreport=report%Y-%M-dT%H%.xls
