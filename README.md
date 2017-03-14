# Yamlead

Yamlead contains decorator functions which enable common csv reader/writer functions to read/write commented yaml headers before the file content.

```python
import pandas as pd
import yamlead

reader = yamlead.reader(pd.read_csv, comment_char='#')
writer = yamlead.writer('to_csv', comment_char='#')

header = {'author': 'authorname', 'items': ['item1', 'item2']}
content = pd.DataFrame({'a': [1, 4, 7], 'b': [2, 5, 8]})

writer(header, content, 'temp.csv')
header, content = reader('temp.csv')
```

The created `temp.csv` file looks like this:

```
#author: authorname
#items: [item1, item2]
,a,b
0,1,2
1,4,5
2,7,8
```

The usage of `reader` is now identical to `pd.read_csv` with the only difference, that it returns a tuple containing the yaml file header as the first element and the actual file content as the second element. 
The arguments of `writer` are similarly almost identical to `content.to_csv()`, with only the `header` and the `content` being prepended to its arguments.
