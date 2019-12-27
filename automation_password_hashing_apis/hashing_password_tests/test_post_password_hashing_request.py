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
    password_hasher_base.setup_module_helper("test_post_password...")


def teardown_module():
    password_hasher_base.teardown_module_helper("test_post_password...")


def setup_function():
    global PASSWORD_HASHING_PROCESS
    PASSWORD_HASHING_PROCESS = password_hasher_base.setup_function_helper()


def teardown_function():
    password_hasher_base.teardown_function_helper(PASSWORD_HASHING_PROCESS)


def test_post_concurrent_password_hash_calls():
    logging.info("Starting concurrent password_hash test calls")
    password_argument = "concurrent"
    pooled_calls = Pool(10)
    callback_pool = []
    for x in range(10):
        json_value = {"password": password_argument + str(x)}
        callback_pool.append(pooled_calls.apply_async(api_test_methods.post_request_hash_helper, [json_value, 200, 10]))
    for callback_response in callback_pool:
        logging.info("GET REST call concurrent response: " + str(callback_response.get()))
    api_test_methods.get_request_stats_helper(200)
    logging.info("Finished concurrent password_hash test calls")


@pytest.mark.parametrize("key,value,code", [
    ("password", "", 400),
    ("password", "a", 200),
    ("password", "!@#$%&*()", 200),
    ("boguskey", "password1", 400),
    ("", "password1", 400),
    ("", "", 400)
])
def test_post_parameterized_password_hash_calls(key, value, code):
    logging.info("Starting parameterized password_hash test calls")
    json_value = {key: value}
    api_test_methods.post_request_hash_helper(json_value, code, 10)
    api_test_methods.get_request_stats_helper(200)
    logging.info("Finished parameterized password_hash test calls")


def test_post_single_password_hash_call_with_long_wait():
    logging.info("Starting single long_wait test call")
    password_argument = "angrymonkey"
    json_value = {"password": password_argument}
    response = api_test_methods.post_request_hash_helper(json_value, 200, 10)
    assert(str(response).isdigit())
    api_test_methods.get_request_stats_helper(200)
    logging.info("Finished single long_wait test call")


def test_post_single_password_hash_call_with_immediate_job_identifier():
    logging.info("Starting single test call with job identifier returned immediately")
    password_argument = "angrymonkey"
    json_value = {"password": password_argument}
    response = api_test_methods.post_request_hash_helper(json_value, 200, 1)
    assert(str(response).isdigit())
    api_test_methods.get_request_stats_helper(200)
    logging.info("Finished single test call with job identifier returned immediately")


def test_post_sequential_password_hash_calls():
    logging.info("Starting sequential password_hash test calls")
    password_argument = "password"
    number_of_tries = 5
    incremented_set_of_integers = set()

    for i in range(number_of_tries):
        json_value = {"password": password_argument + str(i)}
        response = api_test_methods.post_request_hash_helper(json_value, 200, 10)
        assert (str(response).isdigit())
        try:
            incremented_set_of_integers.add(str(response))
        except:
            logging.info("Added a duplicate number, each hash call should return a unique number")
            pytest.raises(RuntimeError, "Duplicate hash number added")

    assert (len(incremented_set_of_integers) == number_of_tries)
    api_test_methods.get_request_stats_helper(200)
    logging.info("Finished sequential password_hash test calls")


def main():
    logging.info("Starting test post_method_hashing_password main function")
    test_post_single_password_hash_call()
    test_post_sequential_password_hash_calls()


if __name__ == "__main__":
    testlogging.logback_info(script_dir + '/../logs/password_hashing_app.log', logging.INFO, True)
    main()
