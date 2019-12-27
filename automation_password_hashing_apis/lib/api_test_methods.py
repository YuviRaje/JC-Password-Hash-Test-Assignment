#!/usr/bin/env python3

import os
import json
import requests
import logging

script_dir = os.path.dirname(__file__)

import password_hasher_base

PORT = password_hasher_base.get_property_value("port")


def post_request_hash_helper(input_data, expected_code, elapsed_time):
    json_payload = json.dumps(input_data)
    url = 'http://localhost:' + PORT + '/hash'
    logging.info("POST API hash call and json: " + url + ", " + str(input_data))
    r = requests.post(url, json_payload)
    logging.info("Expected status Code from POST REST call from query parameter:" + str(r.status_code)
                 + " ," + str(input_data))
    try:
        logging.info("POST API response: " + str(r.json()))
    except:
        logging.info("POST API response(text):  " + r.text)
    logging.info("POST REST Request elapsed time: " + str(r.elapsed.seconds))
    logging.info("POST REST response code: " + str(r.status_code))
    if r.status_code == 503:
        assert(r.status_code == 503)
    else:
        assert(r.status_code == expected_code)
        assert(r.elapsed.seconds < elapsed_time)
    try:
        return r.json()
    except:
        return "No returned response"


def get_request_hash_helper(hash_parameter, expected_code):
    url = 'http://localhost:' + PORT + '/hash/' + str(hash_parameter)
    logging.info("GET REST base64 call and hash integer parameter: " + url + ", " + str(hash_parameter))
    r = requests.get(url)
    logging.info("Status Code from GET base64 call: " + str(r.status_code))
    logging.info("GET REST base64 response: " + str(r.text))
    logging.info("GET REST base64 total elapsed time (seconds): " + str(r.elapsed.seconds))
    assert (r.status_code == expected_code)
    assert (r.elapsed.seconds < 10)
    return r.text


def get_request_stats_helper(expected_code):
    url = 'http://localhost:' + PORT + '/stats'
    logging.info("GET URL stats call: " + url)
    r = requests.get(url)
    assert (r.status_code == expected_code)
    logging.info("GET JSON stats response :" + r.text)
    assert ("TotalRequests" in r.text)
    assert ("AverageTime" in r.text)
    logging.info("GET JSON stats response :" + r.text)
    return r.text


def post_request_shutdown_helper():
    data = 'shutdown'
    url = 'http://localhost:' + PORT + '/hash/'
    logging.info("POST URL call for shutdown: " + url)
    r = requests.post(url, data)
    assert (r.status_code == 200)
    return r.text


def post_request_shutdown_helper_no_validation():
    data = 'shutdown'
    url = 'http://localhost:' + PORT + '/hash/'
    logging.info("POST URL call for shutdown (with no validation): " + url + ", " + data)
    requests.post(url, data)
