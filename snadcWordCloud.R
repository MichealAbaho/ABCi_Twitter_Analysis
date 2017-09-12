#load
library(tm)
library(SnowballC)
library(wordcloud)
library(RColorBrewer)
library(data.table)

filePath <- "../diabetes/diabetes-hashtags.txt"
text <- readLines(filePath)

docs <- Corpus(VectorSource(text))
inspect(docs)

# Convert the text to lower case
docs <- tm_map(docs, content_transformer(tolower))
# Remove numbers
docs <- tm_map(docs, removeNumbers)
# Remove english common stopwords
docs <- tm_map(docs, removeWords, stopwords("english"))
# Remove punctuations
docs <- tm_map(docs, removePunctuation)
# Eliminate extra white spaces
docs <- tm_map(docs, stripWhitespace)
# Text stemming
# docs <- tm_map(docs, stemDocument)

dtm <- TermDocumentMatrix(docs)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)

#head(d, 50)
set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 1,
          max.words=80, random.order=FALSE, rot.per=0.35,
          colors=brewer.pal(8, "Accent"))


