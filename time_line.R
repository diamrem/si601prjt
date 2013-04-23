all_page <- read.table('~/documents/winter2013/si618/project/all_page.tsv',sep='\t',head=TRUE, fill=TRUE, quote="")
page_5000 <- read.table('~/documents/winter2013/si618/project/page_5000.tsv',sep='\t',head=TRUE, fill=TRUE, quote="")

library(ggplot2)

page_5000$timestamp <- as.numeric(format(as.Date(page_5000$timestamp,'%Y-%m-%d %H:%M:%S'), '%Y'))
#month_5000 <- as.numeric(format(as.Date(page_5000$timestamp,'%Y-%m-%d %H:%M:%S'), '%Y%m'))
qplot(x=year_5000, data=page_5000, geom="histogram", xlab="Year", main="Revisions(>5000) by Year", alpha = I(1/2))
#qplot(x=month_5000, data=page_5000, geom="histogram", xlab="Month", main="Revisions by Month", alpha = I(1/2))

year_all <- as.numeric(format(as.Date(all_page$timestamp,'%Y-%m-%d %H:%M:%S'), '%Y'))
qplot(x=year_all, data=all_page, geom="histogram", xlab="Year", main="Revisions(all) by Year", alpha = I(1/2))

p2 <- ggplot(page_5000, aes(x=year_5000)) + geom_bar(alpha=I(0.5)) + geom_bar(data=all_page, aes(x=year_all),alpha=I(0.5))

#+title('Revisions by Year')
print(p2)

library(plyr)
page_5000$timestamp <- factor(page_5000$timestamp)
page_5000$page_title <- factor(page_5000$page_title)
page_sum <- ddply(page_5000, c('page_title','timestamp'),function(x) c(count=nrow(x)))
png(file = "~/documents/winter2013/si618/project/page_revision_year.png",width=1076,height=467)
# all articles
p <- ggplot(page_sum,aes(timestamp,count,color=page_title, group=page_title))+geom_line()+guides(color=guide_legend(ncol=2))+labs(x='Year',y='Revisions')
print(p)
dev.off()

# apple
png(file = "~/documents/winter2013/si618/project/apple.png",width=1076,height=467)
p1 <- ggplot(page_sum[page_sum$page_title=='Apple Inc.',],aes(timestamp,count,color=page_title, group=page_title))+geom_line()+guides(color=guide_legend(ncol=2))+labs(x='Year',y='Revisions')
print(p1)
dev.off()