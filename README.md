# Overview

This interface supports the integration between Barbican and secrets stores.

# Usage

No explicit handler is required to consume this interface in charms
that consume this interface.

The interface provides `secrets.connected` and `secrets.available` states.

## For an secrets subordinate charm

The `secrets.connected` state indicates that the Barbican principle charms has been
connected to.  At this point the plugin data required for to configure the secrets store
from Barbican should be presented.

# metadata

To consume this interface in your charm or layer, add the following to `layer.yaml`:

```yaml
includes: ['interface:barbican-secrets']
```

and add a provides interface of type `secrets` to your charm or layers
`metadata.yaml`:

```yaml
provides:
  secrets:
    interface: barbican-secrets
    scope: container
```

Please see the example 'Barbican Vault' charm for an example of how to author
an secrets store charm.

# Bugs

Please report bugs on [Launchpad](https://bugs.launchpad.net/openstack-charms/+filebug).

For development questions please refer to the OpenStack [Charm Guide](https://github.com/openstack/charm-guide).
