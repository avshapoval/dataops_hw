import os

c.JupyterHub.bind_url = 'http://0.0.0.0:8000'

c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'

c.Spawner.default_url = '/lab'

c.Authenticator.admin_users = {os.getenv('JUPYTERHUB_ADMIN_USER', 'admin')}

c.LocalAuthenticator.create_system_users = False

c.Authenticator.allowed_users = {'admin', 'user1', 'user2'}

c.JupyterHub.admin_access = True

c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

c.ConfigurableHTTPProxy.should_start = True
