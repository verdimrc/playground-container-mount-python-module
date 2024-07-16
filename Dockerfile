FROM python:3.12.4

ADD . /tmp/haha-repo

#Switch from sh to bash to allow parameter expansion
RUN cd /tmp/haha-repo \
    # Introduce a distinct marker to the module.
    && sed -i 's/^__version__ = "\(.*\)$/__version__ = "CONTAINER \1/' src/haha/__init__.py \
    # # Install this repo (which will also install its dependencies). No need editable because
    # # /tmp/haha-repo is a separate copy from the host's repo.
    && pip install . \
    && rm -fr /tmp/haha-repo

##### Demonstration of PYTHONPATH.
# NOTE: parent container does not define PYTHONPATH, hence below stanza.
ENV PYTHONPATH=/workspace/my-python-path
#
# For other parent containers that define define PYTHONPATH, comment the previous stanza, and
# uncomment the next stanza.
#ENV PYTHONPATH=/workspace/my-python-path:$PYTHONPATH
