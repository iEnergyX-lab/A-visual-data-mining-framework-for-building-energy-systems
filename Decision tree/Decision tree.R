library(party)
#Read data using the code "data <- read.csv("file_name.csv")"
test_data <- iris
#Run the conditional inference tree algorithm
DT <- ctree(Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width, data = test_data)
plot(DT)