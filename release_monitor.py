#!/usr/bin/env python3
import json
import logging
import os
import signal
import sys
import time

import feedparser
import psutil
import requests
from f8a_worker.setup_celery import init_celery, init_selinon
from selinon import run_flow

from defaults import NPM_URL, PYPI_URL, ENABLE_SCHEDULING, \
    PROBE_FILE_LOCATION, SLEEP_INTERVAL

logger = logging.getLogger(__name__)


def handler(signum, frame):
    logger.debug("Running Liveness Probe")
    if ENABLE_SCHEDULING:
        run_flow('livenessFlow', [None])
    else:
        logger.debug("Liveness probe - livenessFlow"
                     " did not run since selinon is not initialized")

    basedir = os.path.dirname(PROBE_FILE_LOCATION)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    with open(PROBE_FILE_LOCATION, 'a'):
        os.utime(PROBE_FILE_LOCATION, None)

    logger.debug("Liveness probe - finished")


def run_liveness():
    # Remove all temp files to ensure that there are no leftovers
    if os.path.isfile(PROBE_FILE_LOCATION):
        os.remove(PROBE_FILE_LOCATION)

    for pid in psutil.process_iter():
        if pid.pid == 1:
            pid.send_signal(signal.SIGUSR1)
            time.sleep(10)

    sys.exit(0 if os.path.isfile(PROBE_FILE_LOCATION) else 1)


def write_package_info_to_file(node_args, file_path):
    with open(file_path, "a+") as f:
        f.write(node_args)
    return True


def was_package_processed(ecosystem, name, version):
    return False


class ReleaseMonitor():
    """Class which check rss feeds for new releases"""

    def __init__(self):
        self.log = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging_handler = logging.StreamHandler(sys.stdout)
        logging_handler.setFormatter(formatter)
        self.log.addHandler(logging_handler)
        self.log.level = logging.DEBUG
        self.old_npm_feed = None
        self.npm_feed = feedparser.parse(NPM_URL + "-/rss")
        self.old_pypi_feed = None
        self.pypi_feed = feedparser.parse(PYPI_URL + "rss/updates.xml")

        if ENABLE_SCHEDULING:
            init_celery(result_backend=False)
            init_selinon()

    def run_package_analisys(self, name, ecosystem, version):
        """Run Selinon flow for analyses.
         :param name: name of the package to analyse
         :param version: package version
         :param ecosystem: package ecosystem
         :return: dispatcher ID serving flow
         """

        node_args = {
            'ecosystem': ecosystem,
            'name': name,
            'version': version,
            'recursive_limit': 0
        }

        self.log.info("Scheduling Selinon flow '%s' with node_args: '%s'", 'bayesianFlow', node_args)
        return run_flow('bayesianFlow', node_args)

    def entry_not_in_previous_npm_set(self, entry):
        if entry in self.old_npm_feed:
            return False
        else:
            return True

    def entry_not_in_previous_pypi_set(self, entry):
        if entry in self.old_pypi_feed:
            return False
        else:
            return True

    def renew_rss_feeds(self):
        if sorted(self.old_pypi_feed.entries) == sorted(self.pypi_feed.entries):
            self.pypi_feed = feedparser.parse(PYPI_URL + "rss/updates.xml")
        else:
            self.old_pypi_feed = self.pypi_feed

        if sorted(self.old_npm_feed.entries) == sorted(self.npm_feed.entries):
            self.npm_feed = feedparser.parse(NPM_URL + "-/rss")
        else:
            self.old_pypi_feed = self.pypi_feed

    def run(self):
        while True:
            for i in self.npm_feed.entries:
                package_name = i['title']
                package_url = NPM_URL + "-/package/{package_name}/dist-tags".format(package_name=package_name)
                package_latest_version = json.loads(
                    requests.get(package_url, headers={'content-type': 'application/json'}).text)
                self.log.info("Processing package from npm: '%s':'%s'", package_name,
                              package_latest_version.get('latest'))
                if ENABLE_SCHEDULING and self.entry_not_in_previous_npm_set(i):
                    # self.run_package_analisys(package_name, 'npm', package_latest_version)
                    print({'package_name': package_name,
                           'latest_version': package_latest_version
                           })

            for i in self.pypi_feed.entries:
                package_name, package_latest_version = i['title'].split(' ')
                self.log.info("Processing package from pypi: '%s':'%s'", package_name, package_latest_version)
                if ENABLE_SCHEDULING and self.entry_not_in_previous_pypi_set(i):
                    # self.run_package_analisys(package_name, 'pypi', package_latest_version)
                    print({'package_name': package_name,
                           'latest_version': package_latest_version
                           })

        self.renew_rss_feeds()




if __name__ == '__main__':
    monitor = ReleaseMonitor()
    monitor.run()
