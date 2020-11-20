from collections import Counter
import csv
from datetime import datetime
import json
import progressbar
import requests
import statistics
import time

ITERATIONS = 10
# PREFIX = "live"
# MAIN_URL = "https://iatidatastore.iatistandard.org"
PREFIX = "staging"
MAIN_URL = "https://test-xslt.iati.cloud"

def main():
    test_urls = [
        "/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=10",
        "/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=10",
        "/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=100",
        "/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=100",
        "/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=1000",
        "/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=1000",
        "/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=10000",
        "/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=10000",
        "/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=100000",
        "/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=100000",
        "/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=1000000",
        "/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=1000000",
    ]
    fieldnames = ['url', 'response_codes', 'response_time_avg', 'response_time_min', 'response_time_max']
    filename = "{}_output_{}.csv".format(PREFIX, datetime.now().strftime("%Y_%m_%d"))

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for test_url in test_urls:
            print(test_url)
            bar = progressbar.ProgressBar()
            response_codes = list()
            response_times = list()
            for _ in bar(range(0, ITERATIONS)):
                start_time = datetime.now()
                try:
                    response = requests.get(MAIN_URL + test_url)
                except:
                    continue
                end_time = datetime.now()
                time_diff = end_time - start_time
                response_codes.append(response.status_code)
                response_times.append(time_diff.total_seconds())
                time.sleep(1)

            writer.writerow(
                {
                    'url': test_url,
                    'response_codes': json.dumps(Counter(response_codes)),
                    'response_time_avg': statistics.mean(response_times),
                    'response_time_min': min(response_times),
                    'response_time_max': max(response_times)
                }
            )

if __name__ == '__main__':
    main()
