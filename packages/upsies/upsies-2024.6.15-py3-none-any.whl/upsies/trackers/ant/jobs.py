"""
Concrete :class:`~.base.TrackerJobsBase` subclass for ANT
"""

import functools

from ... import jobs, utils
from ..base import TrackerJobsBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class AntTrackerJobs(TrackerJobsBase):

    @functools.cached_property
    def jobs_before_upload(self):
        return (
            # Interactive jobs
            self.tmdb_job,
            self.source_job,
            self.scene_check_job,

            # Background jobs
            self.create_torrent_job,
            self.group_job,
            self.mediainfo_job,
            self.flags_job,
            self.anonymous_job,
        )

    @functools.cached_property
    def source_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('source'),
            label='Source',
            precondition=self.make_precondition('source_job'),
            options=(
                ('Blu-ray', 'Blu-ray'),
                ('DVD', 'DVD'),
                ('WEB', 'WEB'),
                ('HD-DVD', 'HD-DVD'),
                ('HDTV', 'HDTV'),
                ('VHS', 'VHS'),
                ('TV', 'TV'),
                ('LaserDisc', 'LaserDisc'),
                ('Unknown', 'Unknown'),
            ),
            autodetect=self.autodetect_source,
            autofinish=True,
            **self.common_job_args(),
        )

    _autodetect_source_map = {
        'Blu-ray': lambda release_name: 'BluRay' in release_name.source,
        'HD-DVD': lambda release_name: 'HD-DVD' in release_name.source,
        'HDTV': lambda release_name: 'HDTV' in release_name.source,
        'DVD': lambda release_name: 'DVD' in release_name.source,
        'WEB': lambda release_name: 'WEB' in release_name.source,
        'VHS': lambda release_name: 'VHS' in release_name.source,
        'TV': lambda release_name: 'TV' in release_name.source,
        # 'LaserDisc': lambda release_name: ...,  # Not supported by ReleaseName
    }

    async def autodetect_source(self, job_):
        for option, autodetect in self._autodetect_source_map.items():
            _log.debug('... checking %r: %r', option, autodetect)
            if autodetect(self.release_name):
                _log.debug('*** MATCH %r', option)
                return option

    @functools.cached_property
    def group_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('group'),
            label='Group',
            precondition=self.make_precondition('group_job'),
            text=self.autodetect_group,
            finish_on_success=True,
            **self.common_job_args(ignore_cache=True),
        )

    async def autodetect_group(self):
        return self.release_name.group

    @functools.cached_property
    def flags_job(self):
        return jobs.custom.CustomJob(
            name=self.get_job_name('flags'),
            label='Flags',
            precondition=self.make_precondition('flags_job'),
            worker=self.autodetect_flags,
            no_output_is_ok=True,
            **self.common_job_args(ignore_cache=True),
        )

    async def autodetect_flags(self, job):
        # supported flags: Directors, Extended, Uncut, IMAX, Unrated, HDR10, DV,
        # 4KRemaster, Atmos, DualAudio, Commentary, Remux, 3D, Criterion

        flags = []
        rn = self.release_name

        if "Director's Cut" in rn.edition:
            flags.append('Directors')
        if 'Extended Cut' in rn.edition:
            flags.append('Extended')
        if 'Uncut' in rn.edition:
            flags.append('Uncut')
        if 'Unrated' in rn.edition:
            flags.append('Unrated')
        if 'Criterion Collection' in rn.edition:
            flags.append('Criterion')
        if 'IMAX' in rn.edition:
            flags.append('IMAX')
        if '4k Remastered' in rn.edition:
            flags.append('4KRemaster')
        if 'Dual Audio' in rn.edition:
            flags.append('DualAudio')

        if 'Remux' in rn.source:
            flags.append('Remux')

        hdr_formats = utils.video.hdr_formats(self.content_path)
        if 'DV' in hdr_formats:
            flags.append('DV')
        if 'HDR10' in hdr_formats or 'HDR10+' in hdr_formats:
            flags.append('HDR10')

        if 'Atmos' in rn.audio_format:
            flags.append('Atmos')

        if utils.video.has_commentary(self.content_path):
            flags.append('Commentary')

        return flags

    @functools.cached_property
    def anonymous_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('anonymous'),
            label='Anonymous',
            precondition=self.make_precondition('anonymous_job'),
            options=(
                ('No', False),
                ('Yes', True),
            ),
            autodetect=self.autodetect_anonymous,
            autofinish=True,
            **self.common_job_args(ignore_cache=True),
        )

    async def autodetect_anonymous(self, job):
        return self.options.get('anonymous', False)

    @property
    def post_data(self):
        return {
            **{
                'api_key': self._tracker.apikey,
                'action': 'upload',
                'tmdbid': self.get_job_output(self.tmdb_job, slice=0).replace('movie/', ''),
                'mediainfo': self.get_job_output(self.mediainfo_job, slice=0),
                'flags[]': self.get_job_output(self.flags_job),
                # Scene release? (I don't know why it's called "censored".)
                'censored': '1' if self.get_job_attribute(self.scene_check_job, 'is_scene_release') else None,
                'anonymous': '1' if self.get_job_attribute(self.anonymous_job, 'choice') else None,
                'media': self.get_job_attribute(self.source_job, 'choice'),
            },
            **self._post_data_release_group,
        }

    @property
    def _post_data_release_group(self):
        group = self.get_job_output(self.group_job, slice=0)
        if group != 'NOGROUP':
            return {'releasegroup': group}
        else:
            # Default value of <input type="checkbox"> is "on":
            # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Input/checkbox
            return {'noreleasegroup': 'on'}

    @property
    def post_files(self):
        return {
            'file_input': {
                'file': self.torrent_filepath,
                'mimetype': 'application/x-bittorrent',
            },
        }
