import json


def extract_column(soup, colname):
    """
    Returns a generator of cell values in selected column.

    For simple columns like timestamp, a cell value can be simple,
    for example: 1414433013197

    For more complex columns like Post Link, a cell value can be an object,
    for example:

      {
        "id": 68102,
        "title": "Bash Script - File Comment out & Notate"
      }

    :param soup: a bs4 (BeautifulSoup) object
    :param colname: name of the SEDE column to extract
    :return: generator of cell values in selected column
    """
    def get_column_index():
        for index, info in enumerate(columns):
            if info['name'] == colname:
                return index
        return -1

    for script in soup.findAll('script'):
        result_sets_col = 'resultSets'
        if result_sets_col in script.text:
            start = script.text.rindex('{', 0, script.text.index(result_sets_col))
            end = script.text.index('}', script.text.index('querySetId')) + 1
            data = json.loads(script.text[start:end])

            results = data[result_sets_col][0]
            columns = results['columns']
            rows = results['rows']

            column_index = get_column_index()
            if column_index > -1:
                for row in rows:
                    yield row[column_index]
