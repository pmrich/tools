/*
Refer to https://alvinalexander.com/scala/sbt-how-to-use-build.scala-instead-of-build.sbt
to replace build.sbt with Build.scala
 */

sbtPlugin := true

resolvers += "Typesafe Repository" at "http://repo.typesafe.com/typesafe/releases/"
resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"
resolvers += "zenaptix at bintray" at "http://dl.bintray.com/zenaptix/rx_zmq_streams"

// sbt sets this internally, but intellij doesn't with it's sbt
conflictManager := ConflictManager.latestRevision

libraryDependencies += "org.scalactic" %% "scalactic" % "3.0.8"
libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.8" % "test"

libraryDependencies += "org.specs2" %% "specs2-core" % "4.2.0" % "test"

scalacOptions in Test ++= Seq("-Yrangepos")

libraryDependencies += "org.slf4j" % "slf4j-api" % "1.7.5"
libraryDependencies += "ch.qos.logback" % "logback-classic" % "1.2.3"
libraryDependencies += "ch.qos.logback" % "logback-core" % "1.2.3"
libraryDependencies += "com.typesafe.scala-logging" %% "scala-logging" % "3.9.2"

libraryDependencies += "commons-io" % "commons-io" % "2.6"
libraryDependencies += "io.spray" %% "spray-json" % "1.3.3"

libraryDependencies += "ch.cern.sparkmeasure" %% "spark-measure" % "0.14"

val akkaVersion = "2.5.23"
val alpakkaVersion = "1.1.0"
libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-slf4j" % akkaVersion,
  "com.typesafe.akka" %% "akka-stream" % akkaVersion,
  "com.typesafe.akka" %% "akka-actor" % akkaVersion,
  "com.typesafe.akka" %% "akka-remote" % akkaVersion,
  "com.typesafe.akka" %% "akka-cluster" % akkaVersion,
  "com.typesafe.akka" %% "akka-stream-testkit" % akkaVersion % Test,
  "com.typesafe.akka" %% "akka-testkit" % akkaVersion % Test
)

libraryDependencies ++= Seq(
  "com.lightbend.akka" %% "akka-stream-alpakka-amqp" % alpakkaVersion,
  "com.lightbend.akka" %% "akka-stream-alpakka-csv" % alpakkaVersion,
  "com.lightbend.akka" %% "akka-stream-alpakka-file" % alpakkaVersion
)

libraryDependencies ++= Seq(
  "com.typesafe.slick" %% "slick" % "3.2.0",
  "mysql" % "mysql-connector-java" % "5.1.+",
  "com.chuusai" %% "shapeless" % "2.3.2",
  "io.underscore" %% "slickless" % "0.3.2",
  "com.github.tototoshi" %% "slick-joda-mapper" % "2.3.0"
)

libraryDependencies ++= Seq(
  "joda-time" % "joda-time" % "2.7",
  "org.joda" % "joda-convert" % "1.7"
)

libraryDependencies += "org.scala-lang.modules" %% "scala-swing" % "2.1.1"

libraryDependencies += "com.github.tototoshi" %% "scala-csv" % "1.3.5"

libraryDependencies += "org.apache.spark" %% "spark-core" % "2.4.3" exclude("org.slf4j", "slf4j-log4j12")
libraryDependencies += "org.apache.spark" %% "spark-sql" % "2.4.3"

enablePlugins(PackPlugin)
packMain := Map("Dragon" -> "Tools.Node")
mainClass in (Compile, run) := Some("Tools.Node")

packJvmOpts := Map("Tools" -> Seq(
  "-Xmx512m"
))

scalaVersion := "2.12.8"
lazy val root = (project in file(".")).
    settings(
      name := "Tools",
      version := "0.0001"
    )
scalacOptions ++= Seq(
  "-encoding", "utf8", // Option and arguments on same line
  "-Ywarn-numeric-widen",
  //"-opt:_",
  //  "-Xlog-implicit-conversions",
  //  "-Xlog-implicits",
  //  "-Ywarn-extra-implicit",

  //  "-Xfatal-warnings",  // New lines for each options
  //  "-deprecation",
  //  "-unchecked",
  //  "-language:implicitConversions",
  //  "-language:higherKinds",
  //  "-language:existentials",
  //  "-language:postfixOps"
)

enablePlugins(sbtdocker.DockerPlugin, JavaAppPackaging)

dockerfile in docker := {
  val appDir: File = stage.value
  val targetDir = "/app"

  new Dockerfile {
    from("openjdk:8-jre")
    entryPoint(s"$targetDir/bin/${executableScriptName.value}")
    copy(appDir, targetDir)//, chown = "daemon:daemon")
  }
}
buildOptions in docker := BuildOptions(cache = false)
fork in run := true
