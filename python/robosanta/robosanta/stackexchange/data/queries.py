import json


def get_column(soup, name):
    def get_column_index():
        for index, info in enumerate(columns):
            if info['name'] == name:
                return index
        return -1

    for script in soup.findAll('script'):
        if 'resultSets' in script.text:
            start = script.text.rindex('{', 0, script.text.index('resultSets'))
            end = script.text.index('}', script.text.index('querySetId')) + 1
            data = json.loads(script.text[start:end])
            results = data['resultSets'][0]
            columns = results['columns']
            rows = results['rows']

            column_index = get_column_index()

            if column_index > -1:
                for row in rows:
                    yield row[column_index]
