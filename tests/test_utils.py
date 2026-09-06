import unittest

from scanner.utils import parse_ports, validate_ipv4, validate_network


class TestUtils(unittest.TestCase):
    def test_parse_ports(self):
        self.assertEqual(parse_ports("22,80,443"), [22, 80, 443])
        self.assertEqual(parse_ports("80-82"), [80, 81, 82])
        self.assertEqual(parse_ports("22,80-82"), [22, 80, 81, 82])

    def test_invalid_port(self):
        with self.assertRaises(ValueError):
            parse_ports("0,80")

    def test_ipv4(self):
        self.assertEqual(validate_ipv4("192.168.1.10"), "192.168.1.10")

    def test_network(self):
        self.assertEqual(str(validate_network("192.168.1.12/24")), "192.168.1.0/24")


if __name__ == "__main__":
    unittest.main()
