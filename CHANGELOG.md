# Changelog

## v0.1.4-beta (01.09.2021) <img src="https://img.shields.io/badge/-latest-brightgreen"/>

### What's new:

- `get_episode_link` is now seperated into `get_episode_link_basic` and `get_episode_link_advanced`. If gogoanime enables the captcha for the links, use `get_episode_link_advanced` else use `get_episode_link_basic` method.

> Note: You still need to initialize the `AniKimi` class to get stuffs.

### Enhancements:

- Reduced the CPU usage as compared to previous releases.

### Bug Fixes:
 - Fixed some wrong regex patterns.

 > Note: You should rewrite the API part of your app to function properly. I'm really sorry becoz you must rewrite your code to make your app support the latest release.


## v0.1.3-beta (01.08.2021)

### Enhancements:

- Little touch-up for the code.

### Bug Fixes:
- Removed an unwanted dependency "validtors".


## v0.1.1-beta (30.07.2021)

### What's new:

- Initial Release of the API Wrapper.
- Advanced Captcha Bypass is supported.