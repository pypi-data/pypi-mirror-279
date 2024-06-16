"""
Concrete :class:`~.base.TrackerConfigBase` subclass for MTV
"""

import base64

from ... import utils
from ..base import TrackerConfigBase, exclude

MtvImageHost = utils.types.ImageHost(
    allowed=(
        ('imgbox', 'ptpimg', 'dummy')
        if utils.is_running_in_development_environment() else
        ('imgbox', 'ptpimg')
    ),
)


class MtvTrackerConfig(TrackerConfigBase):
    defaults = {
        'base_url': base64.b64decode('aHR0cHM6Ly93d3cubW9yZXRoYW50di5tZQ==').decode('ascii'),
        'username': '',
        'password': '',
        'announce_url': utils.configfiles.config_value(
            value='',
            description='Your personal announce URL. Automatically fetched from the website if not set.',
        ),
        'image_host': utils.configfiles.config_value(
            value=utils.types.ListOf(
                item_type=MtvImageHost,
                default=('imgbox',),
                separator=',',
            ),
            description=(
                'List of image hosting service names. The first service is normally used '
                'with the others as backup if uploading to the first fails.\n'
                + 'Supported services: ' + ', '.join(MtvImageHost.options)
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
        'anonymous': utils.configfiles.config_value(
            value=utils.types.Bool('no'),
            description='Whether your username is displayed on your uploads.',
        ),
    }

    argument_definitions = {
        'submit': {
            ('--imdb', '--im'): {
                'help': 'IMDb ID or URL',
                'type': utils.argtypes.webdb_id('imdb'),
            },
            ('--anonymous', '--an'): {
                'help': 'Hide your username for this submission',
                'action': 'store_true',
                # This must be `None` so it doesn't override the "anonymous"
                # value from the config file. See CommandBase.get_options().
                'default': None,
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
            ('--ignore-dupes', '--id'): {
                'help': 'Force submission even if the tracker reports duplicates',
                'action': 'store_true',
            },
        },
    }
