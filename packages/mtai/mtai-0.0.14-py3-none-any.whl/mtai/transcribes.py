import mimetypes
from mtai.base import MTAIBase


class Transcribe(MTAIBase):
    """
    Transcribe Class used for various transcription-related operations.
    """

    @classmethod
    def list(cls):
        """
        List all transcriptions.

        Returns:
            JSON Response: A JSON response containing the list of all transcriptions.
        """
        return cls().requests.get("/transcribes/list")

    @classmethod
    def get_transcribe_by_id(cls, transcribe_id):
        """
        Get a transcription by its ID.

        Args:
            transcribe_id (str): The ID of the transcription to retrieve.

        Returns:
            JSON Response: A JSON response containing the transcription data.
        """
        return cls().requests.get(f"/transcribes/retrieve/{transcribe_id}")

    @classmethod
    def create_transcribe_from_audio_url(cls, audio_url, services):
        """
        Create a transcription from an audio URL.

        Args:
            audio_url (str): The URL of the audio file to transcribe.
            services (list of str): A list of services to use for transcription.

        Returns:
            JSON Response: A JSON response containing the result of the transcription.
        """
        return cls().requests.post(
            "/transcribes/transcribe-audio-url",
            data={"audio_url": audio_url, "services": ",".join(services)},
        )

    @classmethod
    def create_transcribe_from_media_file(cls, media_file, services):
        """
        Create a transcription from a media file.

        Args:
            media_file (str): The path or identifier of the media file to transcribe.
            services (list of str): A list of services to use for transcription.

        Returns:
            JSON Response: A JSON response containing the result of the transcription.
        """
        mime_type, _ = mimetypes.guess_type(media_file)
        if mime_type is None:
            raise ValueError("Could not detect MIME type of the file")
        data = {"services": ",".join(services)}
        with open(media_file, "rb") as file:
            files = {"media": (media_file, file, mime_type)}
            return cls().requests.post(
                "/transcribes/transcribe-media-file", data=data, files=files
            )

    @classmethod
    def create_transcribe_from_youtube_video(cls, youtube_url: str, services):
        """
        Create a transcription from a YouTube video.

        Args:
            youtube_url (str): The URL of the YouTube video to transcribe.
            services (list of str): A list of services to use for transcription.

        Returns:
            JSON Response: A JSON response containing the result of the transcription.
        """
        return cls().requests.post(
            "/transcribes/transcribe-youtube-audio",
            data={"youtube_url": youtube_url, "services": ",".join(services)},
        )

    @classmethod
    def delete_transcribe_by_id(cls, transcribe_id):
        """
        Delete a transcription by its ID.

        Args:
            transcribe_id (str): The ID of the transcription to delete.

        Returns:
            JSON Response: A JSON response indicating the result of the deletion.
        """
        return cls().requests.delete(f"/transcribes/delete/{transcribe_id}")
