from time import sleep

from ios_device.remote.remote_lockdown import RemoteLockdownClient
from ios_device.servers.Instrument import InstrumentServer

host = 'fd34:5ffc:a411::1'
port = 54223

with RemoteLockdownClient((host, port)) as rsd:
    channel = 'com.apple.instruments.server.services.LocationSimulation'
    rpc = InstrumentServer(rsd).init()
    rpc.call(channel, "simulateLocationWithLatitude:longitude:", '25.37', '127.8')
    sleep(20)
    rpc.call(channel, "stopLocationSimulation")
    rpc.stop()
