library(caret)
library(rattle)

#Load data file
input <- read.csv("fundaInventory_20150509.csv", sep = "|")
str(input)

#Some minor preprocessing
input2 <- input[input$price <= 5000,]    #Filter out cases where we crawled (incorrectly) the sale price
input2$exterior_space[is.na(input2$exterior_space)] <- 0 #Exterior space = NA -> exterior space = 0
funda <- input2

#Split training and testing sets
set.seed(1234)
inTrain <- createDataPartition(funda$price, p=0.75, list = FALSE)
training <- funda[inTrain,]
testing <- funda[-inTrain,]

#Run a regression model and see what will happen
fit1 <- train(price ~ living_area + exterior_space + hood_avg_property_value +
                hood + height + number_rooms + year_of_construction + type_of_property, 
              data = training, method = "glm")    #Fit a glm model

#Test on testing set, write output to csv file for inspection
testing.complete <- testing[complete.cases(testing),]
testing.complete$glm.pred <- predict(fit1, newdata = testing.complete)
testing.complete$glm.diff <- testing.complete$glm.pred - testing.complete$price
testing.complete$glm.percent <- abs(testing.complete$glm.pred / testing.complete$price -1)


mean(testing.complete$glm.percent)
write.csv(testing.complete, file = "glm_testing_result.csv", row.names =  FALSE)
