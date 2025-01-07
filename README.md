# slabvis

A data visualiser for the upload history of EthosLab (Etho).

## Requirements

* Python >= 3.13

* pdm (you can install it with `pip install pdm`).

* yt-dlp

## Installation and usage

```bash
git clone https://github.com/AcipenserSturio/slabvis
cd slabvis
pdm install
yt-dlp --skip-download --write-info-json --output "./assets/ethoslab/%(id)s.%(ext)s" "https://www.youtube.com/@EthosLab"
pdm run python -m slabvis
```

# License

slabvis is licensed under the GNU General Public License Version 3.
