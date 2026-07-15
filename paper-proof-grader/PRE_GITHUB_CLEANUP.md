# Pre-GitHub Cleanup

Cleaned on 2026-07-10.

Moved generated/unstructured/local material to:

```text
E:\paper-grade\paper-proof-grader-pre-github-cleanout_20260710_052412
```

Moved items include:

- `ARCHIVE`
- `DOCKER_PACKAGE_20260507_191530`
- `INPUT`
- `ONLINE_CODEX_PACKAGE`
- `OUTPUT`
- `__pycache__`
- `.fisnote`
- `FIS_FOLDER_INDEX.fisnote`
- `paper-snapshot-online-codex-package.zip`

Move manifests:

```text
E:\paper-grade\paper-proof-grader-pre-github-cleanout_20260710_052412\MOVE_MANIFEST.json
E:\paper-grade\paper-proof-grader-pre-github-cleanout_20260710_052412\MOVE_MANIFEST_REMAINDERS.json
```

Note: a small `OUTPUT` remainder stayed behind because old nested run folders
returned access-denied errors over the share. `OUTPUT/` is ignored in `.gitignore`
and should not be committed.
