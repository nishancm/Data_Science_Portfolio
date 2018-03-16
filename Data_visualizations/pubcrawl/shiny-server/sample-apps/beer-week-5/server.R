library(shiny)
library(leaflet)
library(dplyr)
library(tidyverse)
library(jsonlite)
library(shinydashboard)
library(htmltools)
library(lubridate)
library(RColorBrewer)

# setwd("~/Desktop/beerWeek/Examples/beer-week-3")

###############
# Process Data
###############

breweryData <- read.csv('data/BreweryData.csv')
# breweryData[is.na(breweryData)] <- 0

# BEER TYPES
# convert beer types string to list
breweryData$beer_lst <- sapply(as.character(breweryData$beer_types), function(x) strsplit(x, ",")) %>% sapply(trimws)

# high-level beer types
# beer_types <- strsplit(as.character(breweryData$beer_types), ",") %>% unlist() %>% sapply(trimws) %>% unique()
beer_types <- c("Berliner Weissbier", "Belgian Witbier", "Kolsch",
                "Blonde Ale", "Golden Ale", "Lager", "Heifenweizen", "Pilsner",
                "Saison", "Pale Ale", "Amber Ale", "IPA", "Double IPA", "Altbier",
                "Barleywine", "Brown Ale", "Rye Beer", "Scotch Ale", "Bock", 
                "Porter", "Stout", "Imperial Stout")
# beer icon 
icons <- list.files("www/beer_type", pattern="*.jpg")
beer_icons <- sapply(icons, function(x) paste("beer_type/", x, sep=""), USE.NAMES = FALSE)

# OPENING DATE & TIME
# function to convert time
process_time <- function(text){
  if(is.null(text) | text =="") {text <- "-1"}
  if (text=="-1") {return (text)}
  else {
    t <- strsplit(text, split="-")[[1]]
    if(t[2]>"24:00") {t[2] <- "24:00"}
    return(t)
  }
}

# combine all opening hours to a column 
breweryData$all_hours <- select(breweryData, starts_with("hour")) %>% apply(1, paste, collapse=",") # combine all opening hours to a str
breweryData$all_hours <- lapply(breweryData$all_hours, function(x) unlist(strsplit(x, ","))) # convert to a vector
breweryData$all_hours <- lapply(breweryData$all_hours, function(x) lapply(x, process_time)) # convert to 12:00 system

# function to determine if open
if_store_open <- function(input, h){
  if(length(h) == 1) {
      return (-1)}
  else {
    input <- input - hours(8)
    input_time <- format(input, "%H:%M")
    if(h[2] == "00:00") {h[2] <- "25:00"}
    if(input_time >= h[1] & input_time < h[2]) {output <- 1}
    else {output <- -1}
  }
  return(output)
}


# PATH DATA
json <- readLines("data/Routes.txt", warn = FALSE) %>%
  paste(collapse = "\n") %>%
  fromJSON(simplifyVector = FALSE)

showPath <- function(click1, click2){
  id1 = click1[1]
  id2 = click2[1]
  path_name = paste0(click1[1], '_', click2[1], '_', 'driving')
  json_tmp = json[[path_name]]
  json_tmp
}

###############
# Server
###############

shinyServer(function(input, output, session){
  
  add_labels <- function(df) {
    labels <- sprintf(
      "<h5><a href='%s'>%s</a></h5></br>Address: %s, %s %s</br>Tel: %s</br>",
      df$website, df$brewery, df$street, df$city, df$zipcode, df$phone_number 
    ) %>% lapply(htmltools::HTML)
    return(labels)
  }
  
  output$map <- renderLeaflet({
    leaflet() %>%
      addTiles(
        urlTemplate = "https://api.mapbox.com/styles/v1/yiqiang/cjb631its10852slahgl3ulex/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoieWlxaWFuZyIsImEiOiJjamI2MjJ2aDgzZTJiMzdvMTEza25vN3czIn0.da7McqdO9XgggUE0LTCx3Q"
      ) %>%
      addMarkers(
        data = breweryData, lat = ~Lat, lng = ~Long, layerId = ~brewery_id
      ) %>% 
      fitBounds(lng1=-122.517745, lat1 = 37.808235, lng2 = -122.186932, lat2 = 37.716482) %>% 
      setView(lat=37.765921, lng=-122.418685, zoom=13)
  })

  BeerIcon <- awesomeIcons(
    icon = 'beer',
    iconColor = '#ffd700',
    library = 'ion',
    markerColor = "black"
  )
  
  filtered_breweryData <- reactive({
    # filter for beer styles
    t <- breweryData[sapply(breweryData$beer_lst, function(x) any(input$beertype %in% x)),]
    
    # filter for other features
    print(input$filters)
    print(input$timeinput)
    print(input$minutesbar)
    if("food" %in% input$filters){t <- subset(t, t$serves_food == T)}
    if("dogs" %in% input$filters){t <- subset(t, t$dog_friendly == T)}
    if("happyhour" %in% input$filters){t <- subset(t, t$happy_hour == T)}
    if("reservations" %in% input$filters){t <- subset(t, t$reservations == T)}
    if("outdoor" %in% input$filters){t <- subset(t, t$outdoor == T)}

    return(t)
  })
  
  observe({
    leafletProxy("map") %>% clearMarkers()
    tmp <- filtered_breweryData()
    updateSelectInput(session, "startbrewery", "Starting Brewery", choices = tmp$brewery)
    d <- dim(tmp)[1]
    if(!is.null(d)){
      labels <- add_labels(tmp)
      for(i in 1:nrow(tmp)){
        leafletProxy("map") %>% 
          addAwesomeMarkers(lat = tmp$Lat[i], lng = tmp$Long[i], layerId = tmp$brewery_id[i],
                            icon = BeerIcon, popup = labels[i], 
                            labelOptions(opacity=1, textsize="20px")
                            )
      }
    }
    
  })
  


# Route Planner
  observeEvent(input$gocrawl, {
      leafletProxy("map") %>% clearGeoJSON()
      tmp <- filtered_breweryData()
      bash_command <- paste0("python Route/route_plan_wrapper.py ", "'starting_brewery=", tmp$brewery_id[tmp$brewery == input$startbrewery]-1,
                               " crawl_starts_at=", format(input$timeinput, '%H:%M')," minutes_per_bar=", stringr::str_extract(input$minutesbar, "\\(?[0-9..]+\\)?"))
      if("food" %in% input$filters){bash_command <- paste0(bash_command, " serves_food=True")}
      if("dogs" %in% input$filters){bash_command <- paste0(bash_command, " dog_friendly=True")}
      # if("happyhour" %in% input$filters){bash_command <- paste0(bash_command, " happyhour=True")}
      if("reservations" %in% input$filters){bash_command <- paste0(bash_command, " reservations=True")}
      if("outdoor" %in% input$filters){bash_command <- paste0(bash_command, " outdoor=True")}
      print(bash_command)
      bash_command <- paste0(bash_command, "'", "| head -n ", stringr::str_extract(input$barnumber, "\\(?[0-9..]+\\)?"))
      a <- system(bash_command, intern = TRUE)
      print(a)
      pubs_list <- lapply(a, function(x){stringi::stri_extract_all_regex(x, "(?<=').*?(?=')")})
      route_color <-c("#00441b", "#810f7c", "#084081", "#e34a33", "#41ae76", "#e7298a",
                      "#6A3D9A", "#54278f", "#fd8d3c", "#78c679")
      for(i in 1:(length(pubs_list)-1)){
        json_tmp <- showPath(tmp$brewery_id[tmp$brewery == pubs_list[i][[1]][[1]][1]], tmp$brewery_id[tmp$brewery == pubs_list[i+1][[1]][[1]][1]])
        leafletProxy("map") %>% addGeoJSON(json_tmp, fill = F, color = route_color[i])
      }
            })
})



