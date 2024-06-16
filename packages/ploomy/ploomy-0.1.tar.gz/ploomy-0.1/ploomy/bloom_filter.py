import socket
import select
from dataclasses import dataclass
from typing import List, Optional

from .exceptions import TimeoutError, FilterNotFoundError
from .operation.operation import Operation
from .operation.create import CreateOperation, CreateResult
from .operation.list import ListOperation, ListResult
from .operation.drop import DropOperation, DropResult
from .operation.info import InfoOperation, InfoResult
from .operation.flush import FlushOperation, FlushResult
from .operation.set_ import SetOperation, SetResult
from .operation.check import CheckOperation, CheckResult


@dataclass
class BloomConfig:
    """
    Configuration for a BloomFilter.

    :param host: The host of the BloomFilter server.
    :param port: The port of the BloomFilter server.
    :param timeout: The timeout for the connection.
    """

    host: str
    port: int
    timeout: int = 5


class BloomFilter:
    """
    A Bloom Filter client.

    :param config: The configuration for the BloomFilter.
    """

    def __init__(self, config: BloomConfig):
        self.__config = config

    def __tcp_comm(self, message: Operation) -> str:
        message = message.compile() + "\r\n"

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.__config.host, self.__config.port))
            s.sendall(message.encode("utf-8"))

            ready_to_read, _, _ = select.select([s], [], [], self.__config.timeout)

            if ready_to_read:
                response = s.recv(4096)
                return response.decode("utf-8").strip()
            else:
                raise TimeoutError("The connection timed out")

    def __check_start_end_markers(self, response: str):
        if not response.startswith("START") or not response.endswith("END"):
            raise ValueError(f"Invalid response: {response}")

    def create(
        self,
        filter_name: str,
        capacity: int,
        prob: float,
    ) -> CreateResult:
        """
        Creates a new bloom filter.

        :param filter_name: The name of the bloom filter.
        :param capacity: The capacity of the bloom filter (must be greater than 10,000).
        :param prob: The probability of false positives (must be between (0, 0.1)).

        :return: CreateResult: The result of the operation.
            - status: The status of the operation.
            - extra: Extra information about the operation (if any error occurred)
        """

        operation = CreateOperation(
            filter_name=filter_name,
            capacity=capacity,
            prob=prob,
        )

        result = self.__tcp_comm(operation)

        match result:
            case "Done":
                return CreateResult(status="DONE", extra="")
            case "Exists":
                return CreateResult(status="EXISTS", extra="")
            case "Delete in progress":
                return CreateResult(status="DELETE_IN_PROGRESS", extra="")
            case _:
                raise ValueError(f"Invalid response: {result}")

    def list(self, prefix: str) -> List[ListResult]:
        """
        Lists the bloom filters with the given prefix.

        :param prefix: The prefix used to search bloom filters.

        :return: List[ListResult]: The list of bloom filters.
            - filter_name: The name of the bloom filter.
            - capacity: The capacity of the bloom filter.
            - prob: The probability of false positives.
            - size: The size (in bytes) of bloom filter in memory.
        """

        operation = ListOperation(filter_name=prefix)
        result = self.__tcp_comm(operation)

        self.__check_start_end_markers(result)

        result_lines = result.split("\n")[1:-1]

        results = []
        for res in result_lines:
            filter_name, prob, size, capacity, _ = res.split()
            results.append(
                ListResult(
                    filter_name=filter_name,
                    capacity=int(capacity),
                    prob=float(prob),
                    size=int(size),
                )
            )

        return results

    def drop(self, filter_name: str) -> DropResult:
        """
        Drops a bloom filter.

        :param filter_name: The name of the bloom filter.

        :return: DropResult: The result of the operation.
            - status: The status of the operation.
            - extra: Extra information about the operation (if any error occurred)
        """

        operation = DropOperation(filter_name=filter_name)

        result = self.__tcp_comm(operation)

        match result:
            case "Done":
                return DropResult(status="DONE", extra="")
            case "Filter does not exist":
                raise FilterNotFoundError(f"The filter '{filter_name}' does not exist")
            case _:
                raise ValueError(f"Invalid response: {result}")

    def info(self, filter_name: str) -> InfoResult:
        """
        Gets the information of a bloom filter.

        :param filter_name: The name of the bloom filter.

        :return: InfoResult: The information of the bloom filter.
            - result: The information of the bloom filter as dictionary.
        """

        operation = InfoOperation(filter_name=filter_name)

        result = self.__tcp_comm(operation)

        self.__check_start_end_markers(result)

        if result == "Filter does not exist":
            raise FilterNotFoundError(f"The filter '{filter_name}' does not exist")

        result_lines = result.split("\n")[1:-1]

        info = {}
        for res in result_lines:
            key, value = res.split()
            if value.isdigit():
                info[key] = int(value)
            elif value.replace(".", "", 1).isdigit():
                info[key] = float(value)
            else:
                info[key] = value

        return InfoResult(result=info)

    def flush(self, filter_name: Optional[str] = "") -> FlushResult:
        """
        Flushes a bloom filter to disk.

        :param filter_name: The name of the bloom filter (optional), if not passed flushes all.

        :return: str: The status of the operation.
        """

        operation = FlushOperation(filter_name=filter_name)

        result = self.__tcp_comm(operation)

        match result:
            case "Done":
                return FlushResult(status="DONE", extra="")
            case "Filter does not exist":
                raise FilterNotFoundError(f"The filter '{filter_name}' does not exist")
            case _:
                raise ValueError(f"Invalid response: {result}")

    def set(self, filter_name: str, key: str) -> SetResult:
        """
        Sets a key in the bloom filter.

        :param filter_name: The name of the bloom filter.
        :param key: The key to set in the bloom filter.

        :return: SetResult: The result of the operation.
            - result: The result of the operation.
        """

        operation = SetOperation(filter_name=filter_name, value=key)

        result = self.__tcp_comm(operation)

        match result:
            case "Yes":
                return SetResult(status="YES")
            case "No":
                return SetResult(status="NO")
            case "Filter does not exist":
                raise FilterNotFoundError(f"The filter '{filter_name}' does not exist")
            case _:
                raise ValueError(f"Invalid response: {result}")

    def check(self, filter_name: str, key: str) -> CheckResult:
        """
        Checks if a key is in the bloom filter.

        :param filter_name: The name of the bloom filter.
        :param key: The key to check in the bloom filter.

        :return: CheckResult: The result of the operation.
            - result: The result of the operation.
        """

        operation = CheckOperation(filter_name=filter_name, value=key)

        result = self.__tcp_comm(operation)

        match result:
            case "Yes":
                return CheckResult(status="YES")
            case "No":
                return CheckResult(status="NO")
            case "Filter does not exist":
                raise FilterNotFoundError(f"The filter '{filter_name}' does not exist")
            case _:
                raise ValueError(f"Invalid response: {result}")
