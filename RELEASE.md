# Release Guide

This document provides step-by-step instructions for releasing a new version of panparsex.

## Prerequisites

1. **PyPI Account**: You need a PyPI account with API token access
2. **GitHub Access**: Push access to the repository
3. **Local Environment**: Python 3.9+ with build tools installed

## Release Process

### 1. Prepare the Release

#### Update Version
```bash
# Edit pyproject.toml and update the version
# Example: version = "0.1.1"
```

#### Update Changelog
```bash
# Edit CHANGELOG.md and add the new version section
# Move items from [Unreleased] to the new version
```

#### Update README (if needed)
```bash
# Update any version-specific information in README.md
```

### 2. Test the Release

#### Run Tests
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run linting
flake8 src/ tests/
black --check src/ tests/
mypy src/

# Run security checks
safety check
bandit -r src/
```

#### Test Installation
```bash
# Build the package
python -m build

# Check the package
twine check dist/*

# Test installation
pip install dist/panparsex-*.whl
```

### 3. Create Release Commit

```bash
# Add all changes
git add .

# Create release commit
git commit -m "chore: prepare release v0.1.1"

# Create and push tag
git tag -a v0.1.1 -m "Release v0.1.1"
git push origin main
git push origin v0.1.1
```

### 4. Automated Release (Recommended)

The GitHub Actions workflow will automatically:
1. Build the package
2. Upload to PyPI
3. Create a GitHub release
4. Upload release assets

#### Trigger Release
```bash
# Push the tag to trigger the release workflow
git push origin v0.1.1
```

### 5. Manual Release (Alternative)

If you need to release manually:

#### Build Package
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build
```

#### Upload to PyPI
```bash
# Upload to PyPI
twine upload dist/*

# Or upload to TestPyPI first
twine upload --repository testpypi dist/*
```

#### Create GitHub Release
1. Go to GitHub Releases page
2. Click "Create a new release"
3. Select the tag (e.g., v0.1.1)
4. Add release title and description
5. Upload dist/ files as assets
6. Publish the release

### 6. Post-Release Tasks

#### Verify Installation
```bash
# Test installation from PyPI
pip install panparsex

# Test basic functionality
python -c "from panparsex import parse; print('Installation successful')"
```

#### Update Documentation
- Update any version-specific documentation
- Update installation instructions if needed
- Update examples if they reference specific versions

#### Announce Release
- Update project status
- Notify users of new features
- Share on relevant forums/communities

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backward compatible
- **PATCH** (0.0.1): Bug fixes, backward compatible

### Examples
- `0.1.0` → `0.1.1`: Bug fix
- `0.1.1` → `0.2.0`: New feature
- `0.2.0` → `1.0.0`: Breaking change

## Release Checklist

### Before Release
- [ ] All tests pass
- [ ] Code is properly formatted
- [ ] No linting errors
- [ ] Security checks pass
- [ ] Documentation is updated
- [ ] Changelog is updated
- [ ] Version is updated in pyproject.toml
- [ ] README is updated (if needed)

### During Release
- [ ] Create release commit
- [ ] Create and push tag
- [ ] Verify automated release or perform manual release
- [ ] Check PyPI upload
- [ ] Verify GitHub release

### After Release
- [ ] Test installation from PyPI
- [ ] Verify basic functionality
- [ ] Update project status
- [ ] Announce release
- [ ] Monitor for issues

## Troubleshooting

### Common Issues

#### Build Failures
```bash
# Clean and rebuild
rm -rf dist/ build/ *.egg-info/
python -m build
```

#### Upload Failures
```bash
# Check PyPI credentials
twine check dist/*

# Verify package
pip install dist/panparsex-*.whl
```

#### Test Failures
```bash
# Run tests with verbose output
pytest -v

# Run specific test
pytest tests/test_basic.py -v
```

### Getting Help

- Check GitHub Issues for known problems
- Review GitHub Actions logs for build issues
- Contact maintainers for assistance

## Security Considerations

- Never commit API tokens or passwords
- Use GitHub Secrets for sensitive information
- Verify package integrity before release
- Monitor for security vulnerabilities

## Rollback Procedure

If a release has issues:

1. **Identify the problem**
2. **Create a hotfix** (if possible)
3. **Release a new version** with the fix
4. **Document the issue** and resolution
5. **Update users** about the fix

### Example Rollback
```bash
# Create hotfix branch
git checkout -b hotfix/v0.1.2

# Make fixes
# ... make changes ...

# Commit and tag
git commit -m "fix: critical bug in v0.1.1"
git tag -a v0.1.2 -m "Hotfix v0.1.2"
git push origin hotfix/v0.1.2
git push origin v0.1.2
```

## Best Practices

1. **Test thoroughly** before release
2. **Use semantic versioning** consistently
3. **Document changes** in changelog
4. **Automate releases** when possible
5. **Monitor after release** for issues
6. **Communicate changes** to users
7. **Keep releases frequent** but stable
8. **Maintain backward compatibility** when possible

## Release Schedule

- **Major releases**: As needed for breaking changes
- **Minor releases**: Monthly for new features
- **Patch releases**: As needed for bug fixes
- **Security releases**: Immediately for security issues

## Contact

For release-related questions or issues:
- Email: dhruvil.darji@gmail.com
- GitHub Issues: https://github.com/dhruvildarji/panparsex/issues
