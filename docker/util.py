#!/usr/bin/env python
import logging

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
NORMAL_FORMAT = '%(name)s - %(levelname)s - %(funcName)-13s:L#%(lineno)d:%(asctime)s>>>%(message)s'
ACTOR_FORMAT = '%(name)s - %(levelname)s - %(actorAddress)s - %(funcName)-13s:L#%(lineno)d:%(asctime)s>>>%(message)s'


class actorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' in logrecord.__dict__


class notActorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' not in logrecord.__dict__


logcfg = {'version': 1,
          'formatters': {
              'normal': {'format': NORMAL_FORMAT},
              'actor': {'format': ACTOR_FORMAT},
          },
          'filters': {'isActorLog': {'()': actorLogFilter},
                      'notActorLog': {'()': notActorLogFilter}},
          'handlers': {'h1': {'class': "logging.FileHandler",
                              'filename': 'docker_thespian.log',
                              'formatter': 'normal',
                              'filters': ['notActorLog'],
                              'level': logging.INFO},
                       'h2': {'class': "logging.StreamHandler",
                              'stream': 'ext://sys.stdout',
                              'formatter': 'actor',
                              'filters': ['isActorLog'],
                              'level': logging.INFO}, },
          'loggers': {'': {'handlers': ['h1', 'h2'], 'level': logging.INFO}}
          }