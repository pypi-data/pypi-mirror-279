"""
Concrete :class:`~.base.TrackerConfigBase` subclass for ANT
"""

import base64

from ... import utils
from ..base import TrackerConfigBase, exclude


class AntTrackerConfig(TrackerConfigBase):
    defaults = {
        'base_url': base64.b64decode('aHR0cHM6Ly9hbnRoZWxpb24ubWU=').decode('ascii'),
        'apikey': utils.configfiles.config_value(
            value='',
            description='Your person upload API key you created in your profile.',
        ),
        'announce_url': utils.configfiles.config_value(
            value='',
            description='Your personal announce URL.',
        ),
        'exclude': (
            exclude.checksums,
            exclude.images,
            exclude.nfo,
            exclude.samples,
        ),
        'anonymous': utils.configfiles.config_value(
            value=utils.types.Bool('no'),
            description='Whether your username is displayed on your uploads.',
        ),
    }

    argument_definitions = {
        'submit': {
            ('--tmdb', '--tm'): {
                'help': 'TMDb ID or URL',
                'type': utils.argtypes.webdb_id('tmdb'),
            },
            ('--anonymous', '--an'): {
                'help': 'Hide your username for this submission',
                'action': 'store_true',
                # This must be `None` so it doesn't override the "anonymous"
                # value from the config file. See CommandBase.get_options().
                'default': None,
            },
        },
    }
