from collections import Counter
import csv
from datetime import datetime
import json
import progressbar
import requests
import statistics
import time

ITERATIONS = 10

def main():
    test_urls = [
        "https://iatidatastore.iatistandard.org/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=10",
        "https://iatidatastore.iatistandard.org/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=10",
        "https://iatidatastore.iatistandard.org/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=100",
        "https://iatidatastore.iatistandard.org/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=100",
        "https://iatidatastore.iatistandard.org/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=1000",
        "https://iatidatastore.iatistandard.org/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=1000",
        "https://iatidatastore.iatistandard.org/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=10000",
        "https://iatidatastore.iatistandard.org/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=10000",
        "https://iatidatastore.iatistandard.org/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=100000",
        "https://iatidatastore.iatistandard.org/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=100000",
        "https://iatidatastore.iatistandard.org/search/transaction?q=((transaction_recipient_country_code:(NG)%20OR%20activity_recipient_country_code:(NG))%20AND%20transaction_date_iso_date:[2015-12-31T00:00:00Z%20TO%20*])&wt=csv&tr=transaction-csv.xsl&rows=1000000",
        "https://iatidatastore.iatistandard.org/search/activity?q=recipient_country_code:(NG)&wt=xslt&tr=activity-csv.xsl&rows=1000000",
    ]
    fieldnames = ['url', 'response_codes', 'response_time_avg', 'response_time_min', 'response_time_max']
    filename = "output_{}.csv".format(datetime.now().strftime("%Y_%m_%d"))

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for test_url in test_urls:
            print(test_url)
            bar = progressbar.ProgressBar()
            response_codes = list()
            response_times = list()
            for _ in bar(range(0, ITERATIONS)):
                response = requests.get(test_url)
                response_codes.append(response.status_code)
                response_times.append(response.elapsed.total_seconds())
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
