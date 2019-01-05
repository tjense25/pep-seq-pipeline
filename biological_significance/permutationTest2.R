# this R script performs a permutation test
library(tidyverse)

set.seed(0)

# null hypothesis: the two populations have the same mean
# alternative hypothesis: the populations have different means (i.e. this is a 2-sided test)

canonical = c(3, 6, 3, 4, 5, 2, 3, 6, 6, 7, 3, 1, 5, 2, 6, 6, 0, 2, 8, 7, 2, 3, 8, 1, 3, 6, 8, 7, 5, 9, 3, 11, 0, 1, 4, 0, 0, 2, 0, 2, 7, 7)
nonCanonical = c(0, 1, 3, 0, 0)

totalCounts = c(canonical, nonCanonical)


# this loop will reassign the counts that appear in "canonical" and "nonCanonical" many times
# as part of a permutation test to give an empirical p-value regarding the null hypothesis

diffs = c()
for (i in 1:100000) {
  # rearrange totalCounts using the sample method
  pseudoTotal = sample(totalCounts, length(totalCounts), replace=FALSE)
  
  # assign the first part to canonical
  pseudoCanon = pseudoTotal[1:length(canonical)]
  # assign the last part to nonCanonical
  pseudoNonCanon = pseudoTotal[(length(canonical) + 1):length(pseudoTotal)] 
  #store the difference between the means
  diffs = c((mean(pseudoCanon) - mean(pseudoNonCanon)), diffs)
}

diffs = sort(diffs)
actualDiff = mean(canonical) - mean(nonCanonical)

moreExtreem = (diffs >= actualDiff)
pVal1 = sum(moreExtreem) / 100000 # calculate the likelihood of a difference as extreme or more extreme
pVal1

lessExtremeVal = mean(diffs) - actualDiff
lessExtremeVal
lessExtreme = (diffs <= lessExtremeVal)
pVal2 = sum(lessExtreme) / 100000
pVal2

pVal = pVal1 + pVal2
print(pVal)
# [1] 0.0144

diffsTibble
# organize the data to facilitate ploting it
diffsTibble = as.tibble(diffs)
greaterDiffs = filter(diffsTibble, value >= actualDiff)
lesserDiffs = filter(diffsTibble, value <= lessExtremeVal)
extremeDiffs = bind_rows(greaterDiffs, lesserDiffs)

diffsTibble = mutate(diffsTibble, value = as.numeric(value))
extremeDiffs = mutate(extremeDiffs, value = as.numeric(value))
# plot the data
theme_update(plot.title = element_text(hjust = 0.5)) 

ggplot() +
  stat_bin(data = diffsTibble,
                 mapping = aes(x = value), 
                 stat="count", bins=44) +
  stat_bin(data = extremeDiffs, mapping = aes(x = value, fill = "more extreme than actual difference"), stat="count", bins=44) +
  labs(x = "permuted difference in means", fill = "") +
  ggtitle("Null Distribution of Difference in Means") +
  theme(legend.position = "bottom")

# this value should match the p-value
(dim(lesserDiffs)[1] + dim(greaterDiffs)[1]) / dim(diffsTibble)[1]
# [1] 0.0144 # it does!
# This demonstrates that the ratio of red to grey on the graph represents the p-value accurately



