
#!/usr/bin/env python3


import sys
import os
import logging
import junit_xml
import re

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "../lib"))

import testlogging
import api_test_methods
import password_hasher_base

PASSWORD_HASHING_PROCESS = 0


def setup_module():
    password_hasher_base.setup_module_helper("test_get_stats_request...")


def teardown_module():
    password_hasher_base.teardown_module_helper("test_get_stats_request...")


def setup_function():
    global PASSWORD_HASHING_PROCESS
    PASSWORD_HASHING_PROCESS = password_hasher_base.setup_function_helper()


def teardown_function():
    password_hasher_base.teardown_function_helper(PASSWORD_HASHING_PROCESS)


def test_get_stats_no_data():
    logging.info("Starting test_get_stats_no_data call")
    response = api_test_methods.get_request_stats_helper(200)
    assert("0" in response)
    pattern = re.compile(r'^\{.*:0,.*:0\}$')
    match = pattern.match(response)
    if match:
        logging.info("matched 0 stats result")
        assert match
    else:
        logging.info("No match for no stats call!")
    logging.info("Finished test_get_stats_no_data call")


def test_get_stats_one_request():
    logging.info("Starting test_get_stats_one_request for one request")
    password_argument = "statsRequestForOneRequest1"
    json_value = {"password": password_argument}
    response = api_test_methods.post_request_hash_helper(json_value, 200, 10)
    assert (str(response).isdigit())
    response = api_test_methods.get_request_stats_helper(200)
    pattern = re.compile(r'^\{.*:1,.*:[0-9]{4,7}\}$')
    match = pattern.match(response)
    if match:
        logging.info("matched stats result for one hash request")
        assert match
    else:
        logging.info("No match for stats results for one hash request!")
    logging.info("Finished test_get_stats_one_request for one request")


def main():
    logging.info("Starting test get_method_hash_stats main function")
    test_get_stats_no_data()
    test_get_stats_one_request()


if __name__ == "__main__":
    testlogging.logback_info(script_dir + '/../logs/password_hashing_app.log', logging.INFO, True)
    main()
