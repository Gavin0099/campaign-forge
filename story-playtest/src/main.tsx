declare const inkjs: { Story: new (json: unknown) => any };
declare const CAMPAIGN_STORY: unknown;
declare const BUILD_INFO: { sourceHash: string; builtAt: string };
declare const REPLAY_ROUTES: Record<string, { route: number[]; state: Record<string, unknown> }>;

type Line = { text: string; speaker: string; scene: string; objective: boolean };
type Entry = { index: number; text: string };
type View = { lines: Line[]; choices: Entry[]; ended: boolean };
const sceneNames: Record<string, string> = {
  L01_pre: '燈芯屋・雨夜', L01_post: '燈火以外', L02_pre: '沼澤燈徑', L02_post: '最後一船',
  L03_pre: '渡口閘門', L03_post: '閘門之後', L04_pre: '高道上的追兵', L04_post: '今晚的燈芯屋',
  L05_pre: '廢塔的燈號', L05_post: '放漿果的人', L06_pre: '懸空書庫', L06_post: '紙星星',
  L07_pre: '塔頂星室', L07_post: '斷崖下的黎明',
};
let story: any;
let lastScene = '';
let currentSpeaker = '';
function read(): View {
  const lines: Line[] = [];
  while (story.canContinue) {
    const text = story.Continue().trim();
    let objective = '';
    for (const tag of story.currentTags as string[]) {
      if (tag.startsWith('scene:')) { lastScene = tag.slice(6); currentSpeaker = ''; }
      if (tag.startsWith('speaker:')) currentSpeaker = tag.slice(8);
      if (tag.startsWith('objective:')) objective = tag.slice(10);
    }
    if (objective) lines.push({ text: objective, speaker: '戰況示意', scene: lastScene, objective: true });
    if (text) lines.push({ text, speaker: currentSpeaker, scene: lastScene, objective: false });
  }
  return { lines, choices: story.currentChoices.map((c: any) => ({ index: c.index, text: c.text.replace(/^#sim\s*/, '') })), ended: story.currentChoices.length === 0 };
}
const routeFromUrl = () => {
  const raw = new URL(location.href).searchParams.get('route');
  if (raw === null || raw === '') return [];
  if (new URL(location.href).searchParams.get('source') !== BUILD_INFO.sourceHash) throw Error('路線屬於另一版或未標明版本，請重新開始。');
  if (!/^\d+(,\d+)*$/.test(raw) || raw.length > 1000) throw Error('路線格式不正確，請重新開始。');
  return raw.split(',').map(Number);
};
function start(indices: number[] = []) {
  story = new inkjs.Story(CAMPAIGN_STORY);
  story.onError = (message: string) => { throw Error(message); };
  lastScene = ''; currentSpeaker = '';
  let view = read();
  const log: Entry[] = [];
  for (const index of indices) {
    const choice = view.choices.find(c => c.index === index);
    if (!choice) throw Error('路線與目前劇本不相容，請重新開始。');
    log.push(choice); story.ChooseChoiceIndex(index); view = read();
  }
  return { view, log };
}
function App() {
  const [initial] = React.useState(() => { try { return { ...start(routeFromUrl()), error: '' }; } catch (e) { return { ...start(), error: (e as Error).message }; } });
  const [view, setView] = React.useState<View>(initial.view);
  const [log, setLog] = React.useState<Entry[]>(initial.log);
  const [history, setHistory] = React.useState<{ snapshot: string; view: View; scene: string; speaker: string; log: Entry[] }[]>([]);
  const [error, setError] = React.useState(initial.error);
  const [large, setLarge] = React.useState(false);
  const [exported, setExported] = React.useState(false);
  const heading = React.useRef<HTMLHeadingElement>(null);
  const status = React.useRef<HTMLParagraphElement>(null);
  function focusReading() { requestAnimationFrame(() => { heading.current?.focus(); heading.current?.scrollIntoView({ block: 'start' }); }); }
  function choose(choice: Entry) {
    const snapshot = story.state.ToJson();
    try {
      const previous = { snapshot, view, scene: lastScene, speaker: currentSpeaker, log };
      story.ChooseChoiceIndex(choice.index);
      const next = read();
      setHistory(h => [...h, previous]); setLog(l => [...l, choice]); setView(next); setError(''); setExported(false); focusReading();
    } catch (e) { story.state.LoadJson(snapshot); setError('這一步無法繼續：' + (e as Error).message); }
  }
  function back() {
    const previous = history.at(-1); if (!previous) return;
    story.state.LoadJson(previous.snapshot); lastScene = previous.scene; currentSpeaker = previous.speaker;
    setView(previous.view); setLog(previous.log); setHistory(h => h.slice(0, -1)); setError(''); focusReading();
  }
  function restart() {
    const next = start(); setView(next.view); setLog([]); setHistory([]); setError(''); setExported(false);
    historyReplace(''); focusReading();
  }
  function exportLog() {
    const route = log.map(x => x.index);
    const url = new URL(location.href); url.searchParams.set('route', route.join(','));
    url.searchParams.set('source', BUILD_INFO.sourceHash);
    const data = { format: 'campaign-forge-route-v1', sourceHash: BUILD_INFO.sourceHash, route, choices: log, replay: url.href, reviewer: 'UNRECORDED', humanFeedback: null };
    const href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a'); link.href = href; link.download = '碑誓-選項紀錄.json'; link.click();
    setTimeout(() => URL.revokeObjectURL(href), 1000); setExported(true); status.current?.focus();
  }
  function historyReplace(route: string) { const url = new URL(location.href); if (route) { url.searchParams.set('route', route); url.searchParams.set('source', BUILD_INFO.sourceHash); } else { url.searchParams.delete('route'); url.searchParams.delete('source'); } window.history.replaceState(null, '', url); }
  function replay(key: string) {
    try { const sample = REPLAY_ROUTES[key]; const next = start(sample.route); setView(next.view); setLog(next.log); setHistory([]); setError(''); historyReplace(sample.route.join(',')); focusReading(); }
    catch(e) { setError((e as Error).message); }
  }
  const result = view.ended ? {
    gate: story.variablesState.$('k1_gate') === 'open' ? '開閘：提歐生還，筆記沉河' : '封閘：保住筆記，提歐失蹤',
    protected: ({ quin: '小昆隨隊撤出；星盤被帶走', starplate: '保住星盤；小昆被帶走', sawin: '護住薩溫；小昆與星盤被帶走' } as Record<string, string>)[story.variablesState.$('l07_protected')],
    nameKey: story.EvaluateFunction('name_key') ? '隊伍仍持有名鑰資料' : '隊伍失去現有名鑰資料，必須另找線索',
    thoma: story.variablesState.$('thoma_public') ? '托瑪拒絕收魂，並公開作證' : '托瑪拒絕收魂，仍不敢公開作證',
  } : null;
  return <div className={large ? 'app large' : 'app'}>
    <a className="skip" href="#reading">跳到故事</a>
    <header><div><p className="eyebrow">CAMPAIGN FORGE · 文字試讀</p><h1>碑誓<span>渡口之夜 — 灰燈廢塔</span></h1></div><p className="edition">L01–L07 工作稿<br />故事與規則尚待確認</p></header>
    <nav aria-label="閱讀工具"><button onClick={back} disabled={!history.length}>回上個選項</button><button onClick={restart}>重新開始</button><button aria-pressed={large} onClick={() => setLarge(!large)}>放大文字</button><button onClick={exportLog}>匯出選項紀錄</button></nav>
    <p className="notice">黑暗奇幻故事，包含失蹤、亡魂與犧牲。戰況以文字示意；你能選擇對話、重大抉擇與模擬戰果。</p>
    <p ref={status} tabIndex={-1} role="status" className="status">{exported ? '選項紀錄已交給瀏覽器下載。' : `已作出 ${log.length} 次選擇`}</p>
    {error && <p role="alert" className="error">{error}</p>}
    <main id="reading"><h2 ref={heading} tabIndex={-1}>{view.ended ? '黎明之後' : sceneNames[view.lines[0]?.scene] || '渡口之夜'}</h2>
      <article aria-label="故事正文">{view.lines.map((line, i) => <React.Fragment key={i}>
        {i > 0 && line.scene !== view.lines[i - 1].scene && <h3>{sceneNames[line.scene] || line.scene}</h3>}
        <div className={line.objective ? 'battle' : 'line'}>{line.speaker && (i === 0 || line.speaker !== view.lines[i - 1].speaker || line.objective) && <p className="speaker">{line.speaker}</p>}<p>{line.text}</p></div>
      </React.Fragment>)}</article>
      <section className="choices" aria-label="目前選項">{view.choices.map(c => <button key={c.index} onClick={() => choose(c)}>{c.text}<span aria-hidden="true"> ↗</span></button>)}</section>
      {result && <section className="consequences"><h3>這條路留下的事</h3><p>{result.gate}</p><p>{result.protected}</p><p>{result.nameKey}</p><p>{result.thoma}</p><p>下一章尚未開放。你可以回到上一個選項，或匯出這次的選擇與試讀意見一起回傳。</p></section>}
    </main>
    <aside><details><summary>本次選項紀錄（{log.length}）</summary><ol>{log.map((c, i) => <li key={i}>{c.text}</li>)}</ol>{!log.length && <p>尚未作出選擇。</p>}</details>
    <details><summary>路線比較（含劇透）</summary><p>直接重播完整選項序列到章末，不代表人類試讀。</p><div className="route-list">{Object.keys(REPLAY_ROUTES).filter(k => k.endsWith('public=false')).map(k => {
      const [gate, who, sheltered] = k.split('|');
      return <button key={k} onClick={() => replay(k)}>{gate === 'open' ? '開閘' : '封閘'}／{({quin:'救小昆', starplate:'救星盤', sawin:'護薩溫'} as Record<string,string>)[who]}／{sheltered.endsWith('true') ? '收留薩溫' : '拒收薩溫'}</button>;
    })}</div></details></aside>
    <footer>這是故事試讀，並非完整戰棋遊戲。<br />試讀稿識別 {BUILD_INFO.sourceHash.slice(0, 12)}</footer>
  </div>;
}
const client = ReactDOM as unknown as { createRoot: (element: HTMLElement) => { render: (node: React.ReactNode) => void } };
client.createRoot(document.getElementById('root')!).render(<App />);
