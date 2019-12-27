#!/usr/bin/env python3

import sys
import os
import logging
import pytest
from multiprocessing.dummy import Pool

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "../lib"))

import testlogging
import api_test_methods
import password_hasher_base

PASSWORD_HASHING_PROCESS = 0


def setup_module():
    password_hasher_base.setup_module_helper("test_post_method_hashapp_shutdown...")


def teardown_module():
    password_hasher_base.teardown_module_helper("test_post_method_hashapp_shutdown...")


def setup_function():
    global PASSWORD_HASHING_PROCESS
    PASSWORD_HASHING_PROCESS = password_hasher_base.setup_function_helper()


def teardown_function():
    password_hasher_base.teardown_function_helper(PASSWORD_HASHING_PROCESS)

def test_post_concurrent_password_hash_calls_with_shutdown_call():
    logging.info("Starting concurrent test calls with shutdown call")
    password_argument = "concurrent"
    pooled_calls = Pool(10)
    callback_pool = []
    for x in range(10):
        if x == 4:
            logging.info("Calling shutdown in the middle of the concurrent requests")
            callback_pool.append(pooled_calls.apply_async(api_test_methods.post_request_shutdown_helper, []))
        else:
            json_value = {"password": password_argument + str(x)}
            callback_pool.append(pooled_calls.apply_async(api_test_methods.post_request_hash_helper, [json_value, 200, 10]))
    for callback_response in callback_pool:
        logging.info("GET REST API call concurrent response (or shutdown response): " + str(callback_response.get()))
    logging.info("Finished concurrent test calls with shutdown call")


def main():
    logging.info("Starting test post_method_hashing_password main function")
    test_post_concurrent_password_hash_calls_with_shutdown_call()


if __name__ == "__main__":
    testlogging.get_logger(script_dir + '/../logs/password_hashing_app.log', logging.INFO, True)
    main()
