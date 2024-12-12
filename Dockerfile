# Using Ubuntu 24.04
# Builder image
FROM ubuntu:24.04 AS python-builder-image

# Avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y tzdata software-properties-common \
      && add-apt-repository ppa:deadsnakes/ppa \
      && apt-get install --no-install-recommends -y \
      python3.11 \
      python3.11-dev \
      python3.11-venv \
      python3-pip \
      python3-wheel \
      build-essential \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*/*

# Create and activate virtual environment
# Using final folder name to avoid path issues with packages
RUN python3.11 -m venv /home/lupin/venv
ENV PATH="/home/lupin/venv/bin:$PATH"

# Install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

# Runner image
FROM ubuntu:24.04 AS runner-image

# Run the script
CMD [ "python3.11", "main.py" ]

# Add labels
LABEL maintainer="SchwartzKamel <lafiamafia@protonmail.com>"

ARG build_number
ARG build_timestamp
ARG build_url
ARG git_branch_name
ARG git_sha1

LABEL net.sierrahackingco.build.number="${build_number}" \
      net.sierrahackingco.build.timestamp="${build_timestamp}" \
      net.sierrahackingco.build.url="${build_url}" \
      net.sierrahackingco.discover.dockerfile="/Dockerfile" \
      net.sierrahackingco.discover.packages="apk info -v | sort" \
      net.sierrahackingco.git.branch-name="${git_branch_name}" \
      net.sierrahackingco.git.url="https://https://github.com/SchwartzKamel/docker-python-base" \
      net.sierrahackingco.git.sha-1="${git_sha1}" \
      net.sierrahackingco.project.name="docker-python-base" \
      net.sierrahackingco.project.url="https://https://github.com/SchwartzKamel/docker-python-base" \
      net.sierrahackingco.version="${git_branch_name}-${build_timestamp}"

RUN apt-get update && apt-get upgrade -y \
      && apt-get install -y tzdata software-properties-common \
      && add-apt-repository ppa:deadsnakes/ppa \
      && apt-get install --no-install-recommends -y \
      python3.11 \
      python3.11-venv \
      groff \
      jq \
      less \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home lupin
COPY --from=python-builder-image /home/lupin/venv /home/lupin/venv

USER lupin
RUN mkdir /home/lupin/code
WORKDIR /home/lupin/code
COPY /app .

# activate virtual environment
ENV VIRTUAL_ENV=/home/lupin/venv \
      PATH="/home/lupin/venv/bin:$PATH"