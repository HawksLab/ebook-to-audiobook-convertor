# 🎧 Narratify 📚

[![GitHub stars](https://img.shields.io/github/stars/HawksLab/narratify.svg?style=social&label=Star)](https://github.com/HawksLab/narratify)
[![GitHub downloads](https://img.shields.io/github/downloads/HawksLab/narratify/total.svg)](https://github.com/HawksLab/narratify/releases)
[![License](https://img.shields.io/badge/License-GPL3-blue.svg)](LICENSE) <!-- Replace MIT with your actual license if different -->

Narratify is a desktop application that transforms your e-books (PDF and EPUB) into engaging audiobooks using Text-to-Speech (TTS) technology. It features a simple, retro-themed graphical interface built with PyQt6, allowing users to easily load documents, choose voices, adjust speed, and listen to or save the generated audio.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=hawks-lab/hawkslab-narratify&type=Date)](https://star-history.com/#hawks-lab/hawkslab-narratify)

## ✨ Features

*   **E-book to Audiobook Conversion:** Convert PDF and EPUB files into WAV audio format.
*   **High-Quality TTS:** Utilizes the Kokoro TTS engine for natural-sounding speech.
*   **Multiple Voices:** Offers a selection of different voices (powered by Kokoro).
*   **Adjustable Speed:** Control the playback speed of the generated audiobook (0.5x to 2.0x).
*   **Voice Preview:** Test different voices with sample audio before conversion.
*   **Integrated Audio Player:** Play, pause, seek forward/backward, and monitor progress of the generated audio.
*   **Save Audiobook:** Save the final generated audiobook as a WAV file.
*   **Retro GUI:** Minimalist, retro-inspired user interface with dark/light theme toggle.
*   **Cross-Platform (Potential):** Built with Python and PyQt6, potentially runnable on Windows, macOS, and Linux (with dependencies met).
*   **Progress Indication:** Visual feedback during the text parsing and audio conversion processes.

## 📸 Screenshots

<!-- Add your screenshots here! -->
*Main Interface (Dark Theme)*

*Conversion Options*

*Audio Player*

*Progress Screen*



## ⚙️ Installation

1.  **Prerequisites:**
    *   Python 3.x installed.
    *   Java Runtime Environment (JRE) installed and accessible in your system's PATH (required by Apache Tika).

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/hawks-lab/hawkslab-narratify.git
    cd hawkslab-narratify
    ```

3.  **Install Dependencies:**
    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
    Then install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The first time Kokoro TTS runs, it might download necessary models.*

## ▶️ Usage

1.  **Run the Application:**
    ```bash
    python main.py
    ```
    You should see the splash screen while dependencies load, followed by the main application window.

2.  **Load an E-book:**
    *   Click the "LOAD EBOOK" button (either top-right or center).
    *   Alternatively, use the menu: `File` > `Open eBook`.
    *   Select a supported file (`.pdf` or `.epub`).
    *   Wait for the parsing process to complete. The text content will appear in the left panel.

3.  **Configure Conversion:**
    *   In the right panel ("CONFIGURATION"), select your desired voice from the "VOICE SELECT" dropdown.
    *   Click "TEST" to hear a preview of the selected voice.
    *   Adjust the "PLAYBACK SPEED" slider (0.5x to 2.0x).

4.  **Convert to Audio:**
    *   Click the "CONVERT TO AUDIO" button.
    *   A progress window will appear, showing the conversion status. This may take several minutes depending on the length of the text and your system speed.

5.  **Playback and Save:**
    *   Once conversion is complete, the "AUDIO PLAYER" panel will become active.
    *   Use the `▶` (Play/Pause), `◀◀` (Seek Back), and `▶▶` (Seek Forward) buttons.
    *   The slider shows playback progress.
    *   Click "SAVE" to save the generated audiobook as a `.wav` file.
    *   Click "NEW" to return to the configuration screen for a new conversion (keeps the current text loaded).

6.  **Other Features:**
    *   **Theme:** Use `View` > `Toggle Theme` (or `Ctrl+T`) to switch between dark and light modes.
    *   **About:** Find application info under `Help` > `About`.
    *   **Exit:** Close the application via the window controls or `File` > `Exit` (`Ctrl+Q`).

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feat/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please report any bugs or suggest features through the GitHub Issues page.

## 📜 License

This project is licensed under the GPL 3 License - see the [LICENSE](LICENSE) file for details. <!-- Create a LICENSE file with MIT License text -->

## 🙏 Acknowledgements

*   Developed by [Hawks Labs](https://github.com/hawks-lab). <!-- Link to Hawks Labs profile/website if available -->
*   GUI built using the excellent [PyQt6](https://riverbankcomputing.com/software/pyqt/) framework.
*   TTS powered by [Kokoro TTS](https://github.com/ranchu/kokoro-tts). <!-- Verify Kokoro source/link -->
*   Document parsing enabled by [Apache Tika](https://tika.apache.org/).