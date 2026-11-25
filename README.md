# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/sholaah/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/sholaah/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A program that renders Wednesday 25 November 2026's world news as one Economist-style cover image: a cream page, a red "THE WORLD TODAY" masthead, the date as a huge title, and the Dow crossing 50,000 for the first time as the lead story, with a small drawn chart of the climb. Below it: three boxed second leads (the Houthi strike on Riyadh's tallest tower, mines in the Strait of Hormuz, Nvidia reinstating Jensen Huang), a schematic drawn world map marking eleven flashpoints, a UTC timeline strip of the day, and 39 short dated story items in three columns grouped by region (Middle East & Conflict, Europe, Americas, Asia-Pacific, Markets & Tech, Sport & World), closed by a "date check" verification footer naming the sources and verification time. The image is pre-rendered with Pillow by build_image.py and copied to the output directory by main.py, so the entrypoint is deterministic and needs no network.

## Run it

```sh
python3 build_image.py && MAKEFUN_OUTPUT_DIR=./output python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=s0dzaxys&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
