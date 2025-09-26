"""
Django settings for MashinMan project.
"""

import os
from decouple import config

# Determine which settings to use based on environment
ENVIRONMENT = config('ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    from .settings.production import *
elif ENVIRONMENT == 'testing':
    from .settings.testing import *
else:
    from .settings.development import *
