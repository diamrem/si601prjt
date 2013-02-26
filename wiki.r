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
