import { useEffect, useId, useMemo, useRef, useState } from "react";
import { AnimatedActor } from "../AnimatedActor";
import type { Playback } from "../combatPlayback";
import { sceneDiamond, sceneProject } from "../l03Scene";
import { command, DEFAULT_CONFIG, initialState, key, MAP, resolve, walkable,
  type Cell, type Command, type Result } from "./rules";
import "../l03.css";
import "./playable.css";

// A is opt-in here only. rules.ts and the P0/P0b/P0c fixtures remain untouched.
const start = () => initialState("open", { ...DEFAULT_CONFIG, p0c: { survivalTurns: 6 } });
const names: Record<string, string> = { karen: "凱倫", lace: "蕾絲", thoma: "托瑪",
  "knight-1": "騎士一", "knight-2": "騎士二" };
const reasons = { "turn-winch": "已在絞盤旁，本回合干擾＋1", approach: "前往最近可達的絞盤鄰格", blocked: "通道被占，無法接近絞盤" };
const cells = MAP.rows.flatMap((row, y) => [...row].map((tile, x) => ({ x, y, tile })));
const center = (p: Cell) => sceneProject(p.x + .5, p.y + .5);
const initialMessage = "選擇我方單位，再點亮格移動。";
type Frame = { unit: string; from: Cell; to: Cell; progress: number };

function Figure({ id }: { id: string }) {
  const column = ["karen", "lace", "thoma"].indexOf(id);
  // The nearest units in the same screen column are only 30 scene units apart.
  // Fit the entire silhouette below that gap; crop the transparent foot padding.
  return column >= 0 ? <svg data-p1v-figure={id} x="-12" y="-26" width="24" height="26"
    viewBox={`${column * 724 + 110} 0 520 ${id === "thoma" ? 711 : 710}`} preserveAspectRatio="xMidYMax meet">
    <image href="/art/l03-party-v1.png" width="2172" height="724" />
  </svg> : <svg data-p1v-figure={id} x="-14" y="-26" width="28" height="26" viewBox="0 0 887 871" preserveAspectRatio="xMidYMax meet">
    <image href="/art/l03-enemies-v1.png" width="1774" height="887" />
  </svg>;
}

export function PlayableL03({ onExit }: { onExit: () => void }) {
  const [state, setState] = useState(start);
  const stateRef = useRef(state);
  const [selected, setSelected] = useState<string | null>(null);
  const [inspected, setInspected] = useState<string | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  const [waited, setWaited] = useState<string[]>([]);
  const [message, setMessage] = useState(initialMessage);
  const [busy, setBusy] = useState(false);
  const busyRef = useRef(false);
  const [skip, setSkip] = useState(false);
  const skipRef = useRef(false);
  const [reduced, setReduced] = useState(() => matchMedia("(prefers-reduced-motion: reduce)").matches);
  const reducedRef = useRef(reduced);
  const [frame, setFrame] = useState<Frame | null>(null);
  const [visualUnits, setVisualUnits] = useState(state.units);
  const raf = useRef(0);
  const pending = useRef<Result | null>(null);
  const root = useRef<HTMLElement>(null);
  const retryButton = useRef<HTMLButtonElement>(null);
  const uid = useId().replace(/:/g, "");

  const finish = () => {
    cancelAnimationFrame(raf.current);
    const result = pending.current;
    if (!result) return;
    pending.current = null;
    stateRef.current = result.state;
    setState(result.state); setVisualUnits(result.state.units); setFrame(null);
    busyRef.current = false; setBusy(false);
    setMessage(result.state.status === "success" ? "守住六回合。" : result.state.status === "failure"
      ? "絞盤干擾已達三格。" : `第 ${result.state.turn} 回合，選擇我方單位。`);
  };
  useEffect(() => {
    root.current?.focus();
    const query = matchMedia("(prefers-reduced-motion: reduce)");
    const change = () => { reducedRef.current = query.matches; setReduced(query.matches); if (query.matches) finish(); };
    query.addEventListener("change", change);
    return () => { cancelAnimationFrame(raf.current); pending.current = null; query.removeEventListener("change", change); };
  }, []);
  useEffect(() => { if (state.status !== "playing") retryButton.current?.focus(); }, [state.status]);

  // Both legal highlights and intent are pure queries against the SAME state.
  const legal = useMemo(() => new Set(selected && !waited.includes(selected) ? cells.filter(p =>
    command(state, { type: "move", turn: state.turn, unit: selected, to: p }).ok).map(key) : []), [state, selected, waited]);
  const preview = useMemo(() => resolve(state, state.turn), [state]);
  const intents = preview.events.filter(e => e.type === "intent");
  const enemyPaths = preview.events.filter(e => e.type === "move");

  function apply(input: Command) {
    if (busyRef.current) return;
    const result = command(stateRef.current, input);
    if (!result.ok) { setMessage("無法執行；請選擇亮格或可行動的我方。" ); return; }
    setSelected(null); setInspected(null); setHovered(null);
    if (input.type === "resolve" || input.type === "retry") setWaited([]);
    if (input.type === "retry") {
      stateRef.current = result.state; setState(result.state); setVisualUnits(result.state.units);
      setSkip(false); skipRef.current = false; setMessage(initialMessage); setFrame(null);
      root.current?.focus(); return;
    }
    pending.current = result; busyRef.current = true; setBusy(true);
    setMessage(input.type === "resolve" ? "敵方行動中…" : "移動中…");
    const steps = result.events.flatMap(e => e.type === "move" ? e.path.slice(1).map((to, i) =>
      ({ unit: e.unit, from: e.path[i], to })) : []);
    if (skipRef.current || reducedRef.current || !steps.length) { finish(); return; }
    let index = 0, began = performance.now(), units = stateRef.current.units;
    const tick = (now: number) => {
      if (!pending.current) return;
      const step = steps[index], progress = Math.min(1, (now - began) / 230);
      setFrame({ ...step, progress });
      if (progress >= 1) {
        units = units.map(u => u.id === step.unit ? { ...u, cell: step.to } : u);
        setVisualUnits(units);
        if (++index >= steps.length) { finish(); return; }
        began = now;
      }
      raf.current = requestAnimationFrame(tick);
    };
    raf.current = requestAnimationFrame(tick);
  }
  function pick(p: Cell) {
    if (busyRef.current || stateRef.current.status !== "playing") return;
    const occupant = state.units.find(u => u.alive && key(u.cell) === key(p));
    setInspected(occupant?.id || null);
    if (occupant?.side === "ally") {
      if (state.moved.includes(occupant.id) || waited.includes(occupant.id)) { setSelected(null); setMessage("此單位本回合已行動。" ); return; }
      setSelected(occupant.id); setMessage(`${names[occupant.id]}：可移動最多三格，或等待。`); return;
    }
    if (selected && legal.has(key(p))) { apply({ type: "move", turn: state.turn, unit: selected, to: { x: p.x, y: p.y } }); return; }
    if (occupant?.side === "enemy") setSelected(null);
    setMessage(occupant?.side === "enemy" ? "敵方單位無法操作，請查看右側意圖。" : "此格無法移動；請先選我方，再點亮格。");
  }
  const endTurn = () => apply({ type: "resolve", turn: stateRef.current.turn });
  const active = state.status === "playing";
  const inspectedUnit = state.units.find(u => u.id === (hovered || inspected));
  // Sort actual animated foot positions, including a stable column tie-breaker.
  const actors = visualUnits.filter(u => u.alive).map(u => {
    const moving = frame?.unit === u.id ? frame : null;
    const f = moving ? moving.progress * moving.progress * (3 - 2 * moving.progress) : 1;
    const p = moving ? center({x:moving.from.x+(moving.to.x-moving.from.x)*f,y:moving.from.y+(moving.to.y-moving.from.y)*f}) : center(u.cell);
    return { u, moving, p };
  }).sort((a,b) => a.p.y-b.p.y || a.p.x-b.p.x || a.u.id.localeCompare(b.u.id));
  return <main className="l03-app p1v" ref={root} tabIndex={-1} data-p1v-status={state.status}
    data-p1v-turn={state.turn} data-p1v-progress={state.progress} data-p1v-busy={busy}
    data-p1v-selected={selected || ""} data-p1v-state={JSON.stringify(state)} data-p1v-waited={waited.join(",")}
    data-p1v-inspected={inspected || ""}
    data-p1v-frame={frame ? JSON.stringify(frame) : ""}
    onKeyDown={e => {
      if (!active && e.key === "Tab") { e.preventDefault(); retryButton.current?.focus(); return; }
      if (e.key === "Enter" && e.repeat) { e.preventDefault(); return; }
      if (e.key === "Escape") { e.preventDefault(); setSelected(null); setInspected(null); setHovered(null); setMessage("已取消選擇。" ); }
      if (e.key === "Enter" && !e.repeat && !e.defaultPrevented &&
        !(e.target as Element).closest("button,input")) { e.preventDefault(); endTurn(); }
    }}>
    <div className="p1v-surface" {...(!active ? { inert: "" } : {})}>
    <header className="p1v-header">
      <div><span className="p1v-kicker">L03 / P1v · A 測試</span><h1>守住絞盤</h1></div>
      <div className="p1v-counters"><span>回合 <strong>{state.turn}<small> / 6</small></strong></span>
        <span>絞盤干擾 <strong>{state.progress}<small> / 3</small></strong></span></div>
      <button onClick={onExit}>返回選單</button>
    </header>
    <p className="p1v-objective">勝利：守過第六回合　／　失敗：絞盤干擾達三格</p>
    <div className="p1v-layout">
      <section className="p1v-board" aria-label="戰場">
        <div className="p1v-map-caption"><span>渡口 · 11 × 9</span><span>圓底座：我方　菱形底座：敵方　點格選人</span></div>
        <div className="p1v-inspection" aria-live="polite">
          <span className={inspectedUnit ? "p1v-inspection-placeholder hidden" : "p1v-inspection-placeholder"}
            aria-hidden={!!inspectedUnit}>指向、聚焦或點選單位所在格，查看姓名與狀態。</span>
          {inspectedUnit && <span data-p1v-label={inspectedUnit.id}>
            {inspectedUnit.side === "ally" ? "● 我方" : "◆ 敵方"} · <strong>{names[inspectedUnit.id]}</strong>
            {` · (${inspectedUnit.cell.x},${inspectedUnit.cell.y}) · `}
            {inspectedUnit.side === "enemy" ? "查看右側意圖" : state.moved.includes(inspectedUnit.id) || waited.includes(inspectedUnit.id) ? "已行動" : "可行動"}
          </span>}
        </div>
        <svg className="p1v-map" viewBox="150 10 900 410" role="group" aria-label="11乘9渡口戰場；空白鍵選格，方向鍵移動焦點">
          <defs>
            {["grass", "stone", "water", "forest"].map((name, index) => <pattern key={name} id={`${uid}-${name}`}
              width="200" height="200" patternUnits="userSpaceOnUse" patternTransform="matrix(1 .34 -1 .34 550 90)">
              <image href="/art/terrain-v2.png" width="400" height="400" x={index % 2 ? -200 : 0} y={index > 1 ? -200 : 0} />
            </pattern>)}
            <marker id={`${uid}-arrow`} viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
              <path d="M0 0L10 5L0 10Z" fill="#ffd2a0" />
            </marker>
          </defs>
          {cells.map(p => <g key={key(p)}>
            <polygon points={sceneDiamond(p.x,p.y)} fill={!walkable(p, "open") ? "#537e78" : p.tile === "R" ? "#b19a72" : "#8c9975"} />
            <polygon points={sceneDiamond(p.x,p.y)} fill={`url(#${uid}-${!walkable(p,"open") ? "water" : p.tile === "F" ? "forest" : p.tile === "R" ? "stone" : "grass"})`} opacity=".4" />
          </g>)}
          <g className="p1v-landmarks" aria-hidden="true">
            <text x={center({x:5,y:4}).x + 20} y={center({x:5,y:4}).y + 30}>斷橋</text>
            <g transform={`translate(${center(MAP.winch).x} ${center(MAP.winch).y})`}>
              <circle r="13" fill="#273b30" stroke="#ffe0a4" strokeWidth="3" />
              <path d="M-12 0H12M0-12V12" stroke="#ffe0a4" strokeWidth="3" />
              <text y="-22" textAnchor="middle">絞盤 (2,1)</text>
            </g>
            <g transform={`translate(${center(MAP.wagon).x} ${center(MAP.wagon).y})`}>
              <path d="m-33-4 27-13 47 23-27 13Z" fill="#8b6b46" stroke="#d4bc89" strokeWidth="2" />
              {[-14,5,24].map(x => <g key={x} transform={`translate(${x} ${x*.5-7})`}>
                <path d="m-9-15 10-5 12 6v17L3 8-9 1Z" fill="#b2a37e" stroke="#504e3c" />
                <path d="M2-18V7" stroke="#526157" strokeWidth="3" />
              </g>)}
              <circle cx="-17" cy="11" r="8" fill="#3f4940" /><circle cx="21" cy="28" r="8" fill="#3f4940" />
              <text x="15" y="-37">車隊</text>
            </g>
          </g>
          {active && !busy && enemyPaths.map((e, i) => <polyline key={e.unit} data-p1v-intent-path={e.unit}
            points={e.path.map(p => `${center(p).x},${center(p).y}`).join(" ")}
            className={`p1v-intent-path knight-${i}`} markerEnd={`url(#${uid}-arrow)`} />)}
          {cells.map(p => {
            const occupant = state.units.find(u => key(u.cell) === key(p));
            const canMove = legal.has(key(p)), chosen = !!occupant && occupant.id === (inspected || selected);
            return <g key={key(p)}>
              <polygon data-p1v-cell={key(p)} data-legal={canMove} role="button" tabIndex={active && !busy ? 0 : -1}
                aria-label={`${p.x},${p.y}${occupant ? ` ${occupant.side === "ally" ? "我方" : "敵方"} ${names[occupant.id]}` : ""}${canMove ? " 可移動" : ""}`}
                aria-disabled={!active || busy} aria-pressed={chosen} points={sceneDiamond(p.x,p.y)}
                className={`p1v-cell ${canMove ? "legal" : ""} ${chosen ? "selected" : ""}`}
                onMouseEnter={() => { if (!busy && active) setHovered(occupant?.id || null); }} onMouseLeave={() => setHovered(null)}
                onFocus={() => { if (!busy && active) setHovered(occupant?.id || null); }} onBlur={() => setHovered(null)}
                onClick={() => pick(p)} onKeyDown={e => {
                  if (e.key === " ") { e.preventDefault(); e.stopPropagation(); pick(p); }
                  const delta = ({ArrowUp:[0,-1],ArrowDown:[0,1],ArrowLeft:[-1,0],ArrowRight:[1,0]} as Record<string, number[]>)[e.key];
                  if (delta) { e.preventDefault(); root.current?.querySelector<SVGElement>(`[data-p1v-cell="${p.x+delta[0]},${p.y+delta[1]}"]`)?.focus(); }
                }} />
              {canMove && <text className="p1v-move-plus" x={center(p).x} y={center(p).y+4} textAnchor="middle" aria-hidden="true">＋</text>}
            </g>;
          })}
          {actors.map(({u, moving, p}) => {
            const clip: Playback | null = moving ? { kind:"physical", actor:u.id, target:"", from:moving.from, to:moving.to,
              committed:true, stage:"move", progress:moving.progress, elapsed:moving.progress*230, sequence:1 } : null;
            return <g key={u.id} transform={`translate(${p.x} ${p.y})`} className="p1v-unit" data-p1v-unit={u.id}
              data-cell={key(u.cell)} data-moving={!!moving} aria-hidden="true">
              <g data-p1v-base={u.side} fill={u.side === "ally" ? "#183c39" : "#532d2b"}
                stroke={u.id === (inspected || selected) ? "#ffe0a4" : u.side === "ally" ? "#a6e2d3" : "#ffbd9c"} strokeWidth="2">
                {u.side === "ally" ? <ellipse rx="14" ry="3" /> : <path d="M-16 0 0-4 16 0 0 4Z" />}
              </g>
              <g>
                <AnimatedActor id={u.id} clip={clip} reduced={reduced}><Figure id={u.id} /></AnimatedActor>
              </g>
            </g>;
          })}
        </svg>
      </section>
      <aside className="p1v-sidebar">
        <h2>敵方意圖</h2>
        <p className="p1v-hint">依目前站位預告；我方移動後更新。</p>
        {intents.map(e => {
          const path = enemyPaths.find(p => p.unit === e.unit)?.path;
          const target = path?.[path.length-1];
          return <div className="p1v-intent" key={e.unit} data-p1v-intent={e.unit}>
            <h3>{names[e.unit]} <span>{target ? `→ (${target.x},${target.y})` : "原地"}</span></h3>
            <p>{reasons[e.reason]}</p>
          </div>;
        })}
        {!active && <p>戰鬥已結束。</p>}
        <h2>我方行動</h2>
        <div className="p1v-roster">{state.units.filter(u => u.side === "ally").map(u => <button key={u.id}
          data-p1v-select={u.id} aria-pressed={selected === u.id} disabled={busy || !active || state.moved.includes(u.id) || waited.includes(u.id)}
          onClick={() => pick(u.cell)}>{names[u.id]}<span>{state.moved.includes(u.id) ? "已移動" : waited.includes(u.id) ? "已等待" : "可行動"}</span></button>)}</div>
        <label className="p1v-skip"><input type="checkbox" checked={skip} onChange={e => { skipRef.current=e.target.checked; setSkip(e.target.checked); if (e.target.checked) finish(); }} />跳過動畫</label>
      </aside>
    </div>
    <footer className="p1v-controls">
      <div><p role="status" data-p1v-message>{message}</p><span>點選／空白鍵：選格　方向鍵：焦點　Esc：取消　Enter：結束回合</span></div>
      <button disabled={!selected || busy || !active} onClick={() => { if (!selected) return; setWaited(w => [...w,selected]); setSelected(null); setMessage("已等待，本回合不再移動。" ); }}>等待</button>
      <button className="p1v-primary" disabled={busy || !active} data-p1v-end onClick={e => { if (e.detail < 2) endTurn(); }}>{busy ? "行動中…" : "結束回合"}</button>
    </footer>
    </div>
    {!active && <section className="p1v-result" role="dialog" aria-modal="true" aria-labelledby="p1v-result-title" data-p1v-result={state.status}>
      <div><span className="p1v-kicker">L03 · 結果</span><h2 id="p1v-result-title">{state.status === "success" ? "防守成功" : "防守失敗"}</h2>
        <p>{state.status === "success" ? "已守過六回合，絞盤未失守。" : "絞盤干擾達三格。可重試改變站位。"}</p>
        <p>回合 {state.turn} / 6　·　干擾 {state.progress} / 3</p>
        <button className="p1v-primary" ref={retryButton} onClick={() => apply({type:"retry"})}>重試</button>
      </div>
    </section>}
  </main>;
}
