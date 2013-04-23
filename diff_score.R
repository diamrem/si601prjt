library(ggplot2)
library(plyr)
top_page <- read.csv('./all_fields.tsv', sep='\t', header=TRUE)
top_page.clean <- subset(top_page, diff_score>=0)
top_page.clean$timestamp <- as.numeric(format(as.Date(top_page.clean$timestamp, "%Y-%m-%d %H:%M:%S"),"%Y"))
head(top_page.clean)
summary(top_page.clean)
mean(top_page.clean$diff_score)
top_page.clean.year <- ddply(top_page.clean, c('page_title', 'timestamp'), summarise, diff_mean=mean(diff_score))

head(top_page.clean.year)

# Distribution of diff score
ggplot(top_page.clean, aes(x=diff_score), smooth=lm) + geom_histogram(binwidth=0.03, aes(y = ..density.., alpha=0.5)) + geom_density()

# Boxplot of diff score of each page
qplot(page_title, diff_score, data=top_page.clean, geom = "boxplot", fill=page_title, colour=page_title, alpha = I(0.5)) + guides(color=guide_legend(ncol=2)) + theme(axis.text.x=element_text(angle=90, hjust = 1))

# Mean diff score over year
ggplot(data=top_page.clean.year, aes(x=timestamp, y=diff_mean, colour=page_title)) + geom_line() + xlab("Year") + ylab("Mean Diff Score") + guides(color=guide_legend(ncol=2)) + geom_text(data = top_page.clean.year[top_page.clean.year$timestamp == "2013",], aes(label=page_title), size=3)

# Correlation between mean diff score and revision number
ddply(top_page.clean, c('page_title'), summarise, total_revision = catcolwise(), diff_mean=mean(diff_score))

top_page_relation <- read.csv('./average_diff_freq', sep='|', header=T)
ggplot(data=top_page_relation, aes(x=avg_diff, y=revision_total)) + geom_point(shape=1) +geom_smooth()
