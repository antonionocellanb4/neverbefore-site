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
        next=('Altri', 'progetti', 'index.html#progetti', 'assets/img/never_before_italia_website_amaro_mediterraneo.jpg'),
    ),
]

ABOUT = dict(
    file='chi-siamo.html', title='Chi siamo · Never Before Italia', desc='Never Before Italia: chi siamo.',
    name='Chi siamo', img='assets/img/chi-siamo-placeholder.jpg', note='Pagina in costruzione.',
    next=('Altri', 'progetti', 'index.html#progetti', 'assets/img/never_before_italia_website_amaro_mediterraneo.jpg'),
)

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
{const t=$('pjTtl');if(t)t.innerHTML=[...t.textContent].map((c,i)=>`<span class="ch" style="--i:${i}" aria-hidden="true">${c===' '?'&nbsp;':c}</span>`).join('')}
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


def build_about(a):
    head = SRC[:SRC.index('</head>')]
    head = re.sub(r'<title>.*?</title>', f"<title>{esc(a['title'])}</title>", head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(a["desc"])}">', head)
    head += '<style>' + CSS + ABOUT_CSS + '</style>\n</head>\n'
    top = local(between(SRC, '<body>', '<main id="top">')).replace('href="index.html#top"', 'href="index.html"')
    main = f'''<main id="top" class="pj">
  <section class="ab-hero" data-dark><div class="ab-bg"><img src="{a['img']}" alt=""></div>
    <div class="ab-txt"><h1 class="pj-ttl" id="pjTtl" aria-label="{esc(a['name'])}">{esc(a['name'])}</h1><p>{esc(a['note'])}</p></div></section>
</main>'''
    page = head + top + main + '\n' + tail_html(a['next']) + script() + '</body>\n</html>\n'
    (ROOT / a['file']).write_text(page, encoding='utf8')
    print('ok', a['file'], len(page))


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


for p in PROJECTS:
    build(p)
build_about(ABOUT)
