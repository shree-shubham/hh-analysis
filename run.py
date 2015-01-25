#!/usr/bin/env python3

import argparse
from collections import Counter,defaultdict
import datetime
from github import Github
from jinja2 import Environment,FileSystemLoader
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

def analyze(github_data):
    data = []
    with open(github_data,"r") as f:
        headers = f.readline().strip().split("\t")
        for line in f.readlines():
            line=line.strip()
            data.append(dict(zip(headers,line.split("\t"))))

    analysis = {'github_count': len(data)}
    location_data = [x['location'] for x in data if 'location' in x]
    analysis["top_locations"] = Counter(location_data).most_common()

    first_names = [x['name'].split(" ")[0] for x in data if 'name' in x]
    analysis["top_first_names"] = Counter(first_names).most_common()

    return analysis

if __name__=='__main__':
    url='https://raw.githubusercontent.com/HackathonHackers/hh-personal-sites/master/README.md'
    websites_data = "data/websites.tsv"
    github_data = "data/github.tsv"

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
        env = Environment(loader=FileSystemLoader("."))

        analysis = analyze(github_data)

        with open("README.md","w") as f:
            f.write(env.get_template("README.jinja.md").render(
                date=datetime.date.today().strftime("%B %d, %Y"),
                analysis=analysis
            ))
