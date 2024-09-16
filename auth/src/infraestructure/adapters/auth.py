class AuthAdapter:
    def __init__(self, app):
        self.app = app
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/")(self.index)

    def index(self):
        return "Hello, World!"

    