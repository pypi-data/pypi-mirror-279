# QM Simulator as a Service

Run Quantum Machines Qua simulator instances at scale.

## Supported versions
 * v2_4_0
 * v2_2_2
 * v2_2_0
 * v2_1_3

# Authentication

Your QM representative provides you an email and password to access the service.
You can use these credentials to authenticate to the service the following way:

```python
client = QoPSaaS(email="your@email.com",
                 password="password")
```

# Running your program on a simulator

You can spawn simulators and directly connect to them with your Qua program.

```python
from qm import QuantumMachinesManager, SimulationConfig
from qm.qua import play, program

from qm_saas.client import QoPSaaS, QoPVersion

config = {
    # your Qua program configuration
}

client = QoPSaaS(email="john.doe@quantum-machines.co", password="secret")

with client.simulator(QoPVersion.v2_2_2) as instance:
    qmm = QuantumMachinesManager(
        host=instance.sim_host,
        port=instance.sim_port,
        connection_headers=instance.default_connection_headers
    )

    with program() as prog:
        play("playOp", "qe1")

    qm = qmm.open_qm(config)
    job = qm.simulate(prog, SimulationConfig(int(1000)))
```

Wrapping your program in a `with` statement ensures that the simulator is properly cleaned up after the program is done running.