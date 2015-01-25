# HH Analysis

This repository generates TSV and a simple analysis of the
GitHub user data from
[HackathonHackers/hh-personal-sites](https://github.com/HackathonHackers/hh-personal-sites).
Add your data there to be included in this repo,
and file an issue or email me to be excluded from this repo.

The README is parsed with Python and the coordinates for the map
are obtained by searching for a user's GitHub location string
in Wikipedia.

The following information was generated on January 25, 2015
from 554 GitHub users.

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


  + United States: 46
  + Canada: 10
  + San Francisco, CA: 8
  + Cambridge, MA: 6
  + New York: 6
  + Boston, MA: 5
  + California: 5
  + New York, NY: 5
  + New York City: 5
  + New Jersey: 4

## Top First Names


  + David: 7
  + Max: 6
  + Andrew: 6
  + Ben: 6
  + Ryan: 6
  + Rohan: 5
  + Kyle: 5
  + Ian: 4
  + Jonathan: 4
  + Matthew: 4

# Instructions for running in Linux

+ Install Python 3 with packages `PyGithub`, `jinja2`, and `wikipedia`.
+ Install R with packages `ggplot2` and `ggmap`.
+ Modify the `Github` object in `run.py` to have your Github
  API username and access token.
+ Run `./run.py --get_data` to parse the raw data into TSV.
+ Run `./run.py --output_map` (or `./plot.r`) to produce the map.
+ Run `./run.py --generate_readme` to generate the README.