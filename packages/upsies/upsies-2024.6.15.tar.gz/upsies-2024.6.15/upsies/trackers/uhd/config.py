"""
Concrete :class:`~.base.TrackerConfigBase` subclass for UHD
"""

import base64

from ... import utils
from ..base import TrackerConfigBase, exclude

UhdImageHost = utils.types.ImageHost(
    disallowed=(
        ()
        if utils.is_running_in_development_environment() else
        ('dummy',)
    ),
)


class UhdTrackerConfig(TrackerConfigBase):
    defaults = {
        'base_url': base64.b64decode('aHR0cHM6Ly91aGRiaXRzLm9yZw==').decode('ascii'),
        'username': '',
        'password': '',
        'anonymous': utils.configfiles.config_value(
            value=utils.types.Bool('no'),
            description='Whether your username is displayed on your uploads.',
        ),
        'announce_url': utils.configfiles.config_value(
            value='',
            description='Your personal announce URL.',
        ),
        'image_host': utils.configfiles.config_value(
            value=utils.types.ListOf(
                item_type=UhdImageHost,
                default=('ptpimg', 'freeimage', 'imgbox'),
                separator=',',
            ),
            description=(
                'List of image hosting service names. The first service is normally used '
                'with the others as backup if uploading to the first fails.\n'
                + 'Supported services: ' + ', '.join(UhdImageHost.options)
            ),
        ),
        'screenshots_count': utils.configfiles.config_value(
            value=utils.types.Integer(4, min=2, max=10),
            description='How many screenshots to make.',
        ),
        'exclude': (
            exclude.checksums,
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
            ('--anonymous', '--an'): {
                'help': 'Hide your username for this submission',
                'action': 'store_true',
                # This must be `None` so it doesn't override the "anonymous"
                # value from the config file. See CommandBase.get_options().
                'default': None,
            },
            ('--internal', '--in'): {
                'help': 'Internal encode (use only if you were told to)',
                'action': 'store_true',
            },
            ('--3d',): {
                'help': 'Mark this as a 3D release',
                'action': 'store_true',
            },
            ('--vie', '--vi'): {
                'help': 'Release contains Vietnamese audio dub',
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
            ('--poster', '--po'): {
                'help': 'Path or URL to poster image (autodetected by default)',
            },
            ('--trailer', '--tr'): {
                'help': 'Trailer YouTube ID or URL (autodetected by default)',
            },
            ('--only-description', '--od'): {
                'help': 'Only generate description (do not upload anything)',
                'action': 'store_true',
                'group': 'generate-metadata',
            },
        },
    }
