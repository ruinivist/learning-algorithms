"""Regenerate the grokking PNGs: python tools/render_dp_visuals.py [renderer_name ...].

Requires matplotlib. All geometry and examples are explicit; no generated text.
"""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle

OUT = Path(__file__).resolve().parents[1] / 'Dynamic Programming' / 'visuals'
INK, MUTED, BLUE, GREEN, ORANGE, RED, PURPLE = '#172536', '#637184', '#3276bb', '#32836e', '#a96e26', '#b95560', '#8062aa'
PALE = {BLUE:'#eaf2fb', GREEN:'#eaf5f0', ORANGE:'#fbf2e4', RED:'#fbeef0', PURPLE:'#f1edf8', MUTED:'#f1f4f7', INK:'#f1f4f7'}
PAGES = {}
TEXTS = []

def page(slug, title, subtitle, cue):
    global fig, ax, TEXTS
    TEXTS = []
    fig, ax = plt.subplots(figsize=(16,10), dpi=100)
    fig.subplots_adjust(0,0,1,1)
    ax.set(xlim=(0,1600), ylim=(1000,0)); ax.axis('off')
    fig.patch.set_facecolor('white')
    text(70,65,title,32,weight='bold')
    text(72,116,subtitle,17,MUTED)
    line(72,158,1528,158,'#dfe5eb',1)
    line(72,886,1528,886,'#dfe5eb',1)
    text(74,931,cue,18,BLUE,weight='bold')
    text(1528,974,'GROKKING  /  DYNAMIC PROGRAMMING',9,MUTED,ha='right')
    PAGES[slug]=(fig,ax)

def text(x,y,s,size=16,color=INK,ha='left',weight='normal',va='center'):
    a=ax.text(x,y,s,fontsize=size,color=color,ha=ha,va=va,weight=weight,
              family='DejaVu Sans',linespacing=1.5)
    TEXTS.append(a)
    return a

def eq(x,y,s,size=23,color=INK,ha='center'):
    return text(x,y,'$'+s+'$',size,color,ha)

def line(x1,y1,x2,y2,c=MUTED,lw=2,style='-'):
    ax.plot([x1,x2],[y1,y2],color=c,lw=lw,ls=style,zorder=0)

def arrow(x1,y1,x2,y2,c=MUTED,label=None,curve=0):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',
        mutation_scale=17,linewidth=2,color=c,connectionstyle=f'arc3,rad={curve}'))
    if label: text((x1+x2)/2,(y1+y2)/2-22,label,13,c,ha='center')

def box(x,y,w,h,label='',c=BLUE,fs=17,fill=True):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=10',
        facecolor=PALE[c] if fill else 'white',edgecolor=c if not fill else '#e0e6ed',linewidth=1.2))
    if label: text(x+w/2,y+h/2,label,fs,c,ha='center',weight='bold')

def array(vals,x,y,w=90,h=65,colors=None,indices=False):
    centers=[]
    for i,v in enumerate(vals):
        col=(colors[i] if colors else MUTED)
        box(x+i*w,y,w-6,h,str(v),col,18)
        centers.append(x+i*w+(w-6)/2)
        if indices: text(centers[-1],y+h+23,str(i),12,MUTED,ha='center')
    return centers

def label(x,y,s,c=BLUE): text(x,y,s,14,c,weight='bold')

def bracket(x1,x2,y,s,c=BLUE):
    line(x1,y,x1,y+12,c);line(x1,y+12,x2,y+12,c);line(x2,y,x2,y+12,c)
    text((x1+x2)/2,y+42,s,15,c,ha='center')

def grid(vals,x,y,w=105,h=80,colors=None):
    for i,row in enumerate(vals):
        for j,v in enumerate(row):
            box(x+j*w,y+i*h,w-6,h-6,str(v),colors[i][j] if colors else MUTED,19)

def balls(s,x,y,step=70):
    colors={'R':RED,'B':BLUE,'W':MUTED,'Y':ORANGE,'G':GREEN}
    for i,ch in enumerate(s):
        c=colors[ch]
        ax.add_patch(Circle((x+i*step,y),24,facecolor=PALE[c],edgecolor=c,lw=1.5))
        text(x+i*step,y,ch,15,c,ha='center',weight='bold')

def save(slug):
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    for artist in TEXTS:
        b=artist.get_window_extent(renderer)
        assert b.x0>=15 and b.x1<=1585 and b.y0>=8 and b.y1<=992,(slug,artist.get_text(),b.bounds)
    OUT.mkdir(parents=True,exist_ok=True)
    fig.savefig(OUT/(slug+'.png'),dpi=100,facecolor='white',metadata={'Software':'grokking / matplotlib'})
    plt.close(fig)

def burst_balloons():
    slug='burst-balloons-last'
    page(slug,'Burst Balloons','Pick the LAST balloon inside [L, R].','Last choice → fixed neighbors → independent intervals')
    label(100,205,'ONE CANDIDATE: k = 1')
    array([1,3,1,5,1],360,240,170,90,[MUTED,BLUE,ORANGE,GREEN,MUTED])
    text(440,366,'L − 1',14,MUTED,ha='center');text(780,366,'k',16,ORANGE,ha='center');text(1120,366,'R + 1',14,MUTED,ha='center')
    bracket(530,690,355,'left interval',BLUE);bracket(870,1030,355,'right interval',GREEN)
    arrow(610,420,610,510,BLUE,'clear left');arrow(950,420,950,510,GREEN,'clear right')
    array([1,'∅',1,'∅',1],360,540,170,90,[MUTED,MUTED,ORANGE,MUTED,MUTED])
    bracket(360,1204,652,'neighbors of k are now exactly L − 1 and R + 1',ORANGE)
    eq(800,773,r'F(L,R)=\max_{k=L}^{R}\left[F(L,k-1)+a_{L-1}a_ka_{R+1}+F(k+1,R)\right]',23)
    text(800,837,'This k: 3 + 1×1×1 + 5 = 9     •     Best over all k: 35',16,MUTED,ha='center')
    save(slug)

def strange_printer():
    slug='strange-printer-shared-turn'
    page(slug,'Strange Printer','A later matching character pays for the shared printing turn.','Merge at k → the turn is already counted in F(k, r)')
    label(100,204,'TARGET: abaca')
    for y,chars,note in [(250,'aaaaa','1  paint a across'),(360,'abaaa','2  overwrite b'),(470,'abaca','3  overwrite c')]:
        array(list(chars),140,y,115,70,[BLUE if ch=='a' else ORANGE if ch=='b' else PURPLE for ch in chars])
        text(790,y+35,note,20)
    array(['a','b','a','c','a'],270,640,160,70,[BLUE,ORANGE,BLUE,PURPLE,BLUE])
    bracket(430,584,725,'middle: F(1,1) = 1',ORANGE)
    bracket(590,1064,725,'right: F(2,4) = 2',BLUE)
    eq(800,835,r'F(0,4)\leq F(1,1)+F(2,4)=1+2=3',24)
    arrow(345,615,665,615,BLUE,curve=-.3)
    text(505,615,'same a: l piggybacks on k',13,BLUE,ha='center')
    save(slug)

def tallest_billboard():
    slug='tallest-billboard-difference'
    page(slug,'Tallest Billboard','Keep the gap; forget which side is called left.','Three choices: skip, add to taller, add to shorter')
    label(110,208,'CURRENT: 8 AND 5  →  d = 3')
    for x,h,c in [(240,8,BLUE),(400,5,GREEN)]:
        ax.add_patch(Rectangle((x,620-h*43),90,h*43,color=PALE[c],ec=c,lw=2));text(x+45,650,str(h),21,c,ha='center')
    line(180,620,550,620)
    text(365,735,'new rod x = 4',23,ORANGE,ha='center')
    for y,name,formula,c in [(250,'Skip','d′ = 3',MUTED),(440,'Add to taller','d′ = 3 + 4 = 7',BLUE),(630,'Add to shorter','d′ = |3 − 4| = 1',GREEN)]:
        arrow(600,480,820,y+25,c)
        text(870,y,name,21,c,weight='bold');text(870,y+52,formula,23)
    text(870,735,'8 vs 9: shorter becomes taller',17,GREEN)
    eq(800,829,r'd=|L-R|,\quad\text{answer}=\frac{\text{maximum used length at }d=0}{2}',22)
    save(slug)

def di_ranks():
    slug='di-sequence-ranks'
    page(slug,'DI Sequence','Append a rank; shift every existing rank ≥ the inserted rank.','I sums old ranks k < j; D sums old ranks k ≥ j')
    label(110,207,'INSERT NEW LAST RANK j = 1')
    array([0,2,1],130,255,135,75,[MUTED,MUTED,BLUE])
    arrow(565,294,745,294,ORANGE,'shift ranks ≥ 1')
    array([0,3,2,1],800,255,135,75,[MUTED,MUTED,BLUE,ORANGE])
    text(390,380,'old last rank k = 1',17,BLUE,ha='center')
    text(1070,380,'2 > 1: D works even when k = j',17,ORANGE,ha='center')
    label(110,485,'WHICH OLD LAST RANKS CAN LEAD TO NEW RANK j = 2?')
    text(140,565,'I',27,GREEN,weight='bold');array([0,1,2,3],240,530,145,75,[GREEN,GREEN,MUTED,MUTED])
    eq(1220,568,r'\mathrm{new}[j]=\sum_{k<j}\mathrm{old}[k]',23)
    text(140,715,'D',27,PURPLE,weight='bold');array([0,1,2,3],240,680,145,75,[MUTED,MUTED,PURPLE,PURPLE])
    eq(1220,717,r'\mathrm{new}[j]=\sum_{k\geq j}\mathrm{old}[k]',23)
    text(800,831,'Relative order survives the shift. Absolute values are unnecessary.',17,MUTED,ha='center')
    save(slug)

def inversions_insert():
    slug='inverse-pairs-insertion'
    page(slug,'K Inverse Pairs · 1','Insert the new largest element. Only elements to its right create NEW inversions.','Each insertion position contributes a different count: 0 through n − 1')
    for y,vals,count in [(225,[4,1,2,3],3),(365,[1,4,2,3],2),(505,[1,2,4,3],1),(645,[1,2,3,4],0)]:
        array(vals,220,y,140,75,[ORANGE if v==4 else BLUE for v in vals])
        text(950,y+38,f'+ {count} inversions',23,ORANGE)
    eq(800,824,r'D(n,k)=\sum_{t=0}^{\min(k,n-1)}D(n-1,k-t)',26)
    save(slug)

def inversions_window():
    slug='inverse-pairs-window'
    page(slug,'K Inverse Pairs · 2','The expensive inner sum is a sliding window on the previous DP row.','Advance k: add the new right edge; subtract the expired left edge')
    text(120,225,'old: permutations of length 3',19)
    centers=array([1,2,2,1,0,0,0],250,280,145,80,[BLUE]*4+[MUTED]*3,True)
    bracket(250,824,405,'new[3] = old[0] + … + old[3] = 6',BLUE)
    array([1,2,2,1,0,0,0],250,545,145,80,[RED]+[GREEN]*4+[MUTED]*2,True)
    text(315,715,'− old[0]',18,RED,ha='center');text(895,715,'+ old[4]',18,GREEN,ha='center')
    eq(800,803,r'\mathrm{new}[4]=\mathrm{new}[3]+\mathrm{old}[4]-\mathrm{old}[0]=6+0-1=5',23)
    text(800,851,'Adding n = 4 creates windows of width 4.   Time: O(nk).',16,MUTED,ha='center')
    save(slug)

def average_transform():
    slug='same-average-transform'
    page(slug,'Same Average · 1','Remove the fraction by centering and scaling.','Find a nonempty, proper subset whose transformed sum is zero')
    eq(800,226,r'\frac{\sum_{i\in A}a_i}{|A|}=\frac{S}{n}\quad\Longleftrightarrow\quad\sum_{i\in A}(na_i-S)=0',29)
    text(110,342,'n = 6, S = 21',20)
    array([1,2,3,4,5,6],320,390,150,75,[BLUE,MUTED,MUTED,MUTED,MUTED,BLUE])
    for x in [392,1142]:arrow(x,475,x,540,BLUE)
    array([-15,-9,-3,3,9,15],320,560,150,75,[BLUE,MUTED,MUTED,MUTED,MUTED,BLUE])
    text(130,598,'bᵢ = 6aᵢ − 21',20,ORANGE)
    bracket(320,1214,680,'choose {1, 6}: −15 + 15 = 0',BLUE)
    eq(800,809,r'\operatorname{avg}\{1,6\}=\operatorname{avg}\{2,3,4,5\}=3.5',26)
    save(slug)

def average_mitm():
    slug='same-average-mitm'
    page(slug,'Same Average · 2','Large sum range? Enumerate half-subsets instead of indexing every possible sum.','Generate ~2^(n/2) sums per half; match x with −x')
    label(110,207,'AFTER TRANSFORM: [−15, −9, −3, 3, 9, 15]')
    text(110,257,'Drop one element: the opposite zero-sum group survives; the full set is excluded.',17,MUTED)
    array([-15,-9],240,350,160,75,[BLUE,BLUE]);array([-3,3,9],900,350,160,75,[GREEN]*3)
    arrow(400,450,400,530,BLUE);arrow(1140,450,1140,530,GREEN)
    box(160,550,480,100,'{−24, −15, −9}',BLUE,23)
    box(810,550,640,100,'{−3, 0, 3, 6, 9, 12}',GREEN,22)
    text(400,702,'nonempty subset sums',17,BLUE,ha='center');text(1130,702,'nonempty subset sums',17,GREEN,ha='center')
    eq(800,796,r'-9+9=0\quad\checkmark',32)
    text(800,850,'Also accept 0 contained entirely in either half. Empty subsets never count.',17,MUTED,ha='center')
    save(slug)

def exam_masks():
    slug='exam-row-masks'
    page(slug,'Maximum Students','One row becomes one mask. Only the previous row can conflict diagonally.','Blocked seats, horizontal neighbors, and diagonal neighbors are separate checks')
    for x,title,prev,c in [(130,'INVALID: diagonal',[0,1,0,0,0],RED),(875,'VALID: vertical is allowed',[0,0,1,0,0],GREEN)]:
        label(x,220,title,c)
        text(x,280,'previous',14,MUTED);text(x,410,'current',14,MUTED)
        array(prev,x,310,105,65,[c if v else MUTED for v in prev])
        array([1,0,1,0,0],x,440,105,65,[BLUE,MUTED,BLUE,MUTED,MUTED])
        if c==RED:
            arrow(x+155,380,x+50,434,RED);arrow(x+155,380,x+260,434,RED)
        else: line(x+260,382,x+260,433,GREEN,2,'--')
        text(x+260,551,'columns displayed 0 → 4',14,MUTED,ha='center')
    eq(800,653,r'm\ \mathrm{AND}\ (m\ll1)=0\qquad\text{horizontal}',24)
    eq(800,720,r'p\ \mathrm{AND}\ (m\ll1)=0,\quad p\ \mathrm{AND}\ (m\gg1)=0\qquad\text{diagonal}',24)
    eq(800,805,r'D(r,m)=\operatorname{popcount}(m)+\max_{p\ \mathrm{compatible}}D(r-1,p)',23)
    save(slug)

def hats_assignment():
    slug='hats-assignment-mask'
    page(slug,'Assign Hats','Process each hat once. Mask the smaller side: people.','Hat ordering prevents hat reuse; the people mask prevents person reuse')
    text(110,215,'A likes {1, 2}      B likes {1, 3}      C likes {2, 3}',22)
    text(110,267,'Bits: C B A     •     state (h, mask): decide hats h…40',17,MUTED)
    box(445,335,700,100,'(hat 2, mask 001)  →  A already assigned',BLUE,19)
    arrow(650,445,380,590,MUTED,'skip hat 2');arrow(940,445,1200,590,GREEN,'give hat 2 to C')
    box(150,610,450,90,'(hat 3, mask 001)',MUTED,23)
    box(970,610,450,90,'(hat 3, mask 101)',GREEN,23)
    text(800,773,'A: already assigned     ×          B: does not like hat 2     ×',18,RED,ha='center')
    eq(800,835,r'F(h,m)=F(h+1,m)+\sum_{p\ \mathrm{eligible}}F(h+1,m\,|\,2^p)',24)
    save(slug)

def superstring():
    slug='superstring-last-word'
    page(slug,'Shortest Superstring','The same subset can leave a different boundary for the next word.','State = (used words, last word); transition cost = new unmatched suffix')
    text(110,215,'Used subset: {ab, ba}       Next word: ac',23)
    for y,word,last,ov,result,c in [(330,'aba','ba',1,'abac',BLUE),(570,'bab','ab',0,'babac',PURPLE)]:
        array(list(word),150,y,110,75,[c]*3)
        text(315,y+119,f'last = {last}',17,c,ha='center')
        arrow(540,y+38,780,y+38,c,f'overlap = {ov}')
        array(list(result),850,y,105,75,[c]*(len(result)-len('ac')+ov)+[GREEN]*(len('ac')-ov))
        text(1080,y+119,f'length {len(result)}',18,GREEN,ha='center')
    eq(800,809,r'\operatorname{cost}(i,j)=|w_j|-\operatorname{overlap}(w_i,w_j)',26)
    save(slug)

def dungeon():
    slug='dungeon-backward-health'
    page(slug,'Dungeon Game','Store minimum health REQUIRED on entering a cell. Health must stay ≥ 1.','Backward requirements compose cleanly; a single forward health total does not')
    label(160,220,'CELL CONTRIBUTIONS');label(1000,220,'HEALTH REQUIRED')
    grid([[-2,-3,3],[-5,-10,1],[10,30,-5]],160,280,125,105)
    grid([[7,5,2],[6,11,5],[1,1,6]],1000,280,125,105,[[BLUE,BLUE,BLUE],[MUTED,MUTED,BLUE],[MUTED,MUTED,BLUE]])
    arrow(615,430,900,430,BLUE,'solve from the exit',curve=.15)
    eq(800,684,r'H(i,j)=\max\left(1,\min(H(i+1,j),H(i,j+1))-g_{ij}\right)',25)
    eq(800,786,r'H(0,0)=\max(1,\min(5,6)-(-2))=7',26)
    text(800,848,'Exit −5 needs 6 health on entry.   Out-of-grid next cells: +∞.',16,MUTED,ha='center')
    save(slug)

def arithmetic():
    slug='arithmetic-subsequence-seeds'
    page(slug,'Arithmetic Subsequences','Store sequences of length ≥ 2; count only extensions that reach length ≥ 3.','New pair: stored only. Existing sequence + current value: stored AND counted.')
    array([2,4,6,8],160,240,155,80,[BLUE,BLUE,BLUE,ORANGE],True)
    text(965,281,'fixed difference d = 2',22,BLUE)
    label(110,411,'AT 8, EXTEND SEQUENCES ENDING AT 6')
    for y,seq in [(470,'[4, 6] → [4, 6, 8]'),(555,'[2, 4, 6] → [2, 4, 6, 8]')]:text(160,y,seq,24,GREEN)
    box(1050,455,350,125,'answer += 2',GREEN,26)
    text(160,668,'Also seed [6, 8]: length 2 → not yet an answer',21,ORANGE)
    eq(800,764,r'D[i,d]\;+=1+D[j,d],\qquad\mathrm{answer}\;+=D[j,d]',26)
    text(800,840,'For [2,4,6,8]: answer increments 0, 0, 1, 2 → total 3.',17,MUTED,ha='center')
    save(slug)

def regex():
    slug='regex-star-transitions'
    page(slug,'Regex Matching','Treat x* as one pattern unit. State (i, j) matches the remaining suffixes.','Consume a character → stay on x*. Skip x* → advance the pattern by two.')
    text(110,220,'Example: s = aaab, p = a*b',23)
    box(545,300,510,95,'F(i, j)  at pattern a*',BLUE,24)
    arrow(650,405,330,550,ORANGE,'zero a characters');arrow(950,405,1260,550,GREEN,'one more a: firstMatch')
    box(100,570,460,95,'F(i, j + 2)',ORANGE,27)
    box(1030,570,460,95,'F(i + 1, j)',GREEN,27)
    text(330,710,'pattern advances past a*',18,ORANGE,ha='center')
    text(1260,710,'pattern stays on a*',18,GREEN,ha='center')
    eq(800,798,r'F(i,j)=F(i,j+2)\ \vee\ \left(\mathrm{firstMatch}\wedge F(i+1,j)\right)',24)
    text(800,850,'Empty s still matches a*. Stop on pattern exhaustion: accept only if s is exhausted too.',16,MUTED,ha='center')
    save(slug)

def stocks():
    slug='stocks-completed-sales'
    page(slug,'Buy / Sell Stock','Let t count COMPLETED sales. Every action or skip advances the day.','Buy preserves t; sell increments t. At most k completed transactions.')
    nodes=[('cash, t=0',BLUE),('hold, t=0',ORANGE),('cash, t=1',BLUE),('hold, t=1',ORANGE),('cash, t=2',GREEN)]
    for i,(s,c) in enumerate(nodes):box(100+300*i,310,220,100,s,c,20)
    for i in range(4):arrow(330+300*i,360,390+300*i,360,GREEN if i%2 else ORANGE)
    for i,s in enumerate(['buy −p','sell +p','buy −p','sell +p']):text(360+300*i,265,s,18,GREEN if i%2 else ORANGE,ha='center')
    for i,name in enumerate(['start','buy1','sell1','buy2','sell2']):text(210+300*i,480,name,22,MUTED,ha='center')
    bracket(400,1520,540,'k = 2: the four compressed values',BLUE)
    eq(800,696,r'\operatorname{buy}: (t,\mathrm{cash})\to(t,\mathrm{hold})\quad\text{only if }t<k',24)
    eq(800,786,r'\operatorname{sell}: (t,\mathrm{hold})\to(t+1,\mathrm{cash})',24)
    text(800,846,'Skip: keep the same holding / transaction state, move to day + 1.',17,MUTED,ha='center')
    save(slug)

def constrained():
    slug='constrained-sum-deque'
    page(slug,'Constrained Subsequence Sum','The best predecessor must end inside [i − k, i − 1].','Deque front = best valid predecessor. Expire old indices; discard dominated tails.')
    text(110,219,'nums = [10, 2, −10, 5, 20]     k = 2     current i = 3',22)
    array([10,12,2,17,37],240,295,175,85,[RED,BLUE,BLUE,GREEN,MUTED],True)
    text(125,337,'dp',23)
    bracket(415,759,420,'eligible predecessor window',BLUE)
    text(320,488,'expired',17,RED,ha='center')
    eq(800,569,r'D[3]=5+\max(0,12,2)=17',28)
    text(160,690,'before insert: deque [1:12, 2:2]',20,BLUE)
    arrow(820,690,1000,690,GREEN,'17 dominates both')
    box(1070,640,300,100,'[3:17]',GREEN,25)
    eq(800,825,r'D[i]=a_i+\max\left(0,\max_{j\in[i-k,i-1]}D[j]\right)',26)
    save(slug)

def repetitions():
    slug='repetitions-block-transition'
    page(slug,'Count the Repetitions','Cache one entire source block as a transition on the target cursor.','State = target cursor j. Repeated state → repeated future behavior.')
    text(110,220,'s₁ = abab     s₂ = aaab     n₁ = 7     n₂ = 2',25)
    coords=[(270,410),(800,410),(1330,410)]
    for (x,y),s in zip(coords,['j = 0','j = 2','j = 1']):box(x-110,y-55,220,110,s,BLUE,28)
    arrow(390,410,675,410,GREEN,'abab → +0 copies')
    arrow(920,410,1205,410,GREEN,'abab → +1 copy')
    arrow(1310,485,290,485,GREEN,curve=-.35)
    text(800,625,'abab → +1 copy',18,GREEN,ha='center')
    text(800,709,'3 source blocks → 2 complete copies of aaab',24,BLUE,ha='center')
    eq(800,796,r'7=2\cdot3+1\quad\Rightarrow\quad\mathrm{copies}=2\cdot2+0=4',26)
    eq(800,849,r'\mathrm{answer}=\left\lfloor4/2\right\rfloor=2',23)
    save(slug)

def encode_choices():
    slug='encode-string-choices'
    page(slug,'Shortest Encoding · 1','Every interval chooses: leave raw, concatenate, or repeat an encoded period.','For repetition, encode the period recursively before wrapping it in k[…].')
    text(800,230,'aaaaabaaaaab',34,ha='center',weight='bold')
    for x,s,c in [(280,'raw',MUTED),(800,'split',BLUE),(1320,'repeat',GREEN)]:
        arrow(800,280,x,365,c);text(x,410,s,25,c,ha='center',weight='bold')
    text(280,492,'12 characters',20,MUTED,ha='center')
    text(800,492,'F(l, k) + F(k+1, r)',20,BLUE,ha='center')
    text(1320,492,'2 × aaaaab',22,GREEN,ha='center')
    array(['aaaaa','b'],390,610,280,85,[ORANGE,BLUE])
    arrow(950,655,1100,655,GREEN)
    box(1140,605,310,100,'2[5[a]b]',GREEN,30)
    text(670,746,'period: aaaaab → 5[a]b',22,ORANGE,ha='center')
    text(1290,746,'8 characters',20,GREEN,ha='center')
    text(800,838,'Compare encoded lengths, not just the number of blocks.',20,MUTED,ha='center')
    save(slug)

def encode_period():
    slug='encode-string-period'
    page(slug,'Shortest Encoding · 2','A repeated interval must tile exactly AND match its shifted copy.','Both tests matter: length % period = 0 and LCP ≥ length − period')
    text(110,221,'s = abababab     length = 8     candidate period p = 2',23)
    array(list('abababab'),230,300,135,70,[BLUE]*8)
    array(list('ababab'),230,435,135,70,[GREEN]*6)
    text(110,335,'s[0:]',16,MUTED);text(110,470,'s[2:]',16,MUTED)
    bracket(230,1034,548,'LCP(0, 2) = 6 = 8 − 2',GREEN)
    eq(800,690,r'8\mathrm{mod}2=0\quad\wedge\quad6\geq8-2\quad\Rightarrow\quad4[ab]',28)
    box(210,772,1180,80,'abababa: shifted prefix matches, but 7 % 2 ≠ 0 → NOT an exact repetition',RED,18)
    save(slug)

def parentheses():
    slug='parentheses-boundary-stack'
    page(slug,'Longest Valid Parentheses','The stack stores an uncrossable boundary, then unmatched opening brackets.','After a successful pop: valid suffix length = i − stack[-1]')
    text(110,220,'s = )()())',26)
    array(list(')()())'),260,300,165,85,[RED,BLUE,BLUE,BLUE,BLUE,RED],True)
    bracket(425,1079,437,'at i = 4: longest valid suffix ()()',BLUE)
    box(180,590,410,95,'stack = [0]',BLUE,27)
    arrow(660,637,920,637,BLUE,'i − boundary = 4 − 0')
    box(1000,590,380,95,'length = 4',GREEN,28)
    text(800,764,'i = 5: pop empties stack → reset boundary to 5',22,RED,ha='center')
    text(800,835,'An unmatched closing bracket cannot be crossed by a valid substring.',18,MUTED,ha='center')
    save(slug)

def lis_range():
    slug='lis-ii-value-range'
    page(slug,'LIS II','A smaller tail can be too far away. Keep the best length for EACH ending value.','For x, query [x − k, x − 1], add 1, then update value x')
    text(110,220,'[4, 1, 5], k = 2: tails cannot simply replace 4 with 1',23)
    box(170,310,250,85,'tail 1',RED,25);box(700,310,250,85,'tail 4',BLUE,25);box(1230,310,200,85,'next 5',GREEN,25)
    arrow(430,354,1210,354,RED,curve=-.25)
    text(720,285,'5 − 1 = 4 > k',16,RED,ha='center')
    arrow(960,354,1210,354,GREEN,'5 − 4 = 1 ≤ k')
    label(110,532,'VALUE AXIS, NOT INDEX AXIS')
    array([1,2,3,4,5,6],300,600,160,80,[MUTED,MUTED,BLUE,BLUE,GREEN,MUTED])
    bracket(620,934,726,'query [3, 4]',BLUE)
    eq(800,825,r'D[5]=1+\max(D[3],D[4])=2',27)
    save(slug)

def three_windows():
    slug='three-subarrays-middle'
    page(slug,'Three Non-overlapping Subarrays','Fix the middle start m. The left and right optima become independent.','Left starts ≤ m − k; right starts ≥ m + k. Preserve earliest starts on ties.')
    text(110,219,'k = 2, m = 3',23)
    array([1,2,1,2,6,7,5,1],155,300,160,85,[BLUE,BLUE,MUTED,ORANGE,ORANGE,GREEN,GREEN,MUTED],True)
    bracket(155,469,435,'left: start 0, sum 3',BLUE)
    bracket(635,949,435,'middle: start 3, sum 8',ORANGE)
    bracket(955,1269,435,'right: start 5, sum 12',GREEN)
    text(110,606,'Window sums',19,MUTED)
    array([3,3,3,8,13,12,6],300,575,140,75,[BLUE,BLUE,MUTED,ORANGE,RED,GREEN,GREEN],True)
    text(930,719,'13 is larger, but overlaps the middle',18,RED,ha='center')
    eq(800,795,r'\mathrm{bestLeft}[m-k]+\mathrm{window}[m]+\mathrm{bestRight}[m+k]',23)
    text(800,850,'3 + 8 + 12 = 23     →     starts [0, 3, 5]',22,BLUE,ha='center')
    save(slug)

def min_swaps():
    slug='min-swaps-two-states'
    page(slug,'Minimum Swaps','Only the previous column’s orientation matters. Choose the current orientation now.','State = (position, previous swapped?). Each legal swap costs +1.')
    text(110,219,'Previous column: (5, 3)       Current column: (4, 7)',23)
    for x,name,cur,c in [(170,'KEEP → invalid',[4,7],RED),(940,'SWAP → valid',[7,4],GREEN)]:
        label(x,303,name,c)
        for y,a,b in [(400,5,cur[0]),(555,3,cur[1])]:
            box(x,y,130,75,str(a),BLUE,25);box(x+360,y,130,75,str(b),c,25)
            arrow(x+145,y+38,x+345,y+38,c,f'{b} > {a}: {"yes" if b>a else "no"}')
    eq(800,738,r'\mathrm{keep}:\ a_i>a_{i-1}\ \wedge\ b_i>b_{i-1}',24)
    eq(800,810,r'\mathrm{swap}:\ b_i>a_{i-1}\ \wedge\ a_i>b_{i-1}',24)
    save(slug)

def refuel_dp():
    slug='refuel-reach-dp'
    page(slug,'Refuelling · Reach DP','Invert the state: maximum distance reachable with j stops.','Take a station only if it is reachable; update stop counts right → left')
    text(110,220,'target = 100, start = 10     stations: (10,60), (20,30), (30,30), (60,40)',20)
    road(340)
    box(150,505,420,95,'dp[1] = 70',BLUE,29)
    arrow(600,552,960,552,GREEN,'station 60 is reachable')
    box(1010,505,430,95,'dp[2] = 70 + 40 = 110',GREEN,23)
    eq(800,715,r'\mathrm{if}\ D[j]\geq\mathrm{pos}:\quad D[j+1]\leftarrow\max(D[j+1],D[j]+\mathrm{fuel})',23)
    text(800,811,'Answer: smallest j with dp[j] ≥ target → 2 stops',24,BLUE,ha='center')
    save(slug)

def road(y):
    line(160,y,1450,y,MUTED,3)
    for pos,fuel in [(0,None),(10,60),(20,30),(30,30),(60,40),(100,None)]:
        x=160+pos*12.5
        ax.add_patch(Circle((x,y),6,color=BLUE))
        text(x,y+42,str(pos),17,ha='center')
        if fuel is not None:text(x,y-49,f'+{fuel}',18,GREEN,ha='center')

def refuel_heap():
    slug='refuel-retrospective-heap'
    page(slug,'Refuelling · Greedy Heap','Delay the choice. When fuel is insufficient, select the largest passed station.','The heap is a menu of reachable, unused refuelling opportunities')
    road(285)
    for y,reach,heap,pick,new in [(465,10,'[60]',60,70),(665,70,'[40, 30, 30]',40,110)]:
        text(120,y,f'reach {reach}',25,BLUE)
        box(450,y-45,430,90,heap,ORANGE,25)
        arrow(920,y,1120,y,GREEN,f'take +{pick}')
        text(1200,y,f'reach {new}',25,GREEN)
    text(800,810,'2 selected stations: position 10, then position 60',24,BLUE,ha='center')
    save(slug)

def digit_one():
    slug='digit-one-ways-and-ones'
    page(slug,'Count Digit One','Return (number of completions, total ones across those completions).','Choosing digit 1 adds one occurrence for EVERY suffix completion')
    box(605,220,390,85,'bound n = 13',BLUE,25)
    arrow(690,320,400,420,MUTED,'first digit 0');arrow(910,320,1200,420,GREEN,'first digit 1')
    box(150,445,500,110,'suffix 0…9: (ways=10, ones=1)',MUTED,19)
    box(950,445,500,110,'suffix 0…3: (ways=4, ones=1)',GREEN,19)
    text(400,623,'contribution: 1 + 0×10 = 1',21,MUTED,ha='center')
    text(1200,623,'contribution: 1 + 1×4 = 5',21,GREEN,ha='center')
    eq(800,731,r'\mathrm{totalOnes}\;+=\mathrm{suffixOnes}+[d=1]\cdot\mathrm{suffixWays}',25)
    text(800,826,'1 + 5 = 6     •     1, 10, 11, 12, 13 contain six ones',23,BLUE,ha='center')
    save(slug)

def digit_set():
    slug='digit-set-leading-padding'
    page(slug,'Numbers from a Digit Set','Leading zero means “not started yet”; it is NOT a digit chosen from the set.','Track (position, tight, leading). Reject the all-padding path.')
    text(110,219,'digits = {1, 3, 5}     bound = 35',25)
    box(580,290,440,85,'first position: tight, leading',BLUE,22)
    for x,name,c in [(300,'skip / padding 0',MUTED),(800,'choose 1',GREEN),(1300,'choose 3',ORANGE)]:
        arrow(800,395,x,480,c);box(x-210,505,420,80,name,c,21)
    for x,s,c in [(300,'loose, still leading\n1, 3, 5 → 3 numbers',MUTED),(800,'loose, started\n11, 13, 15 → 3 numbers',GREEN),(1300,'tight, started\n31, 33, 35 → 3 numbers',ORANGE)]:
        text(x,678,s,18,c,ha='center')
    text(800,822,'3 + 3 + 3 = 9     •     00 is not a number in the answer',24,BLUE,ha='center')
    save(slug)

def schemes():
    slug='profitable-schemes-saturation'
    page(slug,'Profitable Schemes','Once the profit threshold is reached, its exact excess no longer affects the future.','Merge equivalent profit states, but ADD their numbers of schemes')
    text(110,220,'Minimum profit P = 3',25)
    array([0,1,2,'3+'],350,300,220,95,[MUTED,MUTED,BLUE,GREEN])
    arrow(880,415,1110,415,GREEN,'2 + profit 3 → bucket 3+')
    label(110,525,'SAME PROCESSED PREFIX AND SAME MEMBER COUNT')
    box(170,595,410,90,'profit 4: count 1',BLUE,23)
    box(170,725,410,90,'profit 6: count 1',PURPLE,23)
    arrow(610,640,1000,695,GREEN);arrow(610,770,1000,695,GREEN)
    box(1050,645,370,100,'profit 3+: count 2',GREEN,24)
    eq(800,848,r"p'=\min(P,p+\mathrm{gain}),\qquad w'=w+\mathrm{members}\leq W",23)
    save(slug)

def scramble():
    slug='scramble-aligned-swapped'
    page(slug,'Scramble String','At each split: preserve the child order OR exchange it.','Equal lengths let the state be just (start₁, start₂, length)')
    label(110,215,'ONE SPLIT: A HAS LENGTH k, B HAS LENGTH L − k')
    array(['A','B'],570,270,230,90,[BLUE,GREEN])
    arrow(620,390,380,485,BLUE,'aligned');arrow(940,390,1220,485,GREEN,'swapped')
    array(['A′','B′'],150,520,230,90,[BLUE,GREEN]);array(['B′','A′'],1000,520,230,90,[GREEN,BLUE])
    text(380,670,'A ↔ A′    and    B ↔ B′',21,BLUE,ha='center')
    text(1230,670,'A ↔ right k    B ↔ left L−k',20,GREEN,ha='center')
    eq(800,756,r'F(i,j,L)=\bigvee_{k=1}^{L-1}\left[(\mathrm{aligned})\vee(\mathrm{swapped})\right]',24)
    text(800,831,'great → gr | eat → rg | eat → rgeat',23,ORANGE,ha='center')
    save(slug)

def visit_all():
    slug='visit-all-state-graph'
    page(slug,'Shortest Path Visiting All Nodes','BFS on (current node, visited mask), not just the original node.','Revisiting node 0 can be useful. Revisiting the SAME (node, mask) is redundant.')
    points={0:(400,390),1:(180,600),2:(620,600),3:(400,215)}
    for j in [1,2,3]:line(*points[0],*points[j],BLUE,2)
    for n,(x,y) in points.items():
        ax.add_patch(Circle((x,y),40,facecolor=PALE[BLUE],edgecolor=BLUE,lw=2));text(x,y,str(n),24,BLUE,ha='center')
    text(1030,255,'Start BFS from every singleton state.',20,MUTED,ha='center')
    for k,(node,mask) in enumerate([(1,'0010'),(0,'0011'),(2,'0111'),(0,'0111'),(3,'1111')]):
        y=355+k*95
        box(865,y,330,66,f'({node}, {mask})',GREEN if k==4 else BLUE,21)
        if k<4:arrow(1030,y+68,1030,y+91,BLUE)
    text(400,743,'Path: 1 → 0 → 2 → 0 → 3',22,BLUE,ha='center')
    text(400,810,'4 edges; node 0 appears twice',19,MUTED,ha='center')
    save(slug)

def stickers():
    slug='stickers-target-mask'
    page(slug,'Stickers to Spell Word','Mask positions in the short TARGET. Equal letters still occupy separate positions.','Apply one sticker’s character counts; recurse only if coverage increases')
    text(110,220,'target = aabb     sticker = ab     bits indexed 0 → 3',23)
    for y,cols,mask in [(310,[MUTED]*4,'0000'),(500,[GREEN,MUTED,GREEN,MUTED],'0101'),(690,[GREEN]*4,'1111')]:
        array(list('aabb'),330,y,150,75,cols,True)
        text(1120,y+38,f'mask {mask}',24,GREEN if mask=='1111' else BLUE)
    arrow(1000,395,1000,480,BLUE,'use ab');arrow(1000,585,1000,670,BLUE,'use ab again')
    text(800,837,'Two a positions require two a characters. Minimum: 2 stickers.',22,BLUE,ha='center')
    save(slug)

def zuma_cascade():
    slug='zuma-cascade'
    page(slug,'Zuma · Chain Reaction','Insert one ball, then repeatedly remove every newly formed run of length ≥ 3.','Memoize the settled board AND remaining hand counts')
    for y,s,note in [(260,'RRBBRR','board; hand = {B: 1}'),(410,'RRBBBRR','insert B → remove BBB'),(560,'RRRR','new adjacency → remove RRRR')]:
        balls(s,210,y,85);text(950,y,note,22)
    arrow(460,305,460,360,BLUE);arrow(460,455,460,510,BLUE);arrow(460,605,460,660,RED)
    box(280,690,360,90,'empty board',GREEN,29)
    text(1030,735,'1 insertion',29,GREEN,ha='center')
    save(slug)

def zuma_delay():
    slug='zuma-delay-collapse'
    page(slug,'Zuma · Delay the Collapse','Sometimes insert a DIFFERENT color inside a pair to preserve a future chain reaction.','Pruning to “always grow a matching run” loses valid solutions')
    label(100,204,'BOARD RRWWRRBBRR    HAND WB')
    rows=[(278,'RRWWRRBBRWR','1  insert W inside the last RR'),(400,'RRWWRRBBBRWR','2  insert B into BB'),(522,'RRWWRRRWR','remove BBB'),(644,'RRWWWR','remove RRR'),(766,'RRR','remove WWW → remove RRR → empty')]
    for y,s,note in rows:
        balls(s,125,y,60);text(920,y,note,17,GREEN if y==766 else INK)
    text(800,851,'Greedy W into WW instead: RRWWWRRBBRR → BBRR → RR (stuck).',17,RED,ha='center')
    save(slug)

RENDERERS = [burst_balloons,strange_printer,tallest_billboard,di_ranks,inversions_insert,inversions_window,
    average_transform,average_mitm,exam_masks,hats_assignment,superstring,dungeon,arithmetic,regex,
    stocks,constrained,repetitions,encode_choices,encode_period,parentheses,lis_range,three_windows,
    min_swaps,refuel_dp,refuel_heap,digit_one,digit_set,schemes,scramble,visit_all,stickers,zuma_cascade,zuma_delay]

if __name__=='__main__':
    # Numeric anchors used by multiple explanations.
    assert sum(str(i).count('1') for i in range(14))==6
    assert sum(6*x-21 for x in [1,6])==0
    assert [sum([1,2,1,2,6,7,5,1][i:i+2]) for i in range(7)]==[3,3,3,8,13,12,6]
    selected=set(sys.argv[1:])
    for render in RENDERERS:
        if not selected or render.__name__ in selected:
            render()
            print(render.__name__)
