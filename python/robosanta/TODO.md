`_fetch_sede_soup` is doing too much, try to decompose:
 - fetch url
 - create bs4 object
 - cache content if bs4 contains result sets
 
