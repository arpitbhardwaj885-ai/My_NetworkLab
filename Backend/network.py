class Host:
    def __init__(self,name):
        self.name=name
class Router:
    def __init__(self,name):
        self.name=name

class server(Host):
    pass
    

pc1=Host("PC1")
print(pc1.name)
router=Router("Router1")
print(router.name)
serve=server("server1")
print(serve.name)

