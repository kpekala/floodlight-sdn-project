#!/usr/bin/python
import json

import httplib
import os
import subprocess
import time
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.util import irange

HOME_FOLDER = os.getenv('HOME')


class LinearTopo(Topo):
    """
    construct a network of N hosts and N-1 switches, connected as follows:
    h1 <-> s1 <-> s2 .. sN-1
           |       |    |
           h2      h3   hN

    """
    def __init__(self, N, **params):
        Topo.__init__(self, **params)

        hosts = [ self.addHost( 'h%s' % h )
                  for h in irange( 1, N ) ]

        switches = [ self.addSwitch( 's%s' % s, protocols=["OpenFlow13"] )
                     for s in irange( 1, N - 1 ) ]

        # Wire up switches
        last = None
        for switch in switches:
            if last:
                self.addLink( last, switch )
            last = switch


        # Wire up hosts
        self.addLink( hosts[ 0 ], switches[ 0 ] )
        for host, switch in zip( hosts[ 1: ], switches ):
            self.addLink( host, switch )


def getControllerIP():
    guest_ip = subprocess.check_output("/sbin/ifconfig eth1 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'",
                                       shell=True)
    split_ip = guest_ip.split('.')
    split_ip[3] = '1'
    return '.'.join(split_ip)


def rest_call(path, data, action):
    headers = {
        'Content-type': 'application/json',
        'Accept'      : 'application/json',
    }
    body = json.dumps(data)

    conn = httplib.HTTPConnection(getControllerIP(), 8080)
    conn.request(action, path, body, headers)
    response = conn.getresponse()

    ret = (response.status, response.reason, response.read())
    conn.close()
    return ret


def addVirtualGateway(name):
    data = {
        "gateway-name" : name,
        "gateway-mac" : "aa:bb:cc:dd:ee:ff"
    }
    ret = rest_call('/wm/routing/gateway', data, 'POST')
    return ret


def addInterfaceToGateway(name):
    data = {
        "interfaces" : [
            {
                "interface-name" : "interface-1",
                "interface-ip" : "10.0.0.1",
                "interface-mask" : "255.255.255.0"
            },
            {
                "interface-name" : "interface-2",
                "interface-ip" : "20.0.0.1",
                "interface-mask" : "255.255.255.0"
            },
            {
                "interface-name" : "interface-3",
                "interface-ip" : "30.0.0.1",
                "interface-mask" : "255.255.255.0"
            },
            {
                "interface-name" : "interface-4",
                "interface-ip" : "40.0.0.1",
                "interface-mask" : "255.255.255.0"
            },
            {
                "interface-name" : "interface-5",
                "interface-ip" : "50.0.0.1",
                "interface-mask" : "255.255.255.0"
            }
        ]
    }
    ret = rest_call('/wm/routing/gateway/' + name, data, 'POST')
    return ret


def addSwitchToGateway(name):
    data = {
        "gateway-name" : name,
        "gateway-ip" : "127.0.0.1",
        "switches": [
            {
                "dpid": "1"
            },
            {
                "dpid": "2"
            },
            {
                "dpid": "3"
            },
            {
                "dpid": "4"
            },
            {
                "dpid": "5"
            }
        ]
    }
    ret = rest_call('/wm/routing/gateway/' + name, data, 'POST')
    return ret


def addDHCPInstance1(name):
    data = {
        "name"         : name,
        "start-ip"     : "10.0.0.101",
        "end-ip"       : "10.0.0.200",
        "server-id"    : "10.0.0.2",
        "server-mac"   : "aa:bb:cc:dd:ee:ff",
        "router-ip"    : "10.0.0.1",
        "broadcast-ip" : "10.0.0.255",
        "subnet-mask"  : "255.255.255.0",
        "lease-time"   : "60",
        "ip-forwarding": "true",
        "domain-name"  : "mininet-domain-name"
    }
    ret = rest_call('/wm/dhcp/instance', data, 'POST')
    return ret


def addDHCPInstance2(name):
    data = {
        "name"         : name,
        "start-ip"     : "20.0.0.101",
        "end-ip"       : "20.0.0.200",
        "server-id"    : "20.0.0.2",
        "server-mac"   : "aa:bb:cc:dd:ee:ff",
        "router-ip"    : "20.0.0.1",
        "broadcast-ip" : "20.0.0.255",
        "subnet-mask"  : "255.255.255.0",
        "lease-time"   : "60",
        "ip-forwarding": "true",
        "domain-name"  : "mininet-domain-name"
    }
    ret = rest_call('/wm/dhcp/instance', data, 'POST')
    return ret


def addSwitchToDHCPInstance1(name):
    data = {
        "switches": [
            {
                "dpid": "1"
            },
            {
                "dpid": "2"
            }
        ]
    }
    ret = rest_call('/wm/dhcp/instance/' + name, data, 'POST')
    return ret


def addSwitchToDHCPInstance2(name):
    data = {
        "switches": [
            {
                "dpid": "3"
            },
            {
                "dpid": "4"
            },
            {
                "dpid": "5"
            }
        ]
    }
    ret = rest_call('/wm/dhcp/instance/' + name, data, 'POST')
    return ret


def enableDHCPServer():
    data = {
        "enable" : "true",
        "lease-gc-period" : "10",
        "dynamic-lease" : "false"
    }
    ret = rest_call('/wm/dhcp/config', data, 'POST')
    return ret


# DHCP client functions
def startDHCPclient(host):
    "Start DHCP client on host"
    intf = host.defaultIntf()
    host.cmd('dhclient -v -d -r', intf)
    host.cmd('dhclient -v -d 1> /tmp/dhclient.log 2>&1', intf, '&')


def stopDHCPclient(host):
    host.cmd('kill %dhclient')


def waitForIP(host):
    "Wait for an IP address"
    info('*', host, 'waiting for IP address')
    while True:
        host.defaultIntf().updateIP()
        if host.IP():
            break
        info('.')
        time.sleep(1)
    info('\n')
    info('*', host, 'is now using',
         host.cmd('grep nameserver /etcresolv.conf'))


def mountPrivateResolvconf(host):
    "Create/mount private /etc/resolv.conf for host"
    etc = '/tmp/etc-%s' % host
    host.cmd('mkdir -p', etc)
    host.cmd('mount --bind /etc', etc)
    host.cmd('mount -n -t tmpfs tmpfs /etc')
    host.cmd('ln -s %s/* /etc/' % etc)
    host.cmd('rm /etc/resolv.conf')
    host.cmd('cp %s/resolv.conf /etc/' % etc)


def unmountPrivateResolvconf(host):
    "Unmount private /etc dir for host"
    etc = '/tmp/etc-%s' % host
    host.cmd('umount /etc')
    host.cmd('umount', etc)
    host.cmd('rmdir', etc)


def configureDefaultGatewayForHost(host, defaultGatewayIP):
    host.cmd('route add default gw ' + defaultGatewayIP);


def enableL3Routing():
    data = {
        "enable" : "true"
    }
    ret = rest_call('/wm/routing/config', data, 'POST')
    return ret


def disableL3Routing():
    data = {
        "enable" : "false"
    }
    ret = rest_call('/wm/routing/config', data, 'POST')
    return ret



def startNetworkWithLinearTopo( hostCount ):
    global net
    net = Mininet(topo=LinearTopo(hostCount), build=False)

    remote_ip = getControllerIP()
    info('** Adding Floodlight Controller\n')
    net.addController('c1', controller=RemoteController,
                      ip=remote_ip, port=6653)

    # Build the network
    net.build()
    net.start()

    # Start DHCP Service
    ret = enableDHCPServer()
    print(ret)

    addDHCPInstance1('mininet-dhcp-1')
    ret = addSwitchToDHCPInstance1('mininet-dhcp-1')
    print(ret)

    addDHCPInstance2('mininet-dhcp-2')
    ret = addSwitchToDHCPInstance2('mininet-dhcp-2')
    print(ret)

    time.sleep(5)

    hosts = net.hosts
    for host in hosts:
        mountPrivateResolvconf(host)
        startDHCPclient(host)
        waitForIP(host)


    # Start L3 Service
    ret = enableL3Routing()
    print (ret)

    ret = addVirtualGateway('mininet-gateway-1')
    print (ret)

    ret = addInterfaceToGateway('mininet-gateway-1')
    print (ret)

    ret = addSwitchToGateway('mininet-gateway-1')
    print (ret)


def clearGatewayInstance(name):
    data = {}
    ret = rest_call('/wm/routing/gateway/' + name, data, 'DELETE')
    return ret


def stopNetwork():
    if net is not None:
        info('** Tearing down network\n')
        clearGatewayInstance('mininet-gateway-1')
        net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    startNetworkWithLinearTopo(6)
    CLI(net)
    stopNetwork()

