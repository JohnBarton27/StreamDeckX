# Stream Deck X
**Stream Deck X** is a cross-platform application for using an Elgato Stream Deck.

## Setup
### Requirements
* Python 3.8+
* A LibUSB HIDAPI Backend (required from Python StreamDeck library)
    * See [this page](https://python-elgato-streamdeck.readthedocs.io/en/stable/pages/backend_libusb_hidapi.html) for download/install instructions for your platform
  
### Running
1. Clone this repository.
1. Run `pip install -r requirements.txt` from the root directory of the repository.
   1. This only needs to be run the first time you are starting the application.
1. Run `python streamdeckx/streamdeckx.py` from the root directory of the repository.
    1. Stream Deck X will now be accessible in your browser of choice at `localhost:5050`

## Development
This section of the README defines the development guidelines.

### Color Scheme
See this [Coolors palette](https://coolors.co/2b2d42-8d99ae-fafded-152815-f18f01) for the standard colors used in Stream Deck X.

### Database Schema
StreamDeckX uses a local SQLite database for storing & saving configurations. The schema for each table is listed here.

#### deck 
Column | Type | Notes/Constraints
--- | --- | ---
id | text | Primary Key
name | text | 
type | text |

#### button

Column | Type | Notes/Constraints
--- | --- | ---
id | int | Primary Key, autoincrement
deck_id | text | Foreign Key (deck.id)
position | int |
icon | text |
font | text |
label | text |

#### action

Column | Type | Notes/Constraints
--- | --- | ---
id | int | Primary Key, autoincrement
type | text |
button_id | int | Foreign Key (button.id)
action_order | int |
parameter | text |