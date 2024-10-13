#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from subprocess import call

setLogLevel('info')

net = Containernet(controller=RemoteController)

info('*** Adding controller\n')
c0 = net.addController(name='c0', ip='127.0.0.1', port=6653)

info('*** Adding docker containers\n')
suricata = net.addDocker('suricata', ip='10.0.0.1/24', dimage="thanh1709/suricata_elk:latest")
victim = net.addDocker('victim', ip='10.0.0.2/24', dimage="thanh1709/ubuntu20.04:latest")
victim2 = net.addDocker('victim', ip='10.0.0.3/24', dimage="mcr.microsoft.com/windows")
attacker = net.addDocker('attacker1', ip='10.0.0.4/24', dimage="thanh1709/ubuntu20.04:latest")

info('*** Adding switch\n')
s1 = net.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
s2 = net.addSwitch('s2', cls=OVSSwitch, protocols='OpenFlow13')
s3 = net.addSwitch('s3', cls=OVSSwitch, protocols='OpenFlow13')

info('*** Creating links\n')
net.addLink(attacker, s1)
net.addLink(suricata, s2)
net.addLink(victim, s3)
net.addLink(victim2, s3)
net.addLink(s1, s2)
net.addLink(s3, s2)

info('*** Starting network\n')
net.start()

# info('*** Enable port mirroring on switch s1\n')
# s2.cmd("ovs-vsctl -- --id=@p get port s2-eth0 -- \
#     --id=@m create mirror name=m0 select-all=true output-port=@p -- \
#     set bridge s2 mirrors=@m")

info('*** Connect switch to controller\n')
c0.start()
s1.start([c0])
#s2.start([c0])
#s3.start([c0])

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network')
net.stop()