import typing

from otf_api.models.responses.studio_detail import Pagination, StudioDetail, StudioDetailList

if typing.TYPE_CHECKING:
    from otf_api import Api


class StudiosApi:
    def __init__(self, api: "Api"):
        self._api = api
        self.logger = api.logger

        # simplify access to member_id and member_uuid
        self._member_id = self._api.user.member_id
        self._member_uuid = self._api.user.member_uuid

    async def get_studio_detail(self, studio_uuid: str | None = None) -> StudioDetail:
        """Get detailed information about a specific studio. If no studio UUID is provided, it will default to the
        user's home studio.

        Args:
            studio_uuid (str): Studio UUID to get details for. Defaults to None, which will default to the user's home\
            studio.

        Returns:
            StudioDetail: Detailed information about the studio.
        """
        studio_uuid = studio_uuid or self._api.home_studio.studio_uuid

        path = f"/mobile/v1/studios/{studio_uuid}"
        params = {"include": "locations"}

        res = await self._api._default_request("GET", path, params=params)
        return StudioDetail(**res["data"])

    async def search_studios_by_geo(
        self,
        latitude: float | None = None,
        longitude: float | None = None,
        distance: float = 50,
        page_index: int = 1,
        page_size: int = 50,
    ) -> StudioDetailList:
        """Search for studios by geographic location.

        Args:
            latitude (float, optional): Latitude of the location to search around, if None uses home studio latitude.
            longitude (float, optional): Longitude of the location to search around, if None uses home studio longitude.
            distance (float, optional): Distance in miles to search around the location. Defaults to 50.
            page_index (int, optional): Page index to start at. Defaults to 1.
            page_size (int, optional): Number of results per page. Defaults to 50.

        Returns:
            StudioDetailList: List of studios that match the search criteria.

        Notes:
            ---
            There does not seem to be a limit to the number of results that can be requested total or per page, the
            library enforces a limit of 50 results per page to avoid potential rate limiting issues.

        """
        path = "/mobile/v1/studios"

        latitude = latitude or self._api.home_studio.studio_location.latitude
        longitude = longitude or self._api.home_studio.studio_location.longitude

        if page_size > 50:
            self.logger.warning("The API does not support more than 50 results per page, limiting to 50.")
            page_size = 50

        if page_index < 1:
            self.logger.warning("Page index must be greater than 0, setting to 1.")
            page_index = 1

        params = {
            "pageIndex": page_index,
            "pageSize": page_size,
            "latitude": latitude,
            "longitude": longitude,
            "distance": distance,
        }

        all_results: list[StudioDetail] = []

        while True:
            res = await self._api._default_request("GET", path, params=params)
            pagination = Pagination(**res["data"].pop("pagination"))
            all_results.extend([StudioDetail(**studio) for studio in res["data"]["studios"]])

            if len(all_results) == pagination.total_count:
                break

            params["pageIndex"] += 1

        return StudioDetailList(studios=all_results)
