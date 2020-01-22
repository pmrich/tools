package Tools

import akka.actor.ActorSystem
import akka.cluster.Cluster
import akka.management.cluster.bootstrap.ClusterBootstrap
import akka.management.scaladsl.AkkaManagement
import akka.stream.ActorMaterializer
import com.typesafe.config.ConfigFactory

object Ignition {
  def main(args: Array[String]): Unit = {
    lazy val config = ConfigFactory.load()
    implicit val system = ActorSystem.create("akka-simple-cluster", config.getConfig("tools").withFallback(config))
    implicit val materializer = ActorMaterializer()
    implicit val executionContext = system.dispatcher
    implicit val cluster = Cluster(system)

    AkkaManagement(system).start()
    ClusterBootstrap(system).start()
  }

}
