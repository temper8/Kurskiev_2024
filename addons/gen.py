import pandas as pd
from pathlib import Path
print('Генератор exp файлов')

def default_options():
    return {
    'AB'    : 0.26,
    'ABC'   : 0.236,
    'AWALL' : 0.27,
    'RTOR'  : 0.367,
    'SHIFT' : 0,
    'BTOR'  : 0.9,
    'ELONM' : 2,
    'TRICH' : 0.4,
    'TRIAN' : 0.39,
    'ELONG' : 1.8,
    'IPL'   : 0.358,
    'UPDWN' : 0,
    'AMJ'   : 2,
    'ZMJ'   : 1,
    'ZRD30X': 1.8,
    'ZRD29X': 4
}
def read_shot(p):
    shot = pd.read_csv(p,delim_whitespace=True, header=None, names= ['x', 'Te', 'Ne'] )
    N = shot.shape[0]

    x = " ".join([f'{i:<8.4f}' for i in shot['x']])
    Te = " ".join([f'{i/1000:<8.4f}' for i in shot['Te']])
    Ne = " ".join([f'{i/1e19:<8.4f}' for i in shot['Ne']])
    lines = ['']
    lines.append('!*************** Te **********************************')
    lines.append(f'NAMEXP TEX POINTS {N} GRIDTYPE 19')
    lines.append('0.0')
    lines.append(x)
    lines.append(Te)

    lines.append(f'')
    lines.append('!*************** ne  **********************************')
    lines.append(f'NAMEXP NEX POINTS {N} GRIDTYPE 19 FACTOR 1')
    lines.append('0.0')
    lines.append(x)
    lines.append(Ne)
    return lines 

def make_exp_file(shot, time, options, shot_fname):
    lines = []
    lines.append(f'#{shot} {time}')
    lines.append(f' ')
    for key, v in options.items():
        lines.append(f'{key:<15}  {v}')

    shot_path= Path('shots').joinpath(Path(shot_fname).name)

    print(shot_path)
    if shot_path.exists():
        lines += read_shot(shot_path)

    fn = f'exp\{shot}_{time*10000:4.0f}.exp'
    with open(fn, 'w') as f:
        f.writelines(f'{s}\n' for s in lines)
    

df = pd.read_csv('database_3.csv')
df = df.rename(columns={"shot#": "shot", 'Ip': 'IPL', "Bt": "BTOR",'a':'ABC', 'R':'RTOR', 'tria': 'TRICH', 'elon': 'ELONM',
                        'Zeff': 'ZRD30X',
                        'Ti0': 'ZRD29X'})  
df['ABC']  = df['ABC'].map(lambda x: round(x/100,5))
df['RTOR'] = df['RTOR'].map(lambda x: round(x/100,5))
print(df)

#for indx in range(0,20):
for indx, row in df.iterrows():
    if indx > 10: break
    opt = default_options()
    for key, v in opt.items():
        if key in row:
            opt[key] = row[key]
    make_exp_file(int(row['shot']), round(row['time'],5), opt, row['fname'])
