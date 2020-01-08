import logging
import os
import time
from thespian.actors import ActorTypeDispatcher
from thespian.actors import InvalidActorSpecification
from thespian.actors import NoCompatibleSystemForActor
from thespian.actors import requireCapability

logging.basicConfig(level=logging.INFO)

# These are actors that will be used to learn the networking of docker
# The sleeps should not be in here, but I need a delayed send.
# After Actor_Ignition gets a "start" message, it will attempt to
# create two actors with requiredCapabilties.  This will only be fulfilled
# once the other two nodes come up with those capabilities.  Then it
# will send them messages over the docker network.


@requireCapability('LEADER', 'yes')
class Actor_Ignition(ActorTypeDispatcher):
    hostname = os.environ['HOSTNAME']

    def __init__(self, *args, **kw):
        self.created_actors = {}
        logging.info("Ignition started")
        super(Actor_Ignition, self).__init__(*args, **kw)

    def receiveMsg_str(self, message, sender):
        if message == "start":
            actors_to_create = {'cn': Actor_Compute, 'sn': Actor_ServiceNode}
            logging.info("waiting for the system to start to create actors")
            while True:
                created = []
                for actor_key, actor_class in actors_to_create.items():
                    try:
                        actor = self.createActor(actor_class)
                    except InvalidActorSpecification:
                        pass
                    except NoCompatibleSystemForActor:
                        pass
                    else:
                        logging.info("created actor %s:%s", actor_class, actor_key)
                        self.created_actors[actor_key] = actor
                        created.append(actor_key)
                # remove the created actors
                for actor_key in created:
                    actors_to_create.pop(actor_key)
                if len(actors_to_create) == 0:
                    break
                time.sleep(0.5)
        elif message == "loop":
            logging.info("sending messages to actors")
            for actor_key, actor_obj in self.created_actors.items():
                self.send(actor_obj, "HI!")
            time.sleep(1.0)
        else:
            logging.error("received unknown %s", message)
        self.send(self.myAddress, "loop")


@requireCapability("node_type", "service_node")
class Actor_ServiceNode(ActorTypeDispatcher):
    hostname = os.environ['HOSTNAME']

    def receiveMsg_str(self, message, sender):
        result = "ServiceNode Received:%s" % message
        logging.info(result)
        self.send(sender, result)


@requireCapability("node_type", "compute_node")
class Actor_Compute(ActorTypeDispatcher):
    hostname = os.environ['HOSTNAME']

    def receiveMsg_str(self, message, sender):
        result = "Compute Received:%s" % message
        logging.info(result)
        self.send(sender, result)