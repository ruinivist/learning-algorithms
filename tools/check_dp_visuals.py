"""Check embedded PNGs and the affected worked examples: python tools/check_dp_visuals.py."""
from collections import Counter
from functools import cache
from itertools import groupby
from pathlib import Path
from typing import List
import heapq
import math
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / 'Dynamic Programming'

def solution(filename, index=0):
    blocks=re.findall(r'^```python\n(.*?)^```', (ROOT/filename).read_text(),re.M|re.S)
    ns={'cache':cache,'math':math,'List':List,'heappop':heapq.heappop,'heappush':heapq.heappush}
    exec(compile(blocks[index],filename,'exec'),ns)
    return ns['Solution']()

def check():
    images=list((ROOT/'visuals').glob('*.png'))
    assert len(images)==33
    refs=[];notes=0
    for p in ROOT.glob('*.md'):
        targets=re.findall(r'!\[[^\]]+\]\((\./visuals/[^)]+)\)',p.read_text())
        notes+=bool(targets)
        for target in targets:
            q=p.parent/target
            assert q.is_file(),(p,target)
            refs.append(q.resolve())
    assert notes==28
    assert Counter(refs)==Counter(p.resolve() for p in images)
    for p in images:
        with Image.open(p) as im:
            assert im.size==(1600,1000),p
            im.verify()

    stocks=solution('Buy and Sell Stock III and IV.md')
    for k,prices,want in [(0,[1,2],0),(1,[1,2],1),(1,[2,1],0),
                          (2,[3,2,6,5,0,3],7),(2,[3,3,5,0,0,3,1,4],6),(2,[],0)]:
        assert stocks.maxProfit(k,prices)==want

    # All four refuelling variants should agree, including the corrected typo.
    for index in range(4):
        solver=solution('Min number of refuelling stops.md',index)
        for t,start,stations,want in [(100,10,[[10,60],[20,30],[30,30],[60,40]],2),
                                      (1,1,[],0),(100,1,[[10,100]],-1)]:
            assert solver.minRefuelStops(t,start,[s[:] for s in stations])==want

    repeats=solution('Count the repetitions.md')
    assert repeats.getMaxRepetitions('abab',7,'aaab',2)==2
    # Explicit block transitions in the cursor diagram.
    for start,end,gain in [(0,2,0),(2,1,1),(1,0,1)]:
        j=start;count=0
        for ch in 'abab':
            if ch=='aaab'[j]:
                j+=1
                if j==4:j=0;count+=1
        assert (j,count)==(end,gain)

    assert solution('Dungeon Game.md').calculateMinimumHP([[-2,-3,3],[-5,-10,1],[10,30,-5]])==7
    assert solution('Burst Balloons.md').maxCoins([3,1,5])==35
    assert solution('Number of Digit One.md',-1).countDigitOne(13)==6

    # Verify every collapse pictured in the two Zuma PNGs.
    def clean(s):
        while True:
            nxt=''.join(ch*len(run) for ch,g in groupby(s) if len(run:=list(g))<3)
            if nxt==s:return s
            s=nxt
    assert clean('RRBBBRR')==''
    b='RRWWRRBBRR'
    b=b[:9]+'W'+b[9:]
    assert b=='RRWWRRBBRWR' and clean(b)==b
    b=b[:6]+'B'+b[6:]
    assert b=='RRWWRRBBBRWR' and clean(b)==''
    print('PASS: 33 PNGs, 28 notes, unique valid embeds, stock/refuel regressions, and worked examples.')

if __name__=='__main__':
    check()
