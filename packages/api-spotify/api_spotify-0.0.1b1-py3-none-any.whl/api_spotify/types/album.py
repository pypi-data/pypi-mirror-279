from __future__ import annotations


from typing import (
	TYPE_CHECKING, Any
)

from pydantic import (
	BaseModel, model_validator
)

from .copyright import Copyright
from .external_ids import External_Ids

from .shorts import (
	Short_Track, Short_Album
)


if TYPE_CHECKING:
	from ..api import API


class Album_Tracks(BaseModel):
	href: str
	limit: int
	offset: int
	next: str | None
	previous: str | None
	total: int
	items: list[Short_Track]


	@model_validator(mode = 'before')
	@classmethod
	def check(cls, data: dict[str, Any]) -> dict[str, Any]:
		cls.__api: API = data['_api']

		return data


	def get_next(self) -> Album_Tracks | None:
		if not self.next:
			return

		method = self.next.removeprefix(self.__api.API_URL)
		res = self.__api.make_req(method)
		res['_api'] = self.__api

		return Album_Tracks.model_validate(res)


class Album(Short_Album):
	tracks: Album_Tracks
	copyrights: list[Copyright]
	external_ids: External_Ids
	genres: list[str]
	label: str
	popularity: int


	@model_validator(mode = 'before')
	@classmethod
	def check(cls, data: dict[str, Any]) -> dict[str, Any]:
		data['tracks']['_api'] = data['_api']

		return data
