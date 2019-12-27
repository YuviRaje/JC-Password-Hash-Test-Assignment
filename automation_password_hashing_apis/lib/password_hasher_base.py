#!/usr/bin/env python3

import os
import sys
import logging
import yaml
import subprocess
import time

script_dir = os.path.dirname(__file__)

import testlogging
import api_test_methods

YAMLCONFIGFILE = './/propertiesfile//password_hash_test_params.yaml'


def setup_module_helper(qualifier):
    logging.info("Starting initialization method in " + qualifier )
    testlogging.logback_info(script_dir + get_property_value("logfile"), logging.INFO, True)
    logging.info("Platform: " + sys.platform)
    logging.info("Finishing initialization method in " + qualifier )


def teardown_module_helper(qualifier):
    logging.info("Starting hashing_module method in " + qualifier)
    logging.info("Finishing teardown_module method in " + qualifier)


def get_os_extension():
    os_extension_name = ""
    if "darwin" == sys.platform:
        os_extension_name = "darwin"
    elif "win32" == sys.platform:
        os_extension_name = "win.exe"
    elif "linux" == sys.platform:
        os_extension_name = "linux"
    return os_extension_name


def startup_call(os_extension_name):
    try:
        logging.info("Starting hashing application")
        password_hashing_process = subprocess.Popen([".//broken-hashserve//broken-hashserve_" + os_extension_name, ""])
        return password_hashing_process
    except subprocess.CalledProcessError:
        logging.info("Hashing process did not start")
        return -1


def setup_function_helper():
    logging.info("Starting setup_function method")
    os.environ["PORT"] = get_property_value("port")
    logging.info("CWD: " + os.getcwd())
    os_extension_name = get_os_extension()

    password_hashing_process = startup_call(os_extension_name)
    logging.info("Finishing setup_function method")
    return password_hashing_process


def teardown_function_helper(password_hashing_process):
    logging.info("Starting teardown_function method")
    try:
        password_hashing_process.terminate()
    except subprocess.CalledProcessError:
        logging.info("Couldn't stop process")
    logging.info("Finishing teardown_function method")


def get_property_value(requested_key_value):
    logging.info("Opening yaml config file")
    try:
        params = yaml.safe_load(open(YAMLCONFIGFILE))
        return str(params[requested_key_value])
    except:
        logging.info("Couldn't load yaml config file: " + YAMLCONFIGFILE)




