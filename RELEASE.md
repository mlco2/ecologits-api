# Release
1. Update version number in `pyproject.toml` and `app/core/config.py`.
2. Run `uv lock`
3. Commit, tag and push changes.
   ```shell
   git add .
   git commit -m "chore: bump version to x.y.z"
   git push origin  # wait for all CI jobs to succeed
   git tag x.y.z
   git push origin --tags
   ```
4. Go to GitHub in the tags section, on the latest tag click "Create release".
5. Click on "Generate release notes" and review the changelog.
6. Click "Publish release".
7. Go to GitHub Actions and check that the Docker publish job succeeded.
