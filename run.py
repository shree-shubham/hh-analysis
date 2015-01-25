#!/usr/bin/env python3

import argparse
from collections import defaultdict
from github import Github
import urllib.request
import os
import re
import sys
import wikipedia

def get_location(gh,github_url):
    r = re.search("github.com/(\S*)",github_url)
    if r:
        username = r.group(1)
        try:
            loc = gh.get_user(username).location
            if loc:
                return loc
        except Exception as e:
            pass
    return ""

def get_lat_long(location):
    if location:
        wiki_search = wikipedia.search(location)
        if len(wiki_search) > 0:
            try:
                term = wiki_search[0]
                if term == "United States":
                    # http://en.wikipedia.org/wiki/Geographic_center_of_the_contiguous_United_States
                    return (39.828127,-98.579404)
                else:
                    wiki_page = wikipedia.page(wiki_search[0])
                    return wiki_page.coordinates
            except Exception as e:
                pass
    return ("","")

def get_data(gh,url,websites_data,github_data):
    websites_key="Hackathon Hackers' Personal Websites"
    github_key="Hackathon Hackers' GitHub profiles"

    f = urllib.request.urlopen(url)
    contents = f.read().decode().split("\n")

    line_before = None
    data = defaultdict(list)
    for line in contents:
        line = line.strip()
        if re.search('^==*$',line):
            header = line_before
            continue
        r = re.search("- (.*) (http\S*)",line)
        if r:
            assert(header)
            name = r.group(1)
            url = r.group(2)
            location = get_location(gh,url)
            lat, lon = get_lat_long(location)
            print(name,url,location,lat,lon)
            if header == websites_key:
                data[header].append((name,url))
            elif header == github_key:
                data[header].append((name,url,location,lat,lon))
            else:
                raise Exception("Unrecognized header: {}".format(header))
        line_before = line

    with open(websites_data,"w") as f:
        f.write("name\turl\n")
        for name,url in data[websites_key]:
            f.write("{}\t{}\n".format(name,url))
    with open(github_data,"w") as f:
        f.write("name\turl\tlocation\tlat\tlong\n")
        for name,url,loc,lat,lon in data[github_key]:
            f.write("{}\t{}\t{}\t{}\t{}\n".format(name,url,loc,lat,lon))
    print("+ Archived {} websites and {} GitHub profiles.".format(
        len(data[websites_key]),len(data[github_key])))

if __name__=='__main__':
    url='https://raw.githubusercontent.com/HackathonHackers/hh-personal-sites/master/README.md'
    websites_data = "websites.tsv"
    github_data = "github.tsv"

    parser = argparse.ArgumentParser()
    parser.add_argument('--get_data',action='store_true')
    parser.add_argument('--output_map',action='store_true')
    parser.add_argument('--generate_readme',action='store_true')

    args = parser.parse_args()
    gh = Github('bamos',os.environ['GITHUB_TOKEN'])

    if args.get_data:
        get_data(gh,url,websites_data,github_data)
    if args.output_map:
        p = Popen(["./plot.r"])
        p.communicate()
    if args.generate_readme:
