### Get an API key
[- License Plate Recognition API](https://platerecognizer.com/dashboard/)

### Github
[GitHub - marcbelmont/deep-license-plate-recognition: Deep learning based Automatic License Plate Recognition API](https://github.com/marcbelmont/deep-license-plate-recognition)

### Installation
```
pip install requests
pip install pillow
pip install opencv-python
```

### Use
```
python alpr_video.py --api YOUR_API_KEY --start 0 --end 2000 --skip 10 1_converted.mp4
```

Explanation:
0 = Start frame
2000 = End frame
10 = Only send a request of the number 10, 20, 30, 40 , ... etc frame