### dekcli

```shell
# Input a token from gitea website, the token has all permissions.
dekcli gitea login https://sample.com

# git-set's repo dir path format: git-set/org/repo/.git
dekcli gitea init /path/to/git-set

# Add local ssh token to the gitea website settings, then clone a mirror repo to add .ssh/known_hosts

# Add secrets according to index.yaml

# Add gitea runner to cluster

dekcli gitea push /path/to/git-set
dekcli gitea pull /path/to/git-set
```
