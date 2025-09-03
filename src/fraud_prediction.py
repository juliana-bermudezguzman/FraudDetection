from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

#Lectura del dataset
spark = SparkSession.builder.appName("fraud_prediction").getOrCreate()

df = spark.read.csv('/home/urosario/BigData/PARCIAL_FINAL/Fraud.csv', header=True, inferSchema=True)

#Eliminar las variables que no me sirven
columns_to_drop = ['step', 'nameOrig', 'nameDest', 'isFlaggedFraud']

df = df.drop(*columns_to_drop)

#Codificar la variable categórica
df = df.withColumn('type_num',
                   when(col('type') == 'PAYMENT', 0)
                   .when(col('type') == 'TRANSFER', 1)
                   .when(col('type') == 'CASH_OUT', 2)
                   .when(col('type') == 'DEBIT', 3)
                   .when(col('type') == 'CASH_IN', 4)
                   .otherwise(-1))

df = df.drop('type')

df = df.withColumnRenamed('type_num', 'type')

#Mostrar los que tenemos
df.show(5)

train_df, test_df = df.randomSplit(weights=[0.7,0.3], seed=100)


fraud_train = train_df.groupBy("isFraud").count()
fraud_test = test_df.groupBy("isFraud").count()


fraud_train.show()
fraud_test.show()

train_df.coalesce(1).write.csv('fraud_train.csv')
test_df.coalesce(1).write.csv('fraud_test.csv')