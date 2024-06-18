## Environment

```
uv venv
source .venv/bin/activate
uv pip install eth_account eth_keys
```

## Commits

Commit messaged follow
[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
specification.

## Versioning

Versioning follows
[Semantic Versioning](https://semver.org/)
specification.

A new version is created as follows:

```
git tag -s $MAJOR.$MINOR.$PATCH -m $MAJOR.$MINOR.$PATCH
git push origin $MAJOR.$MINOR.$PATCH
```

## Resources

* https://tools.allnodes.com/eth/generate
