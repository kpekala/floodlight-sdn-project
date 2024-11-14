from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController

class CustomTopo(Topo):

    def build( self ):

        # Add hosts and switches
        kolobrzeg = self.addSwitch( 's1' )
        gdansk = self.addSwitch( 's2' )
        szczecin = self.addSwitch( 's3' )
        bydgoszcz = self.addSwitch( 's4' )
        poznan = self.addSwitch( 's5' )
        bialystok = self.addSwitch( 's6' )
        warszawa = self.addSwitch( 's7' )
        lodz = self.addSwitch( 's8' )
        wroclaw = self.addSwitch( 's9' )
        katowice = self.addSwitch( 's10' )
        krakow = self.addSwitch( 's11' )
        rzeszow = self.addSwitch( 's12' )
        kolobrzeg_host = self.addHost( 'h1' )
        gdansk_host = self.addHost( 'h2' )
        szczecin_host = self.addHost( 'h3' )
        poznan_host = self.addHost( 'h4' )
        bialystok_host = self.addHost( 'h5' )
        wroclaw_host = self.addHost( 'h6' )
        katowice_host = self.addHost( 'h7' )
        krakow_host = self.addHost( 'h8' )
        rzeszow_host = self.addHost( 'h9' )


        # Add links
        self.addLink( kolobrzeg, kolobrzeg_host )
        self.addLink( gdansk, gdansk_host )
        self.addLink( szczecin, szczecin_host )
        self.addLink( poznan, poznan_host )
        self.addLink( bialystok, bialystok_host )
        self.addLink( wroclaw, wroclaw_host )
        self.addLink( katowice, katowice_host )
        self.addLink( krakow, krakow_host )
        self.addLink( rzeszow, rzeszow_host )

        self.addLink( szczecin, kolobrzeg )
        self.addLink( szczecin, poznan )
        self.addLink( kolobrzeg, bydgoszcz )
        self.addLink( kolobrzeg, gdansk )
        self.addLink( gdansk, warszawa )
        self.addLink( gdansk, bialystok )
        self.addLink( poznan, bydgoszcz )
        self.addLink( poznan, wroclaw )
        self.addLink( bydgoszcz, warszawa )
        self.addLink( warszawa, bialystok )
        self.addLink( warszawa, lodz )
        self.addLink( warszawa, krakow )
        self.addLink( bialystok, rzeszow )
        self.addLink( lodz, katowice )
        self.addLink( lodz, wroclaw )
        self.addLink( wroclaw, katowice )
        self.addLink( katowice, krakow )
        self.addLink( krakow, rzeszow )

def topoSetup():
	topo = CustomTopo()
	net = Mininet(topo=topo, controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6653))
	net.start()
    # Run CLI for interaction
	print("wezly i polaczenia:")
	dumpNodeConnections(net.hosts)
	net.pingAll()

	CLI(net)
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	topoSetup()
