import sys
sys.path.append('..')

from src.sim import Sim
from src import packet
from fileParser import Parser

from networks.network import Network

import random

class DelayHandler(object):
    outputName = "output.txt"
    outputFile = file
    packetCount = -1

    def __init__(self, packetCount, outputFile):
        self.packetCount = packetCount
        self.outputFile = outputFile

    def receive_packet(self,packet):
        # if packet.ident == 999999:
        print "Current Time: %f, Packet Id: %d, Creation Time: %f, Elapsed Time: %f, TD: %f, PD: %f, QD: %f" % (Sim.scheduler.current_time(), packet.ident, packet.created, Sim.scheduler.current_time() - packet.created, packet.transmission_delay, packet.propagation_delay, packet.queueing_delay)
        print >> outputFile, Sim.scheduler.current_time(), packet.ident, packet.created, Sim.scheduler.current_time() - packet.created, packet.transmission_delay, packet.propagation_delay, packet.queueing_delay

        if packet.ident == self.packetCount - 1:
            self.endOutput()

    def endOutput(self):
        outputFile.close()

if __name__ == '__main__':
    outputFile = open('output-problem2-1a.txt', 'w')

    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('config-3n-1Mbps-1Mbps-100ms-100ms.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')

    # setup forwarding entries
    a2 = n2.get_address('n1')
    a1 = n1.get_address('n2')
    a3 = n3.get_address('n2')

    n1.add_forwarding_entry(address=a2, link=n1.links[0])
    n2.add_forwarding_entry(address=a1,link=n2.links[0])
    n2.add_forwarding_entry(address=a3,link=n2.links[1])
    n3.add_forwarding_entry(address=a2,link=n3.links[0])

    # if packet is going from n1 -> n3
    n1.add_forwarding_entry(address=a3,link=n1.links[0])

    packetCount = 100

    # setup app
    d = DelayHandler(packetCount,outputFile)
    net.nodes['n1'].add_protocol(protocol="delay",handler=d)
    net.nodes['n2'].add_protocol(protocol="delay",handler=d)
    net.nodes['n3'].add_protocol(protocol="delay",handler=d)

    for i in range(0, packetCount):
        p = packet.Packet(destination_address=a3,ident=i,protocol='delay',length=1000)
        Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # run the simulation
    Sim.scheduler.run()
