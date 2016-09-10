## Set working directory
setwd("~/Twitter Project")

## Check for required packages and install if need be.
packages<-function(x){
     x<-as.character(match.call()[[2]])
     if (!require(x,character.only=TRUE)){
          install.packages(pkgs=x,repos="http://cran.r-project.org")
          require(x,character.only=TRUE)
     }
}

packages(jsonlite)
packages(tm)
packages(wordcloud)
packages(RColorBrewer)
packages(ggplot2)
## packages(quanteda)
## packages(stringr)
## packages(RWeka)

## Determine size of text files
cat("File size (Bytes):", file.info("WNIT3rdRnd_WomensNIT_UNCvUCLA_12.out")$size)
cat("File size (MegaBytes):", (file.info("WNIT3rdRnd_WomensNIT_UNCvUCLA_12.out")$size/1024/1024))

## The original file contains the BOM or Byte Order Mark found at the beginning
## of the file and signifies the file is unicode. This is great but is a headache
## when processing text as it appear as <U+FEFF> in the string. The only solution
## I found was to open the file in NotePad++ and resave as UTF-8 without BOM. So,
## fname contains the resaved file.
## filename <- "WNIT3rdRnd_WomensNIT_UNCvUCLA_12.out"
fname <- "WomensNIT noBOM.txt"

## I think this is a JSON file I will try to read with rjson package per 
## http://stackoverflow.com/questions/2617600/importing-data-from-a-json-file-into-r
## It works! This produces a list object with 23 elements in the list. 
## **** Now is doesn't work. It produces a parse error: training garbage error ****
## FUTURE TASK: I think the variable 'created_at' needs the date format changed.
## library(rjson)
## json_file <- fname
## json_data <- fromJSON(paste(readLines(json_file), collapse=""))

## Per http://stackoverflow.com/questions/2617600/importing-data-from-a-json-file-into-r
## Let's try jsonlite which puts the data in a data frame
## OMG! It worked. The data are now in a data frame object. Columns such as "coordinates"
## is itself a data frame containing 225 observations of 2 variables.
library(jsonlite)
json_file <- fname
system.time(wnit <- stream_in(file(json_file)))
colnames(wnit)
head(wnit$text)
class(wnit)

## Grab the tweets
wnitTweets <- wnit$text
head(wnitTweets)

## Remove URL's using new package to remove url addresses from text.
## Reference: http://stackoverflow.com/questions/25352448/remove-urls-from-string-in-r
## This package includes a function that could collect the URL's if that becomes
## and important factor.
library (devtools)
install_github("trinker/qdapRegex")
library(qdapRegex)

wnitTweets <- rm_url(wnitTweets, pattern = pastex("@rm_twitter_url", "@rm_url"))
head(wnitTweets)

## create corpus of tweet text. Punctuation for the English language can be referenced
## here: http://www.enchantedlearning.com/grammar/punctuation/. It is removed from
## the corpus to consolidate term list. removePunctuation() includes the list from
## Enchanted Learning as well as @ and /. Numbers and stopwords have also been removed.
library(tm)
wnitCorp <- VCorpus(VectorSource(wnitTweets))
inspect(wnitCorp)
class(wnitCorp)
wnitTdm <- TermDocumentMatrix(wnitCorp,
                          control = list(removePunctuation = TRUE,
                                         removeNumbers = TRUE,
                                         stopwords = TRUE))
Docs(wnitTdm)
nDocs(wnitTdm)
nTerms(wnitTdm)
Terms(wnitTdm)

## Wordcloud anyone? The process of creating a wordcloud is as follows: 
## define tdm as matrix
## get word counts in decreasing order
## create a data frame with words and their frequencies
## plot wordcloud
m = as.matrix(wnitTdm)
word_freqs = sort(rowSums(m), decreasing=TRUE) 
head(word_freqs)
class(word_freqs)
dm = data.frame(word=names(word_freqs), freq=word_freqs)
library(wordcloud); library(RColorBrewer)
wordcloud(dm$word, dm$freq, random.order=FALSE, colors=brewer.pal(8, "Dark2"))

## Let's view the top 10 most frequent words in a bar plot
library(ggplot2)
wf <- data.frame(word = names(word_freqs), freq = word_freqs)
wf10 <- wf[1:10,]
g <- ggplot(wf10, aes(reorder(word, -freq), freq))
g <- g + geom_bar(stat = "identity", fill = I("skyblue"))
g <- g + labs(x = "Top 20 Most Frequent Words", y = "Frequency")
g <- g + theme_bw()
g <- g + theme(axis.text.x = element_text(angle = 90, size = 12, hjust = 1))
g

## FUTURE TASK: Per http://stackoverflow.com/questions/2617600/importing-data-from-a-json-file-into-r
## the ndjson::stream_in() function is faster than jsonlite::stream_in() function. Let's
## try this. ndjson is only available in source form and needs to be compiled. This can
## be a future project. Right now I will deal with the nested data frame and use jsonlite
## package. ndjson is also designed to stream directly from the URL .gz format. Two examples
## are below. One uses the curl package which allows for better performance and customization
## of the http request.
install.packages("ndjson")
system.time(wnit1 <- ndjson::stream_in(file(json_file)))

con <- url("http://1usagov.measuredvoice.com/bitly_archive/usagov_bitly_data2013-05-17-1368832207.gz")
mydata <- jsonlite::stream_in(gzcon(con))

library(curl)
con <- curl("http://1usagov.measuredvoice.com/bitly_archive/usagov_bitly_data2013-05-17-1368832207.gz")
mydata <- jsonlite::stream_in(gzcon(con))



