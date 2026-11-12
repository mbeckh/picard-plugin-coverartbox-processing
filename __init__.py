# Perform cover art processing on covers added in metadata cover art box.
# cf. https://tickets.metabrainz.org/projects/PICARD/issues/PICARD-3547
#
# Copyright 2026 Michael Beckh (mbeckh)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import cast

from picard.album_requests import TaskType
from picard.coverart import (
    CoverArtImage,
    CoverArtImageProcessing,
)
from picard.item import MetadataItem
from picard.plugin3.api import (
    Album,
    File,
    PluginApi,
    Track,
)
from picard.util.imageinfo import identify

from . import monkey

from picard.ui.coverartbox import (
    CoverArtBox,
    CoverArtSetter,
    CoverArtSetterMode,
)


_api: PluginApi
_enabled = False


def _process_image_data(self: CoverArtBox, image: CoverArtImage, data, image_info):
    """Perform cover art processing on provided image data."""

    def callback(result=None, error=None):
        pass

    album = None
    if isinstance(self.item, File):
        parent = cast(File, self.item).parent_item
        if isinstance(parent, Track):
            album = cast(Track, parent).album
    elif isinstance(self.item, Track):
        album = cast(Track, self.item).album
    elif isinstance(self.item, Album):
        album = cast(Album, self.item)

    if album:
        album.add_task(
            f'coverart_processing_{id(image)}',
            TaskType.OPTIONAL,
            f'Cover art processing: {image}',
        )

        image_processing = CoverArtImageProcessing(album)
        image_processing.run_image_processors(image, data, image_info, callback)
        image_processing.wait_for_processing()

        album.complete_task(f'coverart_processing_{id(image)}')
    else:
        _api.logger.error('Cannot process cover because album is missing for %r', self.item)


@monkey.patch(CoverArtBox, CoverArtBox._try_load_remote_image)
def _enhanced_try_load_remote_image(wrapped, self: CoverArtBox, url, data):
    """Add cover art processing to metadata cover art box."""

    if not _enabled:
        return wrapped(self, url, data)

    coverartimage = CoverArtImage(url=url.toString(), types=['front'], data=data)
    # BEGIN FIX: Call CoverArtProcessing
    _process_image_data(self, coverartimage, data, identify(data))
    # END FIX

    config = _api.global_config
    if config.setting['load_image_behavior'] == 'replace':
        mode = CoverArtSetterMode.REPLACE
    else:
        mode = CoverArtSetterMode.APPEND

    setter = CoverArtSetter(mode, coverartimage, cast(MetadataItem, self.item))
    setter.set_coverart()

    return coverartimage


def enable(api: PluginApi):
    """Enable plugin."""

    global _api, _enabled

    _api = api
    _enabled = True


def disable():
    """Disable plugin."""

    global _api, _enabled

    _enabled = False
    monkey.unpatch_module(__name__)
    del _api
