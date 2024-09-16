class UserAdapter:
    def __init__(self, app):
        self.app = app
        self.setup_routes()
    
    def setup_routes(self):
        self.app.route("/user")(self.user)

    def user(self):
        return "Hello, user!"
