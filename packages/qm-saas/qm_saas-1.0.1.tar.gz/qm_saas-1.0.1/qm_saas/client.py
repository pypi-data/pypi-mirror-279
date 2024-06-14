import logging
from enum import Enum

import requests


class QoPSaaSInstance:
    """
    Simulator creation as context manager. Do not try to instantiate this class directly.
    Use it the following way:

    > qopsass = client.simulator(QoPVersion.v2_2_0)

    Additionally use the methods to_dict and from_dict to serialize and deserialize the instance.
    Keep in mind that some attributes are only available after the simulator has been spawned.
    """

    def __init__(self, host, port, cookies, headers, version, auto_cleanup=True, log=None):
        if type(version) is not QoPVersion:
            raise ValueError(f"version must be of type QoPSaaSVersion, not {type(version)}")
        self.api_host = host
        self.api_port = port
        self.api_protocol = "https"
        self.headers = headers.copy()
        self.cookies = cookies
        self.version = version.value

        self.spawned = False
        self.auto_cleanup = auto_cleanup
        self.sim_port = None
        self.sim_host = None
        self.sim_id = None
        self.log = log or logging.getLogger(__name__)

    def to_dict(self):
        return dict(
            api_host=self.api_host,
            api_port=self.api_port,
            sim_host=self.sim_host,
            sim_port=self.sim_port,
            sim_id=self.sim_id,
            version=self.version,
            headers=self.headers,
            cookies=self.cookies,
            spawned=self.spawned,
            auto_cleanup=self.auto_cleanup,
        )

    @staticmethod
    def from_dict(
        sim_host, sim_port, api_host, api_port, cookies, headers, version, spawned, sim_id, auto_cleanup, log=None
    ):
        """
        Creates a QoPSaaSInstance from a dict
        """
        # version is a string but we want to use the enum
        ver = QoPVersion(version)
        qops = QoPSaaSInstance(
            host=api_host,
            port=api_port,
            cookies=cookies,
            headers=headers,
            version=ver,
            auto_cleanup=auto_cleanup,
            log=log,
        )
        qops.sim_host = sim_host
        qops.sim_port = sim_port
        qops.spawned = spawned
        qops.sim_id = sim_id
        return qops

    def __enter__(self):
        self.spawn()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def spawn(self):
        """
        Spawns the simulator instance on the QoPSaaS platform.
        This is a blocking operation.

        The simulator is spawned only once, subsequent calls to this method
        will not spawn a new simulator.
        """
        if not self.spawned:
            self.sim_id = self._create_simulator(self.version)
            # the token is used to authenticate and identify this specific simulation instance
            self.headers["Simulation"] = self.sim_id
            self.spawned = True

    def close(self):
        """
        Destroy the remote simulator and close the session.
        This operation is idempotent and can be called multiple times.
        """
        # A delete request to /api/v1/simulator/' with cookies, token and Authorization in the headers
        # will destroy the remote simulator and close the session
        if not self.spawned:
            self.log.debug("Simulator was not spawned, nothing to close")
            return
        if not self.auto_cleanup:
            self.log.debug("Simulator was spawned but autocleanup is disabled, nothing to close")
            return
        simulator_url = f"{self.api_protocol}://{self.api_host}:{self.api_port}/api/v1/simulator/"
        self.log.debug(f"Deleting simulator at {simulator_url}")

        response = requests.delete(simulator_url, headers=self.headers, cookies=self.cookies)
        if response.status_code not in (200, 201):
            self.log.error(f"HTTP {response.status_code}: {response.text}")
            raise ValueError(
                f'Deletion of simulation instance failed ({response.status_code}). Message {response.json().get("message", "no message provided")}'
            )
        else:
            self.log.info("Simulator deleted successfully")
            # reset the headers, although the cookies are still valid.
            # It is not a good to reuse the instance after it has been closed
            # but it should be possible (untested)
            self.spawned = False
            self.sim_host = None
            self.sim_port = None
            self.sim_id = None
            del self.headers["Simulation"]

    def _request(self, version):
        simulator_url = f"{self.api_protocol}://{self.api_host}:{self.api_port}/api/v1/simulator/{version}"
        self.log.debug(f"Creating simulator at {simulator_url} with headers: {self.headers}")
        response = requests.post(simulator_url, headers=self.headers, cookies=self.cookies, verify=True)
        if response.status_code not in (200, 201):
            self.log.error(f"HTTP {response.status_code}: {response.text}")
            try:
                j = response.json()
                msg = j.get("message", "No message provided")
            except requests.exceptions.JSONDecodeError:
                msg = response.text

            raise ValueError(f"Creation of simulation instance failed ({response.status_code}). Message: {msg}")
        else:
            # We got a valid response from the server but its contents
            # may be invalid
            j = response.json()
            if not ("token" in j and "host" in j and "port" in j):
                self.log.error(response.text)
                raise ValueError(
                    f'Creation of simulation instance failed (HTTP {response.status_code}). Message {response.json().get("message", "no message provided")}'
                )

            self._sim_token = j["token"]
            self.sim_host = j["host"]
            self.sim_port = j["port"]
            self.log.info(f"Simulator created at {self.sim_host}:{self.sim_port} with token {self._sim_token}")
            return self._sim_token

    def _create_simulator(self, version):
        if version is None:
            raise ValueError("version must be provided")
        simulation_id = self._request(version)
        return simulation_id

    @property
    def qm_manager_parameters(self):
        if not self.spawned:
            raise ValueError("Simulator was not spawned")
        return dict(host=self.sim_host, port=self.sim_port, connection_headers=self.sim_token)

    @property
    def default_connection_headers(self):
        return {"simulation-auth": self.sim_id}

    @property
    def sim_token(self):
        return self.sim_id


class QoPSaaS:
    """
    QoPSaaS class for creating a simulator on the QoPSaaS platform.

    host: the host of the QoPSaaS platform
    port: the port of the QoPSaaS platform
    version: the version of the simulator to use

    Provide authentication credentials to the simulator.
    either email and password or bearer_token must be provided.

    email: the email of the user
    password: the password of the user
    token_path: the path to the bearer token file to avoid re-authentication
    cookie_path: the path to the cookie file to avoid re-authentication
    verbose: print debug messages
    autocleanup: automatically delete the simulator instance when the context manager exits
                 otherwise it will be left running and timeout after 15 minutes

    Usage:

    > client = QoPSaaS(host, port, version, email, password, cookie_path="cookie.txt")
    >
    > QMm = QuantumMachinesManager(host=instance.qm_manager_parameters['host'],
    >                        port=instance.qm_manager_parameters['port'],
    >                        connection_headers={
    >                            "simulation-auth": instance.qm_manager_parameters['connection_headers']}
    >                         )
    >    # your QUA program

    """

    def __init__(
        self,
        host="simulator.qopsim.prod.quantum-machines.co",
        port=9000,
        email=None,
        password=None,
        auto_cleanup=True,
        log=None,
    ):
        self._host = host
        self._port = port
        self._protocol = "https"
        self.cookies = None
        self.log = log or logging.getLogger(__name__)
        self._headers = {
            "x-appwrite-response-format": "1.0.0",
            "Content-Type": "application/json",
            "X-Appwrite-Project": "64e38dcad0ed251cb8f9",
        }
        self._email = email
        self._password = password
        self._authenticate(self._email, self._password)

        # here the context manager is created
        def _sim(version, auto_cleanup=auto_cleanup):
            """
            If auto_cleanup is True, the simulator will be deleted when the context manager exits.
            Otherwise it will be left running and timeout after 15 minutes

            If no value is provided the setting of the QoPSaaS class is used
            """
            return QoPSaaSInstance(
                auto_cleanup=auto_cleanup,
                host=self._host,
                port=self._port,
                version=version,
                cookies=self.cookies,
                headers=self._headers,
                log=self.log,
            )

        self.simulator = _sim

    def _authenticate(self, email, password):
        if not self.cookies or len(self.cookies) == 0:
            auth_url = f"{self._protocol}://{self._host}/v1/account/sessions/email"
            logging.info(f"Authenticating with email and password on {auth_url}")
            auth_body = {"email": email, "password": password}

            response = requests.post(auth_url, headers=self._headers, json=auth_body)
            if response.status_code not in (200, 201):
                error = response.json().get("message", "no message provided")
                self.log.error(error)
                raise ValueError(f"Authentication failed with status code {response.status_code} and message {error}")
            cookies = response.cookies.get_dict()
            self.cookies = cookies

        jwt_auth_url = f"{self._protocol}://{self._host}/v1/account/jwt"
        logging.info("Getting JWT token from {jwt_auth_url}")
        # cookies are now in place, get a JWT token
        response = requests.post(jwt_auth_url, headers=self._headers, cookies=self.cookies)
        if response.status_code not in (200, 201):
            raise ValueError(
                f"Authentication failed with status code {response.status_code} and message {response.json()}"
            )
        auth_token = response.json()["jwt"]

        self._headers["Authorization"] = auth_token

    @property
    def port(self):
        return self._port

    @property
    def host(self):
        return self._host


class QoPVersion(Enum):
    # An enum of the available QoP Versions
    v2_4_0 = "v2_4_0"
    v2_2_2 = "v2_2_2"
    v2_2_0 = "v2_2_0"
    v2_1_3 = "v2_1_3"
