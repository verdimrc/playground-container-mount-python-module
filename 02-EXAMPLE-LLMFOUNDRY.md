# Real example

## Pre-built dependencies in the llm-foundry container

```console
$ docker pull mosaicml/llm-foundry:2.2.1_cu121_flash2-latest

# Verify container provides the dependencies equivalent to the ones installed by:
# ( cd composer && pip install -e '.[libcloud,wandb,oci,gcs] )' => read composer/setup.py to find out.
$ docker run -it --rm --user $(id -u):$(id -g) \
    mosaicml/llm-foundry:2.2.1_cu121_flash2-latest \
    /bin/bash -c "pip --disable-pip-version-check list | egrep 'libcloud|wandb|oci|google-cloud-storage'"
apache-libcloud             3.8.0
google-cloud-storage        2.10.0
oci                         2.126.1
wandb                       0.16.6

# Verify container provides the dependencies equivalent to the ones installed by:
# ( cd llm-foundry && pip install -e '.[gpu] )' => read llm-foundry/setup.py to find out.
$ docker run -it --rm --user $(id -u):$(id -g) \
    mosaicml/llm-foundry:2.2.1_cu121_flash2-latest \
    /bin/bash -c "pip --disable-pip-version-check list | egrep 'mosaicml|flash-attn' ; which composer"
flash-attn                  2.5.8
mosaicml                    0.22.0
mosaicml-cli                0.6.23
mosaicml-streaming          0.7.5
/usr/bin/composer

# According to composer.git's README.md, the container does not include llm-foundry. Users must
# provide it themselves.
$ docker run -it --rm --user $(id -u):$(id -g) \
    mosaicml/llm-foundry:2.2.1_cu121_flash2-latest \
    /bin/bash -c "pip --disable-pip-version-check list | egrep 'llmfoundry'"
<blank>

# See the container's default current dir
$ docker run -it --rm --user $(id -u):$(id -g) mosaicml/llm-foundry:2.2.1_cu121_flash2-latest pwd
/

# See if the container defines PYTHONPATH
$ docker run -it --rm --user $(id -u):$(id -g) mosaicml/llm-foundry:2.2.1_cu121_flash2-latest /bin/bash -c 'env | grep PYTHONPATH'
<blank>
```

## Override versions

```console
$ cd ~/src

$ git clone -b v0.22.0 https://github.com/mosaicml/composer.git
$ git clone -b v0.7.0 https://github.com/mosaicml/llm-foundry.git

# Verify that the container loads the host's versions. Mount the composer and llmfoundry into below
# tree:
#
# /                 # Current directory in the container
# |-- /composer     # Host's version of this module
# `-- /llmfoundry   # Host's version of this module
#
# NOTE: feel free to change or add more folders to mount, e.g., training scripts, data, etc.
$ docker run -it --rm --user $(id -u):$(id -g) \
    -v $(pwd)/composer/composer:/composer \
    -v $(pwd)/llm-foundry/llmfoundry:/llmfoundry \
    mosaicml/llm-foundry:2.2.1_cu121_flash2-latest \
    python -c "import composer, llmfoundry; print(f'{composer.__file__=}'); print(f'{llmfoundry.__file__=}')"
composer.__file__='/composer/__init__.py'
llmfoundry.__file__='/llmfoundry/__init__.py'

# Let's add some marker to the host's repos, then verify that the composer CLI (in the container)
# still correctly find the host's version.
$ echo "print ('HAHA: composer')" >> composer/composer/__init__.py
$ echo "print ('HAHA: llmfoundry')" >> llm-foundry/llmfoundry/__init__.py

# Re-probe the container, to validate it prints our HAHA markers.
$ docker run -it --rm --user $(id -u):$(id -g) \
    -v $(pwd)/composer/composer:/composer \
    -v $(pwd)/llm-foundry/llmfoundry:/llmfoundry \
    mosaicml/llm-foundry:2.2.1_cu121_flash2-latest \
    python -c "import composer, llmfoundry; print(f'{composer.__file__=}'); print(f'{llmfoundry.__file__=}')"
HAHA: composer
HAHA: llmfoundry
composer.__file__='/composer/__init__.py'
llmfoundry.__file__='/llmfoundry/__init__.py'
```
