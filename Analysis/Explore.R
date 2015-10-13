library(psych)
library(ggplot2)
library(caret)
library(sqldf)

#Read in data file
input <- read.csv("~/ADNUF/Scripts/FundaExpanded_20151005_added_header.csv",
                  sep = "|")
str(input)

#Some explorative analysis
date <- as.Date(input$date_of_sale, "%m/%d/%Y")
date <- date[order(date)]

input$date <- as.Date(input$date_of_sale, "%m/%d/%Y")
s <- aggregate(input$price, by=list(input$date), FUN=function(x){NROW(x)})
str(s)
plot(s)
#Note: data seems to be a rolling 18 months 
#Question: does Funda have more historical data? They must..

#Zoom in on all sold properties. What can we find?
verkocht <- subset(input, type == "verkocht")
#describe(verkocht)
#describe.by(verkocht, group = "hood")
summary(verkocht)

#Living area and price
verkocht$living_area <- as.character(verkocht$living_area)
verkocht$living_area <- as.numeric(verkocht$living_area)


qplot(x=living_area, y = price, data = verkocht)

#Strong correlation between price and living area

#Find out what influences price per square meter
verkocht$pps <- verkocht$price / verkocht$living_area
verkocht$type_of_apartment <- as.character(verkocht$type_of_apartment)
qplot(x=type_of_apartment, y=pps, data=verkocht)

#Find pps per neighborhood
verkocht2015 <- subset(verkocht, date >= "2015-01-01")
verkocht2014 <- subset(verkocht, date < "2015-01-01")
t_2015 <- sqldf("
select hood, avg(pps) AS pps, count(pps) AS count
FROM verkocht2015
group by 1 order by 2 desc
      ")
t_2014 <- sqldf("
select hood, avg(pps) AS pps, count(pps) AS count
FROM verkocht2014
group by 1 order by 2 desc
      ")
t <- merge(t_2015, t_2014, by = "hood")

write.csv(t, file = "ppsByHood.csv", row.names = FALSE)


#Build a linear model
#Make a copy to handle NA
df1 <- verkocht2015
df1[is.na(df1)] <- 0
df1$city <- as.character(df1$city)
df1$region <- as.character(df1$region)
df1$snapshot_date <- as.Date(df1$snapshot_date)
str(df1, list.len = 170)
df2 <- df1[,!colnames(df1) %in% c("city", "region", "snapshot_date")]
#df2 <- subset(df1, select = -c("city", "region", "snapshot_date"))

df3 <- df2[, colSums(df2 != 0) > 0]

#fit <- train(price ~., data = df3[1:10,], method = "glm")

fit2 <- glm(pps ~ final_year_of_construction + jacuzzi + number.of.showers + 
              monumental_building + number.of.baths + near.busy.road+
              central.location + number_of_bathrooms + hood,
            data = df3, family = "gaussian")
summary(fit2)


summary(df3$complete_floor_insulation)
