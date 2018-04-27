
library(ggplot2)
library(ggthemes)
library(readr)
library(tidyr)


results <- read_tsv("./results/testResults.txt")
print(results)
results <- gather(results, key="Metric", value="Performance", -NumMotifs)
print(results)

resultPlot <- ggplot(results, aes(x=NumMotifs, y=Performance, colour=Metric)) +
	geom_line() +
	theme_bw() +
	xlab("Number of Implanted Motifs") + 
	theme(text = element_text(size=20),
	panel.border = element_blank(),
	panel.grid.major = element_blank(),
	axis.line = element_line(colour = "black"))

ggsave(plot=resultPlot, file="./results/testResults.png")
