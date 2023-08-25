# PowerMet Generators Bot

🔌 Welcome to PowerMet Generators Bot! ⛽️

PowerMet Generators Bot is your ultimate assistant for selecting the perfect generator to meet your power needs. Whether you're looking for gasoline ⛽️ or diesel ⛽️ generators, we've got you covered. 💡😊 Get expert consultation and find the generator that suits your requirements with ease. 

Explore our wide range of generators, get personalized recommendations, and make informed decisions. Let us guide you through the world of power solutions. 🌐💪


## Table of Contents

- [Overview](#overview)
- [Linux Installation](#linux-installation)
    - [Autostart on Linux](#autostart-on-linux)
- [Windows Installation](#windows-installation)
    - [Autostart on Windows](#autostart-on-windows)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

Brief overview of your project.

## Linux Installation

For deployment on Linux operating systems:

1. Install Python 3.x: [Python Official Website](https://www.python.org/downloads/)
2. Clone the repository: `git clone github.com/Saidalo1/power_met_bot`
3. Navigate to the project folder: `cd [folder name]`
4. Install dependencies: `pip install -r requirements.txt`
5. **Create a virtual environment** (venv): `python -m venv venv`
6. **Activate the virtual environment:**

   - On Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`

7. Configure the `.env` file:

   Create a `.env` file in the project root and add the following:

   ```dotenv
   # Telegram Bot Token
    TOKEN="Your_Telegram_Bot_Token_Here"

   # Database settings
    DATABASE_FOLDER='database'
    DATABASE_NAME='power_met_bot'

    # Greeting Text
    GREETING_TEXT="Explanation of the greeting text."

    # Start Message
    START_MESSAGE="Explanation of the start message."

    # Incorrect Selected Language
    ERROR_LANGUAGE="Explanation of the error message for incorrect language selection."

    # Locale Directory
    LOCALE_DIRECTORY="locales"

    # Group Chat ID
    GROUP_CHAT_ID=Your_Group_Chat_ID_Here

    # Generators Per Page
    GENERATORS_PER_PAGE=20

    # Phone Number for order
    SALES_DP_NUM='Phone Number of manager'

    # Media Folder Name
    MEDIA_FOLDER_NAME=\media\

    # Generator Photo Name
    GENERATOR_PHOTO_NAME='generator.png'

   ```

8. Run the bot: `python bot.py`

### Autostart on Linux

To automatically start the bot when your system boots, you can create a systemd service. Here's how:

1. Create a new service file: `sudo nano /etc/systemd/system/your_bot.service`
2. Add the following to the file:

    ```
    [Unit]
    Description=Your Bot Service
    After=network.target

    [Service]
    User=username
    WorkingDirectory=/path/to/your/project
    ExecStart=/usr/bin/python /path/to/your/project/bot.py

    [Install]
    WantedBy=multi-user.target
    ```

   Replace `username` with your username and `/path/to/your/project` with the actual path to your project folder.

3. Save the file and close the editor.
4. Start the service: `sudo systemctl start your_bot.service`
5. Enable the service to start on boot: `sudo systemctl enable your_bot.service`

## Windows Installation

To install and run the bot on a Windows operating system, follow these steps:

1. Install Python 3.x: [Python Official Website](https://www.python.org/downloads/)
2. Clone the repository: `git clone github.com/Saidalo1/power_met_bot`
3. Open a command prompt and navigate to the project folder: `cd [folder name]`
4. Install dependencies: `pip install -r requirements.txt`
5. **Create a virtual environment** (venv): `python -m venv venv`
6. **Activate the virtual environment:** `venv\Scripts\activate`
7. Configure the `.env` file: [Instructions below](#configuration)
8. Run the bot: `python bot.py`

### Autostart on Windows

To automatically start the bot when your system boots, you can create a batch script to activate the virtual environment
and then launch the bot:

1. Create a new text file named `start_bot.bat` in the project folder.
2. Open the file with a text editor and add the following lines:

    ```batch
    @echo off
    cd /d [path to your project folder]
    call venv\Scripts\activate
    python bot.py
    ```

3. Save the file.

4. Press `Win + R`, type `shell:startup`, and press Enter. This will open the Startup folder.

5. Create a shortcut to the `start_bot.bat` script in the Startup folder.

## Configuration

Instructions on how to configure your bot using the `.env` file.

## Usage

Instructions on how to use your bot.

## Contributing

Information for contributors.

## License

Your project's license information.
