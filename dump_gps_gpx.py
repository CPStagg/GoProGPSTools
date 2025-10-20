#!/usr/bin/env python3
import argparse
from datetime import datetime, timedelta
from py_gpmf_parser.gopro_telemetry_extractor import GoProTelemetryExtractor
from math import radians, sin, cos, sqrt, atan2
import subprocess
import json

def haversine(lat1, lon1, lat2, lon2):
    """Return great-circle distance between two lat/lon pairs in meters."""
    R = 6371000  # Earth radius (m)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def write_gpx(file_360, mp4_file, output_gpx):
    # Extract GPS data from .360 file
    extractor = GoProTelemetryExtractor(file_360)
    extractor.open_source()
    gps_data, timestamps = extractor.extract_data("GPS5")
    extractor.close_source()

    if len(gps_data) == 0:
        raise RuntimeError("No GPS data found in .360 file.")

    # Calculate offsets from first timestamp
    first_ts = timestamps[0]
    local_deltas = [ts - first_ts for ts in timestamps]

    # Get the MP4 creation time
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", mp4_file],
        capture_output=True, text=True
    )
    info = json.loads(result.stdout)
    creation_time_str = info['format']['tags']['creation_time']
    mp4_start = datetime.fromisoformat(creation_time_str.replace('Z', '+00:00'))

    pointLast = None

    # Write GPX
    with open(output_gpx, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<gpx version="1.1" creator="GoPro360GPX">\n')
        f.write('  <trk>\n')
        f.write('    <name>GoPro Track</name>\n')
        f.write('    <trkseg>\n')
        for delta, point in zip(local_deltas, gps_data):
            dt = mp4_start + timedelta(seconds=delta)
            lat, lon, alt, *_ = point
            
            skipWrite = False
            if pointLast is not None:
                lat0, lon0 = pointLast
                dist = haversine(lat0, lon0, lat, lon)
                if dist > 100:  # e.g. more than 100 meters between consecutive samples
                    print(f"⚠️  GPS jump detected: {dist:.0f} m at {dt.isoformat()}, lat = {lat:.0f}, lon = {lon:.0f} (skipping entry)")
                    skipWrite = True
        
            if not skipWrite:
                pointLast = (lat, lon)
                f.write(f'      <trkpt lat="{lat}" lon="{lon}"><ele>{alt}</ele><time>{dt.isoformat()}</time></trkpt>\n')

        f.write('    </trkseg>\n')
        f.write('  </trk>\n')
        f.write('</gpx>\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract GPS from GoPro .360 and align to MP4 timestamps")
    parser.add_argument("file_360", help="Path to .360 file")
    parser.add_argument("mp4_file", help="Path to corresponding MP4 file")
    parser.add_argument("-o", "--output", default="track.gpx", help="Output GPX filename")
    args = parser.parse_args()

    write_gpx(args.file_360, args.mp4_file, args.output)
    print(f"GPX file written to {args.output}")
