name := "Spark Project"

version := "1.0"

scalaVersion := "2.11.8"
name := "Spark Project"

version := "1.0"

scalaVersion := "2.11.8"

resolvers += "Typesafe Repo" at "http://repo.typesafe.com/typesafe/releases/"

libraryDependencies +=  "com.typesafe.play" %% "play-json" % "2.3.0"

libraryDependencies += "org.apache.spark" %% "spark-core" % "2.0.0"

libraryDependencies += "org.scalatest" %% "scalatest" % "2.2.6"

resolvers += "sbt-idea-repo" at "http://mpeltonen.github.com/maven/"
libraryDependencies += "org.apache.spark" %% "spark-core" % "2.0.0"
libraryDependencies += "org.scalatest" %% "scalatest" % "2.2.6"
libraryDependencies += "org.apache.spark" % "spark-streaming_2.11" % "2.1.1"
libraryDependencies += "org.apache.spark" % "spark-streaming-kafka-0-8_2.11" % "2.1.1"

libraryDependencies ++= Seq(
  "org.apache.hbase" % "hbase-server" % "1.2.6",
  "org.apache.hbase" % "hbase-client" % "1.2.6",
  "org.apache.hbase" % "hbase-common" % "1.2.6",
  "org.apache.hadoop" % "hadoop-common" % "2.7.3"
)