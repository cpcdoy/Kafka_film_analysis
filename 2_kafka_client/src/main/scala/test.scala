import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.apache.spark.{SparkConf, SparkContext};
import org.apache.spark.streaming.kafka._
import kafka.serializer.StringDecoder

import com.client_kafka.spark.utils.JsonUtils._

object test {

  def main(arg: Array[String]): Unit = {

    val Array(topics : String, numThreads : String) = Array("popularity,", "1")
    val sparkConf = new SparkConf().setAppName("test").setMaster("local[*]")
    val ssc = new StreamingContext(sparkConf, Seconds(2))
    ssc.checkpoint("checkpoint")

    val ip = "10.41.175.16"
    val kafkaConf = Map(
      "metadata.broker.list" -> "localhost:6667",
      "zookeeper.connect" -> "localhost:2181",
      "group.id" -> "test"
    )

    val topicMap = topics.split(",").map((_, numThreads.toInt)).toMap
    val lines = KafkaUtils.createStream[String, String, StringDecoder, StringDecoder](ssc, kafkaConf, topicMap, StorageLevel.MEMORY_ONLY_SER).map(_._2)
    lines.foreachRDD
    {
      rdd =>
        if (rdd.count > 0)
          rdd.repartition(1).saveAsTextFile("./test/" + rdd.hashCode())
    }

    ssc.start()
    ssc.awaitTermination()
  }
}