**JumpCloud Password Hashing Application:**

**Objective:**

It's a password hashing application test assignment for four REST endpoints.

**Platforms and IDEs**

This was developed using python 3.8.1 and PyCharm 4.5 on a windows environment. Password hashing application execution archive file contains binaries for Linux, Windows & Mac OS X
operating systems. Unpack and use the binary corresponding to your OS of choice.

**Resource Endpoints**

| Method | Resource Endpoint | URL Parameters               | JSON Payload             |
| ------ | ----------------- | ---------------------------- | ------------------------ |
| `POST` | `/hash`           | N/A                          | "password":"angrymonkey" |
| `GET`  | `/hash`           | `id` the 32 character job ID | N/A                      |
| `GET`  | `/stats`          | N/A                          | N/A                      |
| `POST` | `/hash            | N/A                          | 'shutdown'               |

**Test Execution:**

To run a specific set of tests

pytest -k automation_password_hashing_apis/test_post_single_ password_hash_call_with_immediate_job_identifier

To run entire  tests:

pytest hashing_password_tests/

**Test Results**:

Tests Failed - 5

Tests Passed - 10

![image-20191226180802161](C:\Users\jadhay\AppData\Roaming\Typora\typora-user-images\image-20191226180802161.png)



**ToDo**

- More tests refactoring

- Modular structure and usage of Python classes

- Possibly addition of more test coverage for both hashing patterns.

  

