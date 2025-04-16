# HandPilot – Slide & Scroll Control with Hand Gestures

HandPilot is a Python-based tool that uses your webcam and hand gestures to control slideshows, scroll pages, and detect common hand signs such as Like, Dislike, Victory, Devil Horns, OK, and more.

## Features

- Real-time hand gesture recognition using your webcam
- Slide control via left/right hand swipes
- Start slideshow using Like gesture with a fist
- Scroll up/down using index finger movement
- Voice feedback for recognized gestures
- Supported gestures include:
  - Numbers 1 to 5 (by finger count)
  - Victory sign
  - Devil Horns
  - Like / Dislike
  - OK
  - Call Me
  - Stop

## Requirements

- Python 3.7 or higher
- A working webcam
- A relatively good lighting condition for accurate recognition

  
## Getting Started

To clone this repository to your local machine, use the following command:

```bash
git clone https://github.com/Agz4roth/Hand-Pilot.git
```

Then navigate into the project folder:

```bash
cd Hand-Pilot
```

## Installation

To install the required packages, run:

```bash
pip install -r requirements.txt
```
How to Run

```bash
python Hand-Pilot.py
```
Usage Notes

To control slides or scroll, make sure the active window (e.g. PowerPoint or a browser) is in focus.

For best performance, use a clean background and ensure your hand is clearly visible.

If the system lags or has delay issues, try reducing camera resolution or limiting frame rate.


Possible Future Enhancements

Add a user-friendly GUI

Train custom gestures using machine learning

Export gesture logs or analytics

---
Author: Farzin Paydar  
License: [MIT License](./[License])
