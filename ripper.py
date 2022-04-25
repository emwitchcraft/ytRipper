import requests
from bs4 import BeautifulSoup
import json
from moviepy import editor
from pathlib import Path
import time
import traceback

try:
    root = Path(__file__).parent
    rips = root/'rips'
    rips.mkdir(parents=True,exist_ok=True)

    while True:
        try:
            ytUrl = input('gimme the youtube link: ')
            fileName = input('what do you wanna call it? (name only, no extension pls): ')
            fileName = fileName.replace(' ','')
            
            #fetch page
            print('getting page...')
            soup = BeautifulSoup(requests.get(ytUrl).text,'html.parser')
            print('page received...')
            print('parsing page data...')
            
            #find script with the data
            for script in soup.find_all('script'):
                try:
                    if '{"itag":' in script.string:
                        data = script.string.split(' = ')[1].strip(';')
                        break
                except:
                    pass
                
            #find the target stream type
            #having completely confirmed, but seems like last format should be highest quality
            streamingData = json.loads(data)['streamingData']
            target = streamingData['formats'][-1]
                
            #download video
            vidFile = root/'temp.mp4'
            print('downloading video...')
            session = requests.Session()
            startTime = time.time()
            with session.get(target['url'],stream=True) as stream:
                with open(str(vidFile),'wb') as file:
                    for chunk in stream.iter_content(chunk_size=1024*1024):
                        file.write(chunk)
            session.close()
            print('download complete')
            print(f'elapsed time: {round((time.time()-startTime)/60,2)}m')
            
            #rip audio
            vid = editor.VideoFileClip(str(vidFile))
            print('ripping audio...')
            vid.audio.write_audiofile(f'rips/{fileName}.mp3',bitrate='3000k')
            vid.close()
            
            print('audio rip complete')
            print(f'file saved to rips/{fileName}.mp3')
            print('deleting video file...')
            vidFile.unlink()
            print('video file deleted')
            print('all done!')
            print()
        except Exception as e:
            print('rip failed :\'(')
            print('ERROR:')
            print(e)
            print()
except Exception as e:
    print('ERROR')
    traceback.format_exc()
    print()