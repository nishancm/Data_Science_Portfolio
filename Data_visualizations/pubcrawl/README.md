MVP --

* All breweries with four fields (name, start, end, address, start time end time, DOW, Food Y/N and #)
* Deploy and pretty front end


* Instance information: ec2-34-229-40-206.compute-1.amazonaws.com

* Installation instructions:
0. Spun up instance (t2) in VA region with ubuntu unix
1. Login to box and created new user "beerweek", generated key.
2. Install R: sudo apt-get update ;  sudo apt-get install r-base ;sudo apt-get install r-base-dev
3. Open port 3838 in the launch-wizard-2 security group.
4. Install shiny: sudo su - -c "R -e \"install.packages('shiny', repos = 'http://cran.rstudio.com/')\""
5. Install shiny server: wget https://download3.rstudio.org/ubuntu-12.04/x86_64/shiny-server-1.4.4.807-amd64.deb
6. sudo dpkg -i shiny-server-1.4.4.807-amd64.deb
7. install rmarkdown: sudo su - -c "R -e \"install.packages('rmarkdown', repos = 'http://cran.rstudio.com/')\""
8. sudo apt-get install -y libxml2-dev libcurl4-openssl-dev libssl-dev
9.  install tidyvers: sudo su - -c "R -e \"install.packages('tidyverse', repos = 'http://cran.rstudio.com/')\""
10.  install magrittr: sudo su - -c "R -e \"install.packages('magrittr', repos = 'http://cran.rstudio.com/')\""
11. horrible solution -- run as user ubuntu--  sudo chmod -R 777 shiny-server/ so that 
