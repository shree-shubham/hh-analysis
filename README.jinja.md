# HH Analysis

This repository generates TSV and a simple analysis of the
GitHub user data from
[HackathonHackers/hh-personal-sites](https://github.com/HackathonHackers/hh-personal-sites).
Add your data there to be included in this repo,
and file an issue or email me to be excluded from this repo.

The README is parsed with Python and the coordinates for the map
are obtained by searching for a user's GitHub location string
in Wikipedia.

The following information was generated on {{ date }}
from {{ analysis["github_count"] }} GitHub users.

# World Map
The following world map with binned locations is generated with
Following is a binned heatmap of locations, generated with
[R](http://r-project.org), [ggplot](http://ggplot2.org),
and [ggmap](http://cran.r-project.org/web/packages/ggmap/ggmap.pdf).
A location string of 'United States' is set to the geographic center.

![](https://raw.githubusercontent.com/bamos/hh-github-analysis/master/plots/map.png)

# Analysis
## Top Locations

The following are the top location strings and frequencies.
This uses the raw location string and can be improved
by intelligently parsing locations.

{% for location, freq in analysis["top_locations"][0:10] %}
  + {{ location }}: {{ freq }}
{%- endfor %}

## Top First Names

{% for name, freq in analysis["top_first_names"][0:10] %}
  + {{ name }}: {{ freq }}
{%- endfor %}

# Instructions for running in Linux

+ Install Python 3 with packages `PyGithub`, `jinja2`, and `wikipedia`.
+ Install R with packages `ggplot2` and `ggmap`.
+ Modify the `Github` object in `run.py` to have your Github
  API username and access token.
+ Run `./run.py --get_data` to parse the raw data into TSV.
+ Run `./run.py --output_map` (or `./plot.r`) to produce the map.
+ Run `./run.py --generate_readme` to generate the README.
