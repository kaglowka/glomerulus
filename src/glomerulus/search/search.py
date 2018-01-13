from glomerulus.io import FileStorage
from glomerulus.search.pws_clone import Google
from glomerulus.config import LINKS_PATH

def get_links_for_keywords(query, num=10, file=LINKS_PATH):
    # omit the first result (it is not a result link)
    results = Google.search(query=query, num=num, start=1, country_code="pl")

    if results['received_num'] == 0:
        raise RuntimeError('Parsed no links from Google search results')

    links = [result['link'] for result in results['results']]

    FileStorage().save_data(
        LINKS_PATH,
        '\n'.join(links),
    )