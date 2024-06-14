import os
import websocket
import json
import threading
import time
import sys

class HEXON_MINI:
    def __init__(self):
        self.ws = None
        self.mode = os.getenv('MODE', 'realtime')  # Default to 'realtime' if not set
        self.connected_event = threading.Event()
        self.response_event = threading.Event()
        self.last_known_positions = {f'j{i}': 0 for i in range(1, 6)}  # Initialize with default positions, e.g., 0

    def connect(self, ip, port=8080):
        websocket_url = f"ws://{ip}:{port}"
        self.ws = websocket.WebSocketApp(websocket_url,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def wait_for_connection(self):
        self.connected_event.wait()

    def on_open(self, ws):
        self.connected_event.set()
        print("WebSocket connection established.")

    def on_message(self, ws, message):
        print("Received message:", message)
        try:
            data = json.loads(message)
            if data.get('type') == 'Joints_data' and data.get('requestId') == 'get-joints-data':
                self.latest_data = data.get('data')
                self.response_event.set()  # Signal that the response has been received
            elif data.get('type') == 'Cartesian_data' and data.get('requestId') == 'get-cartesian-data':
                self.latest_data = data.get('data')
                self.response_event.set()
            elif data.get('type') == 'calculate-data' and data.get('requestId') == 'calculate-joints':
                self.latest_data = data.get('data')
                self.response_event.set()
        except Exception as e:
            print("Error processing message:", e)

    def on_error(self, ws, error):
        print("Error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")

    def move_joints(self, joint_angles, velocity):
        command_type = "move-joints"
        self.wait_for_connection()
        command = {
            "type": command_type,
            "data": {"joints": joint_angles, "velocity": velocity}
        }
        self.ws.send(json.dumps(command))

    def move_xyz(self, x, y, z, velocity):
        command_type = "move-xyz"
        self.wait_for_connection()
        command = {
            "type": command_type,
            "data": {"x": x, "y": y, "z": z, "velocity": velocity}
        }
        self.ws.send(json.dumps(command))

    def close_gripper(self):
        self._send_gripper_command(False)

    def open_gripper(self):
        self._send_gripper_command(True)

    def _send_gripper_command(self, position):
        command_type = "move-gripper"
        self.wait_for_connection()
        command = {
            "type": command_type,
            "data": {"position": position, "velocity": 20, "acceleration": 10}
        }
        self.ws.send(json.dumps(command))

    def close_connection(self):
        if not self.ws:
            print("WebSocket not initialized: Skipping close operation.")
            return
        self.ws.close()
        print("WebSocket connection closed.")
