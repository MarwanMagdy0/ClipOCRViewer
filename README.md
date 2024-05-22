# ClipOCRViewer

ClipOCRViewer is a Python application that allows users to capture images from the clipboard, preprocess them for optimal text recognition, and extract text using Tesseract OCR. This tool is particularly useful for quickly converting text from screenshots or other images copied to the clipboard into editable text.

## Features

- **Clipboard Image Capture**: Automatically captures images from the clipboard.
- **Change window opacity**: you can change window opacity using `CTRL + Plus` and `CTRL + minus`.
- **Change window size**: Using `CTRL + ArrowUp` and `CTRL + ArrowDown`.
- **Image Preprocessing**: Enhances image quality to improve OCR accuracy (grayscale conversion, resizing).
- **Tesseract OCR Integration**: Utilizes Tesseract OCR to extract text from preprocessed images.
- **GUI Interface**: Simple and intuitive interface built with PyQt5.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6+
- Tesseract OCR installed and configured
- The following Python packages:
  - `pytesseract`
  - `Pillow`
  - `numpy`
  - `pyqt5`

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/MarwanMagdy0/ClipOCRViewer.git
    ```
2. **Install the required Python packages:**
    ```bash
    pip install pytesseract pillow numpy pyqt5
    ```
3. **Install Tesseract OCR:**
    ```bash
    sudo apt-get install tesseract-ocr
    ```

## Configuration

Make sure Tesseract is added to your system's PATH. You can test this by running `tesseract --version` in your command line.

1. **Set the TESSDATA_PREFIX environment variable:**

   This environment variable should point to the directory containing your Tesseract data files (`.traineddata`). Typically, this is set automatically, but if you're encountering issues, you can set it manually:

   - **Windows:**
     ```cmd
     setx TESSDATA_PREFIX "C:\Program Files\Tesseract-OCR\tessdata"
     ```

   - **macOS/Linux:**
     ```bash
     export TESSDATA_PREFIX="/usr/local/share/tessdata/"
     ```

2. **Ensure the language data files are present:**

   Verify that the appropriate language files (e.g., `eng.traineddata` for English) are present in the `tessdata` directory specified by `TESSDATA_PREFIX`. If not, download them from the [Tesseract GitHub repository](https://github.com/tesseract-ocr/tessdata) and place them in the directory.

## Usage

1. **Run the application:**

    ```bash
    python main.py
    ```

2. **Using the GUI:**
   - Copy an image to your clipboard.
   - The application will automatically capture and preprocess the image.
   - To apply OCR, press `CTRL+E` for English or `CTRL+A` for Arabic.
   - A textbox will appear, allowing you to copy the extracted text.

3. **Opacity**
   - To increase the window opacity, press `CTRL +`.
   - To decrease the window opacity, press `CTRL -`.
## Project Structure

- `main.py`: Main application file.
- `utils.py`: Utility functions used in the application.
- `README.md`: Project documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
