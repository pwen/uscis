from collections import defaultdict
import logging
import json
import click
from datetime import datetime

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

logger = logging.getLogger(__name__)

EMPLOYMENT_BASED_CATEGORY_IDX = {
    '1st': 1,
    '2nd': 2,
    '3rd': 3,
    'other workers': 4,
    '4th': 5,
}

COUNTRY_IDX = {
    "mainland_china": 2,
}

def query_per_month(year: str, month: str):
    month = month.lower()
    logger.info(f"query {year}, {month}")

    page_url = f"https://travel.state.gov/content/travel/en/legal/visa-law0/visa-bulletin/{year}/visa-bulletin-for-{month}-{year}.html"
    res = requests.get(page_url)

    tables = bs(res.content, 'html.parser').findAll('table')

    for table in tables:
        rows = table.findAll('tr')
        data = []
        for row in rows:
            cols = row.findAll('td')
            data.append(cols)
        header = data[0]
        try:
            if header[0].text.lower().find('employment') >=0 and header[0].text.lower().find('based') >=0:
                country_idx = COUNTRY_IDX["mainland_china"]
                return {
                    '2nd': data[EMPLOYMENT_BASED_CATEGORY_IDX['2nd']][country_idx].text.strip(),
                    '3rd': data[EMPLOYMENT_BASED_CATEGORY_IDX['3rd']][country_idx].text.strip(),
                }
        except:
            pass


@click.command()
@click.option('--latest', default="y", show_default=True, help='Show most recent visa bulletin')
@click.option('--category', default="3rd", show_default=True, help='Employment-based category')
def main(latest, category):
    def _tuple(d):
        return tuple(d.split('-'))

    if category not in EMPLOYMENT_BASED_CATEGORY_IDX.keys():
        raise ValueError(f"Invalid category: {category}; must be one of {EMPLOYMENT_BASED_CATEGORY_IDX.keys()}")

    if latest.lower() == "y":
        now = datetime.now()
        result = query_per_month(month=now.strftime("%B"), year=str(now.year))
        print(result[category])
    else:
        dates = list(map(_tuple, pd.date_range('2020-01-01','2020-07-01', freq='MS').strftime("%Y-%B")))
        results = defaultdict(lambda: defaultdict(dict))
        for y, m in dates:
            results[y][m] = query_per_month(year=y, month=m)

        print(json.dumps(results, sort_keys=True, indent=4))

if __name__=="__main__":
    main()
