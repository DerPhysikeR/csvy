# csvy

Csvy contains decorator functions which enable common csv reader/writer functions to read/write commented yaml headers before the file content.

```python
import pandas as pd
import csvy

read_csvy = csv.reader(pd.read_csv, comment_char='#')
write_csvy = csv.writer('to_csv', comment_char='#')

header = {'author: 'authorname', 'items': ['item1', 'item2']}
content = pd.DataFrame({'a': [1, 4, 7], 'b': [2, 5, 8]})

write_csvy(header, content, 'temp.csv')
header, content = read_csvy('temp.csv')
```

The arguments for `read_csvy` are identical to `pd.read_csv`.
The arguments for `write_csvy` are prepended with `header` and `content` compared to the `content.to_csv('temp.csv')`.
