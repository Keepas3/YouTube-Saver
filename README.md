# Youtube Saver

## Overview
Youtube Saver is a locally hosted web application powered by a Python backend. It enables users to download YouTube videos via a URL to a MP4 file with the option to also convert them to high-quality FLAC audio files. Offering a seamless and efficient solution, Youtube Saver combines video downloading and audio conversion in one platform.

## Key Components

### Website (index.html & result.html)
* Interface for file/URL submission
* Saves files to a folder named "Converted Flac Files" and "Downloaded Youtube Videos" respectively

### Backend Side (Server.py)
* Creates output folders on user's desktop
* Downloads YT Videos and converts files
* Handles routing through the html pages


## Technical Stack
* Backend: Python
* Frontend: HTML/CSS
* Imports: flask, moviepy, pytubefix, os


## Getting Started

### Prerequisites
* Python JDK 11+

### Installation
1. Clone the repository
   ```bash
   git clone https://github.com/Keepas3/FLAC-Converter-YT-Downloader.git
   ```
2. Create virtual environment to isolate dependencies (Optional)
   ```bash
   python -m venv myproject_env
   ```
3. Download all dependencies
   ```bash
   pip -r requirements.txt
   ```
4. Compile Python file
   ```bash
   python Server.py
   ```


## Project Structure
Flac Converter YT Downloader/
├── images/              # Images used on website
├── templates/           # Contains the html files


## Classes Overview
* `Server.py`: Handles all the downloading/converting and routing
* `index.html`: Home page of the site 
* `result.html`: Resulting page after clicking on submit
* `requirements.txt`: All the dependencies needed for the project


## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Submit Pull Request

## Authors
* Keepas3

