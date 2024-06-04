# Workflow for Release

1. Goto ``pyproject.toml`` and bump the version.
2. Goto ``CHANGELOG.md`` and bump the version.
3. Add a tag ``git tag -s 'vX.Y.Z' -m 'Release vX.Y.Z'``.
4. Push tag ``git push origin vX.Y.Z``.
5. Goto [Releases] and ``Draft new release``.
6. Add changelog to release and create the new release.

[Releases]: https://github.com/instructions-d-installation/installation-instruction/releases