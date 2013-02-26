articles=read.table("articles.txt",header=TRUE, sep="\t")
num=articles$number.of.edits
h<-hist(num,plot=F,breaks=1000)
plot(h$counts, log="xy",type="h",xlab="Number of Edits in articles", ylab="Frequency")
editors=read.table("editor.txt",header=TRUE, sep="\t")
ed=editors$number.of.edits
mean(num)
sd(num)
mean(ed)
sd(ed)
top=read.table("top_editor.txt",header=TRUE, sep="\t")
toped=top$number.of.edits
mean(toped)
sd(toped)
top1=read.table("top_articles.txt",header=TRUE, sep="\t")
top1
top1=top1$number.of.edits
mean(top1)
sd(top1)

# time --by wenke
# all dates
time=read.table("2_output_hour_sorted.txt", header=TRUE,sep="\t")
plot(time,type='h')
# weekdays average
time=read.table("2_output_weekday.txt", header=TRUE,sep="\t")
plot(time,type='h')
# weekends average
time=read.table("2_output_weekend.txt", header=TRUE,sep="\t")
plot(time,type='h')
# weekdays & weekends
time1=read.table("2_output_wdays_wends.txt", header=TRUE,sep="\t")
plot(time1$Weekdays, type="l", col=plot_colors[1], ylim=range(time),ylab="Counts",xlab="Hours")
lines(time1$Weekends, type="l", col=plot_colors[5])
legend("topleft",names(time1[2:3]), cex=0.8, col=c("red","blue"), bty="n", lwd=1)
# days in a week
time=read.table("2_output_wdays.txt", header=TRUE,sep="\t")
plot_colors <- c("red","orange","brown","green","blue","purple","black")
plot(time$Mon, type="l", col=plot_colors[1], ylim=range(time),ylab="Counts",xlab="Hours")
lines(time$Tue, type="l", col=plot_colors[2])
lines(time$Wed, type="l", col=plot_colors[3])
lines(time$Thu, type="l", col=plot_colors[4])
lines(time$Fri, type="l", col=plot_colors[5])
lines(time$Sat, type="l", col=plot_colors[6])
lines(time$Sun, type="l", col=plot_colors[7])
legend("topleft",names(time[2:8]), cex=0.5,col=plot_colors, bty="n", lwd=1);