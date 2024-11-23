import os


ENVIRONMENT = os.getenv('ENGILORE_ENV', 'dev')

if ENVIRONMENT == 'prod':
    from engilore.settings.prod import *
else:
    from engilore.settings.dev import *
