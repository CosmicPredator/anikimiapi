<h1 style="text-align: center;">AniKimi API</h1>
<div align="center">A Simple, LightWeight, Statically-Typed Python3 API wrapper for GogoAnime</div>
<div align="center">The v2 of gogoanimeapi (depreciated)</div>
<div align="center">Made with JavaScript and Python3</div>

###

<div align="center">
<img src="https://img.shields.io/pypi/v/anikimiapi?style=for-the-badge">
<img src="https://img.shields.io/pypi/dd/anikimiapi?style=for-the-badge">
<img src="https://img.shields.io/pypi/status/anikimiapi?style=for-the-badge">
<img src="https://img.shields.io/github/repo-size/BaraniARR/anikimiapi?style=for-the-badge">
<img src="https://img.shields.io/pypi/l/anikimiapi?style=for-the-badge">
<img src="https://img.shields.io/pypi/pyversions/anikimiapi?style=for-the-badge">
<img src="https://img.shields.io/pypi/implementation/anikimiapi?style=for-the-badge">
</div>

###

### Features of AniKimi
* Custom url changing option.
* Statically-Typed, No more annoying JSON responses.
* Autocomplete supported by most IDE's.
* Complete solution.
* Faster response.
* Less CPU consumption.

### Installing
Using Pypi

```$ pip3 install anikimiapi```

### Getting Started
#### Pre-Requisites
* #### Getting Required Tokens
  * Visit the GogoAnime Website.
  * Login or SignUp using ur email or google.
  * Add an extension to your browser named [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid?hl=en).
  * Now in the GogoAnime Website, right click and select "Get cookies.txt"
  * A `.txt` file will be downloaded.
  * In the `.txt` file, find the name "gogoanime" and "auth".
  * Copy the respective tokens on the right side of the above names.
  * Keep it safely, since its your private credentials.

### Diving into the API
###
#### Authorize the API
To Authorize the API, use AniKimi class. You can also import it from other files. It also supports cross imports. But all API request should be made using this class only.
```python3
from anikimiapi import AniKimi

# Initialize AniKimi class
anime = AniKimi(
    gogoanime_token="the saved gogoanime token",
    auth_token="the saved auth token",
    host="https://gogoanime.pe/"  
)
```
###
>**Note:** If GogoAnime changes their domain, use the 'host' parameter. Otherwise, leave it blank. This parameter was optional and defaults to https://gogoanime.pe/
###
#### Getting Anime search results
You can search anime by using `search_anime` method, It returns the search results as `ResultObject` which contains two arguments, the `title` and `animeid`.
```python3
from anikimiapi import AniKimi

anime = AniKimi(
    gogoanime_token="the saved gogoanime token",
    auth_token="the saved auth token"
)

# Search Anime
results = anime.search_anime(query="tokikaku kawaii")

for i in results:
    print(i.title) # (or)
    print(i.animeid)
```

###
>**Note:** If no search results found, the API will raise `NoSearchResultsError` error. Make sure to handle it.
###
#### Getting details of a specific Anime
You can the basic information about a specific anime with `animeid` using `get_details` method. It will return anime details as `MediaInfoObject`.

The `MediaInfoObject` contains the following arguments,
* title
* other_names
* season
* year
* status
* genres
* episodes
* image_url
* summary
```python
from anikimiapi import AniKimi

anime = AniKimi(
    gogoanime_token="the saved gogoanime token",
    auth_token="the saved auth token"
)

# Get anime Details
details = anime.get_details(animeid="clannad-dub")
print(details.title)
print(details.genres) # And many more...
```

###
>**Note:** If an Invalid `animeid` is given, the API will raise `InvalidAnimeIdError`. Make sure to handle it.
###
#### Getting the Anime Links
You can simply get the streamable and downloadable links of a specific episode of an Anime by its `animeid` and `episode_num` using `get_episode_link` method. It will return anime links in `MediaLinksObject`.

The `MediaLinksObject` returns the links, if available. Otherwise, it will return `None`. The `MediaLinksObject` has the following arguments,
* link_hdp
* link_sdp
* link_360p
* link_480p
* link_720p
* link_1080p
* link_streamsb
* link_xstreamcdn
* link_streamtape
* link_mixdrop
* link_mp4upload
* link_doodstream
```python3
from anikimiapi import AniKimi

anime = AniKimi(
    gogoanime_token="the saved gogoanime token",
    auth_token="the saved auth token"
)

# Getting Anime Links basic method
anime_link = anime.get_episode_link_basic(animeid="clannad-dub", episode_num=3)

print(anime_link.link_hdp)
print(anime_link.link_720p)
print(anime_link.link_streamsb) # And many more...

# Getting Anime Links advanced method
anime_link = anime.get_episode_link_advanced(animeid="clannad-dub", episode_num=3)

print(anime_link.link_hdp)
print(anime_link.link_720p)
print(anime_link.link_streamsb) # And many more...
```
### 
>**Note:** If invalid `animeid` or `episode_num` is passed, the API will return `InvalidAnimeIdError`. Make sure to handle it.
>
> If the given `gogoanime_token` and `auth_token` are invalid, the API will raise `InvalidTokenError`. So, be careful of that.
###
#### Getting a List of anime by Genre
You can also get the List of anime by their genres using `get_by_genres` method. This method will return results as a List of `ResultObject`.

Currently, the following genres are supported,
* action                                
* adventure
* cars
* comedy
* dementia
* demons
* drama
* dub
* ecchi
* fantasy
* game
* harem
* hentai - Temporarily Unavailable
* historical
* horror
* josei
* kids
* magic
* martial-arts
* mecha
* military
* music
* mystery
* parody
* police
* psychological
* romance
* samurai
* school
* sci-fi
* seinen
* shoujo
* shoujo-ai
* shounen-ai
* shounen
* slice-of-life
* space
* sports
* super-power
* supernatural
* thriller
* vampire
* yaoi
* yuri
```python
from anikimiapi import AniKimi

anime = AniKimi(
    gogoanime_token="the saved gogoanime token",
    auth_token="the saved auth token"
)

# Getting anime list by genres
gen = anime.get_by_genres(genre_name="romance", page=1)

for result in gen:
    print(result.title)
    print(result.animeid)
```
###
>**Note:** If invalid `genre_name` or `page` is passed, the API will raise `InvalidGenreNameError`. Make sure to handle it.
###
#### Getting List of Airing Anime (v2 API New Feature)
You can get a List of currently Airing Anime using `get_airing_anime` method. This method will return results as a List of `ResultObject`.
```python
from anikimiapi import AniKimi

anime = AniKimi(
    gogoanime_token="the saved gogoanime token",
    auth_token="the saved auth token"
)

# Getting Airing Anime List
airing = anime.get_airing_anime(count=15)
for i in airing:
    print(i.title)
    print(i.animeid)
```
###
>**Note:** If the value of count exceeds 20, The API will raise `AiringIndexError`. So, pass a value less than or equal to 20.

# Copyrights ©2021 BaraniARR;
### Licensed under GNU GPLv3 Licnense;
