import { CSSProperties, useEffect, useRef, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { artwork, Choice, mapRows, scenario, Screen, unitSeeds } from './data'
import './style.css'

function Portrait({id, large=false}: {id:string;large?:boolean}) { return <span role="img" aria-label={`${scenario.party.find(p=>p.id===id)?.name || id}・展示人物美術`} className={`${large ? 'character-art' : 'portrait'} art-${id}`} /> }

type Unit = (typeof unitSeeds)[number] & { acted?: boolean }
type Point = { x: number; y: number }
type Phase = 'select' | 'move' | 'skill' | 'confirm'
const same = (a: Point, b: Point) => a.x === b.x && a.y === b.y
const distance = (a: Point, b: Point) => Math.abs(a.x - b.x) + Math.abs(a.y - b.y)
const key = (p: Point) => `${p.x},${p.y}`
const terrainName = (t: string) => ({ '.': '平地', F: '林地', R: '道路', '~': '河道' }[t] || '地形')

function App() {
  const [screen, setScreen] = useState<Screen>('menu')
  const [returnScreen, setReturnScreen] = useState<Screen>('menu')
  const [choice, setChoice] = useState<Choice | null>(null)
  const [complete, setComplete] = useState(false)
  const [textLarge, setTextLarge] = useState(false)
  const [historyOpen, setHistoryOpen] = useState(false)
  const [partyFocus, setPartyFocus] = useState('shien')
  const [deployed, setDeployed] = useState(['shien', 'lida', 'olun'])
  const [partyLimit, setPartyLimit] = useState(3)
  const [units, setUnits] = useState<Unit[]>(unitSeeds.map(u => ({ ...u })))
  const [selected, setSelected] = useState<string | null>(null)
  const [destination, setDestination] = useState<Point | null>(null)
  const [target, setTarget] = useState<string | null>(null)
  const [phase, setPhase] = useState<Phase>('select')
  const [turn, setTurn] = useState(1)
  const [actions, setActions] = useState(0)
  const [log, setLog] = useState<string[]>(['渡口前線已展開。這是固定資料操作展示。'])
  const [confirmFinish, setConfirmFinish] = useState(false)
  const modalRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    const heading = document.querySelector<HTMLElement>('main h1')
    heading?.setAttribute('tabindex', '-1')
    heading?.focus({ preventScroll: true })
    window.scrollTo(0, 0)
  }, [screen])
  useEffect(() => {
    if (confirmFinish) modalRef.current?.querySelector<HTMLButtonElement>('button')?.focus()
  }, [confirmFinish])

  const choiceData = choice ? scenario.choices[choice] : null
  const actor = units.find(u => u.id === selected)
  const enemy = units.find(u => u.id === target)
  const actorPoint = actor ? { x: actor.x, y: actor.y } : null
  const plannedPoint = destination || actorPoint
  const moveCells = new Set<string>()
  if (actor && phase === 'move') {
    mapRows.forEach((row, y) => [...row].forEach((tile, x) => {
      if (tile !== '~' && distance(actor, { x, y }) <= 3 && !units.some(u => u.hp > 0 && u.x === x && u.y === y)) moveCells.add(key({ x, y }))
    }))
  }
  const skillCells = new Set<string>()
  if (plannedPoint && (phase === 'skill' || phase === 'confirm')) {
    mapRows.forEach((row, y) => [...row].forEach((_, x) => {
      if (distance(plannedPoint, { x, y }) <= 2) skillCells.add(key({ x, y }))
    }))
  }

  function resetDemo() {
    setChoice(null); setComplete(false); setScreen('journey'); setHistoryOpen(false)
    setDeployed(['shien', 'lida', 'olun']); setPartyLimit(3)
    setUnits(unitSeeds.map(u => ({ ...u }))); setSelected(null); setDestination(null); setTarget(null)
    setPhase('select'); setTurn(1); setActions(0); setLog(['渡口前線已展開。這是固定資料操作展示。']); setConfirmFinish(false)
  }
  function back() {
    if (confirmFinish) { setConfirmFinish(false); return }
    if (screen === 'settings') { setScreen(returnScreen); return }
    if (screen === 'battle') { setScreen('deploy'); return }
    if (screen === 'deploy') { setScreen('story'); return }
    if (screen === 'story') { setScreen('camp'); return }
    if (screen === 'camp') { setScreen('journey'); return }
    if (screen === 'result') { setScreen('journey'); return }
    setScreen('menu')
  }
  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if (event.key === 'Escape') { event.preventDefault(); back() }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  })
  function openSettings() { setReturnScreen(screen); setScreen('settings') }
  function choose(c: Choice) { setChoice(c); setScreen('deploy') }
  function toggleDeploy(id: string) {
    setDeployed(current => current.includes(id) ? current.filter(x => x !== id) : current.length < partyLimit ? [...current, id] : current)
  }
  function enterBattle() {
    if (!choice || deployed.length === 0) return
    setUnits(unitSeeds.filter(u => u.side === 'enemy' || deployed.includes(u.id)).map(u => ({ ...u })))
    setSelected(null); setDestination(null); setTarget(null); setPhase('select'); setTurn(1); setActions(0)
    setLog([`${scenario.choices[choice].objective}。固定資料展示開始。`]); setScreen('battle')
  }
  function pickCell(p: Point) {
    const occupant = units.find(u => u.hp > 0 && same(u, p))
    if (phase === 'select') {
      if (occupant?.side === 'ally' && !occupant.acted) { setSelected(occupant.id); setPhase('move'); setDestination(null); setTarget(null) }
      return
    }
    if (phase === 'move' && moveCells.has(key(p))) { setDestination(p); setPhase('skill'); return }
    if (phase === 'skill' && occupant?.side === 'enemy' && skillCells.has(key(p))) { setTarget(occupant.id); setPhase('confirm') }
  }
  function confirmAction() {
    if (!actor || !destination || !enemy || !choice) return
    const updated = units.map(u => {
      if (u.id === actor.id) return { ...u, ...destination, acted: true }
      if (u.id === enemy.id) return { ...u, hp: Math.max(0, u.hp - 3) }
      return u
    })
    setUnits(updated); setLog(current => [`${actor.name}移動後使用「掩護推進」；${enemy.name}承受固定示範效果 3。`, ...current])
    setActions(n => n + 1); setSelected(null); setDestination(null); setTarget(null); setPhase('select')
  }
  function endTurn() {
    setTurn(n => n + 1); setUnits(current => current.map(u => ({ ...u, acted: false })))
    setLog(current => ['回合結束。敵方行動在此展示中省略，所有我方角色恢復可行動。', ...current])
    setSelected(null); setDestination(null); setTarget(null); setPhase('select')
  }
  function finishBattle() {
    if (!choice || actions === 0) return
    setComplete(true); setConfirmFinish(false); setScreen('result')
  }
  const partyMember = scenario.party.find(p => p.id === partyFocus) || scenario.party[0]

  return <div style={Object.fromEntries(Object.entries(artwork).map(([k,v])=>[`--art-${k}`,`url("${v}")`])) as CSSProperties} className={`app ${textLarge ? 'large-text' : ''}`}>
    <header className="topbar">
      <div className="brand"><span className="brand-mark">✦</span><span>CAMPAIGN FORGE <small>介面展示</small></span></div>
      <div className="top-right"><span className="demo-flag">{scenario.label}</span>{screen !== 'settings' && screen !== 'menu' && <button className="quiet" onClick={openSettings} aria-label="閱讀設定">Aa</button>}{screen !== 'menu' && <button className="quiet" onClick={back}>← 返回 <kbd>Esc</kbd></button>}</div>
    </header>

    {screen === 'menu' && <main className="menu-page">
      <div className="menu-art" aria-hidden="true"></div>
      <section className="menu-copy"><div className="eyebrow">一段關於命令與承擔的旅程</div><h1>界碑之外</h1><p>渡口只剩最後一趟船。你帶走誰，另一邊就要自己尋路。</p><div className="menu-actions"><button className="primary" onClick={() => setScreen('journey')}>繼續旅程 <span>→</span></button><button onClick={resetDemo}>開始展示／重設</button><button onClick={openSettings}>設定</button></div><p className="fine">候選 A 僅供介面驗證；故事、人物與規則尚未定案。</p></section>
    </main>}

    {screen === 'journey' && <main className="content-page journey-page">
      <div className="page-heading"><div><div className="eyebrow">戰役旅程 · 章節示意</div><h1>路從渡口展開</h1><p>六章、約 24 個節點僅表示節奏容量，不是正式關卡表。</p></div><div className="chapter-stamp">第 01 章 <strong>名冊之外</strong></div></div>
      <div className="journey-layout"><section className="journey-map" aria-label="六章旅程示意">{scenario.chapters.map((chapter, ci) => <div className={`chapter-row chapter-${ci} ${ci === 0 ? 'active' : ''}`} key={chapter}><span className="chapter-number">{String(ci + 1).padStart(2, '0')}</span><div className="chapter-nodes">{[0,1,2,3].map((i) => <span className={`journey-node ${ci === 0 && i === 0 ? complete ? 'done' : 'current' : 'locked'}`} key={i}>{ci === 0 && i === 0 ? complete ? '✓' : '◆' : '·'}</span>)}</div><div className="chapter-title"><strong>{ci === 0 ? chapter : `第 ${ci+1} 章・未揭露`}</strong><small>{ci === 0 ? '當前章節' : '未揭露路線'}</small></div></div>)}</section>
      <aside className="story-panel"><div className="eyebrow">目前節點</div><h2>{scenario.mission}</h2><p>{complete ? choiceData?.outcome : scenario.premise}</p><div className="divider"/><dl><dt>為何出發</dt><dd>{complete ? choiceData?.next : '實測發現低地仍有人。隊伍必須在裂潮前決定渡口的最後一趟船。'}</dd><dt>先前選擇</dt><dd>{choiceData ? `${choiceData.title}；${choiceData.cost}` : '尚未作出渡口選擇。'}</dd><dt>隊伍狀態</dt><dd>{choiceData?.camp || '席恩、莉妲與奧倫同行。瑪芮仍在渡口安排自己的船。'}</dd></dl><div className="panel-actions"><button className="primary" onClick={() => setScreen('camp')}>{complete ? '查看營地與後果' : '前往營地'} →</button>{complete && <button onClick={resetDemo}>重新開始展示</button>}</div></aside></div>
    </main>}

    {screen === 'camp' && <main className="content-page camp-page"><div className="page-heading"><div><div className="eyebrow">營地 · 北岸歇腳處</div><h1>火光照得到每個人</h1><p>{choiceData?.camp || '船夫在整理纜繩，醫療帳裡仍有空位。今晚的安靜不會維持太久。'}</p></div><button className="primary" onClick={() => setScreen('story')}>前往渡口事件 →</button></div>
      <div className="camp-layout"><div className="camp-scene"><Portrait id={partyFocus} large/><div className="scene-caption">{partyMember.name} · 人物外觀展示提案</div></div><div className="companion-list" aria-label="同伴列表">{scenario.party.map(p => <button key={p.id} className={`companion-row ${partyFocus === p.id ? 'chosen' : ''}`} onClick={() => setPartyFocus(p.id)}><Portrait id={p.id}/><span><strong>{p.name}</strong><small>{p.role}</small></span><span className="arrow">›</span></button>)}</div><section className="companion-detail"><div className="eyebrow">人物檔案 · 展示資料</div><h2>{partyMember.name}</h2><p className="role">{partyMember.role}</p><dl><dt>為何同行</dt><dd>{partyMember.why}</dd><dt>現在擔心</dt><dd>{partyMember.worry}</dd><dt>個人心願</dt><dd>{partyMember.wish}</dd><dt>拒絕條件</dt><dd>{partyMember.limit}</dd><dt>離隊後</dt><dd>{partyMember.leave}</dd><dt>關係與近況</dt><dd>{choice ? partyMember.id === 'olun' && choice === 'residents' ? '有所保留；要求席恩承認守線風險。' : partyMember.id === 'lida' && choice === 'grain' ? '有所保留；要求回渡口尋人。' : '仍同行；會記得渡口的命令。' : '信任仍在建立；渡口的決定尚未發生。'}</dd></dl><div className="slots"><span>裝備：展示占位</span><span>技能：掩護推進（模擬）</span></div></section></div>
    </main>}

    {screen === 'story' && <main className="content-page story-page"><div className="page-heading"><div><div className="eyebrow">劇情事件 · {scenario.chapter}</div><h1>渡口的最後一趟船</h1></div><button onClick={() => setHistoryOpen(v => !v)}>{historyOpen ? '收起' : '展開'}對白紀錄</button></div><div className="story-stage"><div className="story-background"><Portrait id="shien" large/><div className="scene-caption">低地渡口 · 場景與人物展示提案</div></div><section className="dialogue-box"><div className="speaker">席恩</div><p>船還能再走一趟。名冊與岸上的人不一致，我們現在就得改令。</p>{historyOpen && <div className="dialogue-history">{scenario.dialogue.map((d, i) => <p key={i}><strong>{d.speaker}：</strong>{d.line}</p>)}</div>}</section></div><div className="choice-layout"><section className="known-panel"><h2>作決定前已知</h2><ul>{scenario.known.map(k => <li key={k}>{k}</li>)}</ul><p className="fine">裂潮抵達時間有誤差；未選一方的結果未知。</p></section><section className="choice-panel"><div className="eyebrow">你的命令 · 兩者都需付代價</div>{(['residents','grain'] as Choice[]).map(c => <button key={c} className={`choice-button ${choice === c ? 'selected-choice' : ''}`} onClick={() => choose(c)}><strong>{scenario.choices[c].title} <span>→</span></strong><small>可預期：{scenario.choices[c].gain}<br/>代價：{scenario.choices[c].cost}</small></button>)}</section></div></main>}

    {screen === 'deploy' && <main className="content-page deploy-page"><div className="page-heading"><div><div className="eyebrow">戰前部署 · 固定示範資料</div><h1>{scenario.mission}</h1><p>{choiceData?.objective || scenario.premise}</p></div><button className="primary" disabled={!choice || deployed.length === 0} onClick={enterBattle}>確認出發 →</button></div><div className="deploy-layout"><section className="brief-panel"><h2>任務簡報</h2><dl><dt>緣由</dt><dd>{scenario.premise}</dd><dt>勝利展示條件</dt><dd>完成至少一次移動與技能確認後，確認護送抵達北岸。</dd><dt>失敗條件</dt><dd>此 UI 原型未模擬失敗判定；正式規則待定。</dd><dt>地形</dt><dd>道路、林地、河道；河道在展示中不可走。</dd><dt>支援</dt><dd>{choiceData?.support || '由渡口選擇決定'}</dd><dt>目前代價</dt><dd>{choiceData?.cost || '尚未選擇'}</dd></dl><button onClick={() => setScreen('story')}>← 返回修改命令</button></section><section className="deployment-panel"><div className="section-title"><h2>選擇出戰者</h2><label>展示名額 <select value={partyLimit} onChange={e => { const n = Number(e.target.value); setPartyLimit(n); setDeployed(p => p.slice(0,n)) }}><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></label></div><p className="fine">{deployed.length} / {partyLimit} 人；席恩可留營，以下只驗證介面狀態，不設定正式隊伍規則。</p>{scenario.party.slice(0,3).map(p => <label key={p.id} className="deploy-unit"><input type="checkbox" checked={deployed.includes(p.id)} onChange={() => toggleDeploy(p.id)} disabled={!deployed.includes(p.id) && deployed.length >= partyLimit}/><Portrait id={p.id}/><span><strong>{p.name}</strong><small>{p.role}</small></span><span className="deploy-slot">{deployed.includes(p.id) ? `部署位 ${scenario.party.findIndex(m => m.id === p.id)+1}` : '待命'}</span></label>)}<div className="deployment-preview"><h3>部署位置</h3><div className="tiny-map">{mapRows.map((row,y) => [...row].map((tile,x) => <span key={`${x}-${y}`} className={`tiny-cell terrain-${tile === '.' ? 'plain' : tile === '~' ? 'water' : tile === 'F' ? 'forest' : 'road'} ${x < 3 && y > 5 ? 'start-cell' : ''}`} title={`${terrainName(tile)} ${x+1},${y+1}`}>{unitSeeds.filter(u=>u.side==='ally' && deployed.includes(u.id) && u.x===x && u.y===y).map(u=><b key={u.id}>{scenario.party.findIndex(p=>p.id===u.id)+1}</b>)}</span>))}</div><p>編號對應出戰者的部署位；未出戰者不出現。實際拖曳選位系統待定。</p></div></section></div></main>}

    {screen === 'battle' && <main className="battle-page"><div className="battle-head"><div><div className="eyebrow">{scenario.chapter} · 戰鬥展示</div><h1>{scenario.mission}</h1><p>{choiceData?.objective} · {choiceData?.support}</p></div><div className="turn-marker">第 {turn} 回合<small>我方行動 · 固定示範</small></div></div><div className="battle-layout"><section className="battlefield" aria-label="11 乘 9 戰場格線">{mapRows.map((row,y) => [...row].map((tile,x) => { const p={x,y}, occupant=units.find(u => u.hp > 0 && same(u,p)); const isMove=moveCells.has(key(p)), isSkill=skillCells.has(key(p)); const actionable = phase === 'select' ? occupant?.side === 'ally' && !occupant.acted : phase === 'move' ? isMove : phase === 'skill' ? occupant?.side === 'enemy' && isSkill : false; return <button disabled={!actionable} key={key(p)} className={`cell terrain-${tile === '.' ? 'plain' : tile === '~' ? 'water' : tile === 'F' ? 'forest' : 'road'} ${isMove ? 'reachable' : ''} ${isSkill ? 'skill-range' : ''} ${destination && same(destination,p) ? 'destination' : ''} ${occupant?.id === selected || occupant?.id === target ? 'active-unit' : ''}`} title={`${terrainName(tile)}，${x+1},${y+1}${occupant ? `，${occupant.name}` : ''}`} aria-label={`${x+1} 列 ${y+1} 行，${terrainName(tile)}${occupant ? `，${occupant.name}，生命 ${occupant.hp}` : ''}${isMove ? '，可移動' : ''}${isSkill ? '，技能範圍' : ''}`} onClick={() => pickCell(p)}><span className="tile-pattern" aria-hidden="true">{tile==='~'?'≈':''}</span>{occupant && <span className={`unit ${occupant.side} ${occupant.acted ? 'spent' : ''}`}><span aria-hidden="true" className={`unit-art sprite-${occupant.id}`}/><b>{occupant.side === 'ally' ? '◆' : '▲'} {occupant.name}</b><small>{occupant.acted ? '已行動 · ' : ''}{occupant.hp}</small></span>}{destination && same(destination,p) && <span className="move-pin">◇</span>}</button> }))}</section><aside className="battle-sidebar"><div className="battle-box"><div className="eyebrow">操作順序</div><ol className="steps"><li className={phase==='select'?'active-step':''}>選角色</li><li className={phase==='move'?'active-step':''}>選移動位置</li><li className={phase==='skill'?'active-step':''}>選範圍內敵人</li><li className={phase==='confirm'?'active-step':''}>確認行動</li></ol><p>{phase==='select' ? '點選尚未行動的我方單位。' : phase==='move' ? '斜紋格為可移動範圍；河道不可走。' : phase==='skill' ? '圈線格為技能範圍，點選其中敵人。' : '移動與技能都還未執行，請先閱讀預覽。'}</p></div><div className="battle-box"><div className="eyebrow">選取與預覽</div><h2>{actor?.name || '尚未選取角色'}</h2><p>{actor ? `生命 ${actor.hp} · ${actor.acted ? '已行動' : '可行動'}` : '選取單位後顯示狀態。'}</p>{destination && <p>移動至：第 {destination.x+1} 列、第 {destination.y+1} 行</p>}{enemy && <p>掩護推進 → {enemy.name}：固定展示效果 3，預計生命 {Math.max(0,enemy.hp-3)}。</p>}<div className="button-stack"><button className="primary" disabled={phase!=='confirm'} onClick={confirmAction}>確認移動與技能</button><button disabled={phase==='select'} onClick={() => { setDestination(null); setTarget(null); if (destination) setPhase('move'); else { setSelected(null); setPhase('select') } }}>撤銷未確認操作</button></div></div><div className="battle-box objective"><div className="eyebrow">任務目標</div><strong>{choiceData?.objective}</strong><p>已確認行動 {actions} 次。固定展示流程在確認一次行動後可結束。</p><button disabled={phase!=='select'} onClick={endTurn}>結束回合</button><button className="finish" disabled={actions===0} onClick={() => setConfirmFinish(true)}>確認護送抵達出口</button></div></aside></div><footer className="battle-footer"><span><b className="legend ally"/> 我方　<b className="legend enemy"/> 敵方　<i className="legend range"/> 移動範圍　<i className="legend skill"/> 技能範圍</span><details className="event-log"><summary>事件紀錄（{log.length}） · {log[0]}</summary><ol>{log.map((entry,i)=><li key={i}>{entry}</li>)}</ol></details></footer>{confirmFinish && <div className="modal-backdrop"><div ref={modalRef} className="confirm-modal" onKeyDown={e => { if (e.key === 'Tab') { const buttons = modalRef.current?.querySelectorAll<HTMLButtonElement>('button'); if (!buttons?.length) return; const first=buttons[0], last=buttons[buttons.length-1]; if (e.shiftKey && document.activeElement===first) { e.preventDefault(); last.focus() } else if (!e.shiftKey && document.activeElement===last) { e.preventDefault(); first.focus() } } }} role="dialog" aria-modal="true" aria-labelledby="finish-title"><div className="eyebrow">重大操作確認</div><h2 id="finish-title">確認護送抵達北岸？</h2><p>將結束這場固定資料戰鬥展示，進入戰後結果。尚未模擬敵方完整回合與勝敗規則。</p><div><button onClick={() => setConfirmFinish(false)}>繼續檢查戰場</button><button className="primary" onClick={finishBattle}>確認完成此關</button></div></div></div>}</main>}

    {screen === 'result' && <main className="content-page result-page"><div className="eyebrow">戰後結果 · 展示結局</div><h1>渡口之後，路還沒完</h1><p className="result-lead">{choiceData?.outcome}</p><div className="result-layout"><section className="result-story"><h2>留下的後果</h2><dl><dt>救下與保住</dt><dd>{choiceData?.gain}</dd><dt>失去與未完成</dt><dd>{choiceData?.cost}</dd><dt>同伴的看法</dt><dd>{choice === 'residents' ? '奧倫仍同行，但要求公開守線風險。莉妲開始照護已抵岸的居民。' : '莉妲仍同行，但要求回渡口尋人；奧倫保住了工事材料。'}</dd><dt>接下來為何出發</dt><dd>{choiceData?.next}</dd></dl></section><aside className="result-reward"><div className="eyebrow">成長與物資 · 模擬</div><h2>一次行動的紀錄</h2><p>隊伍經驗：展示占位</p><p>物資：{choice === 'residents' ? '短缺，等待徵集' : '營地糧倉保有存量'}</p><p className="fine">未設定正式數值成長、掉落或存檔。</p></aside></div><button className="primary" onClick={() => setScreen('journey')}>返回戰役旅程 →</button></main>}

    {screen === 'settings' && <main className="content-page settings-page"><div className="eyebrow">展示設定</div><h1>閱讀與操作</h1><section className="settings-content"><label className="setting-row"><span><strong>放大文字</strong><small>對白與資訊字級同步提高；長內容可捲動。</small></span><input type="checkbox" checked={textLarge} onChange={e => setTextLarge(e.target.checked)}/></label><div className="setting-row"><span><strong>鍵盤</strong><small>Tab 移動焦點、Enter／空白鍵操作、Esc 返回；戰場格子可用 Tab 選取。</small></span></div><div className="setting-row"><span><strong>手把映射規劃</strong><small>方向鍵移焦點、A 確認、B 返回、肩鍵切換面板。尚未實作，也未測試。</small></span></div><div className="setting-row"><span><strong>畫面</strong><small>目標 1920×1080；另檢查 1280×720。縮放以排版調整，不縮小正文。</small></span></div></section><button className="primary" onClick={() => setScreen(returnScreen)}>完成 →</button></main>}
  </div>
}

createRoot(document.getElementById('root')!).render(<App />)
