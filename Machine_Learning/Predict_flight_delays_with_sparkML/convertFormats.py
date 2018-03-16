from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import HiveContext
from pyspark.sql.types import IntegerType
from pyspark.ml.feature import StringIndexer, IndexToString

# String indexing categorical variables before applying random forest
conf = SparkConf().setMaster("local").setAppName('convertFormats')
sc = SparkContext(conf = conf)
sqlContext = HiveContext(sc)

flightsDF = sqlContext.sql('select * from flights')

def indexStringColumns(df, cols):
  newdf = df
  for c in cols:
    si = StringIndexer(inputCol = c, outputCol = c+'-num')
    sm = si.fit(newdf)
    newdf = sm.transform(newdf).drop(c)
    newdf = newdf.withColumnRenamed(c+'-num', c)
    ids = IndexToString(inputCol=c, outputCol='categoryVal')
    ids.transform(newdf).select(c, 'categoryVal').distinct().toPandas().to_csv('rf_regression_'+c+'.csv')
  return newdf
  
flightsDF = flightsDF.withColumn('ArrDelayTmp', flightsDF.ArrDelay.cast(IntegerType())).drop('ArrDelay').withColumnRenamed('ArrDelayTmp','ArrDelay')
flightsDF = flightsDF.withColumn('CRSElapsedTimeTmp', flightsDF.CRSElapsedTime.cast(IntegerType())).drop('CRSElapsedTime').withColumnRenamed('CRSElapsedTimeTmp','CRSElapsedTime')
flightsDFNumeric = indexStringColumns(flightsDF, ['UniqueCarrier','FlightNum','TailNum','Origin','Dest'])


flightsDFNumeric.printSchema()
flightsDFNumeric.limit(10).show()
flightsDFNumeric.write.saveAsTable('flightsNumeric', mode='OverWrite')

sc.stop()
