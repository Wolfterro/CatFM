# CatFM - A Simple Python Project for Creating a Music Streaming Service

![Static Badge](https://img.shields.io/badge/Python-3.9_%7C_3.10_%7C_3.11_%7C_3.12-blue)
![Static Badge](https://img.shields.io/badge/License-MIT_License-green)
![Static Badge](https://img.shields.io/badge/Coverage-0_%25-red)

# CatFM

CatFM is a simple Python project that creates a music streaming service using Django and Django Channels. It is a Django project that uses the Django REST framework for creating a REST API, and Django Channels for handling WebSocket connections.

The project is divided into three main apps: `catuser`, `radio`, and `streaming`. The `catuser` app is used for user authentication, the `radio` app is used for creating radio streams, and the `streaming` app is used for creating playlists and handling music streaming.

The project is still under development and should not be used in production yet.

## Apps Overview

### catuser

The `catuser` app is responsible for managing user authentication and account management. It provides the necessary infrastructure for user registration, login, and management of user credentials. The app integrates with Django's authentication system and extends it as necessary to meet the specific requirements of the CatFM project. It includes models for storing user data and APIs for handling user-related operations, ensuring secure access to the streaming services.

### radio

The `radio` app facilitates the creation and management of live radio streams. It leverages WebSocket technology to stream audio files continuously over selected channels. The app allows administrators to manage audio files, add or remove them using Django's admin interface, and create multiple broadcast channels. These channels can stream various genres or types of music. The app includes models to represent radio streams and their attributes, as well as services to handle broadcasting logic and WebSocket connections.

### streaming

The `streaming` app is designed for on-demand music streaming. It provides users with the capability to request and play different audio files as needed. The app includes functionality for managing audio content, downloading new tracks, and handling requests for new music. Administrators can approve or reject these requests through an API and manage content visibility. The app also supports playlist creation, allowing users to curate playlists based on their preferences. Models within the app store metadata about the audio files and playlists, and APIs enable interaction with the streaming service.

For more information about the project, please visit the GitHub repository: https://github.com/Wolfterro/CatFM