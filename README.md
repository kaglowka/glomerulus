# glomerulus

### install requirements
```
pip install -r requirements.txt
```

### application entry points
#### in src/main.py

```python
from glomerulus.search.search import get_links_for_keywords

get_links_for_keywords('dzieci papierosy')
```
or 
```
python main.py
```
then find and replace '&sa=.*' with '' in data/links.txt
and delete all lines not starting with 'http'
#### spider
```
scrapy runspider links_spider.py
```
or
```
python scrapy_run.py
```

#### Save to json:
```
scrapy runspider links_spider.py -o <json file>
```

