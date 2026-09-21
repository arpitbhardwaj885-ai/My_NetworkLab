from collections import deque
class Host:
    def __init__(self,name):
        self.name=name
        self.interfaces=[]
class Router:
    def __init__(self,name):
        self.name=name
        self.interfaces=[]

class server(Host):
    pass

class Interface:
    def __init__(self,name,device,mac_address):
        self.name=name
        self.device=device
        self.mac_address = mac_address

    def receive_frame(self,frame):
          if frame.destination_mac == self.mac_address:
            print("frame accepted by", self.device.name)
          else:
            print("frame rejected by", self.device.name)

class Link:
    def __init__(self,interface1,interface2):
        self.interface1=interface1
        self.interface2=interface2

    def transmit(self,frame,sender):
        if sender==self.interface1 :
            receiver=self.interface2
        else:
            receiver=self.interface1
        print(
         sender.device.name,
                    "->",
                receiver.device.name)
        print(
        "Frame:",
        frame.source_mac,
        "->",
        frame.destination_mac
                                )

        receiver.receive_frame(frame)

class Network:
    def __init__(self):
        self.devices=[]
        self.links=[]
        self.graph={}

    def add_device(self,device):
        self.devices.append(device)
        self.graph[device]=[]

    def add_link(self,link):
        self.links.append(link)

        device1=link.interface1.device
        device2=link.interface2.device

        self.graph[device1].append(device2)
        self.graph[device2].append(device1)
    

    def find_path(self,start,destination):
        queue=deque([start])
        visited={start}
        parent={start:None}
        while queue:
            current=queue.popleft()

            if current==destination:
                break

            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor]=current
                    queue.append(neighbor)

        path=[]
        current=destination
        while current is not None:
            path.append(current)
            current=parent[current]

        path.reverse()
        return path


class EthernetFrame:
    def __init__(self,source_mac,destination_mac,payload):
        self.source_mac=source_mac
        self.destination_mac=destination_mac
        self.payload=payload




# Create devices
pc1 = Host("PC1")
router1 = Router("Router1")
server = server("Server1")


# Create interfaces
pc1_interface = Interface("eth0", pc1,"00:11:22:33:44:01")

router_interface1 = Interface("eth0", router1,"00:11:22:33:44:02")
router_interface2 = Interface("eth1", router1,"00:11:22:33:44:03")

server_interface = Interface("eth0", server,"00:11:22:33:44:04")


# Attach interfaces
pc1.interfaces.append(pc1_interface)

router1.interfaces.append(router_interface1)
router1.interfaces.append(router_interface2)

server.interfaces.append(server_interface)

# Create links
link1 = Link(pc1_interface, router_interface1)
link2 = Link(router_interface2, server_interface)


# Create network
network = Network()

network.add_device(pc1)
network.add_device(router1)
network.add_device(server)

network.add_link(link1)
network.add_link(link2)


# Display topology
print("Devices:")

for device in network.devices:
    print("-", device.name)

print("\nLinks:")

for link in network.links:
    print(
        link.interface1.device.name,
        "<->",
        link.interface2.device.name
    )
print("\nGraph:")

for device, neighbors in network.graph.items():
    print(device.name, "->", [neighbor.name for neighbor in neighbors])

path = network.find_path(pc1, server)

print("\nPath:")
print(" -> ".join(device.name for device in path))

frame = EthernetFrame(
    pc1_interface.mac_address,
    router_interface1.mac_address,
    "Hello Router1"
)

link1.transmit(frame, pc1_interface)