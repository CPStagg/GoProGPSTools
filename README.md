# GoPro 360 GPX Generator

This script extracts GPS telemetry from a GoPro `.360` file and aligns it with the timestamp of a rectilinear `.mp4` export (e.g., from GoPro Player). It outputs a `.gpx` file suitable for use with platforms like Google Street View Studio, even when the exported video lacks embedded GPS data.

## 🔧 System Requirements

- Python 3.7+
- macOS, Linux, or Windows
- GoPro `.360` file with embedded GPS
- Corresponding `.mp4` file exported from GoPro Player

## 📦 Python Dependencies

Install the required packages using pip:

pip install py-gpmf-parser

This script also uses the following standard Python libraries:
• 	argparse
• 	datetime
• 	subprocess
• 	json

No additional dependencies are required beyond py-gpmf-parser.
🛠️ Additional Notes
• 	py-gpmf-parser is a Python wrapper for GoPro’s GPMF telemetry extraction. It may require ffmpeg to be installed and available in your system’s PATH.
• 	If you're using a virtual environment, activate it before installing dependencies.

USE:
Let's say you have a 360 file that you've recorded using your GoPro and imported onto your Mac or PC. Let's call it 100125.360
First use GoPro Player to export from your 100125.360 file an mp4, using the H.264 codec. I'm sure you'd like to retain GPX data,
but at the time of writing GoPro have thoughtfully removed that option on Mac, and they never had it on Windows. Very useful.

Anyway, let's say you chose to call your exported file MyFootage.mp4

Your mp4 is in the right format for Google Street View Studio, but it lacks the GPS data needed. But if you created a corresponding GPX file, you'd be able to satisfy
Street View by uploading both files (the .mp4 and the .gpx files).

We can now create that .gpx file as follows:

python3 dump_gps_gpx.py 100125.360 MyFootage.mp4 -o MyFootage.gpx

In Street View, you can now choose to import your MyFootage.mp4 file. At this point the importer will run around with its hair on fire and put up orange warning triangles
telling you you're a terrible person for not including any GPS data. Fret not, Google. You can assuage its misery by choosing to click on the small context menu that allows
you to upload a separate GPX file. Choose MyFootage.gpx. At this point Street View will be all smiles, showing you the GPS path in blue, and it will be ready for you to confirm
your upload, taking a new attitude of, "Why didn't you say so? Come IN, old boy!" sort of thing.

But why does dump_gps_gpx.py require input arguments of both the 360 file AND the mp4 file? Well, this is because GoPro Player cheerfully screws up all the timestamps from the original
360 file when it exports, so you have to do a weird dance to satisfy Street View, which will spit the dummy if the .gpx and .mp4 timings are out of sync. Basically it discards the
objective timings from the 360 file but uses its deltas, while taking the creation time of the .mp4 as the official start of its timing sequence. This does entail the odd
consequence that if you recorded three minutes of footage at noon on Wednesday 12th but exported the mp4 at midnight on Friday 14th, the files uploaded to Street View will officially
have timestamps from midnight to three minutes past midnight on Friday 14th, but, ehh, nobody really cares. 

## 📝 License

This project is licensed under the MIT License.

MIT License
Copyright (c) 2025 cpstagg
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
