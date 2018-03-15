# Load data and create the time series object
br <- read.csv('train.csv')
br$Month <- NULL
br <- ts(br, start = c(1987, 1), end = c(2010, 12), frequency = 12)

# create training and validation sets
train <- window(br, start = c(1987, 1), end = c(2005, 12))
val <- window(br, start = c(2006, 1), end = c(2007, 12))

# holt-winters modeling
bank <- train[,3]

# Looking at acf plot of data, we can see both a trend and seasonality
acf(bank)
acf(diff(bank), lag.max = 48)

# additive holt-winters model parameter tunning
best_add_nl_rmse = Inf
best_add_nl_para = c(0,0,0)
for(a in c(0.400,0.405,0.410)){
    for(b in  c(0.250,0.255,0.260)){
        for(g in c(0.585,0.590,0.595)) {
            hw.AD <- HoltWinters(x = bank, alpha = a, beta =  b, gamma = g, seasonal = "add")
            pred <- forecast(hw.AD,h = 24, level = 0.95)$mean
            rmse_HW <- sqrt(mean((pred - val[,3])^2))*10000
            if(rmse_HW < best_add_nl_rmse) {
                best_add_nl_rmse = rmse_HW
                best_add_nl_para = c(a,b,g)
            }
        }
    }
}
# best rmse observed 12.22
m1 <- forecast(HoltWinters(x = bank, alpha = 0.405, beta =  0.255, 
                           gamma = 0.590, seasonal = "add"), h=24)$mean



# multiplicative holt-winters model parameter tuning
best_mult_rmse = Inf
best_mult_para = c(0,0,0)
for(a in c(0.395,0.400,0.405)){
    for(b in  c(0.225,0.230,0.235)){
        for(g in c(0.585,0.590,0.595)) {
            hw.AD <- HoltWinters(x = bank, alpha = a, beta =  b, gamma = g, seasonal = "mult")
            pred <- forecast(hw.AD,h = 24, level = 0.95)$mean
            rmse_HW <- sqrt(mean((pred - val[,3])^2))*10000
            if(rmse_HW < best_mult_rmse) {
                best_mult_rmse = rmse_HW
                best_mult_para = c(a,b,g)
            }
        }
    }
}

# best is multiplicative model
# rmse 12.18
m2 <- forecast(HoltWinters(x = train[,3], alpha = 0.4, beta =  0.23, 
                           gamma = 0.59, seasonal = "mult"), h=24)$mean
sqrt(mean((m2 - val[,3])^2))*10000

#model stacking

# means
pred = (m1+m2)/2
sqrt(mean((pred - val[,3])^2))*10000 #12.19

#max
pred = rep(0,24)
for(i in 1:24){
    pred[i] = max(c(m1[i], m2[i]))
}
sqrt(mean((pred - val[,3])^2))*10000 #12.20

#min
pred = rep(0,24)
for(i in 1:24){
    pred[i] = min(c(m1[i], m2[i]))
}
sqrt(mean((pred - val[,3])^2))*10000 #12.19


# best holt-winter model picked as multiplicative model and then trained in training adn validation set combined
f_model <- HoltWinters(x = bank, alpha = 0.4, beta =  0.23, 
                       gamma = 0.59, seasonal = "mult")


# plot predictions
plot(HoltWinters(x = br[,3], alpha = 0.4, beta =  0.23, 
                          gamma = 0.59, seasonal = "mult"), xlim = c(1990, 2013))
pred <- forecast(HoltWinters(x = br[,3], alpha = 0.4, beta =  0.23, 
                            gamma = 0.59, seasonal = "mult"), h=24)$mean
lines(pred, col = 'blue')
















