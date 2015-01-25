#!/usr/bin/env Rscript

library(ggplot2)
library(ggmap)

gh = read.table("data/github.tsv",sep="\t",header=TRUE)
world_map <- borders("world",colour="gray70",fill="gray70")
mp <- ggplot() +
  world_map +
  stat_bin2d(aes(x=gh$long,y=gh$lat,
                 fill=..count..),bins=100) +
  xlab("") + ylab("") +
  theme_bw() +
  theme(legend.position="bottom",
        axis.text.y=element_blank(),
        axis.text.x=element_blank())
ggsave("plots/map.png",width=8,height=7)
ggsave("plots/map.pdf",width=8,height=7)
