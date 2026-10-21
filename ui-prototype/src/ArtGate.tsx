import { CSSProperties, useEffect, useId, useRef, useState } from "react";
import { artDirections, ArtDirection, artGateState } from "./artGateScene";
import "./artGate.css";

function StudyFigure({
  id,
  direction,
  onError,
}: {
  id: string;
  direction: ArtDirection;
  onError: () => void;
}) {
  const column = ["karen", "lace", "thoma"].indexOf(id);
  const enemy = column < 0;
  const cell = enemy ? 887 : 724;
  const index = enemy ? (id === "crawler" ? 1 : 0) : column;
  const set = artDirections[direction];
  return (
    <svg
      className="ag-figure"
      viewBox={`${index * cell} 0 ${cell} ${cell}`}
      aria-hidden="true"
    >
      <image
        href={enemy ? set.enemy : set.party}
        width={cell * (enemy ? 2 : 3)}
        height={cell}
        onError={onError}
      />
    </svg>
  );
}

export function ArtGate({ onExit }: { onExit: () => void }) {
  const initial =
    new URLSearchParams(location.search).get("art") === "b" ? "b" : "a";
  const [direction, setDirection] = useState<ArtDirection>(initial);
  const [selected, setSelected] = useState<string | null>("karen");
  const [labels, setLabels] = useState(false);
  const [large, setLarge] = useState(false);
  const [plateFailed, setPlateFailed] = useState(false);
  const [figureFailed, setFigureFailed] = useState(false);
  const [ready, setReady] = useState(false);
  const focusRef = useRef<HTMLButtonElement>(null);
  const clip = `bridge-${useId().replace(/:/g, "")}`;
  const art = artDirections[direction];
  const unit = artGateState.units.find((u) => u.id === selected);
  const landmark = artGateState.landmarks.find((p) => p.id === selected);
  const stamp = JSON.stringify(artGateState);
  useEffect(() => {
    focusRef.current?.focus({ preventScroll: true });
  }, []);
  useEffect(() => {
    const esc = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        setSelected(null);
      }
    };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, []);
  function switchDirection(next: ArtDirection) {
    if (next === direction) return;
    setReady(false);
    setPlateFailed(false);
    setFigureFailed(false);
    setDirection(next);
    const url = new URL(location.href);
    url.searchParams.set("scene", "art-gate");
    url.searchParams.set("art", next);
    history.replaceState(null, "", url);
  }
  return (
    <main
      className={`ag-app ${large ? "ag-large" : ""}`}
      data-art={direction}
      data-scene-state={stamp}
      data-ready={ready && !plateFailed && !figureFailed}
    >
      <a className="ag-skip" href="#ag-inspection">
        跳到場景檢視
      </a>
      <div className="ag-stage">
        <img
          key={art.plate}
          className="ag-plate"
          src={art.plate}
          alt="洪水衝過渡口，三艘船困在橋上游；閘門高台與三箱車隊位於右岸，瑪歌和逃難者守在車旁。"
          onLoad={() => setReady(true)}
          onError={() => {
            setReady(false);
            setPlateFailed(true);
          }}
        />
        {plateFailed && (
          <div className="ag-failure" role="alert">
            場景圖片載入失敗。仍可使用下方人物與地標檢視。
            <button
              onClick={() => {
                setPlateFailed(false);
                setReady(false);
                const img =
                  document.querySelector<HTMLImageElement>(".ag-plate");
                if (img) img.src = `${art.plate}?retry=${Date.now()}`;
              }}
            >
              重試場景圖片
            </button>
          </div>
        )}
        <div className="ag-actors" aria-label="場上人物">
          {artGateState.anchors.map((p) => {
            const u = artGateState.units.find((u) => u.id === p.id)!;
            return (
              <button
                key={p.id}
                type="button"
                className={`ag-actor ${u.side} ${selected === u.id ? "is-selected" : ""}`}
                data-unit={u.id}
                aria-label={`檢視${u.name}，${u.side === "ally" ? "我方" : "敵方"}，生命${u.hp}/${u.max}`}
                aria-pressed={selected === u.id}
                style={
                  {
                    "--x": `${p.x / 16}%`,
                    "--y": `${p.y / 9}%`,
                    "--size": `${p.size / 16}cqw`,
                    zIndex: Math.round(p.y),
                  } as CSSProperties
                }
                onClick={() => setSelected(u.id)}
              >
                <span className="ag-cast-shadow" />
                <span className="ag-contact-shadow" />
                <span className="ag-ground-ring" />
                <StudyFigure
                  id={u.id}
                  direction={direction}
                  onError={() => setFigureFailed(true)}
                />
                {figureFailed && (
                  <span className="ag-figure-fallback">{u.name}</span>
                )}
              </button>
            );
          })}
        </div>
        {/* Repaint only the front bridge rail over the knight's boots. This is a fixed camera occlusion mask, not a depth buffer. */}
        {!plateFailed && (
          <svg
            className="ag-occlusion"
            viewBox="0 0 1600 900"
            aria-hidden="true"
          >
            <defs>
              <clipPath id={clip}>
                <path d="M518 369 1084 428 1080 447 1072 459 519 402Z" />
              </clipPath>
            </defs>
            <image
              href={art.plate}
              width="1600"
              height="900"
              clipPath={`url(#${clip})`}
            />
          </svg>
        )}
        <div className="ag-unit-tags" aria-hidden="true">
          {artGateState.anchors.map((p) => {
            const u = artGateState.units.find((u) => u.id === p.id)!;
            return (
              <span
                key={p.id}
                className={`ag-unit-tag ${u.side}`}
                style={{
                  left: `${p.x / 16}%`,
                  top: `${(p.y + p.size * 0.05) / 9}%`,
                }}
              >
                <b>
                  {u.side === "ally" ? "◆" : "▲"} {u.name}
                </b>
                <span className="ag-hp">
                  <i style={{ width: `${(u.hp / u.max) * 100}%` }} />
                </span>
              </span>
            );
          })}
        </div>
        <div className={`ag-landmarks ${labels ? "show-labels" : ""}`}>
          {artGateState.landmarks.map((p) => (
            <button
              type="button"
              key={p.id}
              className={`ag-landmark ${p.id === "teo" || p.id === "maggie" ? "ag-named-anchor" : ""} ${selected === p.id ? "is-selected" : ""}`}
              data-landmark={p.id}
              aria-label={`檢視${p.name}`}
              aria-pressed={selected === p.id}
              style={{ left: `${p.x / 16}%`, top: `${p.y / 9}%` }}
              onClick={() => setSelected(p.id)}
            >
              <span className="ag-landmark-dot">◇</span>
              <span className="ag-landmark-label">{p.name}</span>
            </button>
          ))}
        </div>
      </div>
      <header className="ag-header">
        <div className="ag-title">
          <span>第一章 · L03</span>
          <h1>渡口閘門</h1>
          <p>水正漲。三艘船還在橋的另一邊。</p>
        </div>
        <nav className="ag-tools" aria-label="美術候選與檢視設定">
          <div className="ag-direction" role="group" aria-label="美術方向">
            <button
              ref={focusRef}
              aria-pressed={direction === "a"}
              onClick={() => switchDirection("a")}
            >
              A <span>手繪奇幻</span>
            </button>
            <button
              aria-pressed={direction === "b"}
              onClick={() => switchDirection("b")}
            >
              B <span>立體造型</span>
            </button>
          </div>
          <button aria-pressed={labels} onClick={() => setLabels(!labels)}>
            地標
          </button>
          <button aria-pressed={large} onClick={() => setLarge(!large)}>
            大字
          </button>
          <button onClick={onExit}>返回</button>
        </nav>
      </header>
      <div className="ag-danger">
        <span aria-hidden="true">≈</span> 洪水逼近{" "}
        <span className="ag-danger-sep">／</span> K1 抉擇前
      </div>
      <footer className="ag-footer" id="ag-inspection" tabIndex={-1}>
        <section className="ag-party" aria-label="隊伍檢視">
          {artGateState.units
            .filter((u) => u.side === "ally")
            .map((u) => (
              <button
                key={u.id}
                aria-pressed={selected === u.id}
                onClick={() => setSelected(u.id)}
              >
                <span className={`ag-bust ${u.id}`}>
                  <StudyFigure
                    id={u.id}
                    direction={direction}
                    onError={() => setFigureFailed(true)}
                  />
                </span>
                <span>
                  <strong>{u.name}</strong>
                  <small>{u.role}</small>
                  <span className="ag-roster-hp">
                    ◆ {u.hp} / {u.max}
                  </span>
                </span>
              </button>
            ))}
        </section>
        <section
          className="ag-inspector"
          aria-label="選取資訊"
          aria-live="polite"
        >
          <span className="ag-inspector-kicker">
            {unit ? (unit.side === "ally" ? "我方" : "敵方") : "渡口"} ·{" "}
            {selected ? "檢視" : "等待抉擇"}
          </span>
          <h2>{unit?.name || landmark?.name || "同一股水，兩條去路"}</h2>
          <p>
            {unit
              ? `${unit.role}　生命 ${unit.hp} / ${unit.max}　·　尚未行動`
              : landmark?.detail || "先看清船上的燈、橋頭的車隊，再作決定。"}
          </p>
        </section>
        <div className="ag-caption">
          <span>
            {direction.toUpperCase()} · {art.name}
          </span>
          <span>靜態美術候選 · 待審</span>
        </div>
      </footer>
      <section className="ag-accessible-index" aria-label="場景地標索引">
        <p>場景檢視：選取只更新資訊，不推進戰鬥或抉擇。Esc 取消選取。</p>
        {artGateState.landmarks.map((p) => (
          <button key={p.id} onClick={() => setSelected(p.id)}>
            {p.name}
          </button>
        ))}
      </section>
    </main>
  );
}
