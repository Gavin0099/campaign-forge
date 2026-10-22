import { useEffect, useId, useMemo, useRef, useState } from "react";
import { AnimatedActor } from "../AnimatedActor";
import type { Playback } from "../combatPlayback";
import { command, DEFAULT_CONFIG, initialState, key, MAP, resolve,
  type Cell, type Command, type Result } from "./rules";
import { center, diamond as sceneDiamond, Figure, Portrait, Terrain, Landmarks } from "./presentation";
import "../l03.css";
import "./playable.css";

// A is opt-in here only. rules.ts and the P0/P0b/P0c fixtures remain untouched.
const start = () => initialState("open", { ...DEFAULT_CONFIG, p0c: { survivalTurns: 6 } });
const names: Record<string, string> = { karen: "凱倫", lace: "蕾絲", thoma: "托瑪",
  "knight-1": "騎士一", "knight-2": "騎士二" };
const reasons = { "turn-winch": "已在絞盤旁，本回合干擾＋1", approach: "前往最近可達的絞盤鄰格", blocked: "通道被占，無法接近絞盤" };
const cells = MAP.rows.flatMap((row, y) => [...row].map((tile, x) => ({ x, y, tile })));
const initialMessage = "選擇我方單位，再點亮格移動。";
type Frame = { unit: string; from: Cell; to: Cell; progress: number };

export function PlayableL03({ onExit }: { onExit: () => void }) {
  const [state, setState] = useState(start);
  const stateRef = useRef(state);
  const [selected, setSelected] = useState<string | null>(null);
  const [inspected, setInspected] = useState<string | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  const [hoverCell, setHoverCell] = useState<Cell | null>(null);
  const [dev, setDev] = useState(false);
  const [phase, setPhase] = useState<"ally" | "enemy">("ally");
  const [banner, setBanner] = useState<{ phase: "ally" | "enemy"; serial: number } | null>(null);
  const [arrival, setArrival] = useState<{ unit: string; serial: number } | null>(null);
  const feedbackSerial = useRef(0);
  const resolving = useRef(false);
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
    const lastMove = [...result.events].reverse().find(e => e.type === "move");
    if (lastMove && !skipRef.current && !reducedRef.current) setArrival({ unit: lastMove.unit, serial: ++feedbackSerial.current });
    if (resolving.current) {
      setPhase("ally");
      setBanner(result.state.status === "playing" ? { phase: "ally", serial: ++feedbackSerial.current } : null);
      resolving.current = false;
    }
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
  useEffect(() => {
    if (!banner) return;
    const timer = window.setTimeout(() => setBanner(null), 900);
    return () => window.clearTimeout(timer);
  }, [banner]);
  useEffect(() => {
    if (!arrival) return;
    const timer = window.setTimeout(() => setArrival(null), 180);
    return () => window.clearTimeout(timer);
  }, [arrival]);

  // Both legal highlights and intent are pure queries against the SAME state.
  const legal = useMemo(() => new Set(selected && !waited.includes(selected) ? cells.filter(p =>
    command(state, { type: "move", turn: state.turn, unit: selected, to: p }).ok).map(key) : []), [state, selected, waited]);
  const preview = useMemo(() => resolve(state, state.turn), [state]);
  const intents = preview.events.filter(e => e.type === "intent");
  const enemyPaths = preview.events.filter(e => e.type === "move");
  // Ask the same pure command for the preview path; never duplicate path rules in the view.
  const movePath = useMemo(() => {
    if (!selected || !hoverCell || !legal.has(key(hoverCell)) || busy) return [];
    const result = command(state, { type: "move", turn: state.turn, unit: selected, to: hoverCell });
    return result.events.find(e => e.type === "move")?.path || [];
  }, [selected, hoverCell, legal, busy, state]);

  function apply(input: Command) {
    if (busyRef.current) return;
    const result = command(stateRef.current, input);
    if (!result.ok) { setMessage("無法執行；請選擇亮格或可行動的我方。" ); return; }
    setSelected(null); setInspected(null); setHovered(null); setHoverCell(null); setArrival(null);
    if (input.type === "resolve" || input.type === "retry") setWaited([]);
    if (input.type === "retry") {
      stateRef.current = result.state; setState(result.state); setVisualUnits(result.state.units);
      setSkip(false); skipRef.current = false; setMessage(initialMessage); setFrame(null);
      setPhase("ally"); setBanner(null); resolving.current = false;
      root.current?.focus(); return;
    }
    pending.current = result; busyRef.current = true; setBusy(true);
    if (input.type === "resolve") {
      resolving.current = true; setPhase("enemy");
      setBanner({ phase: "enemy", serial: ++feedbackSerial.current });
    } else setBanner(null);
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
  return <main className="l03-app p1v" ref={root} tabIndex={-1} data-p1v-status={state.status} data-p1v-dev={dev}
    data-p1v-turn={state.turn} data-p1v-progress={state.progress} data-p1v-busy={busy}
    data-p1v-selected={selected || ""} data-p1v-state={JSON.stringify(state)} data-p1v-waited={waited.join(",")}
    data-p1v-inspected={inspected || ""}
    data-p1v-frame={frame ? JSON.stringify(frame) : ""}
    onKeyDown={e => {
      if (!active && e.key === "Tab") { e.preventDefault(); retryButton.current?.focus(); return; }
      if (e.key === "Enter" && e.repeat) { e.preventDefault(); return; }
      if (e.key === "Escape") { e.preventDefault(); setSelected(null); setInspected(null); setHovered(null); setHoverCell(null); setMessage("已取消選擇。" ); }
      if (e.key === "Enter" && !e.repeat && !e.defaultPrevented &&
        !(e.target as Element).closest("button,input")) { e.preventDefault(); endTurn(); }
    }}>
    <div className="p1v-surface" {...(!active ? { inert: "" } : {})}>
    <header className="p1v-header">
      <div className="p1v-title"><span className="p1v-title-seal" aria-hidden="true">⚜</span><div><span className="p1v-kicker">渡口防衛{dev ? " · L03 / P1v · A 測試" : ""}</span><h1>守住絞盤</h1></div></div>
      <div className="p1v-counters">
        <div className="p1v-gauge" aria-label={`回合 ${state.turn} / 6`}><span aria-hidden="true">◷</span><div><span>回合 <strong>{state.turn}<small> / 6</small></strong></span><div className="p1v-pips" aria-hidden="true">{Array.from({length:6},(_,i)=><i key={i} className={i < state.turn ? "filled" : ""} />)}</div></div></div>
        <div className="p1v-gauge danger" aria-label={`絞盤干擾 ${state.progress} / 3`}><span aria-hidden="true">⚙</span><div><span>絞盤干擾 <strong>{state.progress}<small> / 3</small></strong></span><div className="p1v-pips" aria-hidden="true">{Array.from({length:3},(_,i)=><i key={i} className={i < state.progress ? "filled" : ""} />)}</div></div></div>
      </div>
      <button onClick={onExit}>返回選單</button>
    </header>
    <p className="p1v-objective"><span aria-hidden="true">◆</span> 勝利：守過第六回合　／　失敗：絞盤干擾達三格 <span className={`p1v-phase ${phase}`} data-p1v-phase={phase}>{phase === "enemy" ? "敵方回合" : "我方回合"}</span></p>
    <div className="p1v-layout">
      <section className="p1v-board" aria-label="戰場">
        <div className="p1v-map-caption"><span>渡口{dev ? " · 11 × 9" : ""}</span><span><i className="ally" />我方　<i className="enemy" />敵方　·　點格選人</span></div>
        <div className="p1v-inspection" aria-live="polite">
          <span className={inspectedUnit ? "p1v-inspection-placeholder hidden" : "p1v-inspection-placeholder"}
            aria-hidden={!!inspectedUnit}>指向、聚焦或點選單位所在格，查看姓名與狀態。</span>
          {inspectedUnit && <span data-p1v-label={inspectedUnit.id}>
            {inspectedUnit.side === "ally" ? "● 我方" : "◆ 敵方"} · <strong>{names[inspectedUnit.id]}</strong>
            {dev ? ` · (${inspectedUnit.cell.x},${inspectedUnit.cell.y}) · ` : " · "}
            {inspectedUnit.side === "enemy" ? "查看右側意圖" : state.moved.includes(inspectedUnit.id) || waited.includes(inspectedUnit.id) ? "已行動" : "可行動"}
          </span>}
        </div>
        <svg className="p1v-map" viewBox="130 32 940 590" role="group" aria-label="11乘9渡口戰場；空白鍵選格，方向鍵移動焦點">
          <defs>
            {["grass", "stone", "water", "forest"].map((name, index) => <pattern key={name} id={`${uid}-${name}`}
              width="176" height="176" patternUnits="userSpaceOnUse" patternTransform="matrix(1 .591 -1 .591 550 70)">
              <image href="/art/terrain-v2.png" width="352" height="352" x={index % 2 ? -176 : 0} y={index > 1 ? -176 : 0} />
            </pattern>)}
            <marker id={`${uid}-arrow`} viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
              <path d="M0 0L10 5L0 10Z" fill="#ffd2a0" />
            </marker>
          </defs>
          <Terrain uid={uid} />
          <Landmarks dev={dev} />
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
                onMouseEnter={() => { if (!busy && active) { setHovered(occupant?.id || null); setHoverCell(p); } }} onMouseLeave={() => { setHovered(null); setHoverCell(null); }}
                onFocus={() => { if (!busy && active) { setHovered(occupant?.id || null); setHoverCell(p); } }} onBlur={() => { setHovered(null); setHoverCell(null); }}
                onClick={() => pick(p)} onKeyDown={e => {
                  if (e.key === " ") { e.preventDefault(); e.stopPropagation(); pick(p); }
                  const delta = ({ArrowUp:[0,-1],ArrowDown:[0,1],ArrowLeft:[-1,0],ArrowRight:[1,0]} as Record<string, number[]>)[e.key];
                  if (delta) { e.preventDefault(); root.current?.querySelector<SVGElement>(`[data-p1v-cell="${p.x+delta[0]},${p.y+delta[1]}"]`)?.focus(); }
                }} />
              {canMove && <text className="p1v-move-plus" x={center(p).x} y={center(p).y+4} textAnchor="middle" aria-hidden="true">＋</text>}
            </g>;
          })}
          {movePath.length > 0 && <g className="p1v-move-path" data-p1v-move-path={movePath.map(key).join(";")} aria-hidden="true">
            <polyline points={movePath.map(p => `${center(p).x},${center(p).y}`).join(" ")} />
            {movePath.slice(1).map((p,i) => <g key={key(p)} transform={`translate(${center(p).x} ${center(p).y})`}><circle r="7" /><text y="3" textAnchor="middle">{i+1}</text></g>)}
          </g>}
          {actors.map(({u, moving, p}) => {
            const clip: Playback | null = moving ? { kind:"physical", actor:u.id, target:"", from:moving.from, to:moving.to,
              committed:true, stage:"move", progress:moving.progress, elapsed:moving.progress*230, sequence:1 } : null;
            return <g key={u.id} transform={`translate(${p.x} ${p.y})`} className="p1v-unit" data-p1v-unit={u.id}
              data-cell={key(u.cell)} data-moving={!!moving} aria-hidden="true">
              <ellipse className="p1v-shadow" rx="21" ry="7" cy="2" />
              <g className={u.id === selected ? "p1v-selection-ring" : ""} data-p1v-base={u.side} fill={u.side === "ally" ? "#183c3966" : "#532d2b66"}
                stroke={u.id === (inspected || selected) ? "#ffe0a4" : u.side === "ally" ? "#a6e2d3" : "#ffbd9c"} strokeWidth="2">
                {u.side === "ally" ? <ellipse rx="17" ry="6" /> : <path d="M-19 0 0-7 19 0 0 7Z" />}
              </g>
              <g key={arrival?.unit === u.id ? arrival.serial : "idle"} className={arrival?.unit === u.id && !reduced && !skip ? "p1v-arrival" : undefined}>
                <AnimatedActor id={u.id} clip={clip} reduced={reduced}><Figure id={u.id} /></AnimatedActor>
              </g>
            </g>;
          })}
        </svg>
        {banner && active && <div key={banner.serial} className={`p1v-turn-banner ${banner.phase}`} data-p1v-turn-banner={banner.phase} role="status"><span>— {String(state.turn).padStart(2,"0")} —</span><strong>{banner.phase === "enemy" ? "敵方回合" : "我方回合"}</strong></div>}
      </section>
      <aside className="p1v-sidebar">
        <h2>敵方意圖</h2>
        <p className="p1v-hint">依目前站位預告；我方移動後更新。</p>
        {intents.map(e => {
          const path = enemyPaths.find(p => p.unit === e.unit)?.path;
          const target = path?.[path.length-1];
          return <div className="p1v-intent" key={e.unit} data-p1v-intent={e.unit}>
            <Portrait id={e.unit} /><div><h3>{names[e.unit]} <span aria-hidden="true">{target ? "↗" : "◇"}</span>{dev && target ? <small> ({target.x},{target.y})</small> : null}</h3>
            <p>{reasons[e.reason]}</p></div>
          </div>;
        })}
        {!active && <p>戰鬥已結束。</p>}
        <h2>我方行動</h2>
        <div className="p1v-roster">{state.units.filter(u => u.side === "ally").map(u => <button key={u.id}
          data-p1v-select={u.id} aria-pressed={selected === u.id} disabled={busy || !active || state.moved.includes(u.id) || waited.includes(u.id)}
          aria-label={`${names[u.id]}：${state.moved.includes(u.id) ? "已移動" : waited.includes(u.id) ? "已等待" : "可行動"}`}
          onClick={() => pick(u.cell)}><Portrait id={u.id} /><strong>{names[u.id]}</strong><span className="p1v-ready-icon" aria-hidden="true">{state.moved.includes(u.id) || waited.includes(u.id) ? "✓" : "◇"}</span></button>)}</div>
        <label className="p1v-skip"><input type="checkbox" checked={skip} onChange={e => { skipRef.current=e.target.checked; setSkip(e.target.checked); if (e.target.checked) finish(); }} />跳過動畫</label>
        <label className="p1v-dev"><input type="checkbox" checked={dev} onChange={e => setDev(e.target.checked)} />開發資訊</label>
      </aside>
    </div>
    <footer className="p1v-controls">
      <div><p role="status" data-p1v-message>{message}</p><span>點選／空白鍵：選格　方向鍵：焦點　Esc：取消　Enter：結束回合</span></div>
      <button disabled={!selected || busy || !active} onClick={() => { if (!selected) return; setWaited(w => [...w,selected]); setSelected(null); setMessage("已等待，本回合不再移動。" ); }}>等待</button>
      <button className="p1v-primary" disabled={busy || !active} data-p1v-end onClick={e => { if (e.detail < 2) endTurn(); }}>{busy ? "行動中…" : "結束回合"}</button>
    </footer>
    </div>
    {!active && <section className="p1v-result" role="dialog" aria-modal="true" aria-labelledby="p1v-result-title" data-p1v-result={state.status}>
      <div><span className="p1v-result-seal" aria-hidden="true">{state.status === "success" ? "⚜" : "⚔"}</span><span className="p1v-kicker">渡口 · 戰鬥結果</span><h2 id="p1v-result-title">{state.status === "success" ? "防守成功" : "防守失敗"}</h2>
        <p>{state.status === "success" ? "已守過六回合，絞盤未失守。" : "絞盤干擾達三格。可重試改變站位。"}</p>
        <p>回合 {state.turn} / 6　·　干擾 {state.progress} / 3</p>
        <button className="p1v-primary" ref={retryButton} onClick={() => apply({type:"retry"})}>重試</button>
      </div>
    </section>}
  </main>;
}
