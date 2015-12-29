`_fetch_sede_soup` is doing too much, try to decompose:
 - fetch url
 - create bs4 object
 - cache content if bs4 contains result sets

the label parameter of `fetch_table(label, url)` is an implementation detail
- should eliminate it
- use the last path segment of the url instead
  + possibly rename some SEDE to match the current simplified names,
    for example "naruto" instead of "naruto-accepted-answer-with-zero-score"
