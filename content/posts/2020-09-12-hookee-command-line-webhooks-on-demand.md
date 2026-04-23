---
title: "hookee - command line webhooks, on demand"
date: 2020-09-12
tags: 
  - "education"
  - "flask"
  - "ngrok"
  - "python"
  - "webhook"
---

[![hookee - command line webhooks, on demand](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fhookee.readthedocs.io%2Fen%2Flatest%2F_images%2Flogo.png)](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fhookee.readthedocs.io%2Fen%2Flatest%2F_images%2Flogo.png)

`hookee` is a utility that provides command line webhooks, on demand! Dump useful request data to the console, process requests and responses, customize response data, and configure `hookee` and its routes further in any number of ways through custom plugins.

## [](https://dev.to/alexdlaird/hookee-command-line-webhooks-on-demand-2of8#installation)Installation

`hookee` is available on [PyPI](https://pypi.org/project/hookee/) and can be installed using `pip`:

```bash
pip install hookee
```

or `conda`:

```bash
conda install -c conda-forge hookee
```

That's it! `hookee` is now available as a Python package and is available from the command line.

## [](https://dev.to/alexdlaird/hookee-command-line-webhooks-on-demand-2of8#basic-usage)Basic Usage

`hookee` makes it easy to get webhooks on the fly right from the console. Simply start it with:

```bash
hookee start
```

With its default configuration, this will start a server on port 8000, open a [`ngrok`](https://ngrok.com/) tunnel using [`pyngrok`](https://pyngrok.readthedocs.io/en/latest/), and mount a URL at `/webhook`. Sending any request to the `/webhook` endpoint will dump the request and response data to the console.

`hookee` can be configured in a number of ways to quickly and easily tweak request and response data. For example, here is how you can customize the response body from `/webhook` using the `--response` arg.

```bash
hookee --response "<Response>Ok</Response>" \
    --content-type application/xml
```

`hookee` can also be started without a tunnel (removing the dependency on an Internet connection). Using the `--no-tunnel` flag only starts `hookee`'s server, allowing responses to be mocked locally. This can be particularly useful when service discovery is done through a proxy service (ex. [HAProxy](https://www.haproxy.org/), [Envoy](https://www.envoyproxy.io/), etc.), meaning you can tell `hookee` to start on the port of an expected downstream, thus intercepting requests to that service to provide your own responses in an isolated environment, very useful for rapid local development, cluster testing, and more.

```bash
hookee --no-tunnel --response "<Response>Ok</Response>" \
    --content-type application/xml \
    --default-route /some/route \
    --port 19780
```

To see the ways `hookee` can be tweaked right from the console, view its documented args and commands like this:

```bash
hookee --help
```

## [](https://dev.to/alexdlaird/hookee-command-line-webhooks-on-demand-2of8#documentation)Documentation

For more advanced usage, including how `hookee`'s default configuration can be changed, extended through plugins, API integrations, and more, see its official documentation is available at [http://hookee.readthedocs.io](http://hookee.readthedocs.io/).

## [](https://dev.to/alexdlaird/hookee-command-line-webhooks-on-demand-2of8#contributing)Contributing

If you would like to get involved, be sure to review the [Contribution Guide](https://github.com/alexdlaird/hookee/blob/main/CONTRIBUTING.rst).

Want to contribute financially? If you've found `hookee` useful, [sponsorship](https://github.com/sponsors/alexdlaird)  
would also be greatly appreciated!
