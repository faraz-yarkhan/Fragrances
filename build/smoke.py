"""Quick browser check of the built pages. Usage: python3 build/smoke.py"""
import os
from playwright.sync_api import sync_playwright
B=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(B)
with sync_playwright() as pw:
    b=pw.chromium.launch();bad=0
    for f,pre,h in [(ROOT+'/index.html',None,'dior'),(ROOT+'/index.html','.coll button[data-c="arabian"]','lattafa'),(B+'/fragrance-shortlist.html',None,'chanel'),(B+'/arabian-houses.html',None,'zimaya')]:
        p=b.new_page(viewport={'width':390,'height':1200});errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
        p.goto('file://'+f);p.wait_for_timeout(800)
        if pre:p.click(pre);p.wait_for_timeout(300)
        p.click(f'#index button[data-id="{h}"]');p.wait_for_timeout(400)
        n=p.eval_on_selector_all(f'#{h} .ritem','e=>e.length')
        p.click('#tab-women');p.wait_for_timeout(300);w=p.eval_on_selector_all(f'#{h} .ritem','e=>e.length')
        p.fill('#q','zzzz');p.wait_for_timeout(200);lk=p.is_visible('#lkbtn')
        ok=not errs and n>0 and lk;bad+=not ok
        print('OK ' if ok else 'FAIL',os.path.basename(f),h,'men',n,'women',w,'lookup',lk,errs[:2])
    b.close();raise SystemExit(bad)
