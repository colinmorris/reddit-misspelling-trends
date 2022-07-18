import os
import datetime
import requests
import json
import time
from collections import namedtuple

from helpers import *

def counts_for_range(pattern, start, end):
    url = format_url(pattern, start, end, limit=0, metadata='true')
    debug(url)
    response = requests.get(url, headers={'User-Agent': "script by /u/halfeatenscone"})
    dat = response.json()
    count = dat['metadata']['total_results']
    return count

def annual_counts(pattern, startyear=2011, endyear=2022):
    assert startyear <= endyear
    year = startyear
    counts = {}
    while year <= endyear:
        start = datetime.datetime(year, 1, 1)
        end = datetime.datetime(year+1, 1, 1)
        n = counts_for_range(pattern, start, end)
        time.sleep(1)
        counts[year] = n
        year += 1
    return counts

def monthly_counts(pattern, year):
    month = 1
    counts = []
    while month <= 12:
        start = datetime.datetime(year, month, 1)
        if month == 12:
            end = datetime.datetime(year+1, 1, 1)
        else:
            end = datetime.datetime(year, month+1, 1)
        n = counts_for_range(pattern, start, end)
        time.sleep(1)
        counts.append(n)
        month += 1
    return counts

def daily_counts(pattern, year, month):
    day = datetime.datetime(year, month, 1)
    daydelta = datetime.timedelta(days=1)
    counts = []
    while day.month == month:
        end = day + daydelta
        n = counts_for_range(pattern, day, end)
        time.sleep(1)
        counts.append(n)
        day += daydelta
    return counts

DATA_DIR = 'data'
def download_counts_for_cluster(cluster):
    fname = cluster.main.replace(' ', '_') + '.json'
    outpath = os.path.join(DATA_DIR, fname)
    if os.path.exists(outpath):
        debug(f"Skipping extant cluster {cluster.main}")
        return
    res = []
    maincounts = annual_counts(cluster.main)
    datum = {'pattern': cluster.main, 'type': 'main',
            'counts': maincounts,
    }
    res.append(datum)
    for alt in cluster.alts:
        counts = annual_counts(alt)
        datum = {'pattern': alt, 'type': 'alt',
                'counts': counts,
        }
        res.append(datum)
    with open(outpath, 'w') as f:
        json.dump(res, f, indent=2)

Cluster = namedtuple('Cluster', ['main', 'alts'])

def load_clusters():
    cs = []
    with open('clusters.txt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            tokens = line.strip().split(',')
            c = Cluster(tokens[0], tokens[1:])
            cs.append(c)
    return cs

def trawl_clusters():
    clusters = load_clusters()
    for clus in clusters:
        debug(clus)
        download_counts_for_cluster(clus)

if __name__ == '__main__':
    trawl_clusters()
    if 0:
        counts = monthly_counts('neccessary', 2020)
        with open('reddit_monthly_neccessary.txt', 'w') as f:
            out = '\n'.join([str(c) for c in counts])
            f.write(out)
    elif 0:
        counts = daily_counts('neccessary', 2020, 5)
        with open('reddit_may_daily_neccessary.txt', 'w') as f:
            out = '\n'.join([str(c) for c in counts])
            f.write(out)
