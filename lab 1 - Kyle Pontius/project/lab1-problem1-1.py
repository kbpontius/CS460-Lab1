import sys
sys.path.append('..')

from src.sim import Sim
from src import node
from src import link
from src import packet

from networks.network import Network

import random

class DelayHandler(object):

    def __init__(self):
        print 
    def receive_packet(self,packet):
        print Sim.scheduler.current_time(),packet.ident,packet.created,Sim.scheduler.current_time() - packet.created,packet.transmission_delay,packet.propagation_delay,packet.queueing_delay
        self.print_data(packet)

    def print_data(self, packet):
        outputFile = open('output-problem1-1.txt', 'w')
        print >> outputFile, Sim.scheduler.current_time(), packet.ident, packet.created, Sim.scheduler.current_time() - packet.created, packet.transmission_delay, packet.propagation_delay, packet.queueing_delay
        outputFile.close()

if __name__ == '__main__':
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('config-2n-1Mbps-1000ms.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'),link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'),link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay",handler=d)

    # send one packet
    p = packet.Packet(destination_address=n2.get_address('n1'),ident=1,protocol='delay',length=1000)
    Sim.scheduler.add(delay=0, event=p, handler=n1.send_packet)

    # run the simulation
    Sim.scheduler.run()
