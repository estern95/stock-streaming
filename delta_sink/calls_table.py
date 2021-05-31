callsRaw = (spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "34.136.146.75:29094")
        .option("subscribe", "TSLA_calls")
        .option("startingOffsets", "earliest") 
        .load())

callsDF = callsRaw.selectExpr("CAST(value AS STRING)")

(callsDF.writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation", "/delta/")
  .table("calls"))