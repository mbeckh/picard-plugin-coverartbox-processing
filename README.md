# Cover Art Box Processing

![Latest Version](https://img.shields.io/github/v/tag/mbeckh/picard-plugin-coverartbox-processing?sort=semver&filter=v*&style=flat-square&label=latest)
![Supports](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmbeckh%2Fpicard-plugin-coverartbox-processing%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&search=dependencies%5Cs*%3D%5Cs*%5C%5B%5B%5E%5D%5D*%22picard%5B%5E%22%5D*(%3E%3D.*%3F)%5B%2C%22%5D&replace=%241&flags=s&style=flat-square&label=picard&color=orange)
![Tested with](https://img.shields.io/badge/dynamic/regex?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmbeckh%2Fpicard-plugin-coverartbox-processing%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&search=dependencies%5Cs*%3D%5Cs*%5C%5B%5B%5E%5D%5D*%22picard%5B%5E%22%5D*(%3C%3D.*%3F)%5B%2C%22%5D&replace=%241&flags=s&style=flat-square&label=tested+with&color=green)

A plugin for [MusicBrainz Picard](https://picard.musicbrainz.org) to add cover
art processing for files added through the UI.

## What it Does

The plugin patches the cover art box to perform cover art processing on files
added using the covert art box in the meta data view. This implements the
behavior suggested in
[PICARD-3547](https://tickets.metabrainz.org/projects/PICARD/issues/PICARD-3547).

## Unsupported Modifications of Picard

> [!IMPORTANT]
> This plugin requires the
> [Monkey Plugin](https://github.com/mbeckh/picard-plugin-monkey/) as a
> prerequisite. Please install this plugin first.

This plugin modifies Picard _way beyond_ the level that was intended by the
implementers of the official API. It relies heavily on internal and private
implementation details and monkey patches its way across the Picard code base to
achieve its goals.

> [!WARNING]
> **Even a minor update of Picard can break this plugin** until I'm able to
> supply an updated version. The plugin is typically tested with the latest
> version of Picard only.

## License

The code is released under the Apache License Version 2.0. Please see
[LICENSE](LICENSE) for details and [NOTICE](NOTICE) for the required information
when using picard-plugin-coverartbox-processing in your own work.
