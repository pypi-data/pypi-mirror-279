import copy
import json
import multiprocessing
import os
from multiprocessing import Process
import webbrowser
import logging

from flask import Flask
from flask_cors import CORS

from DIAL.Simulator import Simulator
from DIAL.API.ControlEndpoints import ControlEndpoints
from DIAL.API.MessageEndpoints import MessageEndpoints
from DIAL.API.StateEndpoints import StateEndpoints
from DIAL.API.TopologyEndpoints import TopologyEndpoints
from DIAL.API.SSL import SSL


class API:
    simulator: Simulator
    host: str
    port: int
    api: Flask
    initial_simulator: Simulator

    control_endpoint: ControlEndpoints
    message_endpoint: MessageEndpoints
    state_endpoint: StateEndpoints
    topology_endpoint: TopologyEndpoints

    def __init__(self, simulator: Simulator, host: str = "localhost", port: int = 10101, verbose: bool = False, open_browser: bool = True):
        self.initial_simulator = copy.deepcopy(simulator)

        self.simulator = simulator
        self.host = host
        self.port = port
        multiprocessing.set_start_method("fork")
        self.api = Flask(__name__, static_folder="web/", static_url_path="/")
        CORS(self.api)
        if not verbose:
            # Do not print every HTTP-request
            logging.getLogger("werkzeug").disabled = True

        self.control_endpoint = ControlEndpoints(api=self)
        self.message_endpoint = MessageEndpoints(api=self)
        self.state_endpoint = StateEndpoints(api=self)
        self.topology_endpoint = TopologyEndpoints(api=self)

        self.api.route('/topology', methods=['GET'])(self.topology_endpoint.get_topology)

        self.api.route('/states', methods=['GET'])(self.state_endpoint.get_states)
        self.api.route('/state/<node>/<algorithm>/<instance>', methods=['GET'])(self.state_endpoint.get_state)
        self.api.route('/state/<node>/<algorithm>/<instance>', methods=['PUT'])(self.state_endpoint.put_state)

        self.api.route('/messages', methods=['GET'])(self.message_endpoint.get_messages)
        self.api.route('/message', methods=['POST'])(self.message_endpoint.add_message)
        self.api.route('/message/<message_id>', methods=['GET'])(self.message_endpoint.get_message)
        self.api.route('/message/<message_id>', methods=['DELETE'])(self.message_endpoint.del_message)
        self.api.route('/message/<message_id>', methods=['PUT'])(self.message_endpoint.put_message)

        self.api.route('/reschedule/<message_id>/<time_str>/<theta_str>', methods=['GET'])(
            self.control_endpoint.get_reschedule)
        self.api.route('/reset', methods=['GET'])(self.control_endpoint.get_reset)
        self.api.route('/step-forward/<steps_str>', methods=['GET'])(self.control_endpoint.get_step_forward)
        self.api.route('/step-backward/<steps_str>', methods=['GET'])(self.control_endpoint.get_step_backward)
        self.api.route('/time-forward/<time_str>', methods=['GET'])(self.control_endpoint.get_time_forward)
        self.api.route('/time-backward/<time_str>', methods=['GET'])(self.control_endpoint.get_time_backward)

        p = Process(target=self.run)
        p.start()
        if open_browser:
            webbrowser.open(f"https://{host}:{port}/index.html", new=0, autoraise=True)

    def response(self, status: int, response: any):
        response = self.api.response_class(
            response=json.dumps(response, indent=4, default=str),
            status=status,
            mimetype='application/json',
        )
        return response



    def run(self):
        ssl_context = SSL().ssl_context()
        self.api.run(host=self.host, port=self.port, ssl_context=ssl_context)
