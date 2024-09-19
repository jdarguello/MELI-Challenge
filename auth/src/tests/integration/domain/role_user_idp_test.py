from src.tests.integration.domain.testconfig_domain import TestConfigDomain
from datetime import datetime
from src.domain.entities.type import Type
from src.domain.entities.permission import Permission
from src.domain.entities.role import Role
from src.domain.entities.scope import Scope
from src.domain.entities.user import User
from src.domain.services.identity_provider import IdentityProvider

class TestRoleUserIDP(TestConfigDomain):
    def setUp(self):
        super().setUp()
        #Crea otro Type, lo relaciona con el permiso Read y lo almacena en la BD
        self.fullstack = Type(name='FullStack', description='Desarrollador FullStack', weight=500)
        self.fullstack.permissions.append(self.read_permission)
        self.db.session.add(self.fullstack)

        # Crea otra instancia de Scope y la almacena en la BD
        self.legal = Scope(name='Legal', description='Departamento Legal')
        self.db.session.add(self.legal)
        self.db.session.commit()

        # Crea una instacia de Role, la relaciona con el scope Corporate y el Type Admin
        self.admin_role = Role(name='Admin', description='Rol Administrador')
        self.admin_role.type = self.admin
        self.admin_role.scope = self.corporate
        self.db.session.add(self.admin_role)
        self.db.session.commit()

        # Crea una instancia de Role, la relaciona con el scope Legal y el Type FullStack
        self.fullstack_role = Role(name='FullStack', description='Rol Desarrollador FullStack')
        self.fullstack_role.type = self.fullstack
        self.fullstack_role.scope = self.legal
        self.db.session.add(self.fullstack_role)
        self.db.session.commit()

        # Crea una instancia de IdentityProvider y la almacena en la BD
        self.google_provider = IdentityProvider(
            clientId='your-google-client-id',  # Replace with your actual Google client ID
            name='Google',
            clientSecret='your-google-client-secret',  # Replace with your actual Google client secret
            baseUrl='https://accounts.google.com',
            tokenUrl='https://oauth2.googleapis.com/token',
            authorizationUrl='https://accounts.google.com/o/oauth2/auth',
            redirectUrl='https://your-app.com/oauth2callback'  # Replace with your app's redirect URI
        )

    def test_create_one_user_with_1_role_idp(self):
        # Crea una instancia de User, la relaciona con el IdentityProvider Google y el Rol Admin
        date = datetime.strptime('2024-12-31', '%Y-%m-%d').date()
        user = User(
            email='john@example.com',
            token='1j2be3b43h4b3h4',
            token_expiry_date=date,
            identity_provider=self.google_provider
        )
        user.roles.append(self.admin_role)
        self.db.session.add(user)
        self.db.session.commit()

        # Verifica que el usuario se haya creado correctamente con el rol y el IdentityProvider asociado
        saved_user = self.db.session.query(User).filter_by(email='john@example.com').first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, user.email)
        self.assertEqual(saved_user.identity_provider.name, user.identity_provider.name)
        self.assertEqual(saved_user.token, user.token)
        self.assertEqual(saved_user.token_expiry_date, date)
        self.assertEqual(len(saved_user.roles), 1)
        self.assertEqual(saved_user.roles[0].name, self.admin_role.name)

    
    def test_create_one_user_with_2_role_idp(self):
        # Crea una instancia de User, la relaciona con el IdentityProvider Google y los Roles Admin y FullStack
        date = datetime.strptime('2024-12-31', '%Y-%m-%d').date()
        user = User(
            email='john_doe@example.com',
            token='123nj343h432432k4p',
            token_expiry_date=date,
            identity_provider=self.google_provider
        )
        user.roles.append(self.admin_role)
        user.roles.append(self.fullstack_role)
        self.db.session.add(user)
        self.db.session.commit()

        # Verifica que el usuario se haya creado correctamente con los dos roles y el IdentityProvider asociado
        saved_user = self.db.session.query(User).filter_by(email='john_doe@example.com').first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, user.email)
        self.assertEqual(saved_user.identity_provider.name, user.identity_provider.name)
        self.assertEqual(len(saved_user.roles), 2)
        role_names = [role.name for role in saved_user.roles]
        self.assertIn(user.roles[0].name, role_names)
        self.assertIn(user.roles[1].name, role_names)
        self.assertEqual(user.roles[0].type.name, self.admin_role.type.name)
        self.assertEqual(user.roles[1].type.name, self.fullstack_role.type.name)
        self.assertEqual(user.roles[0].scope.name, self.admin_role.scope.name)
        self.assertEqual(user.roles[1].scope.name, self.fullstack_role.scope.name)
        self.assertEqual(user.roles[0].type.permissions[0].kind, self.admin.permissions[0].kind)