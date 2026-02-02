FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV CKAN_HOME=/usr/lib/ckan
ENV CKAN_CONFIG=/etc/ckan/default/ckan.ini

# Disable broken dep11 indexes (Ubuntu noble mirror issue)
RUN echo 'Acquire::IndexTargets::deb::Packages::KeepCompressed "true";' > /etc/apt/apt.conf.d/99no-dep11 \
 && echo 'Acquire::IndexTargets::deb::Translations "none";' >> /etc/apt/apt.conf.d/99no-dep11 \
 && echo 'Acquire::IndexTargets::deb::DEP-11 "false";' >> /etc/apt/apt.conf.d/99no-dep11
 
# -------------------------------
# 1. Sistema base + PPA
# -------------------------------
RUN apt-get update && apt-get install -y \
    software-properties-common \
    ca-certificates \
    curl \
    gnupg \
    nano \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update

# -------------------------------
# 2. Python 3.10 + deps nativas
# -------------------------------
RUN apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip \
    build-essential \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libssl-dev \
    libgeos-dev \
    libjpeg-dev \
    zlib1g-dev \
    git \
    wget \
    locales \
    postgresql-client \
    redis-server \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# 3. Locale
# -------------------------------
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# -------------------------------
# 4. Usuario CKAN
# -------------------------------
RUN useradd -r -m -d ${CKAN_HOME} -s /bin/bash ckan

# -------------------------------
# 5. Virtualenv Python 3.10
# -------------------------------
RUN python3.10 -m venv ${CKAN_HOME}/venv
# virtualenv ya creado
ENV PATH="/usr/lib/ckan/venv/bin:$PATH"

RUN pip install --upgrade pip "setuptools<81" wheel

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt




# -------------------------------
# 8. Directorios
# -------------------------------
RUN mkdir -p /etc/ckan/default /var/lib/ckan /var/log/ckan \
    && chown -R ckan:ckan /etc/ckan /var/lib/ckan /var/log/ckan ${CKAN_HOME}

USER ckan
