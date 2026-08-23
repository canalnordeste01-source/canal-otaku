import datetime
import subprocess
from flask import Flask, Response

app = Flask(__name__)

LOGO_URL = "https://static.wikia.nocookie.net/televisoesficticias/images/2/23/Otaku.png/revision/latest?cb=20241029201948&path-prefix=pt"

MAGNETS_NYAA = {
    "black_clover": "magnet:?xt=urn:btih:3e7f6e09c86df2728329623e6605ddf799a4dd55",
    "free_iwatobi": "magnet:?xt=urn:btih:1a383d47c403fb2fb7b433e100f7e1adbd8b4a83",
    "jujutsu_kaisen": "magnet:?xt=urn:btih:7b2e1f48123ef9a83110294711f71a171d9b3b4f",
    "demon_slayer": "magnet:?xt=urn:btih:6a3b2e59178df9e82110294711f71a171d9a2a3e",
    "my_hero_academia": "magnet:?xt=urn:btih:8c3f2a19234fd8b94120305822f82b282e0c4c5a"
}

def obter_url_fonte():
    hora = datetime.datetime.now().hour
    
    if 6 <= hora < 9:
        return "torrent", MAGNETS_NYAA["black_clover"]
    elif 9 <= hora < 11:
        cmd = 'yt-dlp "ytsearch1:entrevista dublador anime brasil" -g -f best'
        return "direct", subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    elif 11 <= hora < 13:
        return "torrent", MAGNETS_NYAA["free_iwatobi"]
    elif 13 <= hora < 16:
        return "torrent", MAGNETS_NYAA["jujutsu_kaisen"]
    elif 16 <= hora < 18:
        cmd = 'yt-dlp "ytsearch1:desfile cosplay anime friends" -g -f best'
        return "direct", subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    elif 18 <= hora < 21:
        return "torrent", MAGNETS_NYAA["demon_slayer"]
    elif 21 <= hora < 24:
        return "torrent", MAGNETS_NYAA["my_hero_academia"]
    else:
        return "torrent", MAGNETS_NYAA["black_clover"]

@app.route('/canal-otaku-ao-vivo')
def canal_otaku_stream():
    tipo, fonte = obter_url_fonte()
    
    input_video = "http://127.0.0.1:8000/0" if tipo == "torrent" else fonte

    ffmpeg_cmd = [
        'ffmpeg', '-re',
        '-i', input_video,
        '-i', LOGO_URL,
        '-filter_complex',
        '[1:v]scale=180:-1,format=rgba,colorchannelmixer=aa=0.75[logo];'
        '[0:v][logo]overlay=main_w-overlay_w-20:20',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
        '-c:a', 'aac', '-f', 'mpegts', 'pipe:1'
    ]

    processo = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return Response(processo.stdout, mimetype='video/mp2t')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
