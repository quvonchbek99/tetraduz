import json, re, sys, os
D = os.path.dirname(os.path.abspath(__file__)) + '/'
CATS = [('ot','Otlar','Существительные'),('fel',"Fe'llar",'Глаголы'),('sifat','Sifatlar','Прилагательные'),
        ('son','Sonlar','Числительные'),('olmosh','Olmoshlar','Местоимения'),('ravish','Ravishlar','Наречия'),
        ('joy','Joylar va shaharlar','Места и города'),('matem','Matematik atamalar','Математика')]
CYR_V = 'аеёиоуыэюяАЕЁИОУЫЭЮЯ'
def stress(s):
    return re.sub('([%s])\'' % CYR_V, '\\1\u0301', s)
out = []
for key, uz, ru in CATS:
    words = []
    stage = 1
    for i, line in enumerate(open(D + key + '.txt', encoding='utf-8')):
        line = line.strip()
        if not line: continue
        if line.startswith('#'):
            stage = int(line[1:].strip()); continue
        f = [x.strip() for x in line.split(' | ')]
        assert len(f) == 8, (key, i, line)
        w = dict(id='%s%d' % (key, len(words)+1), ru=stress(f[0]), uz=f[1], em=f[2], g=stress(f[3]),
                 h=f[4], s=f[5], er=stress(f[6]), eu=f[7], b=stage)
        words.append(w)
    out.append(dict(k=key, uz=uz, ru=ru, w=words))
json.dump(out, open(D + 'tog.json', 'w', encoding='utf-8'), ensure_ascii=False)
js = "/* ТЕТРАДЬ — TOG lug'ati (Tarjima · Obraz · Garmoniya). Manba: lugat/data/*.txt */\nwindow.TOG_CATS = " + json.dumps(out, ensure_ascii=False, separators=(',',':')) + ";\n"
open(sys.argv[1], 'w', encoding='utf-8').write(js)
print(sum(len(c['w']) for c in out), 'words', len(js)//1024, 'KB')
# leftover apostrophe check in ru fields
for c in out:
    for w in c['w']:
        for k in ('ru','g','er'):
            if re.search("[а-яё]'", w[k], re.I): print('STRESS?', w['id'], w[k])
