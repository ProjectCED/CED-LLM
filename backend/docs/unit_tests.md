# Unit tests

This document provides an overview of the unit tests for the backend of the CED-LLM project.

## Table of Contents

- [Unit tests](#unit-tests)
    - [api_handler](#api_handler)
    - [backend_api](#backend_api)
    - [database](#database)
    - [utils](#utils)

## API Handler

The `api_handler` module contains the `APIHandler` class, which is responsible for handling the API requests. The unit tests for this module are located in the `tests/test_api_handler.py` file.

The `APIHandler` class is tested using the `unittest` module. The tests are organized into test cases, each of which tests a specific aspect of the `APIHandler` class. The test cases are defined as subclasses of the `unittest.TestCase` class.

The `APIHandler` class is tested using a combination of unit tests and integration tests. The unit tests focus on testing the individual methods of the `APIHandler` class in isolation, while the integration tests focus on testing the interactions between the methods.

::: app.api_handler

## Backend API

The `backend_api` module contains the `BackendAPI` class, which is responsible for interacting with the backend API. The unit tests for this module are located in the `tests/test_backend_api.py` file.

The `BackendAPI` class is tested using the `unittest` module. The tests are organized into test cases, each of which tests a specific aspect of the `BackendAPI` class. The test cases are defined as subclasses of the `unittest.TestCase` class.

The `BackendAPI` class is tested using a combination of unit tests and integration tests. The unit tests focus on testing the individual methods of the `BackendAPI` class in isolation, while the integration tests focus on testing the interactions between the methods.

::: app.backend_api

## Database

The `database` module contains the `Database` class, which is responsible for interacting with the database. The unit tests for this module are located in the `tests/test_database.py` file.

The `Database` class is tested using the `unittest` module. The tests are organized into test cases, each of which tests a specific aspect of the `Database` class. The test cases are defined as subclasses of the `unittest.TestCase` class.

The `Database` class is tested using a combination of unit tests and integration tests. The unit tests focus on testing the individual methods of the `Database` class in isolation, while the integration tests focus on testing the interactions between the methods.

::: app.database

## Utils

The `utils` module contains utility functions used throughout the backend. The unit tests for this module are located in the `tests/test_utils.py` file.

The utility functions are tested using the `unittest` module. The tests are organized into test cases, each of which tests a specific utility function. The test cases are defined as subclasses of the `unittest.TestCase` class.

The utility functions are tested using a combination of unit tests and integration tests. The unit tests focus on testing the individual utility functions in isolation, while the integration tests focus on testing the interactions between the utility functions.

::: app.utils
