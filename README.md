# Project for decision making course at AGH university
- For server, go to [server](server/) directory.
- For client, go to [ranking_client](ranking_client/) directory

## The experts are supposed to be able to rank items using the UI below
![diagram](media/views.png)

## Usage:
### Compile client
1. Go to [ranking_client](ranking_client/) directory
2. Run the following command
```bash
cd ranking_client
mkdir -p dist && trunk build --release --public-url '/app' --dist 'dist/app'
```
### Run client using a webserver:
```bash
cd dist
python3 -m http.server 5000
```
Test if you can load the app by going to http://127.0.0.1:5000/app/ in your webrowser

### Run the API server
1. Go to [server](server/) directory
2. Run the following
```bash
cd server
python3 -m uvicorn main:app --reload
```


Test if you can load the app by going to http://127.0.0.1:8000/docs in your webrowser

### Run haproxy
```bash
haproxy -f server/haproxy/haproxy.cfg
```

Now you should be able to access the app, by going to http://127.0.0.1:9999/app/ in your browser.