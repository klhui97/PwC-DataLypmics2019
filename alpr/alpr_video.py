#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PIL import Image
import argparse
import cv2
import json
import requests
import tempfile
import time


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Read license plates from a video and output the result as JSON.',
        epilog='For example: python alpr_video.py --api MY_API_KEY --start 900 --end 2000 --skip 3 "/path/to/cars.mp4"')
    parser.add_argument('--api', help='Your API key.', required=True)
    parser.add_argument('--start', help='Start reading from this frame.', type=int)
    parser.add_argument('--end', help='End reading after this frame.', type=int)
    parser.add_argument('--skip', help='Read 1 out of N frames.', type=int)
    parser.add_argument('FILE', help='Path to video.')
    return parser.parse_args()


def main():
    args = parse_arguments()
    result = []
    frame_ids = []
    cap = cv2.VideoCapture(args.FILE)
    frame_id = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame_id += 1
        if args.skip and frame_id % args.skip != 0:
            continue
        if args.start and frame_id < args.start:
            continue
        if args.end and frame_id > args.end:
            break
        print('Reading frame %s' % frame_id)
        fp = tempfile.NamedTemporaryFile()
        im = Image.fromarray(frame)
        im.save(fp, 'JPEG')
        fp.seek(0)
        response = requests.post(
            'https://platerecognizer.com/plate-reader/',
            files=dict(upload=fp),
            headers={'Authorization': 'Token ' + args.api})
        result.append(response.json())
        frame_ids.append(frame_id)
        time.sleep(1)
    print(json.dumps(result, indent=2))
    text_file = open(str(args.start) + "-" + str(args.end) + "data.csv", "w")
    for i, r in enumerate(result):
        if len(r.get('results', [])) > 0:
            for d in r.get('results', []):
                text_file.write(str(frame_ids[i]) + "," + str(d['score']) + "," + d['plate'] + "\n")
        
    text_file.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
