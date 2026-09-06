import socket
import threading
import unittest

from scanner.ports import scan_ports


class TestPorts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.server.bind(("127.0.0.1", 0))
        cls.server.listen()
        cls.port = cls.server.getsockname()[1]
        cls.stop = False

        def accept_loop():
            cls.server.settimeout(0.2)
            while not cls.stop:
                try:
                    conn, _ = cls.server.accept()
                    conn.close()
                except socket.timeout:
                    continue
                except OSError:
                    break

        cls.thread = threading.Thread(target=accept_loop, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.stop = True
        cls.server.close()
        cls.thread.join(timeout=1)

    def test_open_port(self):
        results = scan_ports("127.0.0.1", [self.port], workers=2, timeout=0.5)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].port, self.port)
        self.assertEqual(results[0].state, "open")


if __name__ == "__main__":
    unittest.main()
