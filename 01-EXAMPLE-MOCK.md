# Mock examples

## 1. Under the hood of Python editable install: simple demonstration

Pre-requisite: a virtual environment.

```console
# Activate my virtual environment
$ pyenv activate pt23-py312

# Ensure we're on the right directory
$ pwd
/home/vmarch/src/playground-container-mount-python-module

$ pip install -e .
...

$ python -c "import haha; print(f'{haha.__file__=}')"
haha.__file__='/home/vmarch/src/playground-container-mount-python-module/src/haha/__init__.py'

$ python -c "import torch; print(f'{torch.__file__=}')"
torch.__file__='/home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/torch/__init__.py'

$ ls -ald /home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/*haha*
-rw-r--r-- 1 vmarch vmarch   51 Jul 16 13:59 /home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/__editable__.haha-0.0.1.pth
drwxr-xr-x 2 vmarch vmarch 4096 Jul 16 13:59 /home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info

$ cat /home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/__editable__.haha-0.0.1.pth
/home/vmarch/src/playground-container-mount-python-module/src

$ find /home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info/ -type f
/home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info/top_level.txt
/home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info/LICENSE
/home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info/INSTALLER
/home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info/RECORD
/home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info/direct_url.json
/home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info/WHEEL
/home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info/METADATA
/home/vmarch/.pyenv/versions/pt23-py312/lib/python3.12/site-packages/haha-0.0.1.dist-info/REQUESTED

$ find . -iname '*egg-info'
./src/haha.egg-info

$ find src/haha.egg-info -type f
src/haha.egg-info/top_level.txt
src/haha.egg-info/dependency_links.txt
src/haha.egg-info/SOURCES.txt
src/haha.egg-info/PKG-INFO

$ pip install build setupext-janitor

# Remove build artifact ONLY by setting VIRTUAL_ENV empty.
# BEWARE: Without VIRTUAL_ENV='', your whole virtualenv will be deleted!
$ VIRTUAL_ENV='' python setup.py clean --all
running clean
'build/lib' does not exist -- can't clean it
'build/bdist.linux-x86_64' does not exist -- can't clean it
'build/scripts-3.12' does not exist -- can't clean it
removing './src/haha/__pycache__' (and everything under it)
removing 'src/haha.egg-info' (and everything under it)

$ find . -iname '*egg-info'
<empty>

# Note the module is still installed.
$ python -c "import haha; print(f'{haha.__file__=}')"
haha.__file__='/home/vmarch/src/playground-container-mount-python-module/src/haha/__init__.py'
```

## 2. Demonstration with container

When working with container, we can directly mount the module to the container with all dependencies
baked in it.

```console
# Ensure we're on the right directory
$ pwd
/home/vmarch/src/playground-container-mount-python-module

$ docker build -t haha .

$ docker run -it --rm --user $(id -u):$(id -g) haha:latest  python -c "import haha; print(f'{haha.__file__=}'); print(f'{haha.__version__=}')"
haha.__file__='/usr/local/lib/python3.12/site-packages/haha/__init__.py'
haha.__version__='CONTAINER HAHA HEHE'

# Let's find the default current directory of this container
$ docker run -it --rm --user $(id -u):$(id -g) haha:latest pwd
/

# Override the built-in haha module (in the container) with the host's version.
#
# When the container runs, there're are two versions: one under / (current directory), and the other
# under /usr/.../dist-packages/.
# Python prioritizes the module in the current directory, hence loading /haha/
$ docker run -it --rm --user $(id -u):$(id -g) \
    -v $(pwd)/src/haha:/haha \
    haha:latest \
    python -c "import haha; print(f'{haha.__file__=}'); print(f'{haha.__version__=}')"
haha.__file__='/haha/__init__.py'
haha.__version__='HAHA HEHE'

# Another validation: checks the presence of two haha/ modules.
$ docker run -it --rm --user $(id -u):$(id -g) \
    -v $(pwd)/src/haha:/haha \
    haha:latest \
    bash -c "find / -name haha 2> /dev/null"
/usr/local/lib/python3.12/site-packages/haha
/haha

# We can also use the PYTHONPATH trick when we mount host's haha/ not directly under / (i.e., the
# container current dir).
#
# First, let's confirm that when host's version is not directly under / or PYTHONPATH, python still
# loads the container's version.
$ docker run -it --rm --user $(id -u):$(id -g) \
    -v $(pwd)/src/haha:/some-random-dir \
    haha:latest \
    python -c "import os; import haha; print(f'{os.getenv(\"PYTHONPATH\")=}'); print(f'{haha.__file__=}'); print(f'{haha.__version__=}')"
haha.__file__='/usr/local/lib/python3.12/site-packages/haha/__init__.py'
haha.__version__='CONTAINER HAHA HEHE'

# Mount the host's version to the PYTHONPATH to override the container's version.
$ docker run -it --rm --user $(id -u):$(id -g) \
    -v $(pwd)/src/haha:/workspace/my-python-path/haha \
    haha:latest \
    python -c "import haha; print(f'{haha.__file__=}'); print(f'{haha.__version__=}')"
haha.__file__='/workspace/my-python-path/haha/__init__.py'
haha.__version__='HAHA HEHE'
```
