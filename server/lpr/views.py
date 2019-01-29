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
import os
from django.conf import settings

from django.shortcuts import render
from rest_framework import generics, viewsets, views
from rest_framework.response import Response
from lpr.models import LrpModel
from lpr.serializers import ConfigSerializer
from django.http import HttpResponse

class FinalView(views.APIView):

    def get(self, request, format=None):
        snippets = LrpModel.objects.all()
        plates = []
        data = []
        for snippet in snippets:
            plate = snippet.plate
            time = snippet.time
            frame = snippet.frame
            if plate not in plates and len(plate) > 3:
                plates.append(plate)
                data.append({
                    'plate': plate,
                    'time': time
                })
        result = "Total no. of car plates detected: " + str(len(data)) + "\n"
        for x in data:
            result += x['plate'] + ", " + x['time'] + "\n"
           
        return HttpResponse(result, content_type="text/plain")

class ListView(views.APIView):
    
    def get(self, request, format=None):
        snippets = LrpModel.objects.all()
        serializer = ConfigSerializer(snippets, many=True)
        return Response(serializer.data)

class MainView(views.APIView):
     def get(self, request, format=None):
        para = request.GET
        args = {}
        args['skip'] = int(para['skip'])
        args['start'] = int(para['start'])
        args['end'] = int(para['end'])
        args['FILE'] = para['FILE']
        args['api'] = para['api']
        result = []
        frame_ids = []
        cap = cv2.VideoCapture(os.path.join(settings.VIDEO_DIR, args.get('FILE')))
        frame_id = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            frame_id += 1
            if args.get('skip') and frame_id % args.get('skip') != 0:
                continue
            if args.get('start') and frame_id < args.get('start'):
                continue
            if args.get('end') and frame_id > args.get('end'):
                break
            print('Reading frame %s' % frame_id)
            fp = tempfile.NamedTemporaryFile()
            im = Image.fromarray(frame)
            im.save(fp, 'JPEG')
            fp.seek(0)
            response = requests.post(
                'https://platerecognizer.com/plate-reader/',
                files=dict(upload=fp),
                headers={'Authorization': 'Token ' + args.get('api')})

            d = response.json()
            results = d.get('results', [])
            if results:
                for result in results:
                    time = int(frame_id / 30)
                    mins = str(int(time / 60))
                    seconds = str(int(time % 60))
                    lrpModel = LrpModel(frame = frame_id, plate = result.get('plate'), time = mins + ":" + seconds)
                    lrpModel.save()
        return Response({'done': "done"})