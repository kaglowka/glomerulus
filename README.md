# glomerulus

### application entry points
#### in src/main.py

```python
from glomerulus.search.search import get_links_for_keywords

get_links_for_keywords('dzieci papierosy')
```

#### spider
```
scrapy runspider links_spider.py
```

Save to json:
```
scrapy runspider links_spider.py -o <json file>
```

