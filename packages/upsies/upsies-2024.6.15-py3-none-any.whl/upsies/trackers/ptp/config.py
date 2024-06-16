"""
Concrete :class:`~.base.TrackerConfigBase` subclass for PTP
"""

import base64

from ... import utils
from ..base import TrackerConfigBase, exclude
from . import metadata

PtpImageHost = utils.types.ImageHost(
    disallowed=(
        ()
        if utils.is_running_in_development_environment() else
        ('dummy',)
    ),
)


class PtpReleaseType(str):
    def __new__(cls, text):
        for type, regex in metadata.types.items():
            if regex.search(text):
                return super().__new__(cls, type)
        raise utils.argtypes.ArgumentTypeError(f'Invalid type: {text}')


class PtpTrackerConfig(TrackerConfigBase):
    defaults = {
        'base_url': base64.b64decode('aHR0cHM6Ly9wYXNzdGhlcG9wY29ybi5tZQ==').decode('ascii'),
        'username': '',
        'password': '',
        'announce_url': utils.configfiles.config_value(
            value='',
            description='Your personal announce URL.',
        ),
        'image_host': utils.configfiles.config_value(
            value=utils.types.ListOf(
                item_type=PtpImageHost,
                default=('ptpimg', 'imgbox'),
                separator=',',
            ),
            description=(
                'List of image hosting service names. The first service is normally used '
                'with the others as backup if uploading to the first fails.\n'
                + 'Supported services: ' + ', '.join(PtpImageHost.options)
            ),
        ),
        'screenshots_from_movie': utils.configfiles.config_value(
            value=utils.types.Integer(3, min=3, max=10),
            description='How many screenshots to make for single-video uploads.',
        ),
        'screenshots_from_episode': utils.configfiles.config_value(
            value=utils.types.Integer(2, min=2, max=10),
            description='How many screenshots to make per video for multi-video uploads.',
        ),
        'exclude': (
            exclude.checksums,
            exclude.images,
            exclude.nfo,
            exclude.samples,
        ),
    }

    argument_definitions = {
        'submit': {
            ('--hardcoded-subtitles', '--hs'): {
                'help': 'Video contains hardcoded subtitles',
                'action': 'store_true',
            },
            ('--no-english-subtitles', '--nes'): {
                'help': (
                    'Whether release contains no English audio and no English subtitles.'
                    '\n'
                    'This is autodetected reliably if all audio and subtitle tracks have '
                    'a correct language tag. If not, you are asked interactively.\n'
                    'Subtitle languages are detected in *.idx/sub, VIDEO_TS trees '
                    'and *.srt/ssa/ass/vtt by language code in the file name, e.g. '
                    '"Foo.en.srt".'
                ),
                'metavar': 'BOOL',
                'type': utils.argtypes.bool_or_none,
            },
            ('--not-main-movie', '--nmm'): {
                'help': 'Upload ONLY contains extras, Rifftrax, Workprints',
                'action': 'store_true',
            },
            ('--personal-rip', '--pr'): {
                'help': 'Tag as your own encode',
                'action': 'store_true',
            },
            ('--poster', '--po'): {
                'help': 'Path or URL to movie poster',
            },
            ('--imdb', '--im'): {
                'help': 'IMDb ID or URL',
                'type': utils.argtypes.webdb_id('imdb'),
            },
            ('--source', '--so'): {
                'help': (
                    'Original source of this release\n'
                    + 'Should vaguely match: '
                    + ', '.join(metadata.sources)
                ),
            },
            ('--type', '--ty'): {
                'help': (
                    'General category of this release\n'
                    + 'Must vaguely match: '
                    + ', '.join(metadata.types)
                ),
                'type': PtpReleaseType,
            },
            ('--screenshots-count', '--ssc'): {
                'help': 'How many screenshots to make per video file',
                'type': utils.argtypes.number_of_screenshots(min=1, max=10),
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
            ('--upload-token', '--ut'): {
                'help': 'Upload token from staff',
            },
            ('--only-description', '--od'): {
                'help': 'Only generate description (do not upload anything)',
                'action': 'store_true',
                'group': 'generate-metadata',
            },
        },
    }
