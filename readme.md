## Challenge 1:  Car Registration Number Recognition API (CRNRA)
___
##  Operational procedures
### Installation
```
pip install -r requirements.txt
```

### Server
```
cd server

# For login to admin portal
python manage.py createsuperuser

python manage.py migrate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Admin portal
```
http://127.0.0.1:8000/admin/
```

### API Endpoint - Analyze video
```
{{ domain }} + Para

api:92035422f0111202f2d2a87f5be8abffc1a8af67
start:0
end:100
skip:10
FILE:1_converted.mp4

Example:
http://127.0.0.1:8000/lpr/?api=92035422f0111202f2d2a87f5be8abffc1a8af67&start=0&end=100&skip=10&FILE=1_converted.mp4
```

api = your api key
set end = 30 * video duration(second)
FILE: the file name inside 
```
server/lpr/helpers
```

### Get the final result when analyze video is done
```
{{ domain }} + lpr/result

Example
http://127.0.0.1:8000/lpr/result
```

### Get a list from database
```
{{ domain }} + lpr/list

Example
http://127.0.0.1:8000/lpr/list
```

Output:
```json
[
    {
        "id": 8,
        "time": "0:0",
        "plate": "nz3821",
        "frame": 10
    },
    {
        "id": 9,
        "time": "0:1",
        "plate": "dj5206",
        "frame": 40
    }
]
```

##  Input and output parameters of the algorithm
The algorithm requires at least four parameters for input and output. 
- "id" : Number of records 
- "time" : Video time of the record 
- "plate" : License plate
- "frame" : Frame number 
```sh
Example: 
｛
    "id": 8,
    "time": "0:0", 
    "plate": "nz3821",
    "frame": 10
 },
```
##  Limitations of the algorithm and potential problems
- Dependency to third-party API and library
-- Performance would be vary if dependencies have change

##  Procedure of the embedment of the algorithm into the camera 
1) Make sure the camera(device) can be connected to the Internet
2) Use the API to call requests from our backend server
3) Call API into the development environment with own camera library

