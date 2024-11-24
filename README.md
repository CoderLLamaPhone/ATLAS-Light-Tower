
# ATLAS Institute Light Tower

A basic python controller for the Light Tower atop the Roser Atlas Institute of CU Boulder. In the spirit of the ATLAS Institute, current implementation is being done to allow more student artistic expression through the tower. Certain steps below have been omitted to protect "hijacking" of the tower.



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`ARTNET_TARGET_IP`

`MUSIC_PATH` (Only required for New_ATLS_LightTower.py)


## Installation

After cloning this repo, you will need to install the following libraries.

numpy,
pyaudio, and
stupidArtnet. These can be installed using the basic pip install commands:

```bash
    pip install stupidArtnet
    pip install pyaudio
    pip install numpy

```
    
## Deployment

To deploy this project run the code in python on the same network as the tower server. You can then run the program using python. The RandomColors.py will give you a light show that mimics a pulsing beat. The New_ATLS_LightTower.py is currently in development and supports conversion of wav files into calls to the light tower.

Using multiple instances of this code will confuse the tower and should be avoided.

