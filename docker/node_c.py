#!/usr/bin/env python
import sys
import time
import logging
from util import logcfg
from thespian.actors import ActorSystem
from capability import get_capability
logging.basicConfig(level=logging.INFO)


def main(systembase):
    actor_name = sys.argv[0].split('.')[0]
    behavior = sys.argv[1]
    capabilities = get_capability(actor_name, behavior)
    asys = ActorSystem(systembase, capabilities=capabilities, logDefs=logcfg)
    logging.info("Compute Node system started.")
    while True:
        try:
            time.sleep(2.0)
        except KeyboardInterrupt:
            asys.shutdown()


if __name__ == "__main__":
    main('multiprocTCPBase')  # multiprocQueueBase, multiprocTCPBase, multiprocUDPBase
