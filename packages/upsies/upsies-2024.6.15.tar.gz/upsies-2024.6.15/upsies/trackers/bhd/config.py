"""
Concrete :class:`~.base.TrackerConfigBase` subclass for BHD
"""

import base64

from ... import utils
from ..base import TrackerConfigBase, exclude

BhdImageHost = utils.types.ImageHost(
    allowed=(
        ('imgbox', 'ptpimg', 'imgbb', 'dummy')
        if utils.is_running_in_development_environment() else
        ('imgbox', 'ptpimg', 'imgbb')
    ),
)


class BhdTrackerConfig(TrackerConfigBase):
    defaults = {
        'upload_url': base64.b64decode('aHR0cHM6Ly9iZXlvbmQtaGQubWUvYXBpL3VwbG9hZA==').decode('ascii'),
        'announce_url': utils.configfiles.config_value(
            value=base64.b64decode('aHR0cHM6Ly9iZXlvbmQtaGQubWUvYW5ub3VuY2U=').decode('ascii'),
            description='The announce URL without the private passkey.',
        ),
        'announce_passkey': utils.configfiles.config_value(
            value='',
            description=(
                'The private part of the announce URL.\n'
                'Get it from the website: My Security -> Passkey'
            ),
        ),
        'apikey': utils.configfiles.config_value(
            value='',
            description=(
                'Your personal private API key.\n'
                'Get it from the website: My Security -> API key'
            ),
        ),
        'anonymous': utils.configfiles.config_value(
            value=utils.types.Bool('no'),
            description='Whether your username is displayed on your uploads.',
        ),
        'draft': utils.configfiles.config_value(
            value=utils.types.Bool('no'),
            description=(
                'Whether your uploads are stashed under Torrents -> Drafts '
                'after the upload instead of going live.'
            ),
        ),
        'image_host': utils.configfiles.config_value(
            value=utils.types.ListOf(
                item_type=BhdImageHost,
                default=('imgbox',),
                separator=',',
            ),
            description=(
                'List of image hosting service names. The first service is normally used '
                'with the others as backup if uploading to the first fails.\n'
                + 'Supported services: ' + ', '.join(BhdImageHost.options)
            ),
        ),
        'screenshots_count': utils.configfiles.config_value(
            value=utils.types.Integer(4, min=3, max=10),
            description='How many screenshots to make.',
        ),
        'exclude': (
            exclude.checksums,
            exclude.extras,
            exclude.images,
            exclude.nfo,
            exclude.samples,
            exclude.subtitles,
        ),
    }

    argument_definitions = {
        'submit': {
            ('--imdb', '--im'): {
                'help': 'IMDb ID or URL',
                'type': utils.argtypes.webdb_id('imdb'),
            },
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
            ('--custom-edition', '--ce'): {
                'help': 'Non-standard edition, e.g. "Final Cut"',
                'default': '',
            },
            ('--draft', '--dr'): {
                'help': 'Upload as draft',
                'action': 'store_true',
                # The default value must be None so CommandBase.get_options()
                # doesn't always overwrite the value with the config file value.
                'default': None,
            },
            ('--personal-rip', '--pr'): {
                'help': 'Tag as your own encode',
                'action': 'store_true',
            },
            ('--screenshots-count', '--ssc'): {
                'help': ('How many screenshots to make '
                         f'(min={defaults["screenshots_count"].min}, '
                         f'max={defaults["screenshots_count"].max})'),
                'type': utils.argtypes.number_of_screenshots(
                    min=defaults['screenshots_count'].min,
                    max=defaults['screenshots_count'].max,
                ),
            },
            ('--screenshots', '--ss'): {
                'help': (
                    'Path(s) to existing screenshot file(s)\n'
                    'Directories are searched recursively.\n'
                    'Precreated screenshots are used in addition to automatically generated screenshots.'
                ),
                'nargs': '+',
                'action': 'extend',
                'type': utils.argtypes.files_with_extension('png'),
            },
            ('--special', '--sp'): {
                'help': 'Tag as special episode, e.g. Christmas special (ignored for movie uploads)',
                'action': 'store_true',
            },
            ('--only-description', '--od'): {
                'help': 'Only generate description (do not upload anything)',
                'action': 'store_true',
                'group': 'generate-metadata',
            },
            ('--only-title', '--ot'): {
                'help': 'Only generate title (do not upload anything)',
                'action': 'store_true',
                'group': 'generate-metadata',
            },
        },
    }
