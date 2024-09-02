# Function to perform analysis
perform_analysis <- function(data) {
  # Convert the data into a data frame
  df <- as.data.frame(data)
  
  # Calculate summary statistics
  mean_grind_size <- mean(as.numeric(df$grind_size), na.rm = TRUE)
  mean_portion <- mean(df$portion, na.rm = TRUE)
  mean_water_temp <- mean(df$water_temp, na.rm = TRUE)
  mean_brew_time <- mean(df$brew_time, na.rm = TRUE)
  
  median_grind_size <- median(as.numeric(df$grind_size), na.rm = TRUE)
  median_portion <- median(df$portion, na.rm = TRUE)
  median_water_temp <- median(df$water_temp, na.rm = TRUE)
  median_brew_time <- median(df$brew_time, na.rm = TRUE)
  
  # Create a list with the results
  results <- list(
    mean_grind_size = mean_grind_size,
    mean_portion = mean_portion,
    mean_water_temp = mean_water_temp,
    mean_brew_time = mean_brew_time,
    median_grind_size = median_grind_size,
    median_portion = median_portion,
    median_water_temp = median_water_temp,
    median_brew_time = median_brew_time
  )
  
  # Return the results as a JSON object
  return(jsonlite::toJSON(results, pretty = TRUE))
}

# Read data from stdin and run analysis
input_data <- read.csv(file = "stdin", header = TRUE)
output <- perform_analysis(input_data)
cat(output)
