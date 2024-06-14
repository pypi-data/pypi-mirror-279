import unittest
import time
from hexon_mini import hexon_mini_client

class TestHEXON_MINI(unittest.TestCase):
    def setUp(self):
        self.client = hexon_mini_client()

    def test_move_joints(self):
        self.client.connect('localhost', port=8080)
        self.client.wait_for_connection()
        self.client.move_joints([45, 30, 15], 10)
        self.client.close_connection()

    def test_move_xyz(self):
        self.client.connect('localhost', port=8080)
        self.client.wait_for_connection()
        self.client.move_xyz(10, 20, 30, 10)
        self.client.close_connection()

    def test_open_close_gripper(self):
        self.client.connect('localhost', port=8080)
        self.client.wait_for_connection()
        self.client.open_gripper()
        time.sleep(1)
        self.client.close_gripper()
        self.client.close_connection()

if __name__ == '__main__':
    unittest.main()
