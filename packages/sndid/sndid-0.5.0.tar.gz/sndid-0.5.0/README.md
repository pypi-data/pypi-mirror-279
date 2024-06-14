# sndid
`sndid` identifies sounds.

* https://sndid.ai

At present only birds are identified.


# Install
Install thine dependencies:

```
sudo apt update
sudo apt install git ffmpeg python3-pip python3-venv python-is-python3 \
  netcat-traditional sox alsa-utils portaudio19-dev
```

Install `sndid` from PyPI:

```
pip install sndid
```

Get the non-commercial use BirdNet model:

```
git clone https://spacecruft.org/deepcrayon/sndid-models models
```

Get the CC by SA 4.0 samples:

```
git clone https://spacecruft.org/deepcrayon/sndid-samples samples
```


# Usage
Note, BirdNet tensorflow works fine with just the CPU, no GPU required to use the model.

## Command line
As such:


Help:
```
$ sndid-file --help
usage: sndid-file [-h] [-c CONFIDENCE] [-i INPUT] [-a LATITUDE] [-o LONGITUDE] [-y YEAR] [-m MONTH] [-d DAY] [-f FORMAT]

Process bird sound file.

options:
  -h, --help            show this help message and exit
  -c CONFIDENCE, --confidence CONFIDENCE
                        Minimum Confidence (default: 0.3)
  -i INPUT, --input INPUT
                        Input filename to process (default: samples/sample.wav)
  -a LATITUDE, --latitude LATITUDE
                        Latitude (default: 40.57)
  -o LONGITUDE, --longitude LONGITUDE
                        Longitude (default: -105.23)
  -y YEAR, --year YEAR  Year (default: today's year)
  -m MONTH, --month MONTH
                        Month (default: today's month)
  -d DAY, --day DAY     Day (default: today's day)
  -f FORMAT, --format FORMAT
                        Print output in CSV or JSON (default CSV)
```

Sample output:

```
$ sndid-file --confidence 0.8 --latitude 40 --longitude -105 --year 2024 --month 6 --day 12
Hairy Woodpecker, Dryobates villosus, 15.0, 18.0, 0.8371532559394836
Hairy Woodpecker, Dryobates villosus, 18.0, 21.0, 0.8111727833747864
Hairy Woodpecker, Dryobates villosus, 48.0, 51.0, 0.8048807382583618
Hairy Woodpecker, Dryobates villosus, 51.0, 54.0, 0.9604988694190979
Hairy Woodpecker, Dryobates villosus, 54.0, 57.0, 0.8156633973121643
Hairy Woodpecker, Dryobates villosus, 57.0, 60.0, 0.8230040073394775
```


## JACK
`sndid-jack` reads audio from JACK ports, Ardour Master Out 1/2 by default,
and identifies birds in the stream.

It logs the identification in a text file.

It saves the identification to an audio file.

```
$ sndid-jack --help
usage: sndid-jack [-h] [--config_file CONFIG_FILE] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--n-inputs N_INPUTS] [--segment-length SEGMENT_LENGTH]
                  [--min-confidence MIN_CONFIDENCE] [--lat LAT] [--lon LON] [--output-dir OUTPUT_DIR] [--version]

sndid-jack - AI processing JACK Audio Connection Kit.

options:
  -h, --help            show this help message and exit
  --config_file CONFIG_FILE, -c CONFIG_FILE
                        Configuration File name
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}, -L {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level.
  --n-inputs N_INPUTS, -n N_INPUTS
                        Number of inputs
  --segment-length SEGMENT_LENGTH, -l SEGMENT_LENGTH
                        Segment length
  --min-confidence MIN_CONFIDENCE, -m MIN_CONFIDENCE
                        Minimum confidence
  --lat LAT, -y LAT     Latitude
  --lon LON, -x LON     Longitude
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory for detections
  --version, -v         show program's version number and exit
```


## Server
The sndid-server waits for connections to feed it wav file segments,
then processes the sound.

It prints to the terminal and also logs to `sndid.log`.

Run thusly:

```
sndid-server
```

Help:
```
$ sndid-server -h
usage: sndid-server.py [-h] [-i IP] [-p PORT] [-t LATITUDE] [-n LONGITUDE] [-y YEAR] [-m MONTH] [-d DAY] [-c CONFIDENCE]

Run sndid-server

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Server IP address (default 127.0.0.1)
  -p PORT, --port PORT  Server network port (default 9988)
  -t LATITUDE, --latitude LATITUDE
                        Latitude (default 40.57)
  -n LONGITUDE, --longitude LONGITUDE
                        Longitude (default -105.23)
  -y YEAR, --year YEAR  Year (default 2023)
  -m MONTH, --month MONTH
                        Month (default 9)
  -d DAY, --day DAY     Day (default 19)
  -c CONFIDENCE, --confidence CONFIDENCE
                        Minimum Confidence (default 0.25)
```

Sample output on startup:

```
$ sndid-server
2023-10-03 10:45:47.343270-06:00 sndid-server started 127.0.0.1:9988
```

After client connects and sends mono wav:

```
$ sndid-server 
2023-10-03 10:45:47.343270-06:00 sndid-server started 127.0.0.1:9988
2023-10-03 10:46:34.060983-06:00 Hairy Woodpecker, Dryobates villosus, 0.3896884322166443
2023-10-03 10:46:34.061248-06:00 Hairy Woodpecker, Dryobates villosus, 0.47060683369636536
2023-10-03 10:46:34.061312-06:00 Hairy Woodpecker, Dryobates villosus, 0.5013241171836853
2023-10-03 10:46:34.061377-06:00 Hairy Woodpecker, Dryobates villosus, 0.6557420492172241
2023-10-03 10:46:34.061429-06:00 Hairy Woodpecker, Dryobates villosus, 0.7146830558776855
2023-10-03 10:46:34.061498-06:00 Hairy Woodpecker, Dryobates villosus, 0.806126594543457
2023-10-03 10:46:34.061553-06:00 Hairy Woodpecker, Dryobates villosus, 0.8105885982513428
2023-10-03 10:46:34.061628-06:00 Hairy Woodpecker, Dryobates villosus, 0.8147749900817871
2023-10-03 10:46:34.061678-06:00 Hairy Woodpecker, Dryobates villosus, 0.8241879343986511
2023-10-03 10:46:34.061725-06:00 Hairy Woodpecker, Dryobates villosus, 0.837184488773346
2023-10-03 10:46:34.061771-06:00 Hairy Woodpecker, Dryobates villosus, 0.9604253768920898
```

Sample server output from a realtime stream:

```
$ sndid-server
2023-10-03 10:38:52.975515-06:00 sndid-server started 127.0.0.1:9988
2023-10-03 10:41:27.162509-06:00 Northern Flicker, Colaptes auratus, 0.2552548944950104
2023-10-03 10:41:27.162775-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.3168713450431824
2023-10-03 10:41:27.172693-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.3708573877811432
2023-10-03 10:41:27.172858-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.4243549406528473
2023-10-03 10:41:38.446815-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.2577541172504425
2023-10-03 10:41:49.688914-06:00 White-crowned Sparrow, Zonotrichia leucophrys, 0.3252100646495819
2023-10-03 10:42:45.590852-06:00 Rock Wren, Salpinctes obsoletus, 0.34000715613365173
2023-10-03 10:43:52.545070-06:00 Spotted Towhee, Pipilo maculatus, 0.31051698327064514
2023-10-03 10:44:15.007297-06:00 Clark's Nutcracker, Nucifraga columbiana, 0.6180582642555237
2023-10-03 10:44:15.007515-06:00 Northern Flicker, Colaptes auratus, 0.35758695006370544
2023-10-03 10:44:26.109497-06:00 Clark's Nutcracker, Nucifraga columbiana, 0.27328306436538696
2023-10-03 10:44:26.109734-06:00 Clark's Nutcracker, Nucifraga columbiana, 0.32902488112449646
2023-10-03 10:44:26.109799-06:00 Clark's Nutcracker, Nucifraga columbiana, 0.6783570647239685
```


## Client
Requires mono wav file.

To convert stereo to mono with sox:

```
sox -c 2 stereo.wav -c 1 mono.wav
```


Run client to submit file to server thusly:

```
sndid-client
```

Help:
```
$ sndid-client -h
usage: sndid-client [-h] [-i IP] [-p PORT] [-f FILE]

Run sndid-client

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Server IP address (default 127.0.0.1)
  -p PORT, --port PORT  Server network port (default 9988)
  -f FILE, --file FILE  Input filename to process (default samples/mono.wav)
```

Sample output:

```
$ sndid-client
Sending samples/mono.wav to 127.0.0.1:9988
```


## ALSA Client
Use this script to stream from the microphone to the server,
using ALSA.

```
sndid-alsa
```


Help:

```
$ sndid-alsa -h
usage: sndid-alsa [-h] [-i IP] [-p PORT] [-r RATE] [-t TIME]

Run sndid-alsa

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Server IP address (default 127.0.0.1)
  -p PORT, --port PORT  Server network port (default 9988)
  -r RATE, --rate RATE  Rate in Hertz (default 48000)
  -t TIME, --time TIME  Length of segments in seconds (default 10)
```

Sample output:

```
$ sndid-alsa 
Streaming ALSA in to 127.0.0.1:9988
Recording WAVE 'stdin' : Float 32 bit Little Endian, Rate 48000 Hz, Mono
```

Exit with `CTRL-C`.


## Stream
`sndid-stream` streams *from* a URL to the `sndid-server`.
Input URL can be anything ffmpeg can read (everything).


Help:
```
$ sndid-stream -h
usage: sndid-stream [-h] [-i IP] [-p PORT] [-t TIME] -u URL

Run sndid-stream

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Server IP address (default 127.0.0.1)
  -p PORT, --port PORT  Server network port (default 9988)
  -t TIME, --time TIME  Length of segments in seconds (default 60)
  -u URL, --url URL     Input url
```

Exit with `CTRL-Z` and `kill %1`  :) por ahora.


## List
`sndid-list` lists sounds available to be identified at a particular
time and location.

Use:

```
sndid-list
```

Help:
```
$ sndid-list --help
usage: sndid-list [-h] [-a LATITUDE] [-o LONGITUDE] [-y YEAR] [-m MONTH] [-d DAY] [-t THRESHOLD]

sndid-list -- List available species. By default return all. Limit list with date and location options.

options:
  -h, --help            show this help message and exit
  -a LATITUDE, --latitude LATITUDE
                        Latitude (default 40.57)
  -o LONGITUDE, --longitude LONGITUDE
                        Longitude (default -105.23)
  -y YEAR, --year YEAR  Year (default today)
  -m MONTH, --month MONTH
                        Month (default today)
  -d DAY, --day DAY     Day (default today)
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold value for species list (default 0.0)
```

Sample output:

```
$ sndid-list --latitude=39.7392 --longitude=104.9849 --year=2024 --month=11 --day=17 --threshold=0.3
Alpine Accentor, Prunella collaris
Amur Falcon, Falco amurensis
Amur Stonechat, Saxicola stejnegeri
Arctic Loon, Gavia arctica
Arctic Warbler, Phylloscopus borealis
...
```

The current count of all species in model:

```
$ sndid-list |& wc -l
6522
```


# Development Install
Using Debian Stable (12/Bookworm).

Install this repo. Adapt to local Python setup, ala:

```
git clone --recursive https://spacecruft.org/deepcrayon/sndid
cd sndid/
pyenv local 3.11 # For example, if pyenv is used
python -m venv venv
source venv/bin/activate
pip install -U pip poetry
poetry install
```

Run black on the Python files for nice formatting:

```
black sndid/*.py
```


# Upstream
## Birds
### BirdNet
BirdNet is the bird model used.
The model is under a non-libre CC NC license.

* https://birdnet.cornell.edu/

The source code is available here:

* https://github.com/kahst/BirdNET-Analyzer


### birdnetlib
birdnetlib is based on BirdNet, but with a different codebase and author.
birdnetlib uses BirdNet's non-libre NC model files.
birdnetlib has a dependency on the non-free BirdNet-Analyzer Python code
just for testing.

The source code to birdnetlib itself is under the Apache 2.0 license.
birdnetlib is Free Software / Open Source Software, with non-libre dependency
for testing.

* https://github.com/joeweiss/birdnetlib

In sum, AFAICT, building upon birdnetlib, then creating a libre model,
would be a fully libre system without any non-libre dependencies.


# Status
Alpha, initial development.

* The system ran from October, 2023 to May, 2024
and generated 671,080 identifications.

* `sndid-jack` works best. Few xruns.

* Analyzing files works.

* Using `sndid-server` then `sndid-stream` works for "realtime",
but is kludgy.


# Disclaimer
I'm not a programmer and I know less about birds.

## AI Code Assistant
Currently using CodeQwen 1.5, Codestral 22B v0.1, Deepseek V2, Eurux 8x22B,
Mixtral 8x7b, Phind CodeLLama 34B, and Qwen2
models with Parrot.

* Parrot IDE with AI Assistant (by me) --- https://parrot.codes

* CodeQwen, Qwen2 --- https://qwenlm.github.io/

* Codestral, Mixtral --- https://mistral.ai/technology/#codestral

* Deepseek --- https://www.deepseek.com/

* Eurux --- https://huggingface.co/openbmb

* Phind --- https://huggingface.co/Phind/Phind-CodeLlama-34B-v2

Many other pseudo-"open source" models were tested.


# Copyright
Unofficial project, not related to upstream projects.

Upstream sources under their respective copyrights.


# License
Apache 2.0.

*Copyright &copy; 2023, 2024 Jeff Moe.*
