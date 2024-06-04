# Workflow for Release

1. Goto ``pyproject.toml`` and bump the version.
2. Goto ``CHANGELOG.md`` and bump the version.
3. `git add *`
4. `git commit -S -m "Bump version for release vX.Y.Z"`
5. Add a tag ``git tag -s 'vX.Y.Z' -m 'Release vX.Y.Z'``.
6. Push tag ``git push origin vX.Y.Z``.
7. Goto [Releases] and ``Draft new release``.
8. Add changelog to release and create the new release.

[Releases]: https://github.com/instructions-d-installation/installation-instruction/releases