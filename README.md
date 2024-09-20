# Python Code Projects

This repository contains a collection of Python games and projects, including a **BlackJack** card game, a **Unicorn-Run** game, and an **ASCII-art** project. Each project is independent, with its own functionality and usage instructions.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

### BlackJack
- A command-line based card game following the traditional rules of Blackjack.
- Built using Tkinter for the GUI.

### Unicorn-Run
- A graphical game where a unicorn runs, avoiding obstacles.
- Built using Pygame for interactive gameplay.

### ASCII-art
- ASCII art generator.
- Converts images to ASCII art using the Pillow library.

## Requirements

This is a Python repository, so you need to have Python installed on your system. The projects are built using different libraries, so you need to install the required dependencies for each project.

- Python 3.x

### Installing Python

Just ask Google! or chatgpt

Okay, Here it is:
1. You can download Python from the [official website](https://www.python.org/downloads/)
2. Install any library that you need using pip:
   - **Windows**:
       ```sh
       pip install library-name
       ```
   - **macOS/Linux**:
        ```sh
        pip3 install library-name
        ```

## Usage

### Clone the Repository

#### Using Git

1. Install Git
   - If you don't have Git installed, you can download and install it from the [official Git website](https://git-scm.com/downloads).
2. Clone the repository:
    ```sh
    git clone https://github.com/DanyilT/Python.git
    ```
3. Navigate to the project folder:
    ```sh
   cd <project-folder>
    ```
   
#### Downloading the ZIP File

1. Download the ZIP file from the [GitHub repository](https://github.com/DanyilT/Python.git) and extract it.
2. Navigate to the project folder in the extracted directory.

### Run The Project

Each project has its own instructions on how to run it. Navigate to the project folder and follow the instructions in the `README.md` file.

## File Structure

The repository is structured as follows:

- [`ASCII-art/..`](ASCII-art): ASCII-art project to convert images to ASCII art.
   - [`ascii_art_generator.py`](ASCII-art/ascii_art_generator.py): Main script to run the ASCII art generator.
   - [`README.md`](ASCII-art/README.md): Documentation for the ASCII-art project.

- [`BlackJack/..`](BlackJack): Blackjack card game project.
   - [`game.py`](BlackJack/game.py): Main script to run the game.
   - [`README.md`](BlackJack/README.md): Documentation for the Blackjack game.

- [`Unicorn-Run/..`](Unicorn-Run): Unicorn-Run game project.
   - [`game.py`](Unicorn-Run/game.py): Main script to run the game.
   - [`README.md`](Unicorn-Run/README.md): Documentation for the Unicorn-Run game.

- [`.gitignore`](.gitignore): Git ignore file to exclude certain files and directories from version control.
- [`LICENSE`](LICENSE): License information for the repository.
- [`README.md`](README.md): Main documentation file for the repository.

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m "Add some feature"
    ```
4. Push to the branch:
    ```sh
    git push origin feature-branch
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for details.
