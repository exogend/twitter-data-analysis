# WNIT
Dianne Waterson  
September 10, 2016  





### Introduction

#####This is a first pass word frequency analysis of tweets from the Women's National Invitation Tournament or WNIT. More information about WNIT can be found [here](http://www.womensnit.com/). This analysis is performed as part of Exogend's Twitter Data Analytics proof-of-concept project.

### Data

#####The file size of file "WNIT3rdRnd_WomensNIT_UNCvUCLA_12.out" is 1.0726842880249 MegaBytes. This file contains the BOM or Byte Order Mark found at the beginning of the file and signifies the file is unicode. This is great but is a headache when processing text as it appear as "U+FEFF" in the string as what I believe is an HTML tag as it is enclosed in carrot brackets. I found a quick solution that requires opening the file in NotePad++ and resaving as UTF-8 without BOM. The file without the BOM is called "WomensNIT noBOM.txt". We need a more robust solution to process very large file sizes. Based on my research, the BOM plagues all programming languages; R, Python, Linux, JavaScript, etc. The BOM is really "0xEF,0xBB,0xBF". There are various regex solutions on the internet to try in the near future.

#####The data are in JSON format and can be read into a data frame quite nicely using the jsonlite package. Further processing to get the final word list includes removing URL, punctuation, numbers and stopwords. There still exists the ellipsis before or after some words in the word list, e.g. "quar.". Further evaluation shows the ellipsis to be the Unicode character "U+0085". There are also word concatentations, e.g. "usmgoldeneagles", and abbreviations, e.g. "miss" for Mississippi.

#####A later project may be to see if the tweets can be extracted from Twitter in such a way the data are already or mostly cleaned and the BOM removed along with the ellipsis unicode character. The ndjson package has functionality to stream in from an http .gz file. This package requires compiling before use and could be an option.

### Exploring

#####Let's stream in the data into a data frame object and time how long it takes to read in 1 MByte of data. We will also see the data frame column names and a sample of tweets. The column names indicate the information available from these data. Some columns are data frames themselves. For example the column "coordinates" is a data frame containing 255 observations of 2 variables. Looking at the tweets presents a sample of data cleaning opportunities. Lastly, the class() function validates the object containing the data is indeed a data frame.


```r
library(jsonlite)
fname <- "WomensNIT noBOM.txt"
json_file <- fname
system.time(wnit <- stream_in(file(json_file)))
```

```
## opening file input connection.
```

```
## 
 Found 225 records...
 Imported 225 records. Simplifying into dataframe...
```

```
## closing file input connection.
```

```
##    user  system elapsed 
##    0.54    0.00    0.54
```

```r
colnames(wnit)
```

```
##  [1] "contributors"              "coordinates"              
##  [3] "created_at"                "entities"                 
##  [5] "favorite_count"            "favorited"                
##  [7] "geo"                       "id"                       
##  [9] "id_str"                    "in_reply_to_screen_name"  
## [11] "in_reply_to_status_id"     "in_reply_to_status_id_str"
## [13] "in_reply_to_user_id"       "in_reply_to_user_id_str"  
## [15] "lang"                      "metadata"                 
## [17] "place"                     "retweet_count"            
## [19] "retweeted"                 "source"                   
## [21] "text"                      "truncated"                
## [23] "user"                      "retweeted_status"         
## [25] "possibly_sensitive"
```

```r
head(wnit$text)
```

```
## [1] "Update: @TUOWLS_WBB takes on Middle Tennessee State in Quarterfinals of @WomensNIT on Sunday at 4PM at Middle Tennessee State #Temple #WNIT"       
## [2] "RT @WCChoops: WBB | At the top of the hour, @smcgaels takes on Sacramento State with the winner advancing to the @WomensNIT Elite Eight. #W<U+0085>"      
## [3] "RT @umichwbball: Michigan is moving on in the @womensnit! U-M 65, Mizzou 55 FINAL #goblue http://t.co/S1urSAQTay"                                  
## [4] "RT @michaelniziolek: Great photos by @adougall of @umichwbball 65-55 win over Missouri in @WomensNIT Sweet 16 http://t.co/m2jII8PFdP story <U+0085>"      
## [5] "Game recaps &amp; scores from 1st 5 games tonight are posted &gt; http://t.co/kDbcxugGpr @umichwbball @MT_WBB @TUOWLS_WBB @WVUWBB @novawbasketball"
## [6] "RT @jesse081990: #Michigan, #Villanova, #WestVirginia, #SouthernMiss, #Temple so far in the #Elite8 of the @WomensNIT"
```

```r
class(wnit)
```

```
## [1] "data.frame"
```




### Cleaning

#####As previously mentioned, further processing to get the final word list includes removing URL, punctuation, numbers and stopwords. Upon completion of these tasks, there still exists the ellipsis before or after some words in the word list, e.g. "quar.". Further evaluation shows the ellipsis to be the Unicode character "U+0085". There are also word concatentations, e.g. "usmgoldeneagles", and abbreviations, e.g. "miss" for Mississippi. This means there are more work to be done, but will use the resulting data set as it is for now to get a glimpse of what we have for the project in the following two sections.

### Word Cloud

#####The tm package is used to create a term document matrix from which word frequencies can be calculated. The term document matrix contains 225 documents. These are the number of tweets captured. The corpus contains 192 unique terms or words. The term list is as follows.


```
##   [1] "action"          "adougall"        "advance"        
##   [4] "advances"        "advancing"       "alex"           
##   [7] "amp"             "asked"           "attendance"     
##  [10] "back"            "backthepac"      "battle"         
##  [13] "beat"            "behind"          "best"           
##  [16] "better"          "blueraiderdj"    "blueraiders"    
##  [19] "brava"           "bwonder"         "call"           
##  [22] "came"            "cats"            "checking"       
##  [25] "cindybrunsonaz"  "coach"           "coachinsell"    
##  [28] "coachtomhodges"  "colorado"        "coming"         
##  [31] "congrats"        "congratulations" "coyer"          
##  [34] "details"         "edged"           "eight"          
##  [37] "elite"           "face"            "fairly"         
##  [40] "fans"            "far"             "father"         
##  [43] "final"           "following"       "gaelswbb"       
##  [46] "game"            "games"           "get"            
##  [49] "goblue"          "good"            "gopack"         
##  [52] "got"             "great"           "harry"          
##  [55] "high"            "home"            "hoops"          
##  [58] "host"            "hosts"           "hour"           
##  [61] "htt<U+0085>"            "huge"            "improved"       
##  [64] "jesse"           "johns"           "katherine"      
##  [67] "keep"            "later"           "led"            
##  [70] "like"            "loss"            "louin"          
##  [73] "loveandbball"    "march"           "michaelniziolek"
##  [76] "michigan"        "middle"          "miss"           
##  [79] "mississip<U+0085>"      "mississippi"     "missouri"       
##  [82] "mizzou"          "moves"           "moving"         
##  [85] "mtathletics"     "mtcoachkim"      "mtsu"           
##  [88] "mtwbb"           "murp<U+0085>"           "murphycenter"   
##  [91] "need"            "next"            "night"          
##  [94] "northern"        "novaathletics"   "novanation"     
##  [97] "novawbasketball" "novawbb"         "now"            
## [100] "ole"             "olemiss"         "olemisswbb"     
## [103] "operationk"      "ota"             "pa<U+0085>"            
## [106] "pachoops"        "pack"            "packwomensbball"
## [109] "pacnetworks"     "perretta"        "photos"         
## [112] "playing"         "posted"          "prepared"       
## [115] "pts"             "quar<U+0085>"           "quarterfinal"   
## [118] "quarterfinals"   "recap"           "recaps"         
## [121] "refs"            "right"           "road"           
## [124] "round"           "sac"             "sacramento"     
## [127] "sacstatewbb"     "said"            "scored"         
## [130] "scores"          "season"          "set"            
## [133] "showdown"        "slated"          "smcgaels"       
## [136] "someone"         "son"             "southern"       
## [139] "southernmiss"    "southernmisswbb" "sportsroadhouse"
## [142] "state"           "still"           "stjohns"        
## [145] "story"           "sunday"          "survive"        
## [148] "sweet"           "takes"           "team"           
## [151] "temple"          "temple<U+0085>"         "tennessee"      
## [154] "thanks"          "third"           "tip"            
## [157] "tonight"         "tonights"        "top"            
## [160] "treys"           "truefanatut"     "tstinnett"      
## [163] "tune"            "tuowlswbb"       "turned"         
## [166] "tying"           "uclawbb"         "umichwbball"    
## [169] "uncbearswbb"     "update"          "usmgoldeneagles"
## [172] "villanova"       "virginia"        "waiting"        
## [175] "wbb"             "wcchoops"        "west"           
## [178] "westvirginia"    "wildcats"        "will"           
## [181] "win"             "winner"          "with<U+0085>"          
## [184] "wnit"            "womensnit"       "wonder"         
## [187] "work"            "wvu"             "wvuwbb"         
## [190] "xavvsaz"         "yet"             "youre"
```

#####The word cloud presents the higher frequency words in larger font and conversely, the lower frequency words in smaller font. I like it because its a nice colorful visualization.

![](WNIT_files/figure-html/wordcloud-1.png)<!-- -->

### Bar Plot

#####Although I enjoy the colors, the bar plot allows us to visualize better the relative differences in word frequencies. It aligns with the cloud presentation, but the relative bar heights help to see the Pareto distribution present in text analyses.

![](WNIT_files/figure-html/barplot-1.png)<!-- -->

