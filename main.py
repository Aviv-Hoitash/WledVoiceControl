import speech_recognition as sr
import requests
import defaults as d
from word2number import w2n

ip = "YOUR_LIGHTS_IP
url="http://{}/json/state".format(ip)


json = {
    "on": d.on,
    "bri": d.bri,
    "transition": d.transition,
    "ps": d.ps,
    "pl": d.pl,
    "ccnf": {
        "min": d.ccnf_min,
        "max": d.ccnf_max,
        "time": d.ccnf_time
    },
    "nl": {
        "on": d.nl_on,
        "dur": d.nl_dur,
        "fade": d.nl_fade,
        "mode": d.nl_mode,
        "tbri": d.nl_tbri,
        "rem": d.nl_rem
    },
    "udpn": {
        "send": d.udpn_send,
        "recv": d.udpn_recv
    },
    "lor": d.lor,
    "mainseg": d.mainseg,
    "seg": [
        {
            "id": d.seg_id,
            "start": d.seg_start,
            "stop": d.seg_stop,
            "len": d.seg_len,
            "grp": d.seg_grp,
            "spc": d.seg_spc,
            "on": d.seg_on,
            "bri": d.seg_bri,
            "col": d.seg_col,
            "fx": d.fx,
            "sx": d.sx,
            "ix": d.ix,
            "pal": d.pal,
            "sel": d.sel,
            "rev": d.rev,
            "mi": d.mi
        }
    ]
}


colors = {"red":(255,0,0),"orange":(255,165,0),"yellow":(255,255,0),"green":(0,255,0),"blue":(0,0,255),"purple":(128,0,128),"white":(255,255,255),"black":(0,0,0),"gold":(212,175,55)}

effects = [
    "Solid", "Blink", "Breathe", "Wipe", "Wipe Random", "Random Colors", "Sweep", "Dynamic", "Color Loop", "Rainbow",
    "Scan", "Dual Scan", "Fade", "Chase", "Chase Rainbow", "Running", "Saw", "Twinkle", "Dissolve", "Dissolve Rnd",
    "Sparkle", "Dark Sparkle", "Sparkle+", "Strobe", "Strobe Rainbow", "Mega Strobe", "Blink Rainbow", "Android", "Chase", "Chase Random",
    "Chase Rainbow", "Chase Flash", "Chase Flash Rnd", "Rainbow Runner", "Colorful", "Traffic Light", "Sweep Random", "Running 2", "Red And Blue", "Stream",
    "Scanner", "Lighthouse", "Fireworks", "Rain", "Merry Christmas", "Fire Flicker", "Gradient", "Loading", "In Out", "In In",
    "Out Out", "Out In", "Circus", "Halloween", "Tri Chase", "Tri Wipe", "Tri Fade", "Lightning", "ICU", "Multi Comet",
    "Dual Scanner", "Stream 2", "Oscillate", "Pride 2015", "Juggle", "Palette", "Fire 2012", "Colorwaves", "BPM", "Fill Noise", "Noise 1",
    "Noise 2", "Noise 3", "Noise 4", "Colortwinkle", "Lake", "Meteor", "Smooth Meteor", "Railway", "Ripple"
  ]

palettes = [
    "Default", "Random Cycle", "Primary Color", "Based on Primary", "Set Colors", "Based on Set", "Party", "Cloud", "Lava", "Ocean",
    "Forest", "Rainbow", "Rainbow Bands", "Sunset", "Rivendell", "Breeze", "Red & Blue", "Yellowout", "Analogous", "Splash",
    "Pastel", "Sunset 2", "Beech", "Vintage", "Departure", "Landscape", "Beach", "Sherbet", "Hult", "Hult 64",
    "Drywet", "Jul", "Grintage", "Rewhi", "Tertiary", "Fire", "Icefire", "Cyane", "Light Pink", "Autumn",
    "Magenta", "Magred", "Yelmag", "Yelblu", "Orange And Teal", "Tiamat", "April Night"
  ]




def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
           pass

    return said
while True:
    speech = get_audio()
    if "animation" in speech:
        animation = speech.split("animation")[1][1::].title()
        if animation in effects:
            d.fx = effects.index(animation)
            json['seg'][0]['fx'] = d.fx
            r = requests.post(url=url, json=json)
        else:
            try:
                animation_num = w2n.word_to_num(animation)
                d.fx = animation_num
                json['seg'][0]['fx'] = d.fx
                r = requests.post(url=url, json=json)
            except:
                pass
    if "pallet" in speech:
        palette = speech.split("pallet")[1][1::].title()
        if palette in palettes:
            d.pal = palettes.index(palette)
            json['seg'][0]['pal'] = d.pal
            r = requests.post(url=url, json=json)
        else:
            print(palette)
            try:
                palette_num = w2n.word_to_num(palette)
                d.pal = palette_num
                json['seg'][0]['pal'] = d.pal
                r = requests.post(url=url, json=json)
                print(json)
            except:
                pass
    elif "second" in speech.lower():
        for color in colors.keys():
            if color in speech.lower():
                d.seg_col[1][0] = colors[color][0]
                d.seg_col[1][1] =colors[color][1]
                d.seg_col[1][2] = colors[color][2]
                json['col'] = d.seg_col
                r = requests.post(url=url, json=json)
    elif "third" in speech.lower():
        for color in colors.keys():
            if color in speech.lower():
                d.seg_col[2][0] = colors[color][0]
                d.seg_col[2][1] =colors[color][1]
                d.seg_col[2][2] = colors[color][2]
                json['col'] = d.seg_col
                r = requests.post(url=url, json=json)
    elif "brightness" in speech:
        brightness_word = speech.split("brightness")[1][1::]
        if brightness_word:
            brightness = w2n.word_to_num(brightness_word)
        else:
            brightness = d.bri
        d.bri = brightness
        json['seg'][0]['bri'] = d.bri
        r = requests.post(url=url, json=json)
    elif "off" in speech:
        d.on = False
        json['on'] = d.on
        r = requests.post(url=url, json=json)
    elif "on" in speech:
        d.on = True
        json['on'] = d.on
        r = requests.post(url=url, json=json)
    elif "speed" in speech:
        speed_word = speech.split("speed")[1][1::]
        if speed_word:
            speed = w2n.word_to_num(speed_word)
        else:
            speed = d.sx
        d.sx = speed
        json['seg'][0]['sx'] = d.sx
        r = requests.post(url=url, json=json)
    elif "intensity" in speech:
        intensity_word = speech.split("intensity")[1][1::]
        if intensity_word:
            intensity = w2n.word_to_num(intensity_word)
        else:
            intensity = d.ix
        d.ix = intensity
        json['seg'][0]['ix'] = d.ix
        r = requests.post(url=url, json=json)
    else:
        for color in colors.keys():
                if color in speech.lower():
                    d.seg_col[0][0] = colors[color][0]
                    d.seg_col[0][1] =colors[color][1]
                    d.seg_col[0][2] = colors[color][2]
                    json['col'] = d.seg_col
                    r = requests.post(url=url, json=json)
    print(speech)




