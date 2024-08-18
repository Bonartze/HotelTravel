import pytest
import socket


def test_calculations():
    test_cases = [
        {"message": b'median\n', "expected": 108.99, "precision": 2},
        {"message": b'std_deviation\n', "expected": 72, "precision": 1},
        {"message": b'average_hotel_price\n', "expected": 121.27, "precision": 2},
        {"message": b'average_rating\n', "expected": 8.5, "precision": 1},
        {"message": b'correlation_price_rating\n', "expected": 0.33, "precision": 2}
    ]

    for case in test_cases:
        print(f"Testing {case['message'].decode('utf-8')}...")

        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect(('127.0.0.1', 8888))
            connection.sendall(case['message'])
            response = connection.recv(1024).decode('utf-8').strip()
            print(f"Received: {response}")

            connection.close()
        except ConnectionRefusedError:
            pytest.fail("Could not connect to the server. Ensure the server is running.")
        except socket.error as e:
            pytest.fail(f"Failed to communicate with the server: {e}")

        try:
            numeric_response = float(response)
        except ValueError:
            pytest.fail(f"Expected a numeric response, but got: {response}")

        assert round(numeric_response, case['precision']) == case['expected'], (
            f"Expected {case['message'].decode('utf-8')} to be {case['expected']}, but got {numeric_response}"
        )
