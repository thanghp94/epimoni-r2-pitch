#!/usr/bin/env python3
"""Build epimoni-round2-pitch-v2.html from the revised v1.
Inlines assets/*.jpg as base64 data URIs, rebuilds S7 as the consolidation
story, adds micro-as-moat lines, the 11th Q&A card, and the demo-screenshot slot.
Every replacement asserts the anchor exists so a failed match aborts loudly."""
import base64, sys

SRC = 'epimoni-round2-pitch.html'
DST = 'epimoni-round2-pitch-v2.html'
s = open(SRC, encoding='utf-8').read()
fails = []

def b64(p):
    return 'data:image/jpeg;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

MINH   = b64('assets/minh-9pm.jpg')          # dark night scene — framed card on light slides
SHIELD = b64('assets/answer-shield-light.jpg')
SEED   = b64('assets/seedling-wins-light.jpg')

def rep(old, new, n=1):
    global s
    if s.count(old) < n:
        fails.append('NOT FOUND: ' + old[:90])
        return
    s = s.replace(old, new, n)

# ---------------- CSS additions ----------------
CSS_ADD = '''
  /* ---------- illustrations (light theme) ---------- */
  .artframe{background:#fff;border:1px solid #ccd2e0;border-radius:14px;padding:10px 10px 9px;
    box-shadow:0 16px 36px rgba(22,33,58,.16);transform:rotate(-1.6deg)}
  .artframe img{display:block;width:100%;border-radius:9px;object-fit:cover}
  .artframe .afc{margin-top:8px;text-align:center;font-size:12.5px;font-weight:700;letter-spacing:.12em;color:var(--dim)}
  .s1-row{display:flex;align-items:center;gap:46px}
  .s1-row .artframe{flex:0 0 300px}
  .s1-row .artframe img{height:312px}
  .s11-top{display:flex;gap:20px;align-items:stretch;margin-bottom:16px}
  .s11-top .artframe{flex:0 0 208px;transform:rotate(-1.2deg)}
  .s11-top .artframe img{height:150px}
  .s11-top .spine{margin-top:0;flex:1;align-self:center}
  .shieldpanel{flex:0 0 176px;display:flex;align-items:center}
  .shieldpanel .artcard{width:100%;height:210px}
  .artcard{border-radius:14px;border:1px solid #e6e2d8;box-shadow:0 10px 26px rgba(22,33,58,.12);object-fit:cover}
  .glowbadge{position:absolute;top:48px;right:14px;z-index:5;background:#fff;border:1.5px solid var(--amber);
    color:var(--amber2);font-size:15px;font-weight:800;letter-spacing:.06em;padding:9px 16px;border-radius:11px;
    box-shadow:0 0 20px rgba(242,166,58,.4);animation:gbpulse 2.4s ease-in-out infinite}
  @keyframes gbpulse{50%{box-shadow:0 0 30px rgba(242,166,58,.65)}}
  .shotframe{margin-top:16px;border:1.5px dashed #b9c2d4;border-radius:12px;height:72px;display:flex;
    align-items:center;justify-content:center;gap:12px;color:var(--dim);font-size:15px;letter-spacing:.1em}
  .shotframe b{color:var(--amber)}
  .slide.app .h{margin-bottom:8px}
  /* ---------- S5 engagement engine ---------- */
  .eng{display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;margin-top:14px;
    background:#fff;border:1px solid var(--line2);border-radius:14px;padding:11px 18px 10px}
  .eng-t{flex:0 0 auto;font-size:11.5px;font-weight:800;letter-spacing:.14em;color:var(--amber);line-height:1.35}
  .cycle{display:flex;align-items:center;gap:7px;flex:1;min-width:0}
  .cycle .cn{background:#f3f0e8;border:1.5px solid var(--line2);border-radius:999px;
    padding:8px 13px;font-size:13.5px;font-weight:800;color:var(--text);white-space:nowrap}
  .cycle .cn.next{background:#fdf3df;border-color:#e3c98f;color:var(--amber2)}
  .cycle .ca{color:var(--amber);font-weight:800;font-size:15px}
  .charcard{display:flex;align-items:center;gap:12px;background:#faf9f6;border:1px solid var(--line2);
    border-radius:11px;padding:8px 12px;flex:0 0 auto}
  .cc-av{width:32px;height:32px;border-radius:50%;background:#e3ded0;position:relative;flex:0 0 auto;overflow:hidden}
  .cc-av:before{content:"";position:absolute;left:50%;top:6px;width:11px;height:11px;border-radius:50%;background:#a8a294;transform:translateX(-50%)}
  .cc-av:after{content:"";position:absolute;left:50%;bottom:3px;width:20px;height:10px;border-radius:9px 9px 0 0;background:#a8a294;transform:translateX(-50%)}
  .cc-bars{display:flex;gap:3px;align-items:flex-end;height:32px;flex:0 0 auto}
  .cc-bars i{width:7px;background:linear-gradient(#f2a63a,#e8890c);border-radius:2px}
  .cc-gear{display:flex;gap:6px}
  .cc-gear span{font-size:11.5px;font-weight:700;color:var(--muted);background:#fff;
    border:1px solid var(--line2);border-radius:6px;padding:2px 7px;white-space:nowrap}
  .cc-cap{font-size:12px;color:var(--dim);font-style:italic;margin-top:5px;line-height:1.2}
  .engrules{flex-basis:100%;font-size:13px;color:var(--dim);border-top:1px solid var(--line2);padding-top:8px;line-height:1.35}
  /* ---------- S7 consolidation ---------- */
  .s7b-wrap{display:flex;gap:26px;margin-top:14px}
  .stack{flex:1;border-radius:16px;padding:20px 24px;border:1px solid var(--line2)}
  .stack.old{background:#fdf0f0;border-color:#f0c4c4}
  .stack.new{background:linear-gradient(160deg,#fffdf4,#fbf3df);border-color:#e3c98f}
  .stack .sh{font-size:13px;font-weight:800;letter-spacing:.16em;margin-bottom:12px}
  .stack.old .sh{color:#dc2626}.stack.new .sh{color:var(--amber2)}
  .stack ul{list-style:none;display:flex;flex-direction:column;gap:11px;font-size:16.5px;color:var(--muted);line-height:1.4}
  .stack ul li{display:flex;gap:10px}
  .stack ul li:before{content:"";flex:0 0 7px;height:7px;border-radius:50%;margin-top:8px;background:var(--dim)}
  .stack.old ul li:before{background:#e5a3a3}.stack.new ul li:before{background:var(--amber)}
  .stack .tot{margin-top:14px;font-size:22px;font-weight:800;line-height:1.2}
  .stack.old .tot{color:#b91c1c}.stack.new .tot{color:var(--amber2)}
  .stack .tot small{display:block;font-size:14px;color:var(--muted);font-weight:600;margin-top:5px;line-height:1.35}
  .stack .key{margin-top:12px;font-size:15.5px;font-style:italic;color:#b91c1c;border-top:1px dashed #f0c4c4;padding-top:11px;line-height:1.4}
  .s7-strip{margin-top:18px;background:#fdf3df;border:1px solid #e3c98f;border-radius:12px;
    padding:14px 20px;display:flex;align-items:baseline;gap:18px;font-size:17.5px}
  .s7-strip .path{font-weight:800;color:var(--amber2);white-space:nowrap}
  .s7-strip .pos{color:var(--muted);line-height:1.4}
'''
rep('  /* ---------- overlays ---------- */', CSS_ADD + '\n  /* ---------- overlays ---------- */')

# ---------------- CSS tweaks ----------------
rep('.screen{background:#0a0f20;border:1px solid #2a3860;border-bottom:none;border-radius:14px 14px 0 0;overflow:hidden}',
    '.screen{position:relative;background:#0a0f20;border:1px solid #2a3860;border-bottom:none;border-radius:14px 14px 0 0;overflow:hidden}')
rep('.subjgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;flex:0 0 400px}',
    '.subjgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px}')
rep('.ckcol{flex:1;background:var(--card);border:1px solid var(--line2);border-radius:16px;padding:22px 26px}',
    '.ckcol{flex:1;background:var(--card);border:1px solid var(--line2);border-radius:16px;padding:20px 24px}')
rep('.ck{list-style:none;display:flex;flex-direction:column;gap:15px}',
    '.ck{list-style:none;display:flex;flex-direction:column;gap:13px}')
# storybar: 12 beats needs tighter packing
rep('font-size:12px;letter-spacing:.11em;color:var(--dim);display:none;pointer-events:none;white-space:nowrap',
    'font-size:11.5px;letter-spacing:.1em;color:var(--dim);display:none;pointer-events:none;white-space:nowrap')
rep('#storybar .sep{opacity:.18;margin:0 7px}','#storybar .sep{opacity:.18;margin:0 6px}')
# S5: shrink chat pane to make room for the engagement engine panel
rep('display:flex;flex-direction:column;height:436px}','display:flex;flex-direction:column;height:300px}')
rep('.qa-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px 24px;margin-top:12px}',
    '.qa-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px 16px;margin-top:8px}')
rep('.qa{background:var(--card2);border:1px solid var(--line2);border-radius:11px;padding:10px 14px}',
    '.qa{background:var(--card2);border:1px solid var(--line2);border-radius:11px;padding:9px 13px}')

# ---------------- A. illustrations ----------------
# S1: framed night-scene art card beside the laptop (kept dark intentionally)
rep('<div class="s1-wrap">\n        <div class="laptop">',
    '<div class="s1-wrap">\n        <div class="s1-row">\n'
    '          <div class="artframe"><img src="' + MINH + '" alt="Minh studying at 9pm"><div class="afc">9:04 PM · MINH, HANOI</div></div>\n'
    '          <div class="laptop">')
rep('          <div class="base"></div>\n        </div>\n        <div class="s1-title" id="s1title">',
    '          <div class="base"></div>\n        </div>\n        </div>\n        <div class="s1-title" id="s1title">')
# S11 close: framed art beside the spine quote; ask + school list → notes; one contact line + URL
rep('''        <div class="s11-right">
          <p class="ask rise" style="--d:.3s">This tab doesn't hand him answers — it hands him a <b>5-minute quest.</b><br>
            The ask: <b>two pilot schools, 200 students, twelve weeks.</b> Help us run it.</p>
          <div class="contact rise" style="--d:.45s">
            <div class="tn">TEAM <span>EPIMONI</span></div>
            <div class="tm">DN · GM · TC · LH — Grade 7–8, four schools<br>
              FPT School · Ivy Global School · Sky-line School · UK Academy<br>
              Supervising teacher: Nguyễn Như Hà</div>
          </div>''',
    '''        <div class="s11-right">
          <div class="s11-top rise" style="--d:.3s">
            <div class="artframe"><img src="''' + MINH + '''" alt="Minh studying at 9pm"><div class="afc">9:04 PM · MINH</div></div>
            <div class="spine">In a world of free answers, we coach the struggle that makes learning stick.</div>
          </div>
          <div class="contact rise" style="--d:.45s">
            <div class="tn">TEAM <span>EPIMONI</span></div>
            <div class="tm">DN · GM · TC · LH — Grade 7–8 · FPT · IGS · Sky-line · UKA · mentor Nguyễn Như Hà</div>
          </div>''')
rep('          <div class="spine rise" style="--d:.75s">In a world of free answers, we coach the struggle that makes learning stick.</div>\n', '')
# S11 badge on the quest-tab side
rep('            <div class="display" style="height:222px',
    '            <div class="glowbadge">Today\'s Quest · 5:00</div>\n'
    '            <div class="display" style="height:222px')
# S5: shield art as a clean panel between the two chat panes (no watermark)
rep('''        </div>
        <div class="chatpane">
          <div class="cp-h r">EPIMONI · AI ANSWER SHIELD''',
    '''        </div>
        <div class="shieldpanel rise" style="--d:.15s"><img class="artcard" src="''' + SHIELD + '''" alt="AI Answer Shield"></div>
        <div class="chatpane">
          <div class="cp-h r">EPIMONI · AI ANSWER SHIELD''')
# S9: seedling art card under the subject grid (left column wrap)
rep('<div class="subjgrid rise" style="--d:.2s" id="subjgrid">',
    '<div class="rise" style="--d:.2s;flex:0 0 400px;display:flex;flex-direction:column;gap:14px">\n'
    '        <div class="subjgrid" id="subjgrid">')
rep('          <button class="subj" data-s="history" style="--sc:#9d7bff"><b>History</b><span>transfer &amp; argument</span></button>\n'
    '        </div>',
    '          <button class="subj" data-s="history" style="--sc:#9d7bff"><b>History</b><span>transfer &amp; argument</span></button>\n'
    '        </div>\n'
    '        <img class="artcard" src="' + SEED + '" alt="" style="width:100%;height:104px">\n'
    '        </div>')

# ---------------- BILLBOARD CUTS: headline + one visual + ~15-25 words ----------------
# S2 — paradox speaks; 3-word cost labels
rep('''<p class="lead rise" style="--d:.35s">The highest scorers are the most brittle.<br>
            The student everyone envies is <em>quietly breaking.</em></p>''',
    '<p class="lead rise" style="--d:.35s">The student everyone envies is <em>quietly breaking.</em></p>')
rep('<div class="cost"><b>01</b>Invisible burnout — nobody sees it</div>', '<div class="cost"><b>01</b>Invisible burnout</div>')
rep('<div class="cost"><b>02</b>Drilled for tests — can\'t transfer</div>', '<div class="cost"><b>02</b>Can\'t transfer</div>')
rep('<div class="cost"><b>03</b>AI-dependence — the shortcut became the strategy</div>', '<div class="cost"><b>03</b>AI-dependence</div>')
rep('          <div class="s2-goal rise" style="--d:.55s">Goal: Paradox Zone → True Mastery, via learning agency.</div>\n', '')
rep('<h1 class="h rise" style="--d:.05s">Top marks. <em>Empty learning.</em></h1>',
    '<h1 class="h rise" style="--d:.05s;font-size:60px">Top marks. <em>Empty learning.</em></h1>')
# S3 — quest card only; rep line becomes the beat
rep('<p class="beat rise" style="--d:.14s">So we asked a different question.</p>',
    '<p class="beat rise" style="--d:.14s">5 minutes isn\'t compromise — it\'s one complete rep.</p>')
rep('''        <div class="s3-right">
          <p class="big rise" style="--d:.4s">Curriculum → <em>one tiny, completable cognitive rep.</em></p>
          <ul class="s3-list">
            <li class="rise" style="--d:.55s"><b>→</b>Small enough to start.</li>
            <li class="rise" style="--d:.7s"><b>→</b>Complete enough to matter.</li>
            <li class="rise" style="--d:.85s"><b>→</b>Trains the process, not the subject.</li>
          </ul>
          <div class="tri rise" style="--d:1s">PREDICT <span>·</span> STRUGGLE <span>·</span> PROVE</div>
        </div>''', '')
rep("<h1 class=\"h rise\" style=\"--d:.05s\">We don't give answers. <em>We run 5-minute quests.</em></h1>",
    "<h1 class=\"h rise\" style=\"--d:.05s;font-size:64px\">We don't give answers. <em>We run 5-minute quests.</em></h1>")
# S4 — ring only; keep the click affordance hint
rep('''        <div class="s4-right">
          <p class="sub rise" style="--d:.35s">Every step maps to a published effect — science, not gimmicks.</p>
          <div class="s4-map">
            <div class="m rise" style="--d:.5s"><i>1</i><span><b>Generation → diagnosis</b> — attempt first, then find the misconception</span></div>
            <div class="m rise" style="--d:.62s"><i>2</i><span><b>Retrieval → transfer</b> — pull it from memory, then make it travel</span></div>
            <div class="m rise" style="--d:.74s"><i>3</i><span><b>Calibration → spacing</b> — know what you know, then space the next rep</span></div>
          </div>
          <div class="s4-note rise" style="--d:.9s">Roediger &amp; Karpicke · Cepeda et al. · Freeman et al. — citations in the appendix.</div>
          <div class="s4-hint rise" style="--d:1s">CLICK A NODE — it explains itself.</div>
        </div>''',
    '''        <div class="s4-right">
          <div class="s4-hint rise" style="--d:.5s">CLICK A NODE — it explains itself.</div>
        </div>''')
rep('<h1 class="h rise" style="--d:.05s">Six steps. <em>One complete rep for your brain.</em></h1>',
    '<h1 class="h rise" style="--d:.05s;font-size:64px">Six steps. <em>One complete rep for your brain.</em></h1>')
# S6 — funnel + hallway line only
rep('''        <div class="s6-right">
          <p class="lead rise" style="--d:.35s">Beachhead: <em>G6–8 students at bilingual &amp; private K-12 schools</em> in Hanoi &amp; HCMC.</p>
          <ul class="s6-why">
            <li class="rise" style="--d:.5s">We attend these schools — zero cold outreach.</li>
            <li class="rise" style="--d:.62s">English-medium curriculum matches our bilingual quests.</li>
            <li class="rise" style="--d:.74s">Families here already pay for edtech and tutoring.</li>
          </ul>
          <div class="s6-cue rise" style="--d:.9s">Our first customers are down the hallway.</div>
        </div>''',
    '''        <div class="s6-right">
          <div class="s6-cue rise" style="--d:.4s">Our first customers are down the hallway.</div>
        </div>''')
rep('<h1 class="h rise" style="--d:.05s">We start <em>where we live.</em></h1>',
    '<h1 class="h rise" style="--d:.05s;font-size:64px">We start <em>where we live.</em></h1>')
# S9 — grid + reskin + art + one line; roadmap and rnote to notes
rep('<p class="beat rise" style="--d:.14s">The coach doesn\'t change. Only the quest does.</p>',
    '<p class="beat rise" style="--d:.14s">Same engine. Every subject.</p>')
rep('          <div class="rnote">Same skeleton — only the quest changes.</div>\n', '')
rep('''      <div class="roadmap rise" style="--d:.5s">
        <div class="rm on">PILOT · G7–8 Science</div><span class="arr">→</span>
        <div class="rm">Full MS Science</div><span class="arr">→</span>
        <div class="rm">Cross-subject quests</div><span class="arr">→</span>
        <div class="rm">Teacher dashboards · school B2B</div>
      </div>
''', '')
rep('<h1 class="h rise" style="--d:.05s">One loop. <em>Every subject.</em></h1>',
    '<h1 class="h rise" style="--d:.05s;font-size:60px">One loop. <em>Every subject.</em></h1>')
# S10 timeline — ≤4-word phase labels, total-only cost bar, cut KPI foot
rep('<div class="ws">Teacher setup · baseline quest</div>', '<div class="ws">setup + baseline</div>')
rep('<div class="ws">G7–8 Science · VN + EN</div>', '<div class="ws">Science · VN+EN</div>')
rep('<div class="ws">Delayed unannounced check</div>', '<div class="ws">delayed check</div>')
rep('''      <div class="costbar rise" style="--d:.4s">
        <div class="cb"><b>$100–150 <sup class="est">est.</sup></b><span>LLM API — hint ladders</span></div>
        <div class="cb"><b>~$20 <sup class="est">est.</sup></b><span>Hosting</span></div>
        <div class="cb"><b>~$12 <sup class="est">est.</sup></b><span>Domain</span></div>
        <div class="cb"><b>~$50 <sup class="est">est.</sup></b><span>Misc / print / tests</span></div>
        <div class="cb total"><b>&lt; ~$300 <sup class="est">est.</sup></b><span>Total — funded by team, families, schools</span></div>
      </div>''',
    '''      <div class="costbar rise" style="--d:.4s">
        <div class="cb total" style="flex:1"><b>&lt; ~$300 <sup class="est">est.</sup></b><span>total pilot cost — funded by team, families, schools</span></div>
      </div>
      <div class="kpirow rise" style="--d:.5s">
        <span class="kchip">ENGAGEMENT KPI — weekly quest completion <b>≥70%</b> <i>(target)</i></span>
      </div>''')
rep('''      <div class="s8-foot rise" style="--d:.55s">
        <span>What four students + one teacher can actually ship.</span>
        <span class="kpi">Primary KPI: <b>learning gain per active minute</b> · ≥70% weekly completion <i style="font-style:normal;color:var(--dim)">(target)</i></span>
      </div>
''', '')
rep('<h1 class="h rise" style="--d:.05s">Twelve weeks. Two schools. <em>Two hundred students.</em></h1>',
    '<h1 class="h rise" style="--d:.05s;font-size:60px">Twelve weeks. Two schools. <em>Two hundred students.</em></h1>')
# S11 progress — ≤6-word checklist items
rep('<li style="--i:0"><span class="box"></span><span>Concept &amp; Good-Student-Paradox framing</span></li>',
    '<li style="--i:0"><span class="box"></span><span>Concept + paradox framing</span></li>')
rep('<li style="--i:1"><span class="box"></span><span>6R loop designed on paper</span></li>',
    '<li style="--i:1"><span class="box"></span><span>6R loop on paper</span></li>')
rep('<li style="--i:2"><span class="box"></span><span>Evidence base assembled (5 citations)</span></li>',
    '<li style="--i:2"><span class="box"></span><span>5 evidence citations</span></li>')
rep('<li style="--i:0"><span class="box"></span><span>G7 Photosynthesis quest — deployed</span></li>',
    '<li style="--i:0"><span class="box"></span><span>Photosynthesis quest deployed</span></li>')
rep('<li style="--i:1"><span class="box"></span><span>Teacher-validated misconception matrix</span></li>',
    '<li style="--i:1"><span class="box"></span><span>Validated misconception matrix</span></li>')
rep('<li style="--i:2"><span class="box"></span><span>AI Answer Shield — graduated hints</span></li>',
    '<li style="--i:2"><span class="box"></span><span>Answer Shield · graduated hints</span></li>')
rep('<li style="--i:3"><span class="box"></span><span>Bilingual quest content (VN + EN)</span></li>',
    '<li style="--i:3"><span class="box"></span><span>Bilingual content · VN + EN</span></li>')
rep('<li style="--i:4"><span class="box"></span><span>Pilot protocol — KPIs defined</span></li>',
    '<li style="--i:4"><span class="box"></span><span>Pilot KPIs defined</span></li>')
rep('<h1 class="h rise" style="--d:.05s">Eight weeks: <em>idea → working product.</em></h1>',
    '<h1 class="h rise" style="--d:.05s;font-size:60px">Eight weeks: <em>idea → working product.</em></h1>')

# ---------------- 1. new main slide: THE OTHER BOTTLENECK (insert before S7) ----------------
i0 = s.index('    <!-- ============ S7 — BUSINESS MODEL ============ -->')
newslide = '''    <!-- ============ S7 — THE OTHER BOTTLENECK ============ -->
    <section class="slide" data-title="Great micro-lessons are hard to make.">
      <div class="tag"><b>S7</b> · THE OTHER BOTTLENECK</div>
      <h1 class="h rise" style="--d:.05s">Great micro-lessons are hard to make. <em>That's the point.</em></h1>
      <p class="beat rise" style="--d:.14s">There's a second bottleneck — on the school side.</p>
      <div class="s7b-wrap">
        <div class="stack old rise" style="--d:.25s">
          <div class="sh">THE TEACHER &amp; SCHOOL PAIN</div>
          <ul>
            <li>An hour per lesson</li>
            <li>Quality = teacher skill</li>
            <li>Can't scale</li>
          </ul>
        </div>
        <div class="stack new rise" style="--d:.4s">
          <div class="sh">THE ENGINE — OUR ANSWER</div>
          <div class="engflow">
            <div class="en">Curriculum</div>
            <div class="e-arr">↓ teacher-validated</div>
            <div class="en">Misconception matrix</div>
            <div class="e-arr">↓ generates in minutes</div>
            <div class="en">5-minute quest</div>
          </div>
        </div>
      </div>
      <div class="s7-strip rise" style="--d:.55s">
        <span class="pos"><b style="color:var(--amber2)">Every school wants micro-lessons. Nobody can manufacture them.</b> We built the machine that makes them.</span>
      </div>
    </section>

'''
s = s[:i0] + newslide + s[i0:]

# ---------------- B. S7 consolidation rebuild ----------------
i0 = s.index('    <!-- ============ S7 — BUSINESS MODEL ============ -->')
i1 = s.index('    <!-- ============ S8 — FEASIBILITY ============ -->')
s7 = '''    <!-- ============ S7 — BUSINESS MODEL ============ -->
    <section class="slide" data-title="One coached rep replaces a fragmented stack.">
      <div class="tag"><b>S7</b> · BUSINESS MODEL</div>
      <h1 class="h rise" style="--d:.05s">One coached rep <em>replaces a fragmented stack.</em></h1>
      <p class="beat rise" style="--d:.14s">What schools pay today — and what they could pay instead.</p>
      <div class="s7b-wrap">
        <div class="stack old rise" style="--d:.25s">
          <div class="sh">WHAT SCHOOLS PAY TODAY</div>
          <div class="tot">$25–50<small> / student / yr <sup class="est">est.</sup></small></div>
          <div class="fnote">Raz-Kids · IXL · Quizlet-style supplements — libraries, not coaches</div>
        </div>
        <div class="stack new rise" style="--d:.4s">
          <div class="sh">EPIMONI SUITE — ONE LICENSE</div>
          <div class="tot">300–800k VND<small> / student / yr <sup class="est">est.</sup></small></div>
          <div class="fnote">coached quests · dashboard · misconception analytics</div>
        </div>
      </div>
      <div class="s7-strip rise" style="--d:.55s">
        <span class="path">Free pilot → paid Science module → suite upsell</span>
        <span class="pos">We land as the coach layer — then consolidate the spend.</span>
      </div>
    </section>

'''
s = s[:i0] + s7 + s[i1:]

# ---------------- tag renumbering downstream of the insert ----------------
rep('<div class="tag"><b>S7</b> · BUSINESS MODEL</div>', '<div class="tag"><b>S8</b> · BUSINESS MODEL</div>')
rep('<div class="tag"><b>S8</b> · FEASIBILITY &amp; PLAN</div>', '<div class="tag"><b>S9</b> · FEASIBILITY &amp; PLAN</div>')
rep('<div class="tag"><b>S9</b> · IMPACT &amp; SCALABILITY</div>', '<div class="tag"><b>S10</b> · IMPACT &amp; SCALABILITY</div>')
rep('<div class="tag"><b>S10</b> · PROGRESS SINCE ROUND 1</div>', '<div class="tag"><b>S11</b> · PROGRESS SINCE ROUND 1</div>')
rep('<div class="tag"><b>S11</b> · THANK YOU &amp; CONTACT</div>', '<div class="tag"><b>S12</b> · THANK YOU &amp; CONTACT</div>')
# S7 consolidation: buying-trigger becomes the beat line
rep('<p class="beat rise" style="--d:.14s">What schools pay today — and what they could pay instead.</p>',
    '<p class="beat rise" style="--d:.14s">Schools don\'t buy apps — they buy proof they can show parents, and a story that wins admissions.</p>')

# ---------------- C. micro-as-moat lines ----------------
# (billboard pass: the tri/rm anchors were cut — rep and economics lines now live
#  in the S3 beat and the S9/business NOTES entries, respectively)
# storybar beats: insert "the bottleneck" before "the stack" (12 main slides now)
rep("const BEATS=['9pm, Hanoi','hidden cost','a new tool','one rep','two futures',\n 'where we live','who pays','the plan','every subject','the proof','tonight'];",
    "const BEATS=['9pm, Hanoi','hidden cost','a new tool','one rep','two futures',\n 'where we live','the bottleneck','the stack','the plan','every subject','the proof','tonight'];")

# ---------------- 2. S5 gamification strip ----------------
rep('''<div class="unlockchip" id="unlock">EXPLANATION UNLOCKED</div>
          </div>
        </div>
      </div>
    </section>''',
    '''<div class="unlockchip" id="unlock">EXPLANATION UNLOCKED</div>
          </div>
        </div>
      </div>
      <div class="eng rise" style="--d:.2s">
        <div class="eng-t">ENGAGEMENT<br>ENGINE</div>
        <div class="cycle">
          <div class="cn">Rep</div><span class="ca">→</span>
          <div class="cn">Struggle XP</div><span class="ca">→</span>
          <div class="cn">Character up</div><span class="ca">→</span>
          <div class="cn">Gear</div><span class="ca">→</span>
          <div class="cn next">↩ tomorrow's quest</div>
        </div>
        <div class="charcard">
          <div class="cc-av"></div>
          <div class="cc-bars"><i style="height:70%"></i><i style="height:45%"></i><i style="height:88%"></i><i style="height:58%"></i></div>
          <div>
            <div class="cc-gear"><span>Lunar Kit</span><span>Shield Lv.2</span></div>
            <div class="cc-cap">Their level is their learning.</div>
          </div>
        </div>
        <div class="engrules">XP for wrong-then-right &gt; easy wins · gear via transfer · no pay-to-skip · no streak punishment</div>
      </div>
    </section>''')

# ---------------- D. demo screenshot slot (S10) ----------------
rep('      <div class="s10-foot rise" style="--d:.7s">',
    '      <!-- REPLACE: paste base64 of real app screenshot here -->\n'
    '      <div class="shotframe rise" style="--d:.5s"><b>DEMO SCREENSHOT</b> — drop in before deck lock</div>\n'
    '      <div class="s10-foot rise" style="--d:.7s">')

# ---------------- appendix: 11th Q&A card ----------------
rep('<div class="aa">One button, five minutes, an immediate win — and schools can assign quests instead of homework.</div></div>\n      </div>',
    '<div class="aa">One button, five minutes, an immediate win — and schools can assign quests instead of homework.</div></div>\n'
    '        <div class="qa rise" style="--d:.6s"><div class="qq">"You want to replace IXL? You\'re four students."<span class="own">LH</span></div><div class="aa">We start beneath them as the coach layer. Schools keep what they like; we consolidate spend as we prove gains.</div></div>\n'
    '        <div class="qa rise" style="--d:.65s"><div class="qq">"Isn\'t XP just Duolingo?"<span class="own">GM</span></div><div class="aa">We reward the process — retrieval, correction, calibration — not completion. Points sit on intrinsic design; never pay-to-skip.</div></div>\n'
    '        <div class="qa rise" style="--d:.7s"><div class="qq">"Isn\'t this just AI-generated lessons?"<span class="own">DN</span></div><div class="aa">AI drafts; the validated misconception matrix is the quality gate. The product isn\'t a lesson — it\'s consistency.</div></div>\n'
    '      </div>')

# ---------------- S5 sim: XP reward toast after "I got it!" / proof unlock ----------------
rep("""$('#unlock').classList.add('show')}]
  ];""",
    """$('#unlock').classList.add('show')}],
   [18200,()=>bubble(chatR,'xp','<b>+40 STRUGGLE XP</b> · Shield Lv.1 → Lv.2','21:04')]
  ];""")

# ---------------- NOTES: wholesale rewrite — word-for-word ESL scripts ----------------
# Replaces the entire NOTES array (15 entries). ~40-45 words per 20s; each first
# line is a transition; interaction cues inline in [brackets]; who/time/tip kept.
n0 = s.index('const NOTES=[')
n1 = s.index('/* ---------- slide enter/leave hooks ---------- */')
end = s.rindex('];', n0, n1)
NEW_NOTES = ''' {tag:'S1 · TITLE & TEAM',title:"Cold open — Minh's 9pm",who:'DN',time:'0:40',
  cue:'Indirect story open. Let the lines type. Speak slowly — this scene IS your unfair advantage: you are the user.',
  script:["It is 9pm in Hanoi. Minh — Grade 7, like us — has a science test tomorrow. Forty pages of notes.",
  "And in the next tab? ChatGPT. Ready to do all of it for him. [let the lines type]",
  "Minh is not lazy. Minh is us.",
  "The tool built to help him learn is quietly teaching him to stop thinking. Tonight, millions of students make the same trade.",
  "We are four students from four schools. And we built the shield."],
  tip:'Backup direct open if judges skew corporate: "The best students in Vietnam are the most at risk. Top marks, brittle understanding — and AI making it worse. We\\'re 13 and 14, and we built the fix."'},
 {tag:'S2 · PROBLEM & MARKET',title:'Top marks. Empty learning.',who:'DN',time:'1:05',
  cue:'"The student everyone envies is the one quietly breaking." Walk the 2×2, land on the Paradox Zone, CLICK it to reveal the 3 costs.',
  script:["So that is Minh\\'s night. But here is the strange part. On paper, Minh is a top student.",
  "Look at the square. [walk the 2×2] Grades go right. Real learning goes up. Bottom right — the Paradox Zone. Top marks. Test-drilled. Brittle.",
  "That is where Minh lives. [click the Paradox Zone]",
  "The student everyone envies is quietly breaking. The costs are invisible: burnout nobody sees, drilling that cannot transfer, and AI-dependence — the shortcut that became the strategy.",
  "This is not a content gap. Students do not need more knowledge. They need to want it — and know how to chase it. Goal: move him from the Paradox Zone to True Mastery."],
  tip:'Scores Problem & Market (10 pts).'},
 {tag:'S3 · SOLUTION',title:"We don't give answers. We run 5-minute quests.",who:'GM',time:'0:55',
  cue:'"Five minutes is small enough to start, complete enough to matter." The countdown starts NOW — point at it in the corner: the timer keeps running through the next slides. That\\'s the gag.',
  script:["So the real question is not: how do we give better answers. It is: how do we protect the question.",
  "Our answer: we do not give answers. We run five-minute quests.",
  "[point at the card] One quest. One objective. Five minutes. The timer is real — it keeps running in the corner through the next slides.",
  "Five minutes is not a compromise. It is the exact length of one complete rep — small enough to start, complete enough to matter.",
  "We are not an edtech app. We are a learning coach. Apps deliver content. Coaches change behavior. Predict, struggle, prove."],
  tip:'Rule of three: predict · struggle · prove.'},
 {tag:'S4 · THE LOOP',title:'Six steps. One complete rep for your brain.',who:'GM',time:'0:55',
  cue:'"REACH to RETURN — each step maps to a published effect: retrieval, spacing, generation." Click 2–3 nodes live; the ring auto-rotates when idle.',
  script:["So what happens inside those five minutes? Six steps. One rep for your brain.",
  "REACH — you predict first. REALIZE — we find the misconception. RECALL — you pull it from memory. RELATE — the idea travels to a new problem. REFLECT — you check what you actually know. RETURN — it comes back tomorrow.",
  "[click 2–3 nodes] Every step maps to a published effect — generation, retrieval, spacing. Science, not gimmicks. Citations are in the appendix.",
  "Attempt first, then find the misconception. Pull it from memory, then make it travel. Know what you know, then space the next rep."],
  tip:'Keep it moving — the ring demos itself.'},
 {tag:'S5 · DEMO',title:'Ask for the answer. Watch the shield.',who:'GM',time:'1:40',
  cue:'"Same question. Two futures." Let the simulated chat run — it auto-plays. This IS the offline fallback demo: it works even if Wi-Fi dies. Replay button is top-right.',
  script:["Now — do not take my word for it. Same question. Two futures. [let the chat play]",
  "Left side: generic AI. He asks — full answer in under a second. Brain icon greys out. Struggle skipped. Learning unverified.",
  "Right side: Epimoni. He begs — 'just tell me.' The Shield gives a Level 1 hint — a solar-panel picture, not a handout. Still stuck? Level 2: a guiding question.",
  "He tries again — and gets it himself. [point at the struggle meter] The reward is for the struggle, not the click. Plus forty Struggle XP. Shield levels up.",
  "Below — the same loop as a system: rep, XP, character, gear, back to tomorrow's quest. His level is his learning. No pay-to-skip. No streak punishment."],
  tip:'Longest slide — rehearse the timing against the animation. Gamification rewards the process — retrieval, correction, calibration — never completion or pay-to-skip.'},
 {tag:'S6 · MARKET',title:'We start where we live.',who:'TC',time:'0:55',
  cue:'"Our first customers are down the hallway." Every number on screen is labeled est. — say so out loud. Judges reward honesty over hockey sticks.',
  script:["So who uses this first? We start where we live.",
  "[point at the funnel] Top: about six point five million secondary students in Vietnam — estimate. Narrow to private and bilingual K-12 — roughly three to five hundred thousand. Then our grade band in Hanoi and HCMC — sixty to one hundred thousand. Every number is an estimate, labeled honestly.",
  "And the last bar: one to two hundred pilot seats — at our own four schools.",
  "Our first customers are down the hallway. We attend these schools — zero cold outreach. English-medium classes match our bilingual quests. Families here already pay for edtech and tutoring."],
  tip:'Scores Problem & Market + Audience template section.'},
 {tag:'S7 · THE OTHER BOTTLENECK',title:'Great micro-lessons are hard to make.',who:'TC',time:'0:45',
  cue:'"Every school wants micro-lessons. Nobody can manufacture them." Two-sided pain: students won\\'t start, schools can\\'t produce.',
  script:["But students are only half the problem. There is a second bottleneck — on the school side.",
  "A great five-minute lesson takes a teacher an hour or more. Quality lives in one teacher's skill — it cannot scale. So schools default to content libraries nobody finishes.",
  "Our engine fixes the supply side: curriculum plus a teacher-validated misconception matrix — and a coached quest is generated in minutes. The teacher approves. The teacher does not author.",
  "Every school wants micro-lessons. Nobody can manufacture them. We built the machine that makes them."],
  tip:'TIME CHECK — full script ≈ 9:40 at 115 wpm. If the clock is past 5:30 here, do this slide in 0:25; S10 is still the designated 20s cut.'},
 {tag:'S8 · BUSINESS MODEL',title:'One coached rep replaces a fragmented stack.',who:'TC',time:'0:55',
  cue:'"We land as the coach layer they don\\'t have — then consolidate the practice spend they overpay for." This slide scores 10 pts — deliver the stack math cold.',
  script:["So what does this cost? Schools do not buy apps — they buy proof they can show parents.",
  "Today: a fragmented stack — Raz-Kids, IXL, quiz supplements — twenty-five to fifty dollars per student a year, est. Libraries. None coaches how to learn.",
  "Epimoni is one license — coached quests, teacher dashboard, misconception analytics — about three to eight hundred thousand VND per student a year. Estimated.",
  "A quest costs cents in LLM tokens, not dollars — that is why this price works. Free pilot, paid Science module, then suite upsell. We land as the coach layer — then consolidate the spend."],
  tip:'Expect "you\\'re four students — replace IXL?" We start beneath them as the coach layer; consolidate practice spend as we prove gains. Full answer in the appendix. Adoption wedge: schools don\\'t change behavior — they swap one homework slot for one quest.'},
 {tag:'S9 · FEASIBILITY',title:'Twelve weeks. Two schools. Two hundred students.',who:'LH',time:'0:50',
  cue:'"This is what four students and one teacher can actually ship." Walk the timeline left to right — total under ~$300, est.',
  script:["So can four students actually run this? Here is the plan — sized to reality on purpose.",
  "Twelve weeks. Two schools. Two hundred students. Weeks one-two: onboard plus baseline. Weeks three-ten: live Science quests, weekly KPI pulses. Weeks eleven-twelve: a delayed, unannounced check — the real proof.",
  "Total cost under three hundred dollars — API, hosting, domain, misc. All estimates. Funded by team, families, schools.",
  "Primary KPI: learning gain per active minute — plus weekly quest completion at seventy percent. Targets, not data — and we say that honestly."],
  tip:'Sized to reality on purpose — that IS the feasibility argument. Secondary metrics for questions: return rate, calibration accuracy, study-friction, avg Struggle XP per student — engagement systems like this already ship in production learning platforms the team builds on.'},
 {tag:'S10 · SCALE',title:'One loop. Every subject.',who:'LH',time:'0:45 (compressible to 0:20)',
  cue:'"The coach doesn\\'t change. Only the quest does." Click one subject card to show the same 6R skeleton re-skinning.',
  script:["This scales because the coach does not change — only the quest does.",
  "[click a subject card] Same six-step skeleton, new quest on top. Expansion costs content matrices, not engineering — and that matrix is the moat.",
  "Path: pilot, full middle-school Science, cross-subject, teacher dashboards."],
  tip:'DESIGNATED COMPRESS SLIDE — if the clock is past 8:30, do this in 20 seconds.'},
 {tag:'S11 · PROGRESS',title:'Eight weeks: idea → working product.',who:'LH',time:'0:40',
  cue:'"Round 1 was a design. Round 2 is a product." Only claim what\\'s true — every R2 item is verifiable.',
  script:["So what changed since Round 1? Eight weeks — idea to working product.",
  "Round 1 was a design: the concept, the loop on paper, five evidence citations. Round 2 is a product: a deployed photosynthesis quest, a validated misconception matrix, the Answer Shield, bilingual content in Vietnamese and English, and a pilot protocol with KPIs defined.",
  "Every item on the right is real — and verifiable. Next milestone: pilot data."],
  tip:'Scores Progress Since R1 + feeds the 10 demo points.'},
 {tag:'S12 · CLOSE',title:"Tonight, Minh opens a different tab.",who:'DN',time:'0:35',
  cue:'CALLBACK — hold this no matter what the clock says. Same laptop, different tab.',
  script:["Remember Minh, at 9pm? Tonight he still opens a tab. But this one does not hand him answers — it hands him a five-minute quest.",
  "The ask: two pilot schools, two hundred students, twelve weeks. Help us run it.",
  "In a world of free answers, we coach the struggle that makes learning stick.",
  "We are Team Epimoni — four students, four schools, one supervising teacher. Thank you — questions welcome."],
  tip:'End on the spine line. Full team list: DN · GM · TC · LH — FPT · IGS · Sky-line · UKA · mentor Nguyễn Như Hà.'},
 {tag:'APPENDIX 1/3',title:'Q&A defense — owners',who:'ALL',time:'Q&A',
  cue:'Jump here during Q&A if useful. Owners in amber. Whole team must answer — coordination is scored (20 pts).',
  script:[],tip:'Never invent numbers. "We don\\'t know yet" + the pilot plan beats a fabricated metric.'},
 {tag:'APPENDIX 2/3',title:'Evidence base',who:'LH',time:'Q&A',
  cue:'Citation slide for "where\\'s the evidence" questions. Published science → mapped to loop steps.',
  script:[],tip:'Be explicit: product evidence = prototype today, pilot data this term.'},
 {tag:'APPENDIX 3/3',title:'Positioning table',who:'GM',time:'Q&A',
  cue:'For "how are you different" questions — five dimensions vs drill apps and generic AI.',
  script:['"Everyone is building a better answer machine. We protect the question."'],tip:''}
'''
s = s[:n0] + 'const NOTES=[\n' + NEW_NOTES + '];\n\n' + s[end+2:]

# ---------------- Script button on every slide + S-key alias ----------------
rep("else if(k==='n'||k==='N'){toggleNotes()}",
    "else if(k==='n'||k==='N'||k==='s'||k==='S'){toggleNotes()}")
rep("notesOv.addEventListener('click',e=>{if(e.target===notesOv)toggleNotes()});",
    "notesOv.addEventListener('click',e=>{if(e.target===notesOv)toggleNotes()});\n"
    "$$('.slide').forEach(sl=>{const sb=document.createElement('button');sb.className='scriptbtn';sb.textContent='SCRIPT';sb.addEventListener('click',e=>{e.stopPropagation();if(!notesOpen)toggleNotes()});sl.appendChild(sb)});")

# ================ UI/UX AUDIT PASS — a11y, motion, fonts, focus ================

# (1) Slide transition .45s -> .35s (and .cost reveal to match the 400ms guide)
rep("transition:opacity .45s ease,transform .45s ease,visibility 0s linear .45s;}",
    "transition:opacity .35s ease,transform .35s ease,visibility 0s linear .35s;}")
rep("transition:opacity .45s ease,transform .45s ease}",
    "transition:opacity .35s ease,transform .35s ease}")
rep("transition:.45s ease;border", "transition:.35s ease;border")

# (2) 12px font floor — bump every size below 12px
rep("#questChip .qd{font-size:10px", "#questChip .qd{font-size:12px")
rep("font-size:11.5px;letter-spacing:.1em;color:var(--dim);display:none",
    "font-size:12px;letter-spacing:.1em;color:var(--dim);display:none")  # storybar
rep(".msg .ts{display:block;font-size:11px", ".msg .ts{display:block;font-size:12px")
rep(".msg.ai .lv{display:block;font-size:11px", ".msg.ai .lv{display:block;font-size:12px")
rep(".qa .qq .own{margin-left:auto;flex:0 0 auto;font-size:11px",
    ".qa .qq .own{margin-left:auto;flex:0 0 auto;font-size:12px")
rep(".eng-t{flex:0 0 auto;font-size:11.5px", ".eng-t{flex:0 0 auto;font-size:12px")
rep(".cc-gear span{font-size:11.5px", ".cc-gear span{font-size:12px")
rep("#notesPanel .np-k{font-size:11px", "#notesPanel .np-k{font-size:12px")
rep("#notesPanel .np-sec{font-size:11px", "#notesPanel .np-sec{font-size:12px")
rep(".ovcard .s{font-size:10.5px", ".ovcard .s{font-size:12px")

# (3) ARIA markup
rep('<div class="q paradox" id="paradox">',
    '<div class="q paradox" id="paradox" role="button" tabindex="0" aria-label="Reveal the three hidden costs">')
rep('<div class="quad" id="quad">',
    '<div class="quad" id="quad" role="group" aria-label="Two by two chart — grades across, learning depth up. Paradox Zone bottom right: top marks, brittle learning.">')
rep('<div class="funnel rise" style="--d:.2s" id="funnel">',
    '<div class="funnel rise" style="--d:.2s" id="funnel" role="group" aria-label="Funnel: 6.5 million Vietnamese secondary students down to 100 to 200 pilot seats at our four schools. All estimates.">')
for nm,ang,lab in [('REACH','0deg','predict'),('REALIZE','60deg','diagnose'),('RECALL','120deg','retrieve'),
                   ('RELATE','180deg','transfer'),('REFLECT','240deg','calibrate'),('RETURN','300deg','space')]:
    rep('<button class="node" style="--a:%s"' % ang,
        '<button class="node" role="button" tabindex="0" aria-label="%s — %s" style="--a:%s"' % (nm,lab,ang))
rep('<button class="subj sel" data-s="science" style="--sc:#3ddc97">',
    '<button class="subj sel" data-s="science" style="--sc:#3ddc97" aria-pressed="true">')
for sk in ['math" style="--sc:#5aa9ff','english" style="--sc:#ffb02e','history" style="--sc:#9d7bff']:
    rep('<button class="subj" data-s="%s">' % sk,
        '<button class="subj" data-s="%s" aria-pressed="false">' % sk)
rep('<div class="overlay" id="notesOv">',
    '<div class="overlay" id="notesOv" role="dialog" aria-modal="true" aria-label="Speaker notes">')
rep('<div class="overlay" id="ovOv">',
    '<div class="overlay" id="ovOv" role="dialog" aria-modal="true" aria-label="Slide overview">')
rep('<div id="questChip">', '<div id="questChip" aria-live="off">')
rep('<div id="elapsed">00:00</div>', '<div id="elapsed" aria-live="off">00:00</div>')
rep('<div id="progress"></div>', '<div id="progress" aria-hidden="true"></div>')
rep('<div class="ringline"></div>', '<div class="ringline" aria-hidden="true"></div>')
rep('<div class="cc-av"></div>', '<div class="cc-av" aria-hidden="true"></div>')
s = s.replace('<span class="ca">', '<span class="ca" aria-hidden="true">')

# (4) JS: reduced-motion flag + timer-driven animation guards
rep("const slides=$$('.slide'), N=slides.length;",
    "const slides=$$('.slide'), N=slides.length;\nconst RM=matchMedia('(prefers-reduced-motion: reduce)').matches;")
rep("function T(fn,ms){const id=setTimeout(fn,ms);timers.push(id);return id}",
    "function T(fn,ms){const id=setTimeout(fn,RM?0:ms);timers.push(id);return id}")
# typewriter — route through T() so reduced-motion renders final state instantly
rep("timers.push(setTimeout(tick,34+Math.random()*40));", "T(tick,34+Math.random()*40);")
rep("caret.remove();li++;timers.push(setTimeout(typeLine,li===S1LINES.length?400:620));",
    "caret.remove();li++;T(typeLine,li===S1LINES.length?400:620);")
rep("timers.push(setTimeout(typeLine,700));", "T(typeLine,700);")
rep("const caret=document.createElement('span');caret.className='caret';div.appendChild(caret);",
    "const caret=document.createElement('span');caret.className='caret';caret.setAttribute('aria-hidden','true');div.appendChild(caret);")
# paradox Enter/Space parity
rep("pz.addEventListener('mouseenter',()=>s2.classList.add('show-costs'));",
    "pz.addEventListener('mouseenter',()=>s2.classList.add('show-costs'));\npz.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();s2.classList.add('show-costs')}});")
# 6R ring: no idle auto-rotate under reduced motion (nodes stay clickable)
rep("function restartR6(){clearInterval(r6int);r6int=setInterval(()=>r6select((r6sel+1)%6),2800)}",
    "function restartR6(){clearInterval(r6int);if(RM)return;r6int=setInterval(()=>r6select((r6sel+1)%6),2800)}")
# funnel: render final numbers instantly under reduced motion
rep("  void $('#funnel').offsetWidth; // restart transitions",
    "  if(RM){rows.forEach(r=>{r.classList.add('go');r.querySelector('.fnum').textContent=r.dataset.final});return}\n  void $('#funnel').offsetWidth; // restart transitions")
# struggle %: snap to final under reduced motion
rep("let p=0;const iv=setInterval(()=>{p+=5;", "let p=0;const iv=setInterval(()=>{p+=RM?100:5;")
# overview cards: button semantics + Enter/Space jump
rep("const c=document.createElement('div');c.className='ovcard';c.dataset.i=i;",
    "const c=document.createElement('div');c.className='ovcard';c.dataset.i=i;\n  c.setAttribute('role','button');c.tabIndex=0;c.setAttribute('aria-label','Go to slide '+(i+1)+' — '+s.dataset.title);")
rep("c.addEventListener('click',e=>{e.stopPropagation();go(i);toggleOv()});",
    "c.addEventListener('click',e=>{e.stopPropagation();go(i);toggleOv()});\n  c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();go(i);toggleOv()}});")
# subject cards: aria-pressed stays in sync with selection
rep("subjBtns.forEach(b=>b.classList.toggle('sel',b.dataset.s===k));",
    "subjBtns.forEach(b=>{b.classList.toggle('sel',b.dataset.s===k);b.setAttribute('aria-pressed',b.dataset.s===k)});")
# script button: accessible name
rep("sb.textContent='SCRIPT';sb.addEventListener",
    "sb.textContent='SCRIPT';sb.setAttribute('aria-label','Speaker script for this slide');sb.addEventListener")

# (5) CSS: focus rings, pointer parity, 36px script-button target, reduced-motion media query
A11Y_CSS = '''
  /* ---------- a11y: focus rings + pointer parity ---------- */
  button{cursor:pointer}
  :focus-visible{outline:3px solid #b45309;outline-offset:2px}
  .q.paradox:focus-visible,.ovcard:focus-visible,.demolink a:focus-visible,
  .node:focus-visible,.subj:focus-visible,.scriptbtn:focus-visible,.replay:focus-visible{
    outline:3px solid #b45309;outline-offset:2px}
  .scriptbtn{min-height:36px;padding:9px 16px}
  /* ---------- reduced motion ---------- */
  @media (prefers-reduced-motion:reduce){
    *{animation-duration:.01s!important;animation-delay:0s!important;animation-iteration-count:1!important;
      transition-duration:.05s!important}
    .caret,#questChip.warn,.q.paradox,.glowbadge,.typing i{animation:none!important}
  }
'''
rep('</style>', A11Y_CSS + '</style>')

# ---------------- JS index updates for 15 slides ----------------
rep("storybar.classList.toggle('show',cur<=10)", "storybar.classList.toggle('show',cur<=11)")
rep('const isApp=i>=11', 'const isApp=i>=12')
rep('<div id="counter">1 / 14</div>', '<div id="counter">1 / 15</div>')

# ---------------- LIGHT THEME: inline colors ----------------
rep('style="--sc:#3ddc97"', 'style="--sc:#047857"')
rep('style="--sc:#5aa9ff"', 'style="--sc:#2563eb"')
rep('style="--sc:#9d7bff"', 'style="--sc:#7c3aed"')
rep('style="--sc:#ffb02e"', 'style="--sc:#b45309"')
rep('color:#ff9d9d;font-weight:700">FULL ANSWER', 'color:#dc2626;font-weight:700">FULL ANSWER')

# ---------------- LIGHT THEME: global overrides (appended last, wins cascade) ----------------
LIGHT = '''
  /* ================= LIGHT THEME ================= */
  :root{
    --bg:#f7f5f0; --bg2:#faf9f6; --card:#ffffff; --card2:#f3f0e8;
    --line:#e6e2d8; --line2:#d8d2c4;
    --text:#16213a; --muted:#4d5878; --dim:#68728d;
    --amber:#b45309; --amber2:#b45309; --amberfill:#f2a63a;
    --red:#dc2626; --red2:#dc2626; --green:#047857; --blue:#2563eb; --violet:#7c3aed;
  }
  body{background:#ece9e1;color:#2a3550}
  #stage{background:
    radial-gradient(1100px 620px at 78% -12%, #fdf6e4 0%, transparent 60%),
    radial-gradient(900px 600px at -10% 110%, #f2ecdd 0%, transparent 55%),
    var(--bg)}
  .h{color:var(--text)}
  .tag{background:rgba(255,255,255,.78);border-color:var(--line);color:var(--muted)}
  .tag b{color:var(--amber)}
  .tag.app{border-color:#d9c9e8;color:#7c3aed}.tag.app b{color:#7c3aed}
  #progress{background:linear-gradient(90deg,#f2a63a,#e8890c)}
  #elapsed{background:rgba(255,255,255,.92);border-color:var(--line);color:var(--amber2)}
  #questChip{background:#fdf3df;border-color:#e9cd92;color:#b45309}
  #questChip .qd{color:#a0763a}
  #questChip.warn{background:#fdecec;border-color:#f0b6b6;color:#dc2626}
  #questChip.warn .qd{color:#dc2626}
  @keyframes qpulse{50%{border-color:#dc2626;box-shadow:0 0 14px rgba(220,38,38,.4)}}
  /* S1 / S11 laptop — light chrome */
  .screen{background:#f4f6fb;border-color:#d9dee8}
  .chrome{background:#eceef3;border-bottom-color:#d9dee8}
  .dots i{background:#ccd2e0}.dots i:first-child{background:#f0b8b8}
  .tabbar{background:#e7eaf2}
  .tab{color:var(--dim);background:#e9edf5;border-color:#d4dae6}
  .tab.on{color:var(--text);background:#f4f6fb;border-color:#c3ccdd}
  .tab .dot{background:var(--amberfill)}
  .display{background:#f4f6fb;color:#2a3550}
  .display .tl-line.dim{color:var(--muted)}
  .caret{background:var(--amberfill)}
  .base{background:linear-gradient(#dfe3ec,#cdd3e0)}
  .base:after{background:#c2c9d8}
  /* S2 quadrant */
  .quad{border-color:var(--line)}
  .q{border-color:#e6e2d8}
  .q.tl{background:#f4f1ea}.q.tr{background:#e7f5ee}.q.bl{background:#faf9f6}
  .q.paradox{background:#fdecec}
  @keyframes pz{0%,100%{box-shadow:inset 0 0 0 0 rgba(220,38,38,0)}50%{box-shadow:inset 0 0 42px 4px rgba(220,38,38,.3)}}
  .minh{color:#dc2626}
  .cost{border-color:#f0c4c4;background:#fdf0f0}
  /* S3 quest card */
  .qcard{background:#fff;border-color:#e6e2d8;box-shadow:0 24px 60px rgba(22,33,58,.12)}
  .qcard-h{background:#fdf3df;border-bottom-color:#ecd9a8;color:var(--amber2)}
  .qcard-b .obj{color:var(--text)}
  .begin{background:var(--amberfill);color:#241300}
  /* S4 6R ring */
  .ringline{border-color:#c9cfdd}
  .ringline:after{background:radial-gradient(circle at 50% 50%, rgba(242,166,58,.12), transparent 65%)}
  .node{background:#fff;border-color:#d8d2c4;color:var(--text)}
  .node.sel{background:#fdf3df;border-color:var(--amber);box-shadow:0 0 26px rgba(242,166,58,.4)}
  .node.sel b{color:var(--amber2)}.node.sel small{color:#a0763a}
  /* S5 chat demo — white/green bubbles with borders */
  .chatpane{background:#faf9f6;border-color:var(--line2)}
  .cp-h.l{background:#fdecec;color:#dc2626;border-bottom-color:#f0c4c4}
  .cp-h.r{background:#fdf3df;color:var(--amber2);border-bottom-color:#ecd9a8}
  .msg.s{background:#fff;border:1px solid #d8d2c4;color:#2a3550}
  .msg.s .ts{color:#68728d}
  .msg.ai{background:#e9f6ee;border:1px solid #c9e6d6;color:#2a3550}
  .msg.ok{background:#d9f2e5;border-color:#9fd6bd;color:#047857}
  .msg.typing i{background:#9aa1b5}
  .brain.off path{fill:#cbd1de}
  .sbar{background:#eee9dc}
  .sbar i{background:linear-gradient(90deg,#e8890c,var(--amberfill))}
  .unlockchip{background:var(--amberfill);color:#241300}
  .replay{background:#fff;border-color:var(--line);color:var(--text)}
  .replay:hover{border-color:var(--amber);color:var(--amber2)}
  /* S6 funnel */
  .fbar{background:#eef1f6;border-color:#d8d2c4}
  .frow.hot .fbar{background:linear-gradient(90deg,#f7ddad,#f2c87e);border-color:var(--amber)}
  /* S8 timeline */
  .tl-bar{border-color:var(--line)}
  .tl-seg{border-right-color:rgba(22,33,58,.1)}
  .tl-seg.p1{background:#eef1f6}
  .tl-seg.p2{background:linear-gradient(90deg,#f7e5c0,#f3d79b)}
  .tl-seg.p3{background:#eef1f6}
  .costbar .cb{background:#fff;border-color:var(--line2)}
  .costbar .total{background:linear-gradient(160deg,#fdf3df,#fbf0d2);border-color:#e3c98f}
  /* S9 subjects */
  .subj{background:#fff;border-color:var(--line2);color:var(--text)}
  .subj:hover{border-color:#b9c0d4}
  .subj.sel{background:#faf7ee}
  .reskin{background:#fff;border-color:var(--line2)}
  .r6row i{background:#eee9dc;color:var(--muted);border-color:var(--line2)}
  .r6row i.on{color:#fff}
  .roadmap .rm{background:#fff;border-color:var(--line2);color:var(--muted)}
  .roadmap .rm.on{background:#fdf3df;color:var(--amber2);border-color:#e3c98f}
  /* S10 checklist */
  .ckcol{background:#fff;border-color:var(--line2)}
  .ckcol.r2{background:linear-gradient(160deg,#fffdf4,#fbf3df);border-color:#e3c98f}
  .ckcol.r2 .ck li{color:var(--text)}
  .ckcol.r2 .ck li .box{border-color:var(--amber);background:rgba(242,166,58,.18)}
  .ckcol.r2 .ck li .box:after{border-color:var(--amber)}
  .ck li .box{border-color:#a8b0c0}
  /* S11 close */
  .contact{background:#fff;border-color:var(--line2)}
  .demolink{background:#fff;border-color:var(--line2)}
  .qrtile{border:1px solid var(--line)}
  .demolink a{color:var(--amber2);border-bottom-color:#e3c98f}
  /* appendix */
  .qa{background:#fff;border-color:var(--line2)}
  .qa .qq .own{color:var(--amber);border-color:#e3c98f;background:#fdf3df}
  .cite{background:#fff;border-color:var(--line2)}
  .evid-foot{border-left-color:var(--amber)}
  table.pos th{background:#f0ede4;color:var(--muted)}
  table.pos th,table.pos td{border-color:var(--line2)}
  table.pos th.ep,table.pos td.ep{background:#fdf3df;border-color:#e3c98f}
  table.pos td.k{color:var(--text);background:#f5f2ea}
  /* overlays */
  .overlay{background:rgba(38,34,24,.55)}
  #notesPanel{background:#fffdf7;border-left-color:var(--line2)}
  #notesPanel h2{color:var(--text)}
  #notesPanel p.script{color:#3c4763}
  .ovcard{background:#fff;border-color:var(--line2)}
  .ovcard:hover{border-color:var(--amber)}
  .ovcard.cur{border-color:var(--amber);box-shadow:0 0 0 2px rgba(242,166,58,.3)}
  .ovcard .t{color:var(--text)}
  /* ---------- billboard layout ---------- */
  .s3-wrap,.s4-wrap{justify-content:center}
  .s6-cue{font-size:24px}
  .stack .tot{font-size:30px}
  .fnote{font-size:13px;color:var(--dim);margin-top:14px;line-height:1.4}
  .engflow{display:flex;flex-direction:column;gap:9px}
  .engflow .en{background:#fff;border:1.5px solid #e3c98f;border-radius:10px;padding:12px 16px;
    font-size:18px;font-weight:700;color:var(--text)}
  .engflow .e-arr{color:var(--dim);font-size:13px;font-weight:700;padding-left:18px;line-height:1}
  /* ---------- S5 XP toast + S10 KPI chip ---------- */
  .msg.xp{align-self:center;max-width:100%;background:#fdf3df;border:1.5px solid var(--amberfill);
    color:#b45309;font-size:14.5px;letter-spacing:.03em;padding:9px 18px;border-radius:999px;
    animation:xppop .5s cubic-bezier(.2,1.4,.3,1) forwards;opacity:0;transform:scale(.6)}
  @keyframes xppop{to{opacity:1;transform:scale(1)}}
  .kpirow{display:flex;margin-top:16px}
  .kchip{font-size:14.5px;font-weight:700;color:var(--muted);background:#fff;
    border:1px solid var(--line2);border-radius:999px;padding:9px 18px}
  .kchip b{color:var(--green)}.kchip i{font-style:normal;color:var(--dim)}
  /* ---------- per-slide Script button ---------- */
  .scriptbtn{position:absolute;right:64px;bottom:34px;z-index:40;font-family:inherit;
    font-size:12px;font-weight:800;letter-spacing:.12em;color:var(--muted);
    background:rgba(255,255,255,.78);border:1px solid var(--line);border-radius:999px;
    padding:6px 14px;cursor:pointer;transition:border-color .2s,color .2s}
  .scriptbtn:hover{border-color:var(--amber);color:var(--amber)}
'''
rep('</style>', LIGHT + '</style>')

# ================ PASS 3: bottom-dock script panel + citations + trims ================

# --- A. teleprompter: notes become a flat bottom dock; stage shrinks above it ---
# markup: drop the fullscreen .overlay wrapper (post-a11y string)
rep('<div class="overlay" id="notesOv" role="dialog" aria-modal="true" aria-label="Speaker notes">',
    '<div id="notesOv" role="dialog" aria-label="Speaker notes">')
# CSS: replace the old right-rail panel block (np-k/np-sec already bumped to 12px by a11y pass)
rep('''  #notesOv{justify-content:flex-end}
  #notesPanel{width:560px;max-width:92vw;background:#0c1226;border-left:1px solid var(--line);height:100%;
    padding:34px 38px;overflow-y:auto;font-size:15px}
  #notesPanel .np-k{font-size:12px;font-weight:800;letter-spacing:.18em;color:var(--amber);margin-bottom:10px}
  #notesPanel h2{font-size:24px;line-height:1.25;margin-bottom:14px}
  #notesPanel .np-meta{display:flex;gap:14px;margin-bottom:18px;font-size:13px;color:var(--muted)}
  #notesPanel .np-meta b{color:var(--amber2)}
  #notesPanel .np-sec{font-size:12px;font-weight:800;letter-spacing:.16em;color:var(--dim);margin:18px 0 8px}
  #notesPanel .np-cue{font-size:17px;line-height:1.5;color:var(--text);border-left:3px solid var(--amber);padding-left:14px;margin-bottom:6px}
  #notesPanel p.script{font-size:15px;line-height:1.55;color:#c6cde8;margin-bottom:10px}
  #notesPanel .np-tip{margin-top:20px;font-size:12.5px;color:var(--dim);border-top:1px solid var(--line);padding-top:14px;line-height:1.6}''',
    '''  /* ---------- bottom-dock speaker panel (teleprompter) ---------- */
  #notesOv{position:fixed;left:0;right:0;bottom:0;height:32vh;min-height:200px;z-index:200;
    display:none;background:#fffdf7;border-top:3px solid var(--amberfill);
    box-shadow:0 -14px 44px rgba(22,33,58,.28)}
  #notesOv.open{display:flex}
  #notesPanel{flex:1;display:flex;gap:30px;padding:14px 28px 10px;overflow:hidden;font-size:15px}
  #notesPanel .np-side{flex:0 0 280px;overflow:hidden}
  #notesPanel .np-main{flex:1;min-width:0;overflow-y:auto;padding-right:8px}
  #notesPanel .np-k{font-size:12px;font-weight:800;letter-spacing:.18em;color:var(--amber);margin-bottom:6px}
  #notesPanel h2{font-size:19px;line-height:1.2;margin-bottom:8px}
  #notesPanel .np-meta{display:flex;flex-wrap:wrap;gap:6px 14px;margin-bottom:8px;font-size:13px;color:var(--muted)}
  #notesPanel .np-meta b{color:var(--amber2)}
  #notesPanel .np-sec{font-size:12px;font-weight:800;letter-spacing:.16em;color:var(--dim);margin:10px 0 5px}
  #notesPanel .np-cue{font-size:13.5px;line-height:1.45;color:var(--text);border-left:3px solid var(--amber);padding-left:12px}
  #notesPanel p.script{font-size:15.5px;line-height:1.5;color:#3c4763;margin-bottom:8px}
  #notesPanel .np-tip{margin-top:12px;font-size:12.5px;color:var(--dim);border-top:1px solid var(--line);padding-top:10px;line-height:1.5}
  #notesPanel .np-x{flex:0 0 auto;align-self:flex-start;width:38px;height:38px;border-radius:9px;
    border:1px solid var(--line);background:#fff;font-size:20px;font-weight:800;color:var(--muted);cursor:pointer}
  #notesPanel .np-x:hover{border-color:var(--amber);color:var(--amber)}''')
# renderNotes: two columns — meta/cue left, script+tip right, close button
rep('''  notesPanel.innerHTML='<div class="np-k">SPEAKER NOTES — SLIDE '+(cur+1)+' / '+N+'</div>'+
   '<h2>'+d.title+'</h2>'+
   '<div class="np-meta"><span>Speaker: <b>'+d.who+'</b></span><span>Target: <b>'+d.time+'</b></span><span>'+d.tag+'</span></div>'+
   '<div class="np-sec">CUE</div><div class="np-cue">'+d.cue+'</div>'+
   (d.script.length?'<div class="np-sec">SCRIPT</div>'+d.script.map(s=>'<p class="script">'+s+'</p>').join(''):'')+
   (d.tip?'<div class="np-tip">'+d.tip+'</div>':'');''',
    '''  notesPanel.innerHTML='<div class="np-side"><div class="np-k">SCRIPT — '+(cur+1)+' / '+N+'</div>'+
   '<h2>'+d.title+'</h2>'+
   '<div class="np-meta"><span><b>'+d.who+'</b></span><span>target <b>'+d.time+'</b></span><span>'+d.tag+'</span></div>'+
   '<div class="np-sec">CUE</div><div class="np-cue">'+d.cue+'</div></div>'+
   '<div class="np-main">'+(d.script.length?d.script.map(s=>'<p class="script">'+s+'</p>').join(''):'<p class="script" style="color:var(--dim)">No script — Q&amp;A backup slide.</p>')+
   (d.tip?'<div class="np-tip">'+d.tip+'</div>':'')+'</div>'+
   '<button class="np-x" aria-label="Close script panel" onclick="toggleNotes()">&times;</button>';''')
# toggleNotes: focus the close button on open; refit stage so the slide stays fully visible
rep("function toggleNotes(){notesOpen=!notesOpen;notesOv.classList.toggle('open',notesOpen);if(notesOpen)renderNotes()}",
    "function toggleNotes(){notesOpen=!notesOpen;notesOv.classList.toggle('open',notesOpen);"
    "if(notesOpen){renderNotes();setTimeout(()=>{const b=notesPanel.querySelector('.np-x');b&&b.focus()},0)}fit()}")
# fit(): subtract the dock height so the whole slide renders above the panel
rep('''function fit(){
  const s=Math.min(innerWidth/1280,innerHeight/720);
  stage.style.transform='scale('+s+')';
  stage.style.left=((innerWidth-1280*s)/2)+'px';
  stage.style.top=((innerHeight-720*s)/2)+'px';
}''',
    '''function fit(){
  const nEl=document.getElementById('notesOv');
  const availH=innerHeight-((nEl&&nEl.classList.contains('open'))?nEl.offsetHeight:0);
  const s=Math.min(innerWidth/1280,availH/720);
  stage.style.transform='scale('+s+')';
  stage.style.left=((innerWidth-1280*s)/2)+'px';
  stage.style.top=((availH-720*s)/2)+'px';
}''')
# light-theme override: panel bg now lives on #notesOv
rep('#notesPanel{background:#fffdf7;border-left-color:var(--line2)}',
    '#notesOv{background:#fffdf7}')

# --- B. storybar -> current beat only; hint hidden behind H/? toggle ---
rep('''storybar.innerHTML=BEATS.map((b,i)=>'<span class="b" data-b="'+i+'">'+b.toUpperCase()+'</span>')
  .join('<span class="sep">—</span>');
function renderStory(){
  storybar.classList.toggle('show',cur<=11);
  [...storybar.querySelectorAll('.b')].forEach((el,i)=>{
    el.className='b'+(i<cur?' done':i===cur?' now':'');
  });
}''',
    '''function renderStory(){
  storybar.classList.toggle('show',cur<=11);
  storybar.innerHTML=cur<=11?'<span class="b now">'+BEATS[cur].toUpperCase()+'</span>':'';
}''')
rep('#hint{position:absolute;left:20px;bottom:14px;font-size:12px;color:var(--dim);opacity:.5;z-index:60;letter-spacing:.03em}',
    '#hint{position:absolute;left:20px;bottom:14px;font-size:12px;color:var(--dim);opacity:0;z-index:60;letter-spacing:.03em;transition:opacity .2s}\n'
    '  #hint.show{opacity:.55}')
rep('<div id="hint">← → navigate · N notes · T timer · O overview · F fullscreen</div>',
    '<div id="hint">← → navigate · N script · T timer · O overview · F fullscreen · H hide</div>')
rep("else if(k==='f'||k==='F'){toggleFs()}",
    "else if(k==='f'||k==='F'){toggleFs()}\n  else if(k==='h'||k==='H'||k==='?'){document.getElementById('hint').classList.toggle('show')}")

# --- C. research citations: expand appendix B into 4 clusters + inline cite chips ---
rep('''      <div style="margin-top:8px">
        <div class="cite rise" style="--d:.15s"><div class="who">Roediger &amp; Karpicke, 2006</div><div class="claim"><b>Retrieval &gt; re-exposure.</b> Test-enhanced learning — pulling from memory beats re-reading. → RECALL</div></div>
        <div class="cite rise" style="--d:.25s"><div class="who">Cepeda et al., 2006</div><div class="claim"><b>Spacing &gt; cramming.</b> Distributed practice outperforms massed study. → RETURN</div></div>
        <div class="cite rise" style="--d:.35s"><div class="who">Freeman et al., 2014</div><div class="claim"><b>Active generation &gt; passive ingestion.</b> Active learning lifts STEM outcomes (PNAS meta-analysis). → REACH</div></div>
        <div class="cite rise" style="--d:.45s"><div class="who">Deci &amp; Ryan</div><div class="claim"><b>Autonomy drives motivation.</b> Self-determination theory — agency over compliance. → the loop itself</div></div>
        <div class="cite rise" style="--d:.55s"><div class="who">Fredrickson</div><div class="claim"><b>Small wins compound.</b> Broaden-and-build — positive momentum widens engagement. → 5-minute completable reps</div></div>
      </div>''',
    '''      <div class="citegrid">
        <div class="cgroup rise" style="--d:.15s">
          <div class="cg-h">RETRIEVAL &amp; SPACING</div>
          <div class="cite"><div class="who">Roediger &amp; Karpicke, 2006</div><div class="claim"><b>Retrieval &gt; re-reading.</b> → RECALL</div></div>
          <div class="cite"><div class="who">Cepeda et al., 2006</div><div class="claim"><b>Spacing &gt; cramming.</b> → RETURN</div></div>
          <div class="cite"><div class="who">Dunlosky et al., 2013</div><div class="claim"><b>Testing + spacing = top-utility techniques.</b> → the loop</div></div>
        </div>
        <div class="cgroup rise" style="--d:.25s">
          <div class="cg-h">STRUGGLE BEFORE HELP</div>
          <div class="cite"><div class="who">Freeman et al., 2014</div><div class="claim"><b>Active learning cuts STEM failure.</b> → REACH</div></div>
          <div class="cite"><div class="who">Kapur — productive failure</div><div class="claim"><b>Struggle first, then instruction sticks.</b> → Answer Shield</div></div>
        </div>
        <div class="cgroup rise" style="--d:.35s">
          <div class="cg-h">MICRO-LEARNING &amp; MOTIVATION</div>
          <div class="cite"><div class="who">RCT, 2025 — 5-min modules</div><div class="claim"><b>+23% retention vs one-day workshop.</b> → quest format</div></div>
          <div class="cite"><div class="who">Deci &amp; Ryan</div><div class="claim"><b>Autonomy drives motivation.</b> → no pay-to-skip</div></div>
          <div class="cite"><div class="who">Fredrickson</div><div class="claim"><b>Small wins compound.</b> → completable reps</div></div>
        </div>
        <div class="cgroup rise" style="--d:.45s">
          <div class="cg-h">GAMIFICATION &amp; AI RISK</div>
          <div class="cite"><div class="who">Sailer &amp; Homner, 2020</div><div class="claim"><b>Gamification g=.49 cognitive; fiction helps.</b> → XP + characters</div></div>
          <div class="cite"><div class="who">Zhang et al., 2024</div><div class="claim"><b>ChatGPT dependency → weaker critical thinking.</b> → the problem</div></div>
          <div class="cite"><div class="who">Zhai et al., 2024</div><div class="claim"><b>AI overreliance erodes reasoning.</b> → why the shield</div></div>
        </div>
      </div>''')
# inline cite chips (direct children of .slide, mirrored against the SCRIPT button)
rep('''    </section>

    <!-- ============ S3 — SOLUTION ============ -->''',
    '''      <div class="citechip">AI overreliance → weaker critical thinking · <b>Zhai et al., 2024</b></div>
    </section>

    <!-- ============ S3 — SOLUTION ============ -->''')
rep('''    </section>

    <!-- ============ S4 — 6R LOOP ============ -->''',
    '''      <div class="citechip">5-min micro-sessions → +23% retention vs workshop · <b>RCT, 2025</b></div>
    </section>

    <!-- ============ S4 — 6R LOOP ============ -->''')
rep('''    </section>

    <!-- ============ S6 — MARKET ============ -->''',
    '''      <div class="citechip">gamification meta-analysis g = 0.49 · <b>Sailer &amp; Homner, 2020</b></div>
    </section>

    <!-- ============ S6 — MARKET ============ -->''')
CITE_CSS = '''
  .citegrid{display:grid;grid-template-columns:1fr 1fr;gap:10px 26px;margin-top:12px}
  .cg-h{font-size:12px;font-weight:800;letter-spacing:.16em;color:var(--amber);margin-bottom:7px}
  .cite{display:flex;gap:12px;align-items:baseline;padding:8px 12px;background:var(--card2);
    border:1px solid var(--line);border-radius:9px;margin-bottom:6px}
  .cite .who{flex:0 0 180px;font-size:13.5px;font-weight:800;color:var(--amber2)}
  .cite .claim{font-size:13.5px;color:var(--muted);line-height:1.35}
  .cite .claim b{color:var(--text)}
  .citechip{position:absolute;left:64px;bottom:34px;z-index:40;font-size:12px;
    font-weight:700;color:var(--dim);letter-spacing:.02em}
  .citechip b{color:var(--amber2);font-weight:800}
'''
rep('</style>', CITE_CSS + '</style>')

if fails:
    print('FAILED ANCHORS:'); [print(' ', f) for f in fails]; sys.exit(1)

open(DST, 'w', encoding='utf-8').write(s)
print('written:', DST, len(s.encode()), 'bytes')
