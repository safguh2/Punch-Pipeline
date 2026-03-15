import socket
import logging
import json

logger = logging.getLogger(__name__)


class SotApi:
    def __init__(self, ipaddress, port):
        self.socket = None
        self.ipaddress = ipaddress
        self.port = port

    def connect(self):
        print("connecting")
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ipaddress, self.port))
        logger.info(f"Connected to SOT at {self.ipaddress}:{self.port}")

    def disconnect(self):
        self.socket.close()
        logger.info(f"Closed connection with SOT at {self.ipaddress}:{self.port}")

    def send_requests(self, requests: list, max_retries: int = 5) -> bool:
        try:
            index = 0
            while index < len(requests):
                request = requests[index]
                retries = 0
                sent = False

                while not sent:
                    if retries > max_retries:
                        logger.error(
                            f"Request #{index} exceeded max retries ({max_retries}). Aborting."
                        )
                        return False

                    # Wrap and send the request
                    self._send_message(request)
                    logger.debug(f"Sent request #{index} (attempt {retries + 1}): {request  }")

                    # Wait for SOT server response
                    response = self._receive_message()
                    if response is None:
                        logger.error("Connection closed by SOT server unexpectedly.")
                        return False

                    action = response.get("Action")
                    logger.debug(f"SOT response for request #{index}: {response}")

                    if action == "next":
                        logger.info(f"Request #{index} acknowledged. Moving to next.")
                        sent = True
                    elif action == "retry":
                        retries += 1
                        logger.warning(f"Request #{index} asked to retry (attempt {retries}).")
                    else:
                        logger.error(f"Unknown action from SOT: '{action}'. Aborting.")
                        return False

                index += 1

            # Signal end of transmission
            done_signal = {"code": 0, "data": []}
            self._send_message(done_signal)
            logger.info("All requests sent. Done signal transmitted.")
            return True

        except (ConnectionRefusedError, OSError) as e:
            logger.error(f"Socket error while communicating with SOT: {e}")
            return False

    def _send_message(self, payload: dict) -> None:
        """Serialise payload to JSON, length-prefix it, and send over the socket."""
        raw = json.dumps(payload).encode("utf-8")
        # 4-byte big-endian length prefix so the receiver knows where the message ends
        length_prefix = len(raw).to_bytes(4, byteorder="big")
        #print(length_prefix.decode())
        #print(int.from_bytes(len(raw).to_bytes(4, byteorder="big")))
        self.socket.sendall(length_prefix + raw)

    def _receive_message(self) -> dict | None:
        raw_length = self._recv_exact(4)
        if raw_length is None:
            return None
        print("got response")
        message_length = int.from_bytes(raw_length, byteorder="little")
        print(message_length)
        raw_body = self._recv_exact(message_length)
        if raw_body is None:
            return None

        try:
            return json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse SOT response as JSON: {e}")
            return None

    def _recv_exact(self, n: int) -> bytes | None:
        """Read exactly n bytes from the socket, returning None if the connection closes."""
        buf = b""
        while len(buf) < n:
            chunk = self.socket.recv(n - len(buf))
            if not chunk:
                return None
            buf += chunk
        return buf
