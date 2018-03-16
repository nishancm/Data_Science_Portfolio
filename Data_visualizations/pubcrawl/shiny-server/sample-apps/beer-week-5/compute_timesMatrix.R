if(!require("tidyverse")){install.packages("tidyverse", repos = "http://cran.us.r-project.org")}
if(!require("magrittr")){install.packages("magrittr", repos = "http://cran.us.r-project.org")}
if(!require("gmapsdistance")){install.packages("gmapsdistance", repos = "http://cran.us.r-project.org")}

doc <- read.csv("data/BreweryData.csv", numerals = "no.loss", stringsAsFactors=FALSE)
## Manually add Brewery Names
brew_name = c('21st Amendment Brewery','Almanac Taproom','Anchor Brewing','Barebottle Brewing','Barrel Head Brewhouse','Bartlett Hall','Black Hammer Brewing','Black Sands Brewery','Cellarmaker Brewing Co.','Emporium','Ferment.Drink.Repeat','Fort Point Beer Co.','Harmonic Brewing','Laughing Monk Brewing Co.','Local Brewing Co.','Magnolia Brewing Co.','SMOKESTACK at Magnolia Brewing Co.','Mikkeller Bar','Public House','Rogue Ales Public House','Smugglers Cove','Speakeasy Ales and Lagers','Beach Chalet Restaurant & Brewery','ThirstyBear Organic Brewery','Old Bus Tavern','Seven Stills - Brewery & Distillery','Social Kitchen & Brewery','Southpaw BBQ & Brewery','Standard Deviant Brewing','Sunset Reservoir Brewing Co.','Triple Voodoo Brewery','Woods Outbound','Woods Cervecería','Woods Polk Station')
#doc['brew_name'] <- brew_name
#doc <-  na.omit(doc)

set.api.key('AIzaSyBXRwAHqo-HK9HzBnY6rjXf6J2A3YYFpXo') 

oriVec <- c(doc %>% select(Lat,Long) %>% mutate(fld = paste(Lat,Long,sep = "+")) %>% select(fld))
nameVec <- c(doc %>% mutate(fld = paste(Lat,Long,sep = "+")) %>% select(fld, brewery))

final_df <- data.frame(matrix(c('1','1',123,123), nrow = 1, ncol = 4),stringsAsFactors = FALSE)
colnames(final_df) <- c('orig','dest','res.Time','res.Distance')
for (orig in oriVec[[1]]) {
  for (dest in oriVec[[1]]) {
    Sys.sleep(0.2)
    res <- gmapsdistance(origin = orig, destination = dest, mode = "driving")
    final <- data.frame(orig, dest, res$Time, res$Distance)
    final_df <- rbind(final_df, final)
  }
}

times_df <- final_df %>% filter(orig != '1') %>% select(orig, dest, res.Time)
colnames(times_df) <- c("origin", "destination", "travelTime")
times_df %<>% 
  left_join(data.frame(nameVec), by=c("origin" = "fld")) %>% 
  left_join(data.frame(nameVec), by=c("destination" = "fld")) %>% 
  rename(origin_name = brewery.x, destination_name=brewery.y) %>% 
  select(origin_name, destination_name, travelTime)

finalTimes <- reshape(times_df, timevar = "destination_name", idvar = "origin_name", direction = "wide")
colnames(finalTimes) <- c("origin_name", doc$brewery)

write_csv(finalTimes, path="data/timesMatrix.csv")
