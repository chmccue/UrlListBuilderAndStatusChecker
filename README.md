# UrlListBuilderAndStatusChecker

Python 2.7

I built these files to serve the following purpose in the following order:
* GSpreadListBuilder: Automatically connect to a google spreadsheet.
* GSpreadListBuilder: Get all relevant data from the google spreadsheet. In this case, Urls.
* GSpreadListBuilder: Compile that relevant data into a list.
* UrlStatusChecker: Take the compiled list and iterate through each list item.
* UrlStatusChecker: During iteration of the compiled list, asserting status codes and other assertion types via the response data.
* UrlStatusChecker: After the tests, displaying the failed responses in dictionary format.


Even briefer descriptions:
* GSpreadListBuilder: class for connecting and scraping a google spreadsheet and storing Urls in list format.
* UrlStatusChecker: class for taking a list of Urls and sending get requests via Python's Requests library, and then 
asserting the response data with specified validations.
* DictionaryUpdating: class that merges dictionaries together. No longer needed for the other 2 class instances to 
work together, but may be useful in the future.


Most of the class file methods have extensive documentation in them, so understanding the methods and what they do
is better suited to review the files and their Docstrings.
