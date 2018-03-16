library(shiny)
library(leaflet)
library(dplyr)
library(shinydashboard)
library(lubridate)
library(shinyWidgets)
library(shinythemes)
library(shinyTime)

breweryData <- read.csv('data/BreweryData.csv')

# unique beer styles
beer_types <- c("Berliner Weissbier", "Belgian Witbier", "Kolsch",
                "Blonde Ale", "Golden Ale", "Lager", "Hefeweizen", "Pilsner",
                "Saison", "Pale Ale", "Amber Ale", "IPA", "Double IPA", "Altbier",
                "Barleywine", "Brown Ale", "Rye Beer", "Scotch Ale", "Bock", 
                "Porter", "Stout", "Imperial Stout")

# beer icon 
icons <- list.files("www/beer_type", pattern="*.jpg")
beer_icons <- sapply(icons, function(x) paste("beer_type/", x, sep=""), USE.NAMES = FALSE)

###############
# UI 
###############

shinyUI(fluidPage(id='main',
    tags$head(
     tags$link(rel = "stylesheet", type = "text/css", href = "css/home.css")
    ),
    title=NULL,
    windowTitle = 'San Francisco Beer Week 2018',
    theme = shinytheme("flatly"),
    tags$div(id='banner', HTML('
      <div id="logo">
        <a href="https://www.usfca.edu/data-institute"></a>
        </div>
        <div class="banner_links">
        <a class="link_1" href="../../about_page.html">About Us</a>
        </div>
    ')),

    
    # BREWERY FEATURES FILTER 
    fluidRow(id="filter_bar",
    column(12,
      checkboxGroupButtons(
      inputId = "filters", label = NULL, 
      choiceNames = c( paste0("Serve Food ", icon("cutlery")),
                paste0("Dog Friendly ", icon("paw")),
                paste0("Reservations ", icon("calendar-check-o")),
                paste0("Outdoor Seating ", icon("sun-o"))),
      choiceValues = c("food", "dogs", "reservations", "outdoor"),
      justified = TRUE, status = "primary top_btn_style",
      checkIcon = list(yes = icon("ok", lib = "glyphicon"), no = icon("remove", lib = "glyphicon"))
    ))
    # column(2, pickerInput(inputId = "beertype", label=NULL, selected = beer_types,
    #                choices=beer_types, options = list(`actions-box` = TRUE, `title`='Beer Type'), multiple=TRUE))
     
    ),

    
    fluidRow(
      column(12, leafletOutput("map", width="100%", height = 800))
      ),
    
    absolutePanel(id = "controls", class = "panel panel-default", fixed = TRUE,
                  draggable = TRUE, top = 150, left = "auto", right = 20, bottom = "auto",
                  width = 330, height = "auto",
                  style="padding-left:7px;padding-right:0px;padding-top:5px;padding-bottom:5px",
                  h2("Route Planning", style="font-size:17px;align:center;"),
                  br(),
                  dateInput("opendate", label="Open Date & Time:", value=format(Sys.time() - 8*60*60, '%Y-%m-%d'), format(Sys.time() - 8*60*60, '%Y-%m-%d')),
                  selectInput("startbrewery", "Starting Brewery", breweryData$brewery),
                  fluidRow(style="padding-right:5px",
                    column(6, selectInput("starthourinput", "Start Hour", selected=17, choices=seq(0, 23, 1))),
                    column(5, selectInput("startmininput", "Minute", selected=0, choices=seq(0, 55, 15)))
                    ),
                  selectInput("duration", "Duration (hours)", selected=3, choices=seq(2, 10, 1)),
                  selectInput("minutesbar", "Minutes Spent per Bar", c("20 mins", "40 mins", "60 mins")),
                  actionButton("gocrawl", "GO", style="color: #fff; background-color: #337ab7; border-color: #2e6da4"),
                  br(), br(),
                  # h4("Best Route:", style="padding-top:10px"),
                  tableOutput('pubs_tbl')
                  ),
    uiOutput("frame")
    
    
    
    ) # end dashboardPage
) # end shinyUI
