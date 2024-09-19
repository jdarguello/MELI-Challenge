from src.domain.entities.scope import Scope

class ScopeService:
    def __init__(self, scope: Scope):
        self.scope = scope

    def create_scope(self, scope_data):
        self.scope.create_scope(scope_data)
    
    def get_scope(self, scope_id):
        return self.scope.get_scope(scope_id)
    
    def get_scopes(self):
        return self.scope.get_scopes()
    
    def update_scope(self, scope_id, scope_data):
        return self.scope.update_scope(scope_id, scope_data)
    
    def delete_scope(self, scope_id):
        return self.scope.delete_scope(scope_id)