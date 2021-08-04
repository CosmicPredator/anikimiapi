from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
from anikimiapi.data_classes import *
from anikimiapi.error_handlers import *
import re


class AniKimi:
    """The `AniKimi` class which authorizes the gogoanime client.

    Parameters:
        gogoanime_token (``str``):
            To get this token, please refer to readme.md in the repository.
        auth_token (``str``):
            To get this token, please refer to readme.md in the repository.
        host (``str``):
            Change the base url, If gogoanime changes the domain, replace the url
            with the new domain. Defaults to https://gogoanime.pe/ .

    Example:
        .. code-block:: python
            :emphasize-lines: 1,4-7

            from anikimiapi import AniKimi

            # Authorize the api to GogoAnime
            anime = AniKimi(
                gogoanime_token="baikdk32hk1nrek3hw9",
                auth_token="NCONW9H48HNFONW9Y94NJT49YTHO45TU4Y8YT93HOGFNRKBI"
            )



    """
    def __init__(
            self,
            gogoanime_token: str,
            auth_token: str,
            host: str = "https://gogoanime.pe/"
    ):
        self.gogoanime_token = gogoanime_token
        self.auth_token = auth_token
        self.host = host

    def search_anime(self, query: str) -> list:
        """The method used to search anime when a query string is passed

        Parameters:
            query(``str``):
                The query String which was to be searched in the API.

        Returns:
            List of :obj:`-anikimiapi.data_classes.ResultObject`: On Success, the list of search results is returned.

        Example:
        .. code-block:: python
            :emphasize-lines: 1,4-7,10-13

            from anikimiapi import AniKimi

            # Authorize the api to GogoAnime
            anime = AniKimi(
                gogoanime_token="baikdk32hk1nrek3hw9",
                auth_token="NCONW9H48HNFONW9Y94NJT49YTHO45TU4Y8YT93HOGFNRKBI"
            )

            # Get search Results
            search_results = anime.search_anime(query="clannad")
            for results in search_results:
                print(results.title)
                print(results.animeid)
        """
        try:
            url1 = f"{self.host}/search.html?keyword={query}"
            session = HTMLSession()
            response = session.get(url1)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            res_list_search = []
            for anime in animes:  # For every anime found
                tit = anime.a["title"]
                urll = anime.a["href"]
                r = urll.split('/')
                res_list_search.append(ResultObject(title=f"{tit}", animeid=f"{r[2]}"))
            if not res_list_search:
                raise NoSearchResultsError("No Search Results found for the query")
            else:
                return res_list_search
        except requests.exceptions.ConnectionError:
            raise NetworkError("Unable to connect to the Server, Check your connection")

    def get_details(self, animeid: str) -> MediaInfoObject:
        """Get the basic details of anime using an animeid parameter.

        Parameters:
            animeid(``str``):
                The animeid of the anime which you want to get the details.

        Returns:
            :obj:`-anikimiapi.data_classes.MediaInfoObject`: On success, the details of anime is returned as ``MediaInfoObject`` object.

        Example:
        .. code-block:: python
            :emphasize-lines: 1,4-7,10-12

            from anikimiapi import AniKimi

            # Authorize the api to GogoAnime
            anime = AniKimi(
                gogoanime_token="baikdk32hk1nrek3hw9",
                auth_token="NCONW9H48HNFONW9Y94NJT49YTHO45TU4Y8YT93HOGFNRKBI"
            )

            # Get anime Details
            details = anime.get_details(animeid="clannad-dub")
            print(details.image_url) # gives the url of the cover image
            print(details.status) # gives the status whether airing or completed

            # And many more...
        """
        try:
            animelink = f'{self.host}category/{animeid}'
            response = requests.get(animelink)
            plainText = response.text
            soup = BeautifulSoup(plainText, "lxml")
            source_url = soup.find("div", {"class": "anime_info_body_bg"}).img
            imgg = source_url.get('src')
            tit_url = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
            lis = soup.find_all('p', {"class": "type"})
            plot_sum = lis[1]
            pl = plot_sum.get_text().split(':')
            pl.remove(pl[0])
            sum = ""
            plot_summary = sum.join(pl)
            type_of_show = lis[0].a['title']
            ai = lis[2].find_all('a')  # .find_all('title')
            genres = []
            for link in ai:
                genres.append(link.get('title'))
            year1 = lis[3].get_text()
            year2 = year1.split(" ")
            year = year2[1]
            status = lis[4].a.get_text()
            oth_names = lis[5].get_text()
            lnk = soup.find(id="episode_page")
            ep_str = str(lnk.contents[-2])
            a_tag = ep_str.split("\n")[-2]
            a_tag_sliced = a_tag[:-4].split(">")
            last_ep_range = a_tag_sliced[-1]
            y = last_ep_range.split("-")
            ep_num = y[-1]
            res_detail_search = MediaInfoObject(
                title=f"{tit_url}",
                year=int(year),
                other_names=f"{oth_names}",
                season=f"{type_of_show}",
                status=f"{status}",
                genres=genres,
                episodes=int(ep_num),
                image_url=f"{imgg}",
                summary=f"{plot_summary}"
            )
            return res_detail_search
        except AttributeError:
            raise InvalidAnimeIdError("Invalid animeid given")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Unable to connect to the Server, Check your connection")

    def get_episode_link(self, animeid: str, episode_num: int) -> MediaLinksObject:
        """Get streamable and downloadable links for a given animeid and episode number.
        If the link is not found, then this method will return ``None`` .

        Parameters:
             animeid(``str``):
                The animeid of the anime you want to download.

             episode_num(``int``):
                The episode number of the anime you want to download.

        Returns:
            :obj:`-anikimiapi.data_classes.MediaLinksObject`: On success, the links of the anime is returned.

        Example:
        .. code-block:: python
            :emphasize-lines: 1,4-7,10-13

            from anikimiapi import AniKimi

            # Authorize the api to GogoAnime
            anime = AniKimi(
                gogoanime_token="baikdk32hk1nrek3hw9",
                auth_token="NCONW9H48HNFONW9Y94NJT49YTHO45TU4Y8YT93HOGFNRKBI"
            )

            # Get anime Link
            link = anime.get_episode_link(animeid="clannad-dub", episode_num=3)
            print(link.link_hdp)
            print(link.link_360p)
            print(link.link_streamtape)

            # and many more...
        """
        try:
            ep_num_link_get = episode_num
            str_qry_final = animeid
            animelink = f'{self.host}category/{str_qry_final}'
            response = requests.get(animelink)
            plainText = response.text
            soup = BeautifulSoup(plainText, "lxml")
            lnk = soup.find(id="episode_page")
            source_url = lnk.find("li").a
            anime_title = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
            ep_num_tot = source_url.get("ep_end")
            last_ep = int(ep_num_tot)
            episode_url = '{}{}-episode-{}'
            url = episode_url.format(self.host, str_qry_final, ep_num_link_get)
            master_keyboard_list = []
            cookies = {
                'gogoanime': self.gogoanime_token,
                'auth': self.auth_token
            }
            response = requests.get(url=url, cookies=cookies)
            plaintext = response.text
            soup = BeautifulSoup(plaintext, "lxml")
            download_div = soup.find("div", {'class': 'cf-download'}).findAll('a')
            links_final = MediaLinksObject()
            for links in download_div:
                download_links = links['href']
                q_name_raw = links.text.strip()
                q_name_raw_list = q_name_raw.split('x')
                quality_name = q_name_raw_list[1]  # 360, 720, 1080p links .just append to keyb lists with name and href
                if quality_name == "360":
                    links_final.link_360p = download_links
                elif quality_name == "480":
                    links_final.link_480p = download_links
                elif quality_name == "720":
                    links_final.link_720p = download_links
                elif quality_name == "1080":
                    links_final.link_1080p = download_links
            anime_multi_link_initial = soup.find('div', {'class': 'anime_muti_link'}).findAll('li')
            anime_multi_link_initial.remove(anime_multi_link_initial[0])
            chumma_list = []
            for l in anime_multi_link_initial:
                get_a = l.find('a')
                video_links = get_a['data-video']
                valid = video_links[0:4]
                if valid == "http":
                    pass
                else:
                    video_links = f"https:{video_links}"
                chumma_list.append(video_links)
            anime_multi_link_initial.remove(anime_multi_link_initial[0])
            for other_links in anime_multi_link_initial:
                get_a_other = other_links.find('a')
                video_link_other = get_a_other['data-video']  # video links other websites
                quality_name_others = other_links.text.strip().split('C')[0]  # other links name quality
                if quality_name_others == "Streamsb":
                    links_final.link_streamsb = video_link_other
                elif quality_name_others == "Xstreamcdn":
                    links_final.link_xstreamcdn = video_link_other
                elif quality_name_others == "Streamtape":
                    links_final.link_streamtape = video_link_other
                elif quality_name_others == "Mixdrop":
                    links_final.link_mixdrop = video_link_other
                elif quality_name_others == "Mp4Upload":
                    links_final.link_mp4upload = video_link_other
                elif quality_name_others == "Doodstream":
                    links_final.link_doodstream = video_link_other
            res = requests.get(chumma_list[0])
            plain = res.text
            s = BeautifulSoup(plain, "lxml")
            t = s.findAll('script')
            hdp_js = t[2].string
            hdp_link_initial = re.search("(?P<url>https?://[^\s]+)", hdp_js).group("url")
            hdp_link_initial_list = hdp_link_initial.split("'")
            hdp_link_final = hdp_link_initial_list[0]  # final hdp links
            links_final.link_hdp = hdp_link_final
            return links_final
        except AttributeError:
            raise InvalidAnimeIdError("Invalid animeid or episode_num given")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Unable to connect to the Server, Check your connection")
        except TypeError:
            raise InvalidTokenError("Invalid tokens passed, Check your tokens")

    def get_by_genres(self, genre_name, page) -> list:
        """Get anime by genres, The genre object has the following genres working,

        action, adventure, cars, comedy, dementia, demons, drama, dub, ecchi, fantasy,
        game, harem, hentai - Temporarily Unavailable, historical, horror, josei, kids,
        magic, martial-arts, mecha, military, music, mystery, parody, police, psychological,
        romance, samurai, school, sci-fi, seinen, shoujo, shoujo-ai, shounen-ai, shounen,
        slice-of-life, space, sports, super-power, supernatural, thriller, vampire,
        yaoi, yuri.

        Parameters:
            genre_name(``str``):
                The name of the genre. You should use any from the above mentioned genres.
            page(``int``):
                The page number of the genre results.

        Returns:
            List of :obj:`-anikimiapi.data_classes.ResultObject`: On Success, the list of genre results is returned.

        Example:
        .. code-block:: python
            :emphasize-lines: 1,4-7,10-13

            from anikimiapi import AniKimi

            # Authorize the api to GogoAnime
            anime = AniKimi(
                gogoanime_token="baikdk32hk1nrek3hw9",
                auth_token="NCONW9H48HNFONW9Y94NJT49YTHO45TU4Y8YT93HOGFNRKBI"
            )

            # Get anime by genre
            get_genre = anime.get_by_genres(genre_name="romance", page=1)
            for result in get_genre:
                print(result.title)
                print(result.animeid)
        """
        try:
            url = f"{self.host}genre/{genre_name}?page={page}"
            response = requests.get(url)
            plainText = response.text
            soup = BeautifulSoup(plainText, "lxml")
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            gen_ani = []
            for anime in animes:  # For every anime found
                tits = anime.a["title"]
                urll = anime.a["href"]
                r = urll.split('/')
                gen_ani.append(ResultObject(title=f"{tits}", animeid=f"{r[2]}"))
            return gen_ani
        except AttributeError or KeyError:
            raise InvalidGenreNameError("Invalid genre_name or page_num")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Unable to connect to server")

    def get_airing_anime(self, count=10) -> list:
        """Get the currently airing anime and their animeid.

        Parameters:
            count(``int`` | ``str``, *optional*):
                The number of search results to be returned, Defaults to 10.

        Returns:
            List of :obj:`-anikimiapi.data_classes.ResultObject`: On Success, the list of currently airing anime results is returned.

        Example:
        .. code-block:: python
            :emphasize-lines: 1,4-7,10-13

            from anikimiapi import AniKimi

            # Authorize the api to GogoAnime
            anime = AniKimi(
                gogoanime_token="baikdk32hk1nrek3hw9",
                auth_token="NCONW9H48HNFONW9Y94NJT49YTHO45TU4Y8YT93HOGFNRKBI"
            )

            airing = anime.get_airing_anime()
            for result in airing:
                print(result.title)
                print(result.animeid)
        """
        try:
            if int(count) >= 20:
                raise CountError("count parameter cannot exceed 20")
            else:
                url = f"{self.host}"
                session = HTMLSession()
                response = session.get(url)
                response_html = response.text
                soup = BeautifulSoup(response_html, 'html.parser')
                anime = soup.find("nav", {"class": "menu_series cron"}).find("ul")
                air = []
                for link in anime.find_all('a'):
                    airing_link = link.get('href')
                    name = link.get('title')  # name of the anime
                    link = airing_link.split('/')
                    lnk_final = link[2]  # animeid of anime
                    air.append(ResultObject(title=f"{name}", animeid=f"{lnk_final}"))
                return air[0:int(count)]
        except IndexError or AttributeError or TypeError:
            raise AiringIndexError("No content found on the given page number")
        except requests.exceptions.ConnectionError:
            raise NetworkError("Unable to connect to server")
