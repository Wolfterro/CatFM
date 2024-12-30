# Models

This document describes the models used in a Django project related to audio streaming. Each model is detailed with its respective properties and functionalities.

## **Models**

### **Genre**

Stores music genres.

- **Fields**:
  - `name`: Name of the genre (unique).

- **Methods**:
  - `__str__`: Returns the genre name.
  - `populate`: Static method to populate the table with predefined music genres.

---

### **Audio**

Stores information about audio files.

- **Fields**:
  - `identifier`: Unique identifier (UUID).
  - `name`: Name of the audio.
  - `album`: Album name (optional).
  - `artist`: Artist name (optional).
  - `year`: Release year.
  - `duration_in_seconds`: Duration in seconds.
  - `cover`: Cover file (optional).
  - `cover_url`: Cover URL (optional).
  - `genres`: *ManyToMany* relationship with the `Genre` model.
  - `file`: Audio file.
  - `format`: File format (e.g., mp3).
  - `md5`: MD5 hash of the file for integrity verification.
  - `is_active`: Indicates if the audio is active.
  - `created_at`: Creation date.
  - `updated_at`: Last update date.

- **Methods**:
  - `__str__`: Returns a string in the format "Artist - Name (Year)".
  - `save`: Overridden to calculate the duration and generate the MD5 hash of the file, as well as convert it to HLS format.
  - **Properties**:
    - `folder`: Full path of the folder where the audio is stored.
    - `cover_full_url`: Full URL of the audio cover.
    - `file_stream_m3u8_url`: URL for HLS streaming of the audio.
    - `genres_list`: List of associated genres.

---

### **DownloadRequest**

Manages download requests for audio files.

- **Fields**:
  - `audio`: Relationship with the `Audio` model (optional).
  - `url`: URL of the file to be downloaded.
  - `title`: Title of the audio (optional).
  - `requested_by`: User who requested the download.
  - `status`: Request status (pending, approved, or rejected).
  - `created_at`: Creation date.
  - `updated_at`: Last update date.
  - `approved_at`: Approval date (optional).

- **Methods**:
  - `__str__`: Returns a string with the status and the request URL.
  - `register`: Registers the downloaded audio and associates it with the request.
  - `set_info`: Retrieves additional information about the request using the download service.
  - **Properties**:
    - `url_id`: Extracts the video ID from the URL (if applicable).

---

### **AdminRequest**

Manages administrative requests for bulk downloads.

- **Fields**:
  - `link_list`: List of download links (as text).
  - `link_list_file`: File containing the list of links (optional).
  - `status`: Request status (pending, completed, error, or in process).
  - `link_status_description`: Detailed description of the status of each link (optional).
  - `created_at`: Creation date.
  - `updated_at`: Last update date.

- **Methods**:
  - `__str__`: Returns a string with the status and the creation date.
  - `save`: Overridden to start the download service in a background thread.
  - **Properties**:
    - `link_list_array`: Converts the list of links into an array.

---

### **Playlist**

Stores audio playlists.

- **Fields**:
  - `name`: Name of the playlist.
  - `identifier`: Unique identifier (UUID).
  - `can_be_shared`: Indicates whether the playlist can be shared.
  - `audios`: *ManyToMany* relationship with the `Audio` model.
  - `owner`: User who owns the playlist (optional).
  - `is_system_playlist`: Indicates whether the playlist is a system playlist.
  - `created_at`: Creation date.
  - `updated_at`: Last update date.

- **Methods**:
  - `__str__`: Returns a string with the sharing status and the playlist name.
  - `save`: Overridden to configure default properties for system playlists.
  - **Properties**:
    - `cover`: Gets the cover of the first audio in the playlist (if available).

---

## **Considerations**

The models provide a robust foundation for managing audios, genres, download requests, playlists, and administrative tasks. They include logic to automate tasks, such as file processing and data association, ensuring an efficient workflow.
