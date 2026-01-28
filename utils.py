import json
from pydantic import BaseModel
from typing import Set, List, Dict, Any
from datetime import date

def load_data():
    with open('tracker.json', 'r') as file:
        data=json.load(file)
        print(type(data))
    
    return data

def save_data(data):
    with open('tracker.json', 'w') as file:
        json.dump(data, file)


def habit2dict(model: BaseModel, exclude:Set[str]=None):
    dump=model.model_dump(exclude=exclude)

    for k, v in dump.items():
        if isinstance(v, date):
            dump[k]=str(dump[k]) if dump[k] else None
        
        if isinstance(v, list):
            if v and  isinstance(v[0], date):
                dump[k]=[str(l) for l in dump[k]]

    return dump

def streak_calculation(logs, dt, freq, check, longest_streak, latest_streak):
    f=1 if freq=='Daily' else 7
    lo=longest_streak
    la=latest_streak
    if len(logs)==0:
        return 0, 0
    if check and dt==logs[0]:
        if len(logs)==1 or (logs[0]-logs[1]).days==f:
            la+=1
            if la>lo:
                lo=la
        else:
            la=1
    else:
        c=1
        l=0
        f_b=True
        for l1,l2 in zip(logs, logs[1:]):
            if (l1-l2).days==f:
                c+=1
            else:
                if f_b:
                    la=c
                    f_b=False
                l=max(l, c)
                c=1
                
        if f_b: la=c
        l=max(l, c)
        lo=l

    return lo, la   