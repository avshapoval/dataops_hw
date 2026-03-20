import os

c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'

c.Authenticator.admin_users = {'admin'}
c.Authenticator.allowed_users = {'admin', 'user1', 'user2'}

c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 8000

c.Spawner.default_url = '/lab'

c.JupyterHub.bind_url = 'http://0.0.0.0:8000'
