# Matrix-RSSBot

[![Support Private.coffee!](https://shields.private.coffee/badge/private.coffee-support%20us!-pink?logo=coffeescript)](https://private.coffee)
[![PyPI](https://shields.private.coffee/pypi/v/matrix-rssbot)](https://pypi.org/project/matrix-rssbot/)
[![PyPI - Python Version](https://shields.private.coffee/pypi/pyversions/matrix-rssbot)](https://pypi.org/project/matrix-rssbot/)
[![PyPI - License](https://shields.private.coffee/pypi/l/matrix-rssbot)](https://pypi.org/project/matrix-rssbot/)
[![Latest Git Commit](https://shields.private.coffee/gitea/last-commit/privatecoffee/matrix-rssbot?gitea_url=https://git.private.coffee)](https://git.private.coffee/privatecoffee/matrix-rssbot)

This is a simple, no-database RSS/Atom feed bot for Matrix. It is designed to be easy to use and lightweight.

## Installation

```bash
pip install matrix-rssbot
```

Create a configuration file in `config.ini` based on the [config.dist.ini](config.dist.ini) provided in the repository.

At the very least, you need to provide the following configuration:

```ini
[Matrix]
Homeserver = http://your-homeserver.example.com
AccessToken = syt_YourAccessTokenHere
```

We recommend using pantalaimon as a proxy, because the bot itself does not support end-to-end encryption.

You can start the bot by running:

```bash
rssbot
```

## Usage

The bot will automatically join all rooms it is invited to.

You have to ensure that the bot has the necessary permissions to send state events and messages in the room. Regular users cannot send state events, so you have to either raise the bot user's power level (`Moderator` level should do) or lower the power level required to send state events.

You can now add a feed to the bot by sending a message to the bot in the room you want the feed to be posted in. The message should be in the following format:

```
!rssbot addfeed https://example.com/feed.xml
```

To list all feeds in a room, you can use the following command:

```
!rssbot listfeeds
```

Finally, to remove a feed, you can use the following command:

```
!rssbot removefeed https://example.com/feed.xml
```

Alternatively, you can use the number of the feed in the list, which you can get by using the `listfeeds` command instead of the URL.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
