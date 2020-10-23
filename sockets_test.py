from peer_socket import PeerSocket

s1 = PeerSocket(36258, 36259)
s2 = PeerSocket(36260, 36261)

print("connecting s1 to s2!")
s1.connect(s2.host, s2.port_in, s2.port_out)
print("connecting s2 to s1!")
s2.connect(s1.host, s1.port_in, s1.port_out)