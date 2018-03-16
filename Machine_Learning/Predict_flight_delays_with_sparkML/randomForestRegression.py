from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import HiveContext
from pyspark.storagelevel import StorageLevel
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler, IndexToString
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.types import IntegerType
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import pandas as pd
import numpy as np

# apply random forest to flights table

conf = SparkConf().setMaster("local").setAppName('randomForest')
sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)

flightsDF = sqlContext.sql('select * from flightsnumeric where Year = 2008').repartition(100)

featureNames = ['Year','Month','DayofMonth','DayOfWeek','CRSDepTime','CRSArrTime','CRSElapsedTime','UniqueCarrier','FlightNum','OddFN','LenFN','Origin','Dest','Distance']
va = VectorAssembler(inputCols = featureNames, outputCol='features')

oddFN = udf(lambda x: int(x % 2 == 1))
lenFN = udf(lambda x: len(str(int(x))))
flightsDF = flightsDF.withColumn('LenFN_str', lenFN('FlightNum'))
flightsDF = flightsDF.withColumn('LenFN', flightsDF.LenFN_str.cast(IntegerType())).drop('LenFN_str')
flightsDF = flightsDF.withColumn('FlightNumTmp', flightsDF.FlightNum.cast(IntegerType())).drop('FlightNum').withColumnRenamed('FlightNumTmp','FlightNum')
flightsDF = flightsDF.withColumn('OddFN_str', oddFN('FlightNum'))
flightsDF = flightsDF.withColumn('OddFN', flightsDF.OddFN_str.cast(IntegerType())).drop('OddFN_str') 

#flightsRegression = va.transform(flightsDF).select('features','ArrDelay')
#flightsRegression = flightsRegression.withColumn('label', flightsRegression.ArrDelay.cast(IntegerType())).drop('ArrDelay').persist(StorageLevel.DISK_ONLY)

trnDF = flightsDF.filter((flightsDF['Year'].isin(2008) & flightsDF['Month'].isin([10,11,12])) == False)
testDF = flightsDF.filter((flightsDF['Year'].isin(2008) & flightsDF['Month'].isin([10,11,12])) == True)
del flightsDF

trn = va.transform(trnDF).select('features', 'ArrDelay').withColumn('label', trnDF.ArrDelay.cast(IntegerType())).drop('ArrDelay').cache()
test = va.transform(testDF).select('features','ArrDelay').withColumn('label', testDF.ArrDelay.cast(IntegerType())).drop('ArrDelay').cache()
del trnDF
del testDF

#rf = RandomForestRegressor(numTrees=50, maxDepth=30, maxBins=512, subsamplingRate=0.8)

#paramGrid = ParamGridBuilder().addGrid(rf.minInstancesPerNode, [3,5,10,15,20,40,80,120]).build()
eval = RegressionEvaluator(metricName='rmse')
#crossval = CrossValidator(estimator=rf, estimatorParamMaps=paramGrid, evaluator=eval, numFolds=3)

#cvmodel = crossval.fit(trn)
#bestmodel = cvmodel.bestModel
#bestMinInstancesPerNode = bestmodel._java_obj.getMinInstancesPerNode()
#print('Best Parameter (minInstancesPerNode): '+str(bestMinInstancesPerNode))
best_rf = RandomForestRegressor(numTrees=100, maxDepth=30, minInstancesPerNode=80, maxBins=512, subsamplingRate=0.8)
best_rfmodel = best_rf.fit(trn)

preds = best_rfmodel.transform(test)
rmse = eval.evaluate(preds)

print('RMSE = %.4f') % rmse
preds.toPandas().to_csv('rf_regression_preds.csv')
pd.DataFrame(zip(np.array(featureNames)[best_rfmodel.featureImportances.indices], best_rfmodel.featureImportances.values), columns=['feats','imps']).to_csv('rf_regression_FI.csv')

sc.stop()
