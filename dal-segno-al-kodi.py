from flask import Flask
import discogs_client
import requests
import json

def search_my_discogs_collection_for_barcode(scan):
    d = discogs_client.Client('DalSegnoAlKodi/0.1', user_token='discogs-api-token-code...')
    me = d.identity()
    releases = d.search(scan)
    if (releases):
        for release in releases:
            if isinstance(release, discogs_client.Release):
                release_instances = me.collection_items(release)
                for instance in release_instances:
                    if (instance):
                        return release
                    else:
                        message = f'Discogs found releases for {scan}, but that release was not in the collection.'
                        raise LookupError(message)
    else:
        message = f'Discogs was searched for: {scan}, but no release was found. In case you have this item in your collection, consider to add this data to the release via the Discogs site.'
        raise LookupError(message)

def generate_path(release):
    artist = release.artists_sort.upper()
    artist = artist.replace(" FEATURING ", " ft. ")
    artist = artist.replace(" FEAT. ", " ft. ")
    artist = artist.replace(" VS. ", " vs. ")
    title = release.title.replace("(Remixes)","[Remixes]")
    title = title
    directory_name = f'{artist} ({release.year}) {title}'
    return(directory_name)

def play_kodi(discogs_folder, path):
    headers = {'Authorization': 'Basic ...'}
    directory = 'smb://nas.domain.local/data/music/' + discogs_folder + '/' + path
    pythondatastructure = { 'jsonrpc': '2.0', 'id': 1, 'method': 'Player.Open', 'params': { 'item': { 'directory': directory }}}
    response = requests.post('http://kodi.domain.local:8080/jsonrpc', data=json.dumps(pythondatastructure), headers=headers)
    return response

app = Flask(__name__)

@app.route('/scan/<barcode>')
def scanned_barcode(barcode):
    release = search_my_discogs_collection_for_barcode(scan=barcode)
    directory_name = generate_path(release)
    response = play_kodi(discogs_folder='Singles',path=directory_name)
    return f'<h1>Dal Segno Al Kodi</h1><code>{directory_name}</code><p>{response}</p>'

