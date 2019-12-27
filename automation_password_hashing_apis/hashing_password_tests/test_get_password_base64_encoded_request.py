#!/usr/bin/env python3

import sys
import os
import logging
import junit_xml
import hashlib
import pytest
import codecs

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, "../lib"))

import testlogging
import api_test_methods
import password_hasher_base

PASSWORD_HASHING_PROCESS = 0


def setup_module():
    password_hasher_base.setup_module_helper("test_get_password_base64_encoded...")

def teardown_module():
    password_hasher_base.teardown_module_helper("test_get_password_base64_encoded...")

def setup_function():
    global PASSWORD_HASHING_PROCESS
    PASSWORD_HASHING_PROCESS = password_hasher_base.setup_function_helper()

def teardown_function():
    password_hasher_base.teardown_function_helper(PASSWORD_HASHING_PROCESS)


@pytest.mark.skip(reason="Unexpected results")
def test_get_password_hash_call():
    password_argument = "angrymonkey"
    json_value = {"password": password_argument}
    response = api_test_methods.post_request_hash_helper(json_value, 200)
    logging.info("Returned Value from POST request: " + str(response))
    returned_base64_encoding = api_test_methods.get_request_hash_helper(response, 200)
    message = hashlib.sha512(password_argument.encode()).hexdigest()
    logging.info("Sha512 hex digest: " + message)
    b64 = codecs.encode(codecs.decode(message, 'hex'), 'base64').decode()
    b64 = b64.replace('\n', '')
    logging.info("Base64 expected string: " + b64)
    assert (str(returned_base64_encoding) == b64)
    assert (len(str(returned_base64_encoding)) == 88)


def test_get_password_hash_with_invalid_number():
    logging.info("Starting get base64 encoded hash call with invalid number")
    password_argument = "testpassword@1234"
    json_value = {"password": password_argument}
    response = api_test_methods.post_request_hash_helper(json_value, 200, 10)
    assert (str(response).isdigit())
    response = api_test_methods.get_request_hash_helper(99, 400)
    assert ("Hash not found" in str(response))
    logging.info("Finished get base64 encoded hash call with invalid number")

def test_get_password_hash_with_ascii_character():
    logging.info("Starting get base64 encoded hash call with ascii character")
    password_argument = "testpassword@1234"
    json_value = {"password": password_argument}
    response = api_test_methods.post_request_hash_helper(json_value, 200, 10)
    response = api_test_methods.get_request_hash_helper('a', 400)
    assert ("strconv.Atoi:" in str(response))
    assert ("invalid syntax" in str(response))
    logging.info("Finished get base64 encoded hash call with ascii character")


def main():
    logging.info("Starting test get_method_hashed_password_base64_encoded main function")
    test_get_password_hash_call()


if __name__ == "__main__":
    testlogging.logback_info(script_dir + '/../logs/password_hashing_app.log', logging.INFO, True)
    main()
