# yamlead

Yamlead contains decorator functions which enable common csv reader/writer functions to read/write commented yaml headers before the file content.

```python
import pandas as pd
import yamlead

reader = yamlead.reader(pd.read_csv, comment_char='#')
writer = yamlead.writer('to_csv', comment_char='#')

header = {'author: 'authorname', 'items': ['item1', 'item2']}
content = pd.DataFrame({'a': [1, 4, 7], 'b': [2, 5, 8]})

writer(header, content, 'temp.csv')
header, content = reader('temp.csv')
```

The arguments for `reader` are identical to `pd.read_csv`.
The arguments for `writer` are prepended with `header` and `content` compared to the `content.to_csv('temp.csv')`.
