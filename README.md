# modl

Install and run AI models locally like packages.

    modl install <model-link>
    modl run <model>

------------------------------------------------------------------------

## Why modl?

Running AI models locally is often painful:

-   dependency conflicts
-   environment setup
-   broken installs
-   no standard way to share models

modl simplifies this.

Package models, share them via links, and run them instantly.

------------------------------------------------------------------------

## What you can do

-   Install models from a URL
-   Run them in isolated environments
-   Share models as `.mdl` files
-   Version and manage models locally

------------------------------------------------------------------------

## Quick Demo

### Install a model

    modl install https://github.com/aryansikhwal/modl/releases/download/sentiment-model-v1.0/sentiment-model-1.0.mdl

### Run it

    modl run sentiment-model

Example:

    Enter text: I love this
    Output: Positive

------------------------------------------------------------------------

## Try another model

    modl install https://github.com/aryansikhwal/modl/releases/download/keyword-model-v1.0/keyword-model-1.0.mdl

    modl run keyword-model

Example:

    Enter text: OpenAI builds powerful AI tools
    Keywords: openai, builds, powerful, tools

------------------------------------------------------------------------

## Installation

    git clone https://github.com/aryansikhwal/modl.git
    cd modl
    pip install -e .

    Requires: Python 3.10+
    Note: Currently install via source (dev mode). Packaging for pip coming soon.

------------------------------------------------------------------------

## Core Commands

    modl init <name>
    modl build .
    modl run <name>
    modl serve <name>
    modl list
    modl info <name>
    modl remove <name>
    modl export <name>
    modl install <file/url>
    modl push <name>
    modl pull <name>
    modl tag <name:version> <tag>
    modl --version        # check version

------------------------------------------------------------------------

## How it works

    init → build → install → run → share

-   Models are packaged as `.mdl` files
-   Installed into a local registry
-   Run in isolated environments
-   Shared via links

------------------------------------------------------------------------

## Create your own model

    modl init my-model
    cd my-model

Edit `run.py`, then:

    modl build .
    modl run my-model

------------------------------------------------------------------------

## Model management

    modl list
    modl info sentiment-model
    modl run sentiment-model:1.0
    modl tag sentiment-model:1.0 latest

-   Version models
-   Tag releases
-   Manage multiple versions locally

------------------------------------------------------------------------

## Why this matters

There is no simple standard today to install and run AI models locally
without friction.

modl aims to change that.

------------------------------------------------------------------------

## Vision

A standard way to package, share, and run AI models.

Similar to pip, npm, or docker --- but for models.

------------------------------------------------------------------------

## Status

Early version (v0.1)

Feedback is welcome.

------------------------------------------------------------------------

Winter is coming.
