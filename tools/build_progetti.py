# Genera le pagine progetto partendo da index.html: stesso <head> (CSS), stesso header, menu, reel,
# footer con le pillole e "pagina successiva". Cambia solo il <main> e lo script, ridotto alle parti comuni.
# Uso: python tools/build_progetti.py   (da rilanciare quando cambiano header, menu o footer della home)
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / 'index.html').read_text(encoding='utf8')

PROJECTS = [
    dict(
        slug='marinobus', name='MarinoBus',
        lede="Dal 1957 nel trasporto su gomma tra Puglia e Basilicata, oggi realtà di riferimento nazionale. Per i sessant'anni dell'azienda abbiamo ridisegnato il marchio e raccontato la sua storia.",
        # colonne sotto il titolo: etichetta e voci una per riga (html ammesso)
        spec=[('Servizi', ['Branding', 'Video', 'Website', 'Social', 'Events']), ('Settore', ['Trasporti']),
              ('Sito', ['<a href="https://www.marinobus.it" target="_blank" rel="noopener">marinobus.it</a>'])],
        hero=('never_before_italia_storytelling_marinobus.jpg', 'Storytelling MarinoBus', '1100/620', 'Video'),  # ultimo: servizio, per la barra dei servizi
        big="Attiva da 60 anni nel settore del trasporto su gomma, la società MarinoBus si attesta oggi come realtà di riferimento a livello nazionale.",
        story=["La MarinoBus nasce nel 1957 ad Irsina (Matera) da un'intuizione del fondatore Michele Marino, allo scopo di assolvere alle esigenze di trasporto nel territorio lucano e pugliese, oltre che al noleggio da rimessa di autobus e auto.",
               "Successivamente la famiglia si trasferisce ad Altamura, posizione strategica del territorio dell'Alta Murgia pugliese, dove attualmente ha la sua sede operativa, legale e gestionale.",
               "Oggi la gestione della MarinoBus continua con il figlio Gerardo e sua moglie Loredana, che hanno ampiamente esteso l'attività nelle principali città lucane e pugliesi non trascurando le grandi località del centro e nord Italia e dell'estero. Nei suoi 60 anni di storia, l'azienda è cresciuta costantemente nei servizi, nella qualità e nelle risorse umane."],
        # blocchi della galleria: ('wide', file, alt, ratio, didascalia, servizio) | ('trio', titolo, servizio, [(file, alt)]) | ('pair', titolo, ratio, [(file, alt, didascalia, servizio)])
        gallery=[
            ('wide', 'never_before_italia_branding_marinobus_restyling_logo.jpg', 'Restyling del marchio MarinoBus', '1100/620', 'Restyling del marchio', 'Branding'),
            ('trio', 'Nuova livrea', 'Branding', [('never_before_italia_nuova_livrea_marinobus.jpg', 'Bozzetto a matita della nuova livrea MarinoBus'),
                                     ('never_before_italia_nuova_livrea_marinobus_2.jpg', 'Nuova livrea MarinoBus'),
                                     ('never_before_italia_nuova_livrea_marinobus_3.jpg', 'Nuova livrea MarinoBus')]),
            ('wide', 'never_before_italia_website_marinobus.jpg', 'Il sito marinobus.it su computer, tablet e telefono', '1100/750', 'marinobus.it', 'Website'),
            ('pair', 'Eventi', '1100/750', [('never_before_italia_events_marinobus_carnevale_putignano.jpg', 'Promoter MarinoBus al Carnevale di Putignano', 'Carnevale di Putignano', 'Events'),
                                            ('never_before_italia_events_marinobus_terrone_fuori_sede.jpg', 'Evento Terrone fuori sede con MarinoBus', 'Terrone fuori sede', 'Events')]),
        ],
        # facoltativo: il percorso che si disegna accanto alla storia (tappe vere del racconto) e il contatore
        route=dict(n=60, unit='anni', since='dal 1957', stops=['Irsina (MT), 1957', 'Altamura', 'Puglia e Basilicata', 'Centro e Nord Italia', 'Estero']),
        # pagina successiva: parola, pillola con foto, parola (come "Chi ⬭ siamo" della home)
        next=('Altri', 'progetti', 'progetti.html', 'assets/img/never_before_italia_website_amaro_mediterraneo.jpg'),
    ),
]

ABOUT_CSS = r'''
/* chi siamo: la foto della pillola "Chi ⬭ siamo" della home, a 10px dai bordi con raggio 22, diventa il fondo della hero */
.ab-hero{position:relative;height:100svh;color:#fff}
.ab-bg{position:absolute;inset:10px;border-radius:22px;overflow:hidden;background:var(--dark);view-transition-name:next-hero}
.ab-bg img{display:block;width:100%;height:100%;object-fit:cover}
.ab-bg::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(5,5,5,.55),rgba(5,5,5,0) 60%)} /* scuro neutro in basso: il titolo bianco si legge */
.ab-txt{position:absolute;left:calc(10px + var(--pad));right:calc(10px + var(--pad));bottom:calc(10px + var(--pad))}
.ab-txt .pj-ttl{font-size:clamp(64px,13vw,240px);line-height:.9}
.ab-txt p{margin-top:16px;font-size:17px}
.nextp-pill{view-transition-name:none} /* un solo elemento per nome nella pagina */
'''

CSS = r'''
/* pagina progetto: struttura da 311labs (titolo enorme, scheda a filetti, media a tutta larghezza, coppie e terne), grammatica della home */
.pj-head{padding:calc(var(--nav-h) + clamp(60px,12vh,140px)) var(--pad) clamp(48px,7vw,96px)}
.pj-ttl{font-size:clamp(72px,15vw,280px);margin-left:-.04em}
.pj-ttl .wd{display:inline-block;white-space:nowrap}
.pj-ttl .ch{display:inline-block;opacity:0}
.shown .pj-ttl .ch{opacity:1;animation:pjUp 1.1s var(--energy) calc(.1s + var(--i)*45ms) both}
@keyframes pjUp{from{opacity:0;transform:translateY(.5em) rotate(6deg)}}
.wf .pj-ttl{visibility:hidden}.wf .pj-ttl *{animation-play-state:paused}
.pj-meta{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));column-gap:var(--gap,16px);margin-top:clamp(40px,6vw,80px);padding-top:16px;border-top:1px solid var(--ink);font-size:clamp(17px,1.3vw,20px);line-height:1.3}
.pj-col h2{font:inherit;letter-spacing:inherit;margin-bottom:1.2em}
.pj-col a{color:inherit;text-underline-offset:4px}
/* testo a destra: rientro sulla prima riga, sotto un filetto e il rimando al racconto */
.pj-lede{grid-column:5/7}
.pj-lede p{text-indent:4em}
.pj-lede a{display:flex;justify-content:space-between;margin-top:clamp(28px,3vw,48px);padding-top:14px;border-top:1px solid var(--ink);color:inherit;text-decoration:none}
.pj-lede a span:last-child{transition:transform .4s var(--energy)}.pj-lede a:hover span:last-child{transform:translateX(4px)}
.pj-m{border-radius:var(--radius-media);overflow:hidden;background:var(--surface)}
.pj-m img{display:block;width:100%;height:100%;object-fit:cover}
.pj figure{margin:0}
.pj figcaption{display:flex;justify-content:space-between;gap:16px;padding-top:12px;font-size:15px;color:var(--ink-2)}
.pj-full,.pj-wide,.pj-pair,.pj-trio,.pj-bh{padding-left:var(--pad);padding-right:var(--pad)}
/* il primo media si apre allo scroll: parte stretto e arriva a tutta larghezza */
.pj-full .pj-m{clip-path:inset(0 calc(var(--k,1)*12%) round var(--radius-media))}
.pj-full .pj-m img{scale:calc(1 + var(--k,1)*.12)}
.pj-story{display:grid;grid-template-columns:1fr 1fr;gap:40px;padding:clamp(80px,12vw,180px) var(--pad)}
.pj-story h2{font:400 15px var(--sans);letter-spacing:-.02em;color:var(--ink-2)}
.pj-big{font-family:var(--display);font-weight:var(--display-w);font-size:clamp(30px,3.4vw,54px);letter-spacing:-.057em;line-height:1.1;margin-bottom:32px}
.pj-story p+p{margin-top:16px}
.pj-story p:not(.pj-big){color:var(--ink-2);max-width:56ch}
.pj-blk{margin-top:clamp(64px,9vw,140px)}
.pj-bh{padding-bottom:24px}.pj-bh h3{font-size:clamp(40px,5vw,84px)}
.pj-pair{display:grid;grid-template-columns:1fr 1fr;gap:clamp(10px,1.2vw,16px)}
.pj-trio{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(10px,1.2vw,16px)}
.pj-trio .pj-m{aspect-ratio:1}
.pj .rv{transform:translateY(60px)}.pj .rv.in{transform:none}
.pj-pair .rv:nth-child(2),.pj-trio .rv:nth-child(2){transition-delay:.08s}.pj-trio .rv:nth-child(3){transition-delay:.16s}
.pj-end{height:clamp(100px,14vw,200px)}
/* storia: a sinistra il percorso che si disegna mentre leggi, con le tappe che si accendono e il contatore degli anni */
.pj-side{position:sticky;top:calc(var(--nav-h) + 24px);align-self:start}
.pj-route{margin-top:28px}
.pj-cnt small{display:block;font-size:15px;color:var(--ink-2)}
.pj-cnt span{font-family:var(--display);font-size:clamp(48px,5vw,88px);letter-spacing:-.06em;line-height:1}
.pj-cnt b{font-weight:inherit;font-variant-numeric:tabular-nums}
.pj-map{position:relative;width:min(100%,190px);margin:24px 0 0 40px}
.pj-map svg{display:block;width:100%;overflow:visible}
.pj-map path{fill:none;stroke-linecap:round}
.pj-map .bg{stroke:var(--line);stroke-width:3;stroke-dasharray:2 10}
.pj-map .ln{stroke:var(--ink);stroke-width:5;stroke-dasharray:1;stroke-dashoffset:1}
.pj-stop{position:absolute;left:0;top:0;display:flex;align-items:center;gap:10px;white-space:nowrap;transform:translate(-8px,-50%)}
.pj-stop.l{flex-direction:row-reverse;transform:translate(calc(-100% + 8px),-50%)}
.pj-stop i{width:16px;height:16px;flex:none;border-radius:50%;background:var(--bg);border:2px solid var(--line);transition:background .4s,border-color .4s,scale .5s var(--energy)}
.pj-stop b{font-weight:400;font-size:15px;padding:6px 12px;border-radius:99px;color:var(--ink-2);transition:background .5s,color .5s}
.pj-stop.on i{background:var(--ink);border-color:var(--ink);scale:1.15}
.pj-stop.on b{background:var(--c);color:var(--ink)}
/* barra dei servizi: un indice della galleria. Si accende il servizio del lavoro a schermo, cliccando si va al primo lavoro di quel servizio */
.pj-svc{position:fixed;left:50%;bottom:calc(var(--safe-b) - 8px);z-index:40;display:flex;gap:2px;padding:5px;border-radius:99px;background:var(--dark);box-shadow:0 8px 28px rgba(0,0,0,.18);opacity:0;visibility:hidden;transform:translate(-50%,24px);transition:opacity .4s,visibility .4s,transform .6s var(--energy)}
.pj-svc.on{opacity:1;visibility:visible;transform:translate(-50%,0)}
.pj-svc button{border:0;background:none;font:400 15px var(--sans);letter-spacing:-.02em;padding:9px 16px;border-radius:99px;color:var(--on-dark-2);white-space:nowrap;cursor:pointer;transition:background .45s,color .45s}
.pj-svc button:hover{color:var(--on-dark)}
.pj-svc button.on{background:var(--c);color:var(--ink)}
.pj-svc button:disabled{color:#5C5C5C;cursor:default} /* servizio senza immagini in galleria */
@media (max-width:820px){
  .pj-story,.pj-pair{grid-template-columns:1fr}
  .pj-side{position:static}.pj-map{width:min(55%,200px);margin-left:22%}
  .pj-svc button{font-size:12.5px;padding:7px 10px}.pj-svc{max-width:calc(100vw - 24px)}
  .pj-meta{grid-template-columns:repeat(3,minmax(0,1fr));row-gap:40px}.pj-lede{grid-column:1/-1}
  .pj-story{gap:16px}
  .pj-trio{grid-template-columns:1fr 1fr}.pj-trio .rv:nth-child(3){grid-column:1/-1;aspect-ratio:2/1}
}
@media (prefers-reduced-motion:reduce){.pj-full .pj-m{clip-path:inset(0 round var(--radius-media))}.pj-full .pj-m img{scale:1}}
'''

esc = html.escape


PASTEL = ['#E2DBFF', '#FFDCCB', '#FFF3B8', '#D7FFE0', '#CDEBFF']  # i pastelli pieni delle pillole della home
ROUTE = 'M40,20 C40,110 200,110 200,200 C200,290 40,290 40,380 C40,470 200,470 200,540'


def route_html(p):
    r = p.get('route')
    if not r:
        return ''
    stops = ''.join(f'<span class="pj-stop" style="--c:{PASTEL[i % len(PASTEL)]}"><i></i><b>{esc(s)}</b></span>' for i, s in enumerate(r['stops']))
    return (f'<div class="pj-route" id="pjRoute" data-n="{r["n"]}"><p class="pj-cnt"><small>{esc(r["since"])}</small><span><b id="pjN">0</b> {esc(r["unit"])}</span></p>'
            f'<div class="pj-map"><svg viewBox="0 0 240 560" aria-hidden="true"><path class="bg" d="{ROUTE}"/><path class="ln" id="pjRouteP" pathLength="1" d="{ROUTE}"/></svg>{stops}</div></div>')


def img(slug, f):
    return f'assets/img/{slug}/{f}'


def main_html(p):
    s = p['slug']
    spec = ''.join(f'<div class="pj-col"><h2>{k}</h2>{"<br>".join(v)}</div>' for k, v in p['spec'])
    out = [f'''<main id="top" class="pj">
  <section class="pj-head">
    <h1 class="pj-ttl" id="pjTtl" aria-label="{esc(p['name'])}">{esc(p['name'])}</h1>
    <div class="pj-meta">{spec}<div class="pj-lede"><p>{esc(p['lede'])}</p><a href="#pj-storia"><span>Leggi la storia</span><span aria-hidden="true">→</span></a></div></div>
  </section>
  <section class="pj-full"><figure class="pj-m" id="pjHero" data-svc="{p['hero'][3]}" style="aspect-ratio:{p['hero'][2]}"><img src="{img(s, p['hero'][0])}" alt="{esc(p['hero'][1])}"></figure></section>
  <section class="pj-story" id="pj-storia"><div class="pj-side"><h2>La storia</h2>{route_html(p)}</div><div><p class="pj-big">{esc(p['big'])}</p>{''.join(f'<p>{esc(t)}</p>' for t in p['story'])}</div></section>''']
    for i, g in enumerate(p['gallery']):
        blk = ' pj-blk' if i else ''
        if g[0] == 'wide':
            _, f, alt, ratio, cap, svc = g
            out.append(f'  <section class="pj-wide{blk}"><figure class="rv" data-svc="{svc}"><div class="pj-m" style="aspect-ratio:{ratio}"><img src="{img(s, f)}" alt="{esc(alt)}" loading="lazy"></div><figcaption><span>{esc(cap)}</span><span>{esc(svc)}</span></figcaption></figure></section>')
        elif g[0] == 'trio':
            _, t, svc, items = g
            figs = ''.join(f'<figure class="rv pj-m" data-svc="{svc}"><img src="{img(s, f)}" alt="{esc(a)}" loading="lazy"></figure>' for f, a in items)
            out.append(f'  <section class="pj-blk"><div class="pj-bh"><h3>{esc(t)}</h3></div><div class="pj-trio">{figs}</div></section>')
        elif g[0] == 'pair':
            _, t, ratio, items = g
            figs = ''.join(f'<figure class="rv" data-svc="{v}"><div class="pj-m" style="aspect-ratio:{ratio}"><img src="{img(s, f)}" alt="{esc(a)}" loading="lazy"></div><figcaption><span>{esc(c)}</span><span>{esc(v)}</span></figcaption></figure>' for f, a, c, v in items)
            out.append(f'  <section class="pj-blk"><div class="pj-bh"><h3>{esc(t)}</h3></div><div class="pj-pair">{figs}</div></section>')
    # barra dei servizi: le voci della colonna Servizi; si accende quella del lavoro che stai guardando
    svcs = dict(p['spec']).get('Servizi', [])
    have = {g[-1] for g in p['gallery'] if g[0] == 'wide'} | {g[2] for g in p['gallery'] if g[0] == 'trio'} | {it[3] for g in p['gallery'] if g[0] == 'pair' for it in g[3]} | {p['hero'][3]}
    pills = ''.join(f'<button type="button" data-s="{esc(v)}" style="--c:{PASTEL[i % len(PASTEL)]}"{"" if v in have else " disabled"}>{esc(v)}</button>' for i, v in enumerate(svcs))
    out.append('  <div class="pj-end"></div>\n</main>')
    out.append(f'<nav class="pj-svc" id="pjSvc" aria-label="Lavori per servizio">{pills}</nav>')
    return '\n'.join(out)


def between(s, a, b, inc_b=False):
    i = s.index(a)
    j = s.index(b, i)
    return s[i:j + (len(b) if inc_b else 0)]


def local(s):
    # i link alle sezioni della home ripartono dalla home
    return re.sub(r'(<a\b[^>]*?\shref=")#(?=[^"])', r'\1index.html#', s)  # solo i link, non <use href="#logo">


def script():
    nextp = between(SRC, '  // la pagina dopo si prepara in anticipo', "e.viewTransition.types.add('expand')});", inc_b=True)
    js = between(SRC, '<script>\nconst $=', '</script>')[len('<script>\n'):]
    head = js[:js.index('// intro della hero')].replace("$('heroPlay').onclick=openReel;", '')
    shut = between(js, '// shutter: 12 lamelle per confine', '// titoli riga per riga')
    roll = between(js, '// lettere che scorrono in hover', '// apertura: il titolo della hero')
    foot = js[js.index('// footer: quando arrivi in fondo'):]
    mine = r'''
// storia: il percorso si disegna mentre la sezione scorre; le tappe si accendono quando la linea ci arriva, il contatore sale
{const rt=$('pjRoute');if(rt){const st=$('pj-storia'),ln=$('pjRouteP'),svg=rt.querySelector('svg'),stops=[...rt.querySelectorAll('.pj-stop')],N=+rt.dataset.n,num=$('pjN');
  const fr=stops.map((_,i)=>i/(stops.length-1)),still=matchMedia('(prefers-reduced-motion:reduce)').matches;
  const place=()=>{const L=ln.getTotalLength(),k=svg.getBoundingClientRect().width/240;stops.forEach((s,i)=>{const pt=ln.getPointAtLength(fr[i]*L);s.style.left=pt.x*k+'px';s.style.top=pt.y*k+'px';s.classList.toggle('l',pt.x>120)})};
  const go=()=>{const r=st.getBoundingClientRect(),p=still?1:clamp((innerHeight*.55-r.top)/Math.max(1,r.height-innerHeight*.5));ln.style.strokeDashoffset=(1-p).toFixed(4);
    stops.forEach((s,i)=>s.classList.toggle('on',p>=fr[i]-.005));num.textContent=Math.round(p*N)};
  place();go();addEventListener('resize',()=>{place();go()});addEventListener('scroll',go,{passive:true})}}
// barra dei servizi: si accende la voce del lavoro al centro dello schermo; cliccando una voce si scorre al suo primo lavoro
{const bar=$('pjSvc'),figs=[...document.querySelectorAll('[data-svc]')];if(bar&&figs.length){const pills=[...bar.querySelectorAll('button')];let act=null;
  const go=()=>{const vh=innerHeight;let best=null,bd=1e9;figs.forEach(f=>{const r=f.getBoundingClientRect(),d=r.top>vh/2?r.top-vh/2:r.bottom<vh/2?vh/2-r.bottom:0;if(d<bd){bd=d;best=f}});
    const show=bd<vh*.2;bar.classList.toggle('on',show);if(!show)return; // solo quando un lavoro occupa il centro dello schermo
    const s=best.dataset.svc;if(s===act)return;act=s;pills.forEach(q=>q.classList.toggle('on',q.dataset.s===s))};
  pills.forEach(q=>q.onclick=()=>{const f=figs.find(f=>f.dataset.svc===q.dataset.s);if(!f)return;const y=f.getBoundingClientRect().top+scrollY-Math.max(0,(innerHeight-f.offsetHeight)/2);
    lenis?lenis.scrollTo(y,{duration:1.2}):scrollTo({top:y,behavior:'smooth'})});
  addEventListener('scroll',go,{passive:true});go()}}
// titolo lettera per lettera
{const t=$('pjTtl');if(t){let i=0;t.innerHTML=t.textContent.split(' ').map(w=>`<span class="wd">${[...w].map(c=>`<span class="ch" style="--i:${i++}" aria-hidden="true">${c}</span>`).join('')}</span>`).join(' ');
  // una parola non va mai a capo a metà: se la più lunga non entra, il titolo si riduce quanto basta
  const fit=()=>{t.style.fontSize='';const w=Math.max(...[...t.querySelectorAll('.wd')].map(e=>e.offsetWidth)),W=t.clientWidth;if(w>W)t.style.fontSize=(parseFloat(getComputedStyle(t).fontSize)*W/w*.98)+'px'};
  document.fonts.ready.then(fit);addEventListener('resize',fit)}}
const nav=$('nav'),darks=[...document.querySelectorAll('[data-dark]')],pjHero=$('pjHero'),still=matchMedia('(prefers-reduced-motion:reduce)').matches;
const mb='Un pullman <a href="progetto-marinobus.html">MarinoBus</a> è lungo circa 12 metri: ';
const onScroll=()=>{
  const vh=innerHeight,y=nav.offsetHeight/2;
  nav.classList.toggle('on-dark',darks.some(s=>{const r=s.getBoundingClientRect();return r.top<=y&&r.bottom>=y}));
  nav.classList.toggle('solid',scrollY>40&&!nav.classList.contains('on-dark'));
  // primo media: si allarga fino a tutta larghezza mentre sale
  {const pr=document.querySelector('.nextp-pill').getBoundingClientRect();if(pr.top<=y&&pr.bottom>=y&&pr.left<innerWidth*.2&&pr.right>innerWidth*.8)nav.classList.add('on-dark')}
  nav.classList.toggle('solid',scrollY>40&&!nav.classList.contains('on-dark'));
  if(!still&&pjHero){const r=pjHero.getBoundingClientRect();pjHero.style.setProperty('--k',clamp((r.top-vh*.15)/(vh*.7)).toFixed(3))}
  shutters.forEach(({el,bands,out})=>{const r=el.getBoundingClientRect();if(r.top>vh*1.3||r.top<-vh*.5)return;
    const p=clamp(out?(vh-r.top)/(vh*.85):(vh*.75-r.top)/(vh*.6)),n=bands.length;
    bands.forEach((b,i)=>{const k=clamp(p*2-(n-1-i)/(n-1));b.style.transform='scaleY('+(out?1-k:k).toFixed(3)+')'})});
  const c=(scrollY+vh)*0.02646,m=c/100;
  $('cm').textContent=c>=100?m.toFixed(1).replace('.',',')+' m':Math.round(c)+' cm';
  $('cmtxt').innerHTML=mb+(m<12?'ne mancano '+(12-m).toFixed(1).replace('.',',')+'.':'l\'hai superato.');
};
addEventListener('scroll',onScroll,{passive:true});addEventListener('resize',onScroll);onScroll();
addEventListener('load',()=>{
  if(!window.gsap)return;
  gsap.registerPlugin(ScrollTrigger);
  if(window.Lenis&&!still){lenis=new Lenis({lerp:.1,anchors:true});lenis.on('scroll',ScrollTrigger.update);gsap.ticker.add(t=>lenis.raf(t*1000));gsap.ticker.lagSmoothing(0)}
  if(matchMedia('(hover:hover) and (pointer:fine) and (prefers-reduced-motion:no-preference)').matches){
    const mags=[...document.querySelectorAll('.nav .btn,.mpill')].map(el=>({el,x:gsap.quickTo(el,'x',{duration:.6,ease:'power3'}),y:gsap.quickTo(el,'y',{duration:.6,ease:'power3'})}));
    addEventListener('pointermove',e=>mags.forEach(({el,x,y})=>{const r=el.getBoundingClientRect(),cx=r.left+r.width/2-gsap.getProperty(el,'x'),cy=r.top+r.height/2-gsap.getProperty(el,'y'),
      dx=e.clientX-cx,dy=e.clientY-cy,R=Math.max(r.width,r.height)/2+70,k=clamp((R-Math.hypot(dx,dy))/40);
      x(clamp(dx*.25,-10,10)*k);y(clamp(dy*.25,-10,10)*k)}),{passive:true});
  }
  let rT;new ResizeObserver(()=>{clearTimeout(rT);rT=setTimeout(()=>ScrollTrigger.refresh(),200)}).observe(document.body);
  // pagina successiva: lo stesso codice della home
NEXTP_JS
});
'''
    return '<script>\n' + head + shut + mine.replace('NEXTP_JS', nextp) + roll + foot + '</script>\n'


def tail_html(nxt):
    tail = local(between(SRC, '</main>', '<script>\nconst $='))[len('</main>'):]
    w1, w2, href, pic = nxt
    return re.sub(r'<section class="nextp".*?</section>', f'''<section class="nextp" id="nextp" data-href="{href}" aria-label="Pagina successiva">
  <div class="nextp-pin">
    <p class="nextp-k">Pagina successiva</p>
    <a class="nextp-t" href="{href}" aria-label="{w1} {w2}"><span>{w1}</span><span class="nextp-pill" aria-hidden="true"><img src="{pic}" alt="" loading="lazy"></span><span>{w2}</span></a>
    <p class="nextp-h">Continua a scorrere</p>
    <span class="nextp-bar" aria-hidden="true"><i></i></span>
  </div>
</section>''', tail, flags=re.S)


def build(p):
    head = SRC[:SRC.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f"<title>{esc(p['name'])} · Progetti · Never Before Italia</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(p["lede"])}">', head)
    head += '<style>' + CSS + '</style>\n</head>\n'
    top = local(between(SRC, '<body>', '<main id="top">')).replace('href="index.html#top"', 'href="index.html"')
    tail = tail_html(p['next'])
    page = head + top + main_html(p) + '\n' + tail + script() + '</body>\n</html>\n'
    (ROOT / f"progetto-{p['slug']}.html").write_text(page, encoding='utf8')
    print('ok', p['slug'], len(page))


# ---------------------------------------------------------------- pagine interne: chi siamo, servizi, singolo servizio, progetti
import json, sys
sys.path.insert(0, str(ROOT / 'tools'))
from contenuti import SERVIZI, SERVIZI_INTRO, CHI_SIAMO

PJ = json.loads((ROOT / 'tools' / 'progetti.json').read_text(encoding='utf8'))  # progetti del sito attuale, copertine in assets/img/progetti
CATS = [('advertising', 'Advertising'), ('architecture', 'Architecture'), ('branding', 'Branding'), ('ecommerce', 'E-commerce'), ('events', 'Events'),
        ('graphics', 'Graphics'), ('social', 'Social'), ('video', 'Photo & Video'), ('website', 'Website')]
COVER = lambda slug: f'assets/img/progetti/{slug}.jpg'

PAGES_CSS = r'''
/* pagine interne: stessa grammatica della home (titolo enorme lettera per lettera, filetti, card bianche col motion design) */
.in-head{padding:calc(var(--nav-h) + clamp(60px,12vh,140px)) var(--pad) 0}
.in-k{font-size:15px;color:var(--ink-2);margin-bottom:12px}
.in-intro{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));column-gap:16px;margin-top:clamp(40px,6vw,80px);padding-top:16px;border-top:1px solid var(--ink)}
.in-intro .pj-big{grid-column:1/4;margin:0}
.in-intro p:not(.pj-big){grid-column:5/7;font-size:clamp(17px,1.3vw,20px);line-height:1.35;text-indent:4em}
/* servizi: una riga per servizio, col suo motion design a destra */
.sv-list{list-style:none;margin:clamp(64px,8vw,120px) var(--pad) 0;padding:0;border-bottom:1px solid var(--line)}
.sv-row{display:grid;grid-template-columns:3em minmax(0,1.25fr) minmax(0,1fr) clamp(170px,19vw,300px);gap:clamp(16px,2.4vw,40px);align-items:center;padding:clamp(14px,1.6vw,22px) 0;border-top:1px solid var(--line);color:inherit;text-decoration:none}
.sv-row .n{font-size:14px;color:var(--ink-2);font-variant-numeric:tabular-nums}
.sv-row h2{font-size:clamp(34px,4.4vw,80px);line-height:1;transition:transform .7s var(--energy)}
.sv-row p{font-size:17px;line-height:1.4;color:var(--ink-2);max-width:28em}
.sv-row figure{margin:0;aspect-ratio:4/3;border-radius:14px;overflow:hidden;background:var(--surface);transition:transform .7s var(--energy)}
.sv-row:hover h2{transform:translateX(14px)}
.sv-row:hover figure{transform:scale(1.04) rotate(-1.5deg)}
/* singolo servizio. Fondo dei disegni = quello delle card in home (surface): su bianco il terreno grigio di alcuni disegni sembrava un pezzo tagliato */
.sv-hero{display:grid;place-items:center;background:var(--surface)}
.sv-hero .mo{width:auto;height:86%;max-width:100%}
.pc-sec{padding:0 var(--pad)}
.pc-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(24px,2.4vw,40px) clamp(10px,1.2vw,16px)}
.pc{display:block;color:inherit;text-decoration:none}
.pc-m{margin:0;aspect-ratio:4/3;border-radius:var(--radius-media);overflow:hidden;background:var(--surface)}
.pc-m img{display:block;width:100%;height:100%;object-fit:cover;transition:scale .8s var(--energy)}
.pc:hover .pc-m img{scale:1.05}
.pc-t{display:flex;justify-content:space-between;gap:16px;padding-top:12px;font-size:15px}
.pc-t b{font-weight:400}.pc-t small{font-size:inherit;color:var(--ink-2);text-align:right}
.sv-all{display:inline-flex;margin-top:clamp(32px,4vw,56px)}
/* progetti: filtri (bottoni neutri, l'attivo pieno) e griglia */
.pf{display:flex;flex-wrap:wrap;gap:8px;margin:clamp(40px,5vw,72px) var(--pad) clamp(28px,3vw,40px)}
.pf button{border:1px solid var(--line);background:none;font:400 15px var(--sans);letter-spacing:-.02em;color:var(--ink);padding:9px 16px;border-radius:99px;cursor:pointer;transition:background .3s,color .3s,border-color .3s}
.pf button:hover{border-color:var(--ink)}
.pf button.on{background:var(--ink);border-color:var(--ink);color:#fff}
.pf sup{font-size:11px;margin-left:4px;color:inherit;opacity:.6}
.pc[hidden]{display:none}
.pf-go .pc{view-transition-name:var(--vt)}
html:active-view-transition-type(filter)::view-transition-old(root),html:active-view-transition-type(filter)::view-transition-new(root){animation:none}
html:active-view-transition-type(filter)::view-transition-group(*){animation-duration:.6s;animation-timing-function:cubic-bezier(.2,.8,.2,1)}
/* chi siamo */
.ab-claim{padding:clamp(100px,14vw,200px) var(--pad) 0}
.ab-claim h2{font-size:clamp(44px,7vw,128px);line-height:.98;max-width:13em}
.ab-vm{display:grid;grid-template-columns:1fr 1fr;gap:clamp(10px,1.2vw,16px);padding:0 var(--pad)}
.ab-vm div{background:#fff;border-radius:22px;padding:clamp(24px,3vw,44px);min-height:clamp(260px,26vw,400px);display:flex;flex-direction:column;justify-content:space-between;gap:40px}
.ab-vm h3{font:400 15px var(--sans);letter-spacing:-.02em;color:var(--ink-2)}
.ab-vm p{font-family:var(--display);font-size:clamp(26px,2.6vw,44px);letter-spacing:-.05em;line-height:1.1}
.ab-num{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:clamp(80px,10vw,160px) var(--pad) 0;padding-top:16px;border-top:1px solid var(--ink)}
.ab-num b{display:block;font-family:var(--display);font-weight:var(--display-w);font-size:clamp(56px,7vw,128px);letter-spacing:-.06em;line-height:1}
.ab-num span{display:block;margin-top:10px;font-size:15px;color:var(--ink-2)}
.ab-q{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));column-gap:16px;padding:clamp(40px,5vw,64px) var(--pad) 0}
.ab-q p{grid-column:span 3;font-size:17px;line-height:1.45;color:var(--ink-2);max-width:40em}
.ab-job{display:flex;justify-content:space-between;align-items:end;gap:24px;flex-wrap:wrap;margin:clamp(80px,10vw,160px) var(--pad) 0;padding-top:16px;border-top:1px solid var(--ink)}
.ab-job h2{font-size:clamp(44px,6vw,110px);line-height:1}
.ab-job p{font-size:17px;color:var(--ink-2);margin-top:12px}
/* servizi: card che si impilano (Osmo "Stacking Cards 3D"): ogni card resta attaccata in alto, quella dopo la copre e lei si inclina all'indietro e si scurisce */
.stk{--row:100svh;--top:calc(var(--nav-h) + 16px);--ch:calc(var(--row) - var(--top) - 24px);view-timeline-name:--stk;display:grid;grid-auto-rows:var(--row);width:min(100% - 2*var(--pad),1240px);margin:clamp(40px,6vw,80px) auto 0}
.stk-i{position:sticky;top:var(--top);height:var(--ch);transform-origin:50% 100%;display:flex;flex-direction:column;gap:clamp(20px,3vw,40px);padding:clamp(20px,2.6vw,36px);border-radius:22px;background:var(--c);color:var(--ink);overflow:hidden}
.stk-top{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:24px 40px;align-items:end}
.stk-top .n{display:block;font-size:15px;margin-bottom:10px}
.stk-top h2{font-size:clamp(40px,5.4vw,96px);line-height:.95}
.stk-top p{font-size:clamp(17px,1.3vw,20px);line-height:1.35;margin-bottom:18px;max-width:30em}
.stk-art{flex:1;min-height:0;display:grid;place-items:center;border-radius:14px;background:#fff;overflow:hidden}
.stk-art .mo{width:auto;height:100%;max-width:100%}
@supports (animation-timeline:view()){@media (prefers-reduced-motion:no-preference){
  .stk-i{animation:stkAway linear forwards;animation-timeline:--stk;animation-range:exit-crossing calc(var(--i) * var(--row) - 100svh) exit-crossing calc(var(--i) * var(--row) - var(--top))}
  .stk-i:last-child{animation:none}
}}
@keyframes stkAway{to{transform:perspective(60em) rotateX(25deg) scale(.85);filter:brightness(.45)}}
/* titolo che scorre in orizzontale, come l'intro della home: la riga entra da destra e le parole si accendono passando */
.hs{position:relative}
.hs-pin{position:sticky;top:0;height:100svh;overflow:hidden;display:flex;align-items:center;padding:0 var(--pad)}
.hs .hx-line .w .c:not(.on),.hs .hx-pill:not(.on){opacity:0} /* niente è già lì: lettere e pillole compaiono quando arrivano */
/* pillole delle pagine interne: pastello pieno, tratto nero */
.hx-pill[class*=hp-] svg *{fill:none;stroke:var(--ink);stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.hp-bubble{background:#CDEBFF}.hp-bubble circle{fill:var(--ink);stroke:none;transform-box:fill-box;transform-origin:center;animation:hpDot 1.2s ease-in-out infinite}
.hp-bubble circle:nth-of-type(2){animation-delay:.15s}.hp-bubble circle:nth-of-type(3){animation-delay:.3s}
@keyframes hpDot{0%,60%,100%{transform:none}30%{transform:translateY(-7px)}}
.hp-pulse{background:#FFDCCB}.hp-pulse .bg{stroke:rgba(5,5,5,.15)}.hp-pulse path:not(.bg){stroke-dasharray:.32 .68;animation:hpRun 1.8s linear infinite}
@keyframes hpRun{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
.hp-spark{background:#FFF3B8}.hp-spark g{transform-box:view-box;transform-origin:105px 39px;animation:hpBurst 1.8s var(--energy) infinite}.hp-spark circle{fill:var(--ink);stroke:none;transform-box:fill-box;transform-origin:center;animation:hpCore 1.8s var(--energy) infinite}
@keyframes hpBurst{0%{transform:scale(.2);opacity:0}15%{opacity:1}70%,100%{transform:scale(1);opacity:0}}
@keyframes hpCore{0%,100%{transform:scale(1)}10%{transform:scale(1.6)}30%{transform:scale(.8)}}
.hp-gauge{background:#D7FFE0}.hp-gauge .bg{stroke:rgba(5,5,5,.15)}.hp-gauge .ar{stroke-dasharray:1;animation:hpArc 2.8s var(--energy) infinite}.hp-gauge circle{fill:var(--ink);stroke:none}
.hp-gauge .nd{transform-box:view-box;transform-origin:105px 62px;animation:hpNeedle 2.8s var(--energy) infinite}
@keyframes hpArc{0%{stroke-dashoffset:1}50%,80%{stroke-dashoffset:.08}100%{stroke-dashoffset:1}}
@keyframes hpNeedle{0%{transform:rotate(-80deg)}50%,80%{transform:rotate(66deg)}100%{transform:rotate(-80deg)}}
.hp-steps{background:#E2DBFF}.hp-steps rect{fill:#fff}.hp-steps path{stroke-dasharray:1;stroke-dashoffset:1;animation:hpTick 2.8s var(--energy) infinite}
@keyframes hpTick{0%,8%{stroke-dashoffset:1}25%,80%{stroke-dashoffset:0}92%,100%{stroke-dashoffset:1}}
.hp-venn{background:#FFDCCB}.hp-venn circle{fill:rgba(255,255,255,.55);animation:hpVa 3s ease-in-out infinite}.hp-venn .b{animation-name:hpVb}
@keyframes hpVa{0%,100%{transform:translateX(-10px)}50%{transform:translateX(8px)}}
@keyframes hpVb{0%,100%{transform:translateX(10px)}50%{transform:translateX(-8px)}}
.hs .hx-pill{transition:opacity .5s,transform .8s var(--energy)}.hs .hx-pill:not(.on){transform:scale(.4)}
.hs-t{display:flex;align-items:center;will-change:transform}
.hs .hx-line{padding-right:var(--pad)}
.hs-k{position:absolute;z-index:1;left:var(--pad);top:calc(var(--nav-h) + 40px);margin:0;font:400 15px var(--sans);letter-spacing:-.02em}
.hs-t{position:relative;z-index:1}
.hs-dark{color:#fff}
.hs-clip{position:absolute;inset:10px;z-index:1;display:flex;align-items:center;padding:0 var(--pad);border-radius:22px;overflow:hidden} /* sulla foto la riga resta dentro il riquadro: entra ed esce dai suoi bordi, non dallo schermo */.hs-dark .hs-k{color:#fff;left:calc(10px + var(--pad))}
.hs-dark .hx-line .w .c,.hs-dark .hx-line .w .c.on{color:#fff}
.hs-dark .ab-bg::after{background:rgba(5,5,5,.42)} /* velo neutro: la riga bianca si legge su tutta la foto */
/* rolodex: tamburo di frasi, gira con lo scroll */
.rdx{position:relative}
.rdx-pin{position:sticky;top:0;height:100svh;overflow:hidden;perspective:1600px}
.rdx-i{position:absolute;left:0;right:0;top:50%;display:flex;justify-content:center;align-items:center;gap:.14em;white-space:nowrap;font-family:var(--display);font-weight:var(--display-w);letter-spacing:var(--display-ls);font-size:var(--rf,clamp(56px,11vw,210px));line-height:1.1;margin-top:-.55em;backface-visibility:hidden;will-change:transform,opacity}
.rdx-i .hx-pill{opacity:1;margin:0}
/* card a ventaglio (Osmo Stacking Sticky Cards Bounce) */
.sc{padding:clamp(80px,12vw,160px) var(--pad) 18svh;overflow-x:clip}
.sc-h{text-align:center;font-size:clamp(44px,6vw,110px);margin-bottom:clamp(40px,6vw,80px)}
.sc-list{display:flex;flex-direction:column;align-items:center;gap:5em}
.sc-i{position:sticky;top:calc(var(--nav-h) + 24px);flex:none;width:clamp(220px,22vw,320px)}
.sc-c{aspect-ratio:2/3;display:flex;flex-direction:column;justify-content:space-between;gap:24px;padding:clamp(20px,2vw,32px);border-radius:22px;background:var(--c);color:var(--ink);box-shadow:0 10px 40px rgba(5,5,5,.08);will-change:transform}
.sc-c.dk{background:var(--dark);color:#fff}
.sc-n{font-family:var(--display);font-size:clamp(64px,6vw,104px);letter-spacing:-.05em;line-height:.9}
.sc-c h3{font-size:clamp(28px,2.4vw,40px);line-height:1}
.sc-c p{margin-top:12px;font-size:15px;line-height:1.4}
.sc-c.bump{animation:scBump 1s cubic-bezier(.2,.8,.2,1)}
@keyframes scBump{0%{scale:1}10%{scale:1.07 .97}35%{scale:.97 1.02}60%{scale:1.015 .995}80%{scale:.997 1.002}100%{scale:1}}
/* progetti: la cupola della home a tutto schermo, la pagina non scorre */
body:has(.pj-dome) .ft,body:has(.pj-dome) .nextp,body:has(.pj-dome) .shutter{display:none}
html:has(.pj-dome),body:has(.pj-dome){overflow:hidden;height:100%}
.pj-dome.projects{height:100svh;touch-action:none}
.pj-dome .dome-pin{height:100svh}
.pj-dome .dome-ui h1{font-size:clamp(56px,8vw,140px);color:#fff}
.pj-dome .dome-ui p{opacity:1;align-self:center}
.pf-d{display:flex;flex-wrap:wrap;justify-content:center;gap:6px;pointer-events:auto;margin-top:12px}
.pf-d button{border:1px solid #3A3A3A;background:var(--dark);font:400 14px var(--sans);letter-spacing:-.02em;color:#fff;padding:8px 14px;border-radius:99px;cursor:pointer;transition:background .3s,color .3s,border-color .3s}
.pf-d button:hover{border-color:#fff}
.pf-d button.on{background:#fff;border-color:#fff;color:var(--ink)}
.pf-d sup{font-size:10px;margin-left:3px;opacity:.6}
.dome-bot{display:flex;flex-direction:column;align-items:center}
@media (max-width:820px){
  .stk-top{grid-template-columns:1fr}.stk-top p{margin-bottom:10px}
  .pf-d{flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start;max-width:100%;padding-bottom:4px;scrollbar-width:none}
  .in-intro{grid-template-columns:1fr;row-gap:24px}.in-intro .pj-big,.in-intro p:not(.pj-big){grid-column:1}
  .sv-row{grid-template-columns:2em minmax(0,1fr);row-gap:10px}.sv-row p,.sv-row figure{grid-column:2}.sv-row figure{width:min(100%,320px)}
  .pc-grid{grid-template-columns:1fr 1fr}
  .ab-vm{grid-template-columns:1fr}.ab-num{grid-template-columns:1fr;row-gap:32px}.ab-q p{grid-column:1/-1}.ab-q p+p{margin-top:16px}
}
@media (max-width:560px){.pc-grid{grid-template-columns:1fr}}
'''

PAGES_JS = r'''
// card a ventaglio: avvicinandosi alla cima ogni card (p 0→1, accelera) si sposta e si inclina al suo posto nel ventaglio; arrivata, rimbalza
{const R=[-5,2,6,-3,4,-6],Y=[2.1,0,4.5,1,3.2,.5];document.querySelectorAll('.sc-list').forEach(L=>{const its=[...L.querySelectorAll('.sc-i')],n=its.length;
  const go=()=>{const vh=innerHeight,top=parseFloat(getComputedStyle(its[0]).top),w=its[0].offsetWidth,sp=n>1?Math.min(w*.92,(L.clientWidth-w)/(n-1)):0,fs=parseFloat(getComputedStyle(L).fontSize);
    its.forEach((it,i)=>{const c=it.firstElementChild,p=still?1:clamp((vh*.75-it.getBoundingClientRect().top)/(vh*.75-top)),e=p*p,done=p>.999;
      c.style.transform=`translate(${((i-(n-1)/2)*sp*e).toFixed(1)}px,${(Y[i%6]*fs*e).toFixed(1)}px) rotate(${(R[i%6]*e).toFixed(2)}deg)`;
      if(done&&!it._d&&!still){c.classList.remove('bump');void c.offsetWidth;c.classList.add('bump')}it._d=done})};
  addEventListener('scroll',go,{passive:true});addEventListener('resize',go);go()})}
// (p con easing morbido per tratto: la frase si ferma un attimo al centro; nel passaggio quella che esce resta visibile fino a fine giro; ferme, le vicine non si vedono)
// rolodex: p va da 0 al numero di frasi-1 lungo la sezione; ogni frase sta su un tamburo (ruota attorno a un asse dietro lo schermo)
{const r=document.querySelector('.rdx');if(r){const it=[...r.querySelectorAll('.rdx-i')],N=it.length,STEP=55,SM=matchMedia('(pointer:coarse)').matches?.08:.2;let sd=null,raf=0;
  const fit=()=>{r.style.removeProperty('--rf');const W=innerWidth*.9,w=Math.max(...it.map(e=>{const g=document.createRange();g.selectNodeContents(e);return g.getBoundingClientRect().width}));
    if(w>W)r.style.setProperty('--rf',parseFloat(getComputedStyle(it[0]).fontSize)*W/w+'px');r.style.height=(innerHeight*(1+(N-1)*.35))+'px'};
  const upd=()=>{const run=r.offsetHeight-innerHeight,d=sd===null?-r.getBoundingClientRect().top:sd,q=clamp(d/run)*(N-1),f=q-Math.floor(q),p=Math.floor(q)+f*f*(3-2*f),R=it[0].offsetHeight*1.15;
    it.forEach((e,i)=>{const k=i-p;e.style.transform=`translateZ(${-R}px) rotateX(${(-k*STEP).toFixed(2)}deg) translateZ(${R}px)`;e.style.opacity=Math.max(0,1-Math.abs(k)**3).toFixed(3);
      e.querySelectorAll('.hx-pill').forEach(q=>q.classList.toggle('on',Math.abs(k)<.5))})};
  const tick=()=>{raf=0;const t=-r.getBoundingClientRect().top;if(sd===null||Math.abs(t-sd)>innerHeight*3)sd=t;sd+=(t-sd)*SM;if(Math.abs(t-sd)<.5)sd=t;upd();if(sd!==t)raf=requestAnimationFrame(tick)};
  addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(tick)},{passive:true});let lw=innerWidth;addEventListener('resize',()=>{if(innerWidth!==lw){lw=innerWidth;fit()}upd()});
  document.fonts.ready.then(()=>{fit();upd()});fit();upd()}}
// (sulla foto, .hs-dark, niente entrata: la riga parte fuori a destra e arriva scorrendo)
// titolo orizzontale (come l'intro della home): la sezione resta ferma, la riga scorre da destra a sinistra e ogni lettera si accende passando
{const FX=['rise','drop','blur','rise','pop','flip','blur','wave','slide','slide','bold'];document.querySelectorAll('.hs').forEach(sec=>{
  const ln=sec.querySelector('.hx-line'),tr=sec.querySelector('.hs-t');let nw=0;
  [...ln.childNodes].forEach(n=>{if(n.nodeType!==3)return;const f=document.createDocumentFragment();
    n.textContent.split(/(\s+)/).forEach(t=>{if(!t)return;if(/^\s+$/.test(t)){f.append(' ');return}const w=document.createElement('span');w.className='w';w.setAttribute('aria-hidden','true');
      w.innerHTML=[...t].map((c,i)=>`<span class="c" style="--i:${i}">${c}</span>`).join('');w.dataset.fx=FX[nw++%FX.length];f.append(w)});n.replaceWith(f)});
  const cs=[...ln.querySelectorAll('.c,.hx-pill')];const dark=sec.classList.contains('hs-dark'),cue=sec.querySelector('.hs-cue');let xs=[],x0=0,x1=0,pl=0,run=1,sd=null,raf=0,ready=dark;const SM=matchMedia('(pointer:coarse)').matches?.08:.2;
  const size=()=>{const vw=innerWidth;xs=cs.map(c=>ln.offsetLeft+c.offsetLeft+c.offsetWidth/2);pl=tr.getBoundingClientRect().left-(new DOMMatrix(getComputedStyle(tr).transform).m41);x0=dark?vw-pl:0;x1=Math.min(0,vw*.8-pl-tr.scrollWidth);run=Math.max(1,(x0-x1)/1.2);sec.style.height=(innerHeight+run)+'px'};
  const upd=()=>{const d=sd===null?-sec.getBoundingClientRect().top:sd,p=still?1:clamp(d/run),x=x0+(x1-x0)*p;tr.style.transform=`translate3d(${x.toFixed(1)}px,0,0)`;
    cue&&cue.classList.toggle('off',d>8);
    if(ready)cs.forEach((c,i)=>c.classList.toggle('on',still||pl+x+xs[i]<innerWidth*.86))};
  // apertura: le lettere già nello schermo compaiono una dopo l'altra, poi comanda lo scroll
  const intro=()=>{const x=x0+(x1-x0)*clamp(-sec.getBoundingClientRect().top/run);let n=0;cs.forEach((c,i)=>{if(pl+x+xs[i]<innerWidth*.86)setTimeout(()=>c.classList.add('on'),still?0:250+(n++)*45)});setTimeout(()=>{ready=true;upd()},still?0:250+n*45+200)};
  const tick=()=>{raf=0;const t=-sec.getBoundingClientRect().top;if(sd===null||Math.abs(t-sd)>innerHeight*3)sd=t;sd+=(t-sd)*SM;if(Math.abs(t-sd)<.5)sd=t;upd();if(sd!==t)raf=requestAnimationFrame(tick)};
  addEventListener('scroll',()=>{if(!raf)raf=requestAnimationFrame(tick)},{passive:true});let lw=innerWidth;addEventListener('resize',()=>{if(innerWidth!==lw){lw=innerWidth;size()}upd()});
  document.fonts.ready.then(()=>{size();upd();dark||intro()});size();upd()})}
'''


def card_svg(h3):
    # il motion design della card del servizio in home: la home resta l'unica fonte
    i = SRC.index(f'<h3>{h3}</h3>')
    a = SRC.rindex('<svg class="mo"', 0, i)
    return SRC[a:SRC.index('</figure>', a)]


def plain(h3):
    return re.sub(r'<[^>]+>', '', h3)


def short_txt(h3):
    i = SRC.index(f'<h3>{h3}</h3>')
    return html.unescape(re.search(r'<p>(.*?)</p>', SRC[i:]).group(1))


def pj_href(p):
    return 'progetto-marinobus.html' if p['slug'] == 'marinobus' else f"https://www.neverbeforeitalia.it/portfolio/{p['slug']}"


def pj_card(p, cls=''):
    return (f'<a class="pc{cls}" href="{pj_href(p)}" data-cats="{" ".join(p["cats"])}"><figure class="pc-m"><img src="{COVER(p["slug"])}" alt="{esc(p["name"])}" loading="lazy"></figure>'
            f'<span class="pc-t"><b>{esc(p["name"])}</b><small>{esc(p["sector"])}</small></span></a>')


def related(s):
    return [p for p in PJ if set(p['cats']) & set(s.get('cats', [])) or any(k in p['svc'] for k in s.get('kw', []))]


def page(file, title, desc, main, nxt, css='', js=''):
    head = SRC[:SRC.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', head)
    head += '<style>' + CSS + PAGES_CSS + css + '</style>\n</head>\n'
    top = local(between(SRC, '<body>', '<main id="top">')).replace('href="index.html#top"', 'href="index.html"')
    out = head + top + main + '\n' + tail_html(nxt) + script().replace('</script>\n', PAGES_JS + js + '</script>\n') + '</body>\n</html>\n'
    (ROOT / file).write_text(out, encoding='utf8')
    print('ok', file, len(out))


def ttl(name):
    return f'<h1 class="pj-ttl" id="pjTtl" aria-label="{esc(name)}">{esc(name)}</h1>'


def hs(text, kicker, bg=''):
    # hero della pagina: un solo titolo che scorre in orizzontale, stessa riga e stessi effetti per lettera dell'intro della home (.hx-line).
    # Con bg la riga passa bianca sopra la foto (la foto della pillola della home: il passaggio di pagina la fa crescere fin qui)
    pic = f'<div class="ab-bg"><img src="{bg}" alt=""></div>' if bg else ''
    line = re.sub(r'\{(\w+)\}', lambda m: PILLS[m.group(1)], esc(text))
    label = re.sub(r'\s*\{\w+\}', '', text)
    return (f'<section class="hs{" hs-dark" if bg else ""}"{" data-dark" if bg else ""} aria-label="{esc(kicker)}"><div class="hs-pin">{pic}<h1 class="sr">{esc(kicker)}</h1>'
            f'{"<p class=hs-cue><span>Scorri</span><i></i></p>" if bg else ""}{"<div class=hs-clip>" if bg else ""}<div class="hs-t"><p class="hx-line" aria-label="{esc(label)}">{line}</p></div>{"</div>" if bg else ""}</div></section>')


def rdx(items, kicker):
    # rolodex: la sezione resta ferma, scorrendo le frasi girano su un tamburo una alla volta, ognuna con la sua pillola animata
    pills = lambda t: re.sub(r'\{(\w+)\}', lambda m: PILLS[m.group(1)], esc(t))
    label = re.sub(r'\s*\{\w+\}', '', ' '.join(items))
    return (f'<section class="rdx" aria-label="{esc(kicker)}"><h1 class="sr">{esc(kicker)}</h1><p class="sr">{esc(label)}</p><div class="rdx-pin" aria-hidden="true">'
            + ''.join(f'<div class="rdx-i">{pills(t)}</div>' for t in items) + '</div></section>')


# le pillole col motion design della frase in home, prese da lì
# pillole col motion design delle pagine interne (non quelle della home): partono quando la frase le raggiunge (.hx-pill.on)
_P = lambda k, svg: f'<span class="hx-pill hp-{k}"><svg viewBox="0 0 210 78" aria-hidden="true">{svg}</svg></span>'
PILLS = dict(
    bubble=_P('bubble', '<path d="M74,16 h62 a14,14 0 0 1 14,14 v14 a14,14 0 0 1 -14,14 h-44 l-14,12 v-12 h-4 a14,14 0 0 1 -14,-14 v-14 a14,14 0 0 1 14,-14 z"/><circle cx="88" cy="37" r="5"/><circle cx="105" cy="37" r="5"/><circle cx="122" cy="37" r="5"/>'),
    pulse=_P('pulse', '<path class="bg" d="M24,40 H74 L86,16 L100,64 L112,28 L120,40 H186"/><path pathLength="1" d="M24,40 H74 L86,16 L100,64 L112,28 L120,40 H186"/>'),
    spark=_P('spark', '<g>' + ''.join(f'<line x1="105" y1="39" x2="{105 + 26 * c:.1f}" y2="{39 + 26 * s:.1f}"/>' for c, s in ((1, 0), (.71, .71), (0, 1), (-.71, .71), (-1, 0), (-.71, -.71), (0, -1), (.71, -.71))) + '</g><circle cx="105" cy="39" r="7"/>'),
    gauge=_P('gauge', '<path class="bg" d="M68,62 A37,37 0 0 1 142,62"/><path class="ar" pathLength="1" d="M68,62 A37,37 0 0 1 142,62"/><line class="nd" x1="105" y1="62" x2="105" y2="32"/><circle cx="105" cy="62" r="5"/>'),
    steps=_P('steps', ''.join(f'<rect x="{x}" y="25" width="28" height="28" rx="7"/><path pathLength="1" d="M{x + 7},39 l5,6 l10,-12" style="animation-delay:{i * .45}s"/>' for i, x in enumerate((56, 91, 126)))),
    venn=_P('venn', '<circle class="a" cx="86" cy="39" r="22"/><circle class="b" cx="124" cy="39" r="22"/>'),
)


def stack(title, items):
    # card numerate che si impilano a ventaglio (Osmo "Stacking Sticky Cards (Bounce)"): ognuna resta attaccata in alto,
    # mentre arriva si inclina e scivola al suo posto, arrivata fa un piccolo rimbalzo. items: (titolo, testo o '')
    tones = ['#fff', None, 'dk']
    cards = ''
    for i, (t, txt) in enumerate(items):
        tone = tones[i % 3]
        cls = ' dk' if tone == 'dk' else ''
        bg = PASTEL[(i // 3) % len(PASTEL)] if tone is None else '#fff'
        body = f'<p>{esc(txt)}</p>' if txt else ''
        cards += f'<div class="sc-i" style="z-index:{i + 1}"><div class="sc-c{cls}" style="--c:{bg}"><span class="sc-n">{i + 1}.</span><div><h3>{esc(t)}</h3>{body}</div></div></div>'
    head = f'<h2 class="sc-h">{esc(title)}</h2>' if title else ''
    return f'<section class="sc">{head}<div class="sc-list">{cards}</div></section>'


def build_servizi():
    cards = ''.join(f'''
    <article class="stk-i" style="--i:{i + 1};--c:{PASTEL[i % len(PASTEL)]}"><div class="stk-top"><div><span class="n">{i + 1:02d} / {len(SERVIZI):02d}</span><h2>{s['h3']}</h2></div>
      <div><p>{esc(short_txt(s['h3']))}</p><a class="go" href="servizio-{s['slug']}.html">Vedi il servizio <i><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 8h12M9 3l5 5-5 5"/></svg></i></a></div></div><div class="stk-art">{card_svg(s['h3'])}</div></article>''' for i, s in enumerate(SERVIZI))
    main = f'''<main id="top" class="pj">
  {rdx(['Efficienza, {gauge}', 'metodo {steps}', 'e trasversalità. {venn}'], 'Servizi')}
  <div class="in-intro" style="margin:0 var(--pad)"><p>{esc(SERVIZI_INTRO['text'])}</p></div>
  <div class="stk">{cards}
  </div>
  <div class="pj-end"></div>
</main>'''
    page('servizi.html', 'Servizi · Never Before Italia', SERVIZI_INTRO['text'], main, ('I nostri', 'progetti', 'progetti.html', COVER('lum')))


def build_servizio(i):
    s, n = SERVIZI[i], SERVIZI[(i + 1) % len(SERVIZI)]
    name, txt = plain(s['h3']), s.get('long') or short_txt(s['h3'])
    pjs = related(s)[:6]
    spec = ''
    if pjs:
        spec += f'<div class="pj-col" style="grid-column:span 2"><h2>Progetti</h2>{"<br>".join(f"""<a href="{pj_href(p)}">{esc(p["name"])}</a>""" for p in pjs[:4])}</div>'
    more = '<a href="#sv-pj"><span>Vedi i progetti</span><span aria-hidden="true">→</span></a>' if pjs else '<a href="mailto:info@neverbeforeitalia.it?subject=Richiesta%20consulenza"><span>Richiedi una consulenza</span><span aria-hidden="true">→</span></a>'
    grid = f'''
  <section class="pj-blk pc-sec" id="sv-pj"><div class="pj-bh" style="padding-left:0"><h3>Progetti</h3></div><div class="pc-grid">{"".join(pj_card(p, " rv") for p in pjs)}</div>
    <a class="go sv-all" href="progetti.html">Tutti i progetti <i><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 8h12M9 3l5 5-5 5"/></svg></i></a></section>''' if pjs else ''
    main = f'''<main id="top" class="pj">
  <section class="pj-head">
    <p class="in-k">Servizio {i + 1:02d} / {len(SERVIZI):02d}</p>
    {ttl(name)}
    <div class="pj-meta">{spec}<div class="pj-lede"><p>{esc(txt)}</p>{more}</div></div>
  </section>
  <section class="pj-full"><figure class="pj-m sv-hero" id="pjHero" style="aspect-ratio:16/8">{card_svg(s['h3'])}</figure></section>{stack('Cosa facciamo', [(x, '') for x in s['subs']]) if s.get('subs') else ''}{grid}
  <div class="pj-end"></div>
</main>'''
    w = plain(n['h3']).rsplit(' ', 1)
    nr = related(n)
    page(f"servizio-{s['slug']}.html", f'{name} · Servizi · Never Before Italia', txt, main, (w[0], w[1], f"servizio-{n['slug']}.html", COVER((nr[0] if nr else PJ[0])['slug'])))


DOME_JS = r'''
// progetti: la cupola della home a tutto schermo. Si trascina (o rotella / due dita), le card arrivano dal fondo all'apertura e a ogni filtro
{const PD=__PD__,stage=$('dome'),sec=$('progetti'),pin=$('domePin'),COLS=10,ROWS=7,cards=[];let list=PD,t0=performance.now();
  for(let r=0;r<ROWS;r++)for(let c=0;c<COLS;c++){const el=document.createElement('div');el.className='dc';el.innerHTML='<img alt="" draggable="false"><span></span><span></span><i></i>';stage.append(el);
    cards.push({el,c,r,img:el.firstChild,s1:el.children[1],s2:el.children[2],dim:el.lastChild,lo:-1,dl:((c*7+r*13)%11)/11*.45,op:-1})}
  const fillCards=()=>cards.forEach(k=>{const d=list[(k.c*3+k.r*5)%list.length];k.d=d;k.img.src=d.i;k.s1.textContent=d.n;k.s2.textContent=d.c});fillCards();
  let ox=0,oy=0,vx=-.3,vy=0,drag=null,cw=0,ch=0,mx=null,my=null,cx=0,cy=0,D=0;
  const size=()=>{cw=cards[0].el.offsetWidth+10;ch=cards[0].el.offsetHeight+10};
  const wrapv=(v,W)=>((v+W/2)%W+W)%W-W/2;
  const frame=()=>{if(!drag){ox+=vx;oy+=vy;vx+=(-.3-vx)*.04;vy*=.94}
    const W=COLS*cw,H=ROWS*ch,b=pin.getBoundingClientRect(),hw=b.width/2,hh=b.height/2,en=still?1:clamp((performance.now()-t0)/1600);
    cx+=((mx===null?0:mx-hw)-cx)*.12;cy+=((my===null?0:my-hh)-cy)*.12;D+=((mx===null?0:drag&&drag.m?300:170)-D)*.08;
    const S=Math.max(b.width,b.height)*.32,S2=S*S;
    for(const k of cards){const x=wrapv(k.c*cw+ox,W),y=wrapv(k.r*ch+oy,H),off=Math.abs(x)>hw+cw||Math.abs(y)>hh+ch;
      if(off!==k.off){k.off=off;k.el.style.display=off?'none':''}if(off)continue;
      const dx=x-cx,dy=y-cy,g=Math.exp(-(dx*dx+dy*dy)/S2),gx=2*D*dx*g/S2,gy=2*D*dy*g/S2,e=1-(1-clamp((en-k.dl)/.55))**3,op=e.toFixed(2);
      if(op!==k.op){k.op=op;k.el.style.opacity=op}
      k.el.style.transform=`translate3d(${x.toFixed(1)}px,${y.toFixed(1)}px,${(-D*g-(1-e)*2600).toFixed(1)}px) rotateX(${Math.atan(gy).toFixed(4)}rad) rotateY(${(-Math.atan(gx)).toFixed(4)}rad)`;
      const lo=(mx===null?.3:.62*Math.min(1,Math.hypot(dx,dy)/(S*1.6))).toFixed(2);if(lo!==k.lo){k.lo=lo;k.dim.style.opacity=lo}}
    requestAnimationFrame(frame)};
  addEventListener('resize',size);
  sec.addEventListener('wheel',e=>{e.preventDefault();ox-=e.deltaX*.6;oy-=e.deltaY*.6},{passive:false}); // la pagina non scorre: la rotella muove la griglia
  sec.addEventListener('pointerleave',()=>{mx=my=null});
  sec.addEventListener('pointermove',e=>{const b=pin.getBoundingClientRect();if(e.pointerType==='mouse'){mx=e.clientX-b.left;my=e.clientY-b.top}
    if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(!drag.m&&Math.hypot(e.clientX-drag.sx,e.clientY-drag.sy)>6){drag.m=true;sec.classList.add('drag')}
    ox+=dx;oy+=dy;vx=dx;vy=dy;drag.x=e.clientX;drag.y=e.clientY});
  sec.addEventListener('pointerdown',e=>{if(e.button||e.target.closest('button,a'))return;drag={x:e.clientX,y:e.clientY,sx:e.clientX,sy:e.clientY,m:false,t:e.target.closest('.dc')}});
  const end=e=>{if(!drag)return;const d=drag;drag=null;sec.classList.remove('drag');if(!d.m&&d.t&&e.type==='pointerup')openLb(d.t)};
  addEventListener('pointerup',end);addEventListener('pointercancel',end);
  // filtri: le card si rimescolano col nuovo elenco e arrivano di nuovo dal fondo
  const bs=[...document.querySelectorAll('#pf button')];bs.forEach(b=>b.onclick=()=>{if(b.classList.contains('on'))return;bs.forEach(q=>q.classList.toggle('on',q===b));
    const f=b.dataset.f;list=f==='*'?PD:PD.filter(d=>d.k.includes(f));fillCards();t0=performance.now()});
  const lb=$('domeLb'),lbImg=$('domeImg'),fill=(id,t)=>{$(id).textContent=t;$(id).hidden=!t};
  const openLb=el=>{const d=cards.find(k=>k.el===el).d,r=el.getBoundingClientRect();
    lbImg.src=d.i;lbImg.alt=d.n;fill('domeC',d.c);fill('domeN',d.n);fill('domeM',d.m);fill('domeD',d.d);$('domeA').href=d.h;
    lb.hidden=false;vx=vy=0;const f=lbImg.getBoundingClientRect();
    if(window.gsap&&!still)gsap.fromTo(lbImg,{x:r.left-f.left,y:r.top-f.top,scaleX:r.width/f.width,scaleY:r.height/f.height,borderRadius:12},{x:0,y:0,scaleX:1,scaleY:1,borderRadius:22,duration:.8,ease:'expo.out'});
    requestAnimationFrame(()=>lb.classList.add('on'));$('domeX').focus()};
  const closeLb=()=>{if(lb.hidden)return;lb.classList.remove('on');setTimeout(()=>{lb.hidden=true},350)};
  $('domeX').onclick=closeLb;lb.addEventListener('click',e=>{if(e.target===lb)closeLb()});addEventListener('keydown',e=>{if(e.key==='Escape')closeLb()});
  size();requestAnimationFrame(frame)}
'''


def build_progetti_index():
    lab = dict(CATS)
    pd = [dict(h=pj_href(p), n=p['name'], m=p['sector'], i=COVER(p['slug']), c=lab.get(p['cats'][0], '') if p['cats'] else '', d=p['svc'], k=p['cats']) for p in PJ]
    btns = '<button type="button" class="on" data-f="*">Tutti<sup>' + str(len(PJ)) + '</sup></button>' + ''.join(
        f'<button type="button" data-f="{k}">{v}<sup>{sum(k in p["cats"] for p in PJ)}</sup></button>' for k, v in CATS if any(k in p['cats'] for p in PJ))
    lbox = re.search(r'<div class="dome-lb".*?</figure>\s*</div>', SRC, re.S).group(0)
    links = ''.join(f'<li><a href="{pj_href(p)}">{esc(p["name"])}</a></li>' for p in PJ)
    main = f'''<main id="top" class="pj">
  <section class="projects pj-dome" id="progetti" data-dark aria-label="Progetti">
    <div class="dome-pin" id="domePin">
      <div class="dome-stage" id="dome" aria-hidden="true"></div>
      <div class="dome-ui"><h1>Progetti</h1><div class="dome-bot"><p>Trascina per esplorare · clicca una foto per aprirla</p><nav class="pf-d" id="pf" aria-label="Filtra i progetti">{btns}</nav></div></div>
    </div>
    <ul class="sr">{links}</ul>
  </section>
  {lbox}
</main>'''
    page('progetti.html', 'Progetti · Never Before Italia', 'I progetti di Never Before Italia.', main, ('Chi', 'siamo', 'chi-siamo.html', 'assets/img/chi-siamo-placeholder.jpg'),
         js=DOME_JS.replace('__PD__', json.dumps(pd, ensure_ascii=False)))


def build_chi_siamo():
    c = CHI_SIAMO
    main = f'''<main id="top" class="pj">
  {hs('Nuovi modi di comunicare {bubble} per emozionare {pulse} e sorprendere {spark}', 'Chi siamo', 'assets/img/chi-siamo-placeholder.jpg')}
  <section class="pj-story"><div class="pj-side"><h2>Il metodo NB4</h2></div><div><p class="pj-big">{esc(c['metodo_big'])}</p>{''.join(f'<p>{esc(t)}</p>' for t in c['metodo'][:2])}</div></section>
  {stack('', [('Metodo', c['metodo'][2]), ('Team', c['metodo'][3]), ('Vision', c['vision']), ('Mission', c['mission']), ('Qualità', c['qualita'][0]), ('Network', c['qualita'][1])])}
  <section class="ab-num">
    <div><b>24</b><span>Premi Mediastar</span></div><div><b>2011</b><span>Certificazione ISO 9001</span></div>
    <div><b>2</b><span>Sedi, Bari e Padova</span></div>
  </section>
  <section class="ab-job"><div><h2>Lavora con noi</h2><p>{esc(c['jobs'])}</p></div>
    <a class="go" href="https://www.neverbeforeitalia.it/jobs">Lavora con noi <i><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 8h12M9 3l5 5-5 5"/></svg></i></a></section>
  <div class="pj-end"></div>
</main>'''
    page('chi-siamo.html', 'Chi siamo · Never Before Italia', c['claim'], main, ('I nostri', 'servizi', 'servizi.html', COVER('marinobus')), ABOUT_CSS)


for p in PROJECTS:
    build(p)
build_chi_siamo()
build_servizi()
for i in range(len(SERVIZI)):
    build_servizio(i)
build_progetti_index()
