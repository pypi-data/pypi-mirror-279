"""
Search api used for searching movies and tv series.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Any, Generator, Dict, Literal, Optional
    from ...http_client import HTTPClient

from ...media import Metadata, MetadataType, ExtraMetadata, AiringType
from base64 import b64decode

__all__ = ("TheMovieDB",)

class TMDbSerial:
    def __init__(self, data, type: MetadataType):
        self.id: int = data.get("id")
        self.title: str = self.__extract_title(data)
        self.release_date: Optional[str] = data.get("release_date") or data.get("first_air_date")
        self.year: Optional[str] = self.release_date[:4] if self.release_date else None
        self.type: MetadataType = type
        self.image_url: Optional[str] = "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + data.get("poster_path") if data.get("poster_path") else None
    
    def __extract_title(self, data):
        title_fields = ["title", "name", "original_title", "original_name"]
        for field in title_fields:
            if field in data:
                return data[field]
        return ""

class TheMovieDB:
    """API-Wrapper for themoviedb.org"""
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.api_key = str(b64decode("ZDM5MjQ1ZTExMTk0N2ViOTJiOTQ3ZTNhOGFhY2M4OWY="), "utf-8")

        self.metadata = "https://api.themoviedb.org/3/{}/{}?language=en-US&append_to_response=episode_groups,alternative_titles,credits&api_key={}"

        self.search_url = "https://api.themoviedb.org/3/search/{}?query={}&include_adult=false&language=en-US&page=1&api_key={}"


    def search(self, query: str, limit: Optional[int]) -> Generator[Metadata, Any, None]:
        max_metadata = 20 if limit is None else limit

        serial_list: List[TMDbSerial] = []

        movie = self.http_client.get(self.search_url.format("movie", query, self.api_key)).json()["results"]
        tv = self.http_client.get(self.search_url.format("tv", query, self.api_key)).json()["results"]

        for item in movie:
            item = TMDbSerial(item, MetadataType.SINGLE)

            if not item.release_date:
                continue

            serial_list.append(item)

        for item in tv:
            item = TMDbSerial(item, MetadataType.MULTI)

            if not item.release_date:
                continue

            serial_list.append(item)
        
        serial_list = serial_list[:max_metadata]

        for item in serial_list:
            yield Metadata(
                id = item.id,
                title = item.title,
                type = item.type,
                image_url = item.image_url,
                year = item.year,
                extra_func = lambda: self.__extra_metadata(item)
            )

    def scrape_episodes(self, metadata: Metadata, **kwargs) -> Dict[int, int] | Dict[None, Literal[1]]:
        scraped_seasons = {}

        seasons = self.http_client.get(self.metadata.format("tv", metadata.id, self.api_key)).json()["seasons"]

        for season in seasons:
            if season["season_number"] == 0:
                continue

            scraped_seasons[season["season_number"]] = season["episode_count"]

        return scraped_seasons

    def __extra_metadata(self, serial: TMDbSerial) -> ExtraMetadata: # This API is dawgshit
        type = "movie" if serial.type == MetadataType.SINGLE else "tv"
        metadata = self.http_client.get(self.metadata.format(type, serial.id, self.api_key)).json()

        description = None
        cast = None
        alternate_titles = None
        genres = None
        airing = None

        if metadata.get("overview"):
            description = metadata.get("overview")

        if metadata["credits"]["cast"]:
            cast = [i.get("name") or i.get("original_name") for i in metadata["credits"]["cast"]]
        
        alternative = metadata["alternative_titles"]

        titles = alternative.get("results") or alternative.get("titles")

        if titles:
            alternate_titles = [(i.get("iso_3166_1"), i.get("title")) for i in titles]

        if metadata["genres"]:
            genres = [i["name"] for i in metadata["genres"]]

        airing_status = metadata["status"]

        if "Released" in airing_status:
            airing = AiringType.RELEASED
        elif "Production" in airing_status:
            airing = AiringType.PRODUCTION
        elif "Returning" in airing_status:
            airing = AiringType.ONGOING
        elif "Canceled" in airing_status:
            airing = AiringType.CANCELED
        else:
            airing = AiringType.DONE

        return ExtraMetadata(
            description = description,
            cast = cast,
            alternate_titles = alternate_titles,
            genres = genres,
            airing = airing
        )