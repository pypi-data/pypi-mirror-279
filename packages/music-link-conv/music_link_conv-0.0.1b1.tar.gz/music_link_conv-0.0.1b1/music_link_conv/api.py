from api_deezer import API as API_Deezer
from api_deezer.exceptions.data import Error_Data_404 as Deezer_Error_Data_404

from api_spotify import API as API_Spotify


class Music_Link_Conv:
	def __init__(
		self,
		spotify_client_id: str,
		spotify_client_secret: str
	) -> None:

		self.__spotify_client_id = spotify_client_id
		self.__spotify_client_secret = spotify_client_secret
		self.__api_deezer = API_Deezer()
		self.__api_spotify = API_Spotify(self.__spotify_client_id, self.__spotify_client_secret)


	def conv_spo_track_2_deezer_track(self, id_track: str):
		spotify_data = self.__api_spotify.get_track(id_track)
		isrc = spotify_data.external_ids.isrc

		if not isrc:
			return

		try:
			deezer_data = self.__api_deezer.get_track_by_isrc(isrc)
		except Deezer_Error_Data_404:
			return

		return deezer_data.link

	def conv_spo_album_2_deezer_album(self, id_album: str):
		spotify_data = self.__api_spotify.get_album(id_album)
		upc = spotify_data.external_ids.upc

		if not upc:
			return

		try:
			deezer_data = self.__api_deezer.get_album_by_upc(upc)
		except Deezer_Error_Data_404:
			return

		return deezer_data.link
