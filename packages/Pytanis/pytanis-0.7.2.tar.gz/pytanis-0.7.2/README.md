<div align="center">

<img src="https://raw.githubusercontent.com/FlorianWilhelm/pytanis/main/docs/assets/images/logo.svg" alt="Pytanis logo" width="500" role="img">
</div>

Pytanis includes a [Pretalx] client and all the tooling you need for conferences using [Pretalx], from handling the initial call for papers to creating the final program.
<br/>

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![CI - Test](https://github.com/FlorianWilhelm/pytanis/actions/workflows/run-tests.yml/badge.svg)](https://github.com/FlorianWilhelm/pytanis/actions/workflows/run-tests.yml) [![Coverage](https://img.shields.io/coveralls/github/FlorianWilhelm/pytanis/main.svg?logo=coveralls&label=Coverage)](https://coveralls.io/r/FlorianWilhelm/pytanis) [![CD - Build](https://github.com/FlorianWilhelm/pytanis/actions/workflows/publish-pkg.yml/badge.svg)](https://github.com/FlorianWilhelm/pytanis/actions/workflows/publish-pkg.yml) [![Docs - Build](https://github.com/FlorianWilhelm/pytanis/actions/workflows/build-rel-docs.yml/badge.svg)](https://github.com/FlorianWilhelm/pytanis/actions/workflows/build-rel-docs.yml)                                                                                                            |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/pytanis.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/pytanis/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/pytanis.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pepy.tech/project/pytanis) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytanis.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/pytanis/)                                                                                                                                                                                                                                                                                                                                                                                        |
| Details | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff) [![types - Mypy](https://img.shields.io/badge/Types-Mypy-blue.svg)](https://github.com/python/mypy) [![License - MIT](https://img.shields.io/badge/License-MIT-9400d3.svg)](https://spdx.org/licenses/) [![GitHub Sponsors](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=ff69b4)](https://github.com/sponsors/FlorianWilhelm) |

**Trivia**: The name *Pytanis* is a reference to [Prytanis] using the typical *py* prefix of [Python] tools. [Prytanis]
was the name given  to the leading members of the government of a city (polis) in ancient Greece. Offices that used this
title usually had responsibility for presiding over councils of some kind, which met in the [Prytaneion]. Romani ite domum!

## Features

- [x] simple configuration management with a config folder in your home directory, just like many other tools do
- [x] easily access [Google Sheets], potentially filled by some [Google Forms], and download sheets as data frames
- [x] easy to use [Pretalx] client that returns proper Python objects thanks to the power of [pydantic]
- [x] simple [HelpDesk] client for batch mails, e.g. to your reviewers
- [x] awesome [documentation] with best practices for the program committee of any community-based conference
- [x] tools to assign proposals to reviewers based on constraints like preferences
- [x] tools to support the final selection process of proposals
- [x] tools to support the creation of the final program schedule

## Getting started

To install Pytanis simple run:

```commandline
pip install pytanis
```

or to install all recommended additional dependencies:

```commandline
pip install 'pytanis[all]'
```

Then create a configuration file and directory in your user's home directory. For Linux/MacOS/Unix use
`~/.pytanis/config.toml` and for Windows `$HOME\.pytanis\config.toml`, where `$HOME` is e.g. `C:\Users\yourusername\`.
Use your favourite editor to open `config.toml` within the `.pytanis` directory and add the following content:

```toml
[Pretalx]
api_token = "932ndsf9uk32nf9sdkn3454532nj32jn"

[Google]
client_secret_json = "client_secret.json"
token_json = "token.json"
service_user_authentication = false

[HelpDesk]
account = "934jcjkdf-39df-9df-93kf-934jfhuuij39fd"
entity_id = "email@host.com"
token = "dal:Sx4id934C3Y-X934jldjdfjk"
```

where you need to replace the dummy values in the sections `[Pretalx]` and `[HelpDesk]` accordingly. Note that `service_user_authentication` is not required to be set if authentication via a service user is not necessary (see [GSpread using Service Account] for more details).

### Retrieving the Credentials and Tokens

- **Google**:
  - For end users: Follow the [Python Quickstart for the Google API] to generate and download the file `client_secret.json`.
Move it to the `~/.pytanis` folder as `client_secret.json`. The file `token.json` will be automatically generated
later. Note that `config.toml` references those two files relative to its own location.
  - For any automation project: Follow [GSpread using Service Account] to generate and download the file `client_secret.json`.
Move it to the `~/.pytanis` folder as `client_secret.json`. Also make sure to set `service_user_authentication = true` in your `~/.pytanis/config.toml`.
- **Pretalx**: The API token can be found in the [Pretalx user settings].
- **HelpDesk**: Login to the [LiveChat Developer Console] then go to <kbd>Tools</kbd> » <kbd>Personal Access Tokens</kbd>.
  Choose <kbd>Create new token +</kbd>, enter a the name `Pytanis`, select all scopes and confirm. In the following screen
  copy the `Account ID`, `Entity ID` and `Token` and paste them into `config.toml`.
  In case there is any trouble with livechat, contact a helpdesk admin. Also note that the `Account ID` from your token is
  the `Agent ID` needed when you create a ticket. The `Team ID` you get from [HelpDesk] then <kbd>Agents</kbd> »
  <kbd>Name of your agent</kbd> and the final part of the URL shown now.

  **When setting up your agent the first time**,
  you also need to go to [LiveChat] then log in with your Helpdesk team credentials and click <kbd>Request</kbd> to get an invitation.
  An admin of [LiveChat] needs to confirm this and add you as role `admin`. Then, check [HelpDesk] to receive the invitation
  and accept.

## Development

This section is only relevant if you want to contribute to Pytanis itself. Your help is highly appreciated!

After having cloned this repository:

1. install [hatch] globally, e.g. `pipx install hatch`,
2. install [pre-commit] globally, e.g. `pipx install pre-commit`,
3. \[only once\] run `hatch config set dirs.env.virtual .direnv`  to let [VS Code] find your virtual environments.

and then you are already set up to start hacking. Use `hatch run` to do everything you would normally do in a virtual
environment, e.g. `hatch run juptyer lab` to start [JupyterLab] in the default environment, `hatch run cov` for unit tests
and coverage (like [tox]) or `hatch run docs:serve` to build & serve the documentation. For code hygiene, execute `hatch run lint:all`
in order to run [ruff] and [mypy] or `hatch run lint:fix` to automatically fix formatting issues.
Check out the `[tool.hatch.envs]` sections  in [pyproject.toml](pyproject.toml) to learn about other commands.
If you really must enter a virtual environment, use `hatch shell` to enter the default environment.

## Documentation

The [documentation] is made with [Material for MkDocs] and is hosted by [GitHub Pages]. Your help to extend the
documentation, especially in the context of using Pytanis for community conferences like [PyConDE], [EuroPython], etc.
is highly appreciated.

## License & Credits

[Pytanis] is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
To start this project off a lot of inspiration and code was taken from [Alexander Hendorf] and [Matthias Hofmann].

[Pytanis]: https://florianwilhelm.info/pytanis/
[Python]: https://www.python.org/
[Pretalx]: https://pretalx.com/
[hatch]: https://hatch.pypa.io/
[pre-commit]: https://pre-commit.com/
[Prytanis]: https://en.wikipedia.org/wiki/Prytaneis
[Prytaneion]: https://en.wikipedia.org/wiki/Prytaneion
[Python Quickstart for the Google API]: https://developers.google.com/sheets/api/quickstart/python
[GSpread using Service Account]: https://docs.gspread.org/en/v5.12.4/oauth2.html#for-bots-using-service-account
[Pretalx user settings]: https://pretalx.com/orga/me
[documentation]: https://florianwilhelm.info/pytanis/
[Alexander Hendorf]: https://github.com/alanderex
[Matthias Hofmann]: https://github.com/mj-hofmann
[Google Forms]: https://www.google.com/forms/about/
[Google Sheets]: https://www.google.com/sheets/about/
[pydantic]: https://docs.pydantic.dev/
[HelpDesk]: https://www.helpdesk.com/
[Material for MkDocs]: https://github.com/squidfunk/mkdocs-material
[GitHub Pages]: https://docs.github.com/en/pages
[PyConDE]: https://pycon.de/
[EuroPython]: https://europython.eu/
[LiveChat Developer Console]: https://platform.text.com/console/
[JupyterLab]: https://jupyter.org/
[tox]: https://tox.wiki/
[mypy]: https://mypy-lang.org/
[ruff]: https://github.com/astral-sh/ruff
[VS Code]: https://code.visualstudio.com/
[LiveChat]: https://www.livechat.com/
