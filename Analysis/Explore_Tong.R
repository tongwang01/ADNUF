library(psych)
library(ggplot2)
library(caret)
library(sqldf)

#Read in data file
input <- read.csv("~/ADNUF/Scripts/Rotterdam/FundaInventoryRotterdamLatestExpanded.csv",
                  sep = "|")
str(input, list.len = 200)

#Some basic proprecessing
input$date_of_sale <- as.Date(input$date_of_sale, "%m/%d/%Y")
input$date_of_rent <- as.Date(input$date_of_rent, "%m/%d/%Y")
input$furnished <- !is.na(input$furnished)
input$furnished_carpets <- !is.na(input$furnished_carpets)
input$furnished_curtains <- !is.na(input$furnished_curtains)
input$number.of.showers <- as.factor(input$number.of.showers)


vk <- subset(input, type == "verkocht")
vk$pps <- vk$price / vk$living_area
vh <- subset(input, type == "verhuurd")


#Explorative analysis
#final_year_of_construction: booms between the two wars, acceleration after WWII until now; not many NAs
summary(input$final_year_of_construction)
qplot(input$final_year_of_construction[input$final_year_of_construction > 1800], binwidth = 5)

#Asking price and price and last asking price
head(verkocht[,c("price", "last_asking_price", "first_selling_price", "asking_price")],100)

#insulation: don't think this matters a lot
str(verkocht$s_insulation)
aggregate(pps ~ s_insulation, FUN = mean, data = verkocht)
qplot(x = s_insulation, y = pps, data = verkocht)
describeBy(verkocht$pps, group = (verkocht$s_insulation == ""))
t.test(verkocht$pps ~ (verkocht$s_insulation == ""))

#Furnished (furnished, furnished_carpet, furnished_curtains): don't seem to make a difference, but extrat
#features anyway
describeBy(verkocht$pps, group = (is.na(verkocht$furnished)))

#Maintainence plan
describeBy(vh$price, group = (vh$maintenance_plan))
head(vh[vh$maintenance_plan=="No","price"])

#number.of.showers: 2+ showers correlates with higher value 
str(vk$number.of.showers)
vk$number.of.showers <- as.factor(vk$number.of.showers)
ggplot(vk, aes(x=number.of.showers, y=pps, fill=number.of.showers)) + geom_boxplot()

head(vk$number.of.showers)




date <- as.Date(input$date_of_sale, "%m/%d/%Y")
date <- date[order(date)]

input$date <- as.Date(input$date_of_sale, "%m/%d/%Y")
s <- aggregate(input$price, by=list(input$date), FUN=function(x){NROW(x)})
str(s)
plot(s)
#Note: data seems to be a rolling 18 months 
#Question: does Funda have more historical data? 

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
