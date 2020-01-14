FROM ubuntu:18.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install --no-install-recommends -y \
    jq curl git \
    python3-minimal python3-pip \
    && pip3 install gitlint \
    && apt-get purge -y --auto-remove python3-pip \
    && rm -rf /var/lib/apt/lists/*

COPY bin/git-burn /usr/bin/
COPY share/git-burn/gitlint* /usr/share/git-burn/

ENTRYPOINT ["/usr/bin/git-burn"]
