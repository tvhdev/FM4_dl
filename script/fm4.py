#!/usr/bin/env python

#Alexander Kutschera, 2018-09-02
#The original script was written by Christoph Glaubitz (https://chrigl.de/, Download: https://chrigl.de/~chris/fm4/)
#Changes are commented

import sys
import simplejson
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
import time

streams = [
    ('4CH', 'Charts'),
    ('4CZ', 'Chez Hermez'),
    ('4DD', 'Davi Decks'),
    ('4DKM', 'Digital Konfusion'),
    ('4DLL', 'Dalia\'s Late Night Lemonade'),
    ('4FP', 'Film Podcast'),
    ('4GL', 'Graue Lagune'),
    ('4GP', 'Worldwide Show'),
    ('4GPC', 'Game Podcast'),
    ('4HE', 'Heartbeat'),
    ('4HF', 'Hallo FM4'),
    ('4HH', 'Happy Hour'),
    ('4HS', 'High Spirits'),
    ('4HOP', 'House Of Pain'),
    ('4IS', 'Im Sumpf'),
    ('4LB', 'La Boum de Luxe'),
    ('4LL', 'Lieblingslieder'),
    ('4LR', 'Liquid Radio'),
    ('4MGMon', 'Morgengrauen (Monday)'),
    ('4MGTue', 'Morgengrauen (Tuesday)'),
    ('4MGWed', 'Morgengrauen (Wednesday)'),
    ('4MGThu', 'Morgengrauen (Thursday)'),
    ('4MGFri', 'Morgengrauen (Friday)'),
    ('4MOMon', 'Morning Show (Monday)'),
    ('4MOTue', 'Morning Show (Tuesday)'),
    ('4MOWed', 'Morning Show (Wednesday)'),
    ('4MOThu', 'Morning Show (Thursday)'),
    ('4MOFri', 'Morning Show (Friday)'),
    ('4MOSat', 'Morning Show (Saturday)'),
    ('4MOSun', 'Morning Show (Sunday)'),
    ('4MPC', 'Musik Podcast'),
    ('4OKMon', 'OKFM4 (Monday)'),
    ('4OKTue', 'OKFM4 (Tuesday)'),
    ('4OKWed', 'OKFM4 (Wednesday)'),
    ('4OKThu', 'OKFM4 (Thursday)'),
    ('4OKFri', 'OKFM4 (Friday)'),
    ('4PH', 'Fivas Ponyhof'),
    ('4PSMon', 'Passt Show (Monday)'),
    ('4PSTue', 'Passt Show (Tuesday)'),
    ('4PSWed', 'Passt Show (Wednesday)'),
    ('4PSThu', 'Passt Show (Thursday)'),
    ('4PSFri', 'Passt Show (Friday)'),
    ('4PX', 'Project X'),
    ('4SPSun', 'Soundpark'),
    ('4SS', 'Swound Sound'),
    ('4SSUSun', 'Sunny Side Up'),
    ('4TV', 'Tribe Vibes'),
    ('4UL', 'Unlimited'),
    ('4ZS', 'Zimmerservice'),
    ]

try:
    if sys.hexversion >= 50331648:
        from urllib.request import urlopen
    else:
        from urllib2 import urlopen
except ImportError:
    print("Unable to run this script. urlopen not available.")

def search_in_json(stream, all_shows=False): # changed function to look for multiple show streams
    """ from audioapi.orf.at. Have a look into https://fm4.orf.at/radio/stories/fm4houseofpain """
    # no exception handling because I want to know if it does not work
    #now_s = datetime.now().strftime('%s')+'000' does not work on windows
    now_s = str(int(time.time()))+'000'
    f = urlopen('https://audioapi.orf.at/fm4/json/2.0/playlist/%s?callback=&_=%s' % (stream, now_s))
    json_s = f.read()
    f.close()
    res = simplejson.loads(json_s)
    # JSON structure changed (e.g. https://audioapi.orf.at/fm4/json/2.0/playlist/4LB). The list contains
    # one entry per broadcast day, going back up to 4 weeks. The "last" entry is always the most recent one.
    broadcasts = res if all_shows else [res[len(res)-1]]

    # entries: list of (date, part_index, total_parts, url) tuples, one per stream/part
    entries = list()
    for broadcast in broadcasts:
        parts = broadcast['streams'] #check num of streams in the json
        for idx, part in enumerate(parts, start=1):
            loop_stream_id = part['loopStreamId']
            date = loop_stream_id.split('_')[0]
            url = 'https://loopstream01.apa.at/?channel=fm4&ua=flash&id=%s' % loop_stream_id
            entries.append((date, idx, len(parts), url))
    return entries

def show_list():
    """ just guessed """
    for s in streams:
        print('%s - %s'% s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get fm4 stream url')
    parser.add_argument('--stream', '-s', default='4HOP', help='name of stream, e.g. 4HOP (House Of Pain) 4UL (Unlimited of the last Friday)')
    parser.add_argument('--list', '-l', action='store_true', help='list all available show tags and exit')
    parser.add_argument('--all', '-a', action='store_true', help='list all available broadcasts (up to 4 weeks back) instead of just the latest one')
    args = parser.parse_args()
    if args.list:
        show_list()
        sys.exit(0)
    entries = search_in_json(args.stream, args.all)
    if args.all:
        # one line per stream/part: "<date> <part_index> <total_parts> <url>"
        for date, idx, total, url in entries:
            print('%s %d %d %s' % (date, idx, total, url))
    elif entries:
        if len(entries) == 1:
            print(entries[0][3])
        else:
            print([e[3] for e in entries])
