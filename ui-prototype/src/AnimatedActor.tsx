import { useId, type ReactNode } from "react";
import type { Playback, Point } from "./combatPlayback";

const ease = (v: number) => v * v * (3 - 2 * v);
const mix = (a: number, b: number, p: number) => a + (b - a) * p;
const rad = Math.PI / 180;
type P = [number, number];
const angle = (a: P, b: P) => Math.atan2(b[1] - a[1], b[0] - a[0]) / rad;
const rotate = (p: P, origin: P, degrees: number): P => {
  const x = p[0] - origin[0],
    y = p[1] - origin[1],
    c = Math.cos(degrees * rad),
    s = Math.sin(degrees * rad);
  return [origin[0] + x * c - y * s, origin[1] + x * s + y * c];
};
function elbow(a: P, end: P, upper: number, lower: number, bend = 1): P {
  const dx = end[0] - a[0],
    dy = end[1] - a[1],
    d = Math.max(0.001, Math.min(upper + lower - 0.001, Math.hypot(dx, dy)));
  const theta =
    Math.atan2(dy, dx) +
    bend *
      Math.acos(
        Math.max(
          -1,
          Math.min(
            1,
            (upper * upper + d * d - lower * lower) / (2 * upper * d),
          ),
        ),
      );
  return [a[0] + Math.cos(theta) * upper, a[1] + Math.sin(theta) * upper];
}
type Piece = { name: string; path: string; anchor: P; end?: P };
type Rig = {
  href: string;
  width: number;
  height: number;
  scale: number;
  origin: P;
  hip: P;
  shoulder: P;
  joint: P;
  wrist: P;
  pieces: Piece[];
};
const soldier: Rig = {
  href: "/art/units-v2.png",
  width: 2000,
  height: 800,
  scale: 0.3,
  origin: [177, 680],
  hip: [186, 486],
  shoulder: [249, 367],
  joint: [262, 417],
  wrist: [289, 477],
  pieces: [
    {
      name: "legs",
      anchor: [186, 486],
      path: "M116 466L246 469L265 544L265 613L279 636L231 643L202 624L199 572L162 601L136 673L111 697L67 688L78 644L100 566Z",
    },
    {
      name: "coat",
      anchor: [186, 486],
      path: "M131 322L187 325L231 335L246 367L244 404L247 442L274 497L300 541L275 562L222 529L207 477L174 477L148 511L101 547L44 522L67 456L83 422L85 367Z",
    },
    {
      name: "head",
      anchor: [186, 486],
      path: "M117 234L199 232L242 251L258 278L250 312L229 339L205 349L163 334L139 309Z",
    },
    {
      name: "upper",
      anchor: [249, 367],
      end: [262, 417],
      path: "M239 350L265 357L278 389L278 420L259 435L242 414L235 378Z",
    },
    {
      name: "fore",
      anchor: [262, 417],
      end: [289, 477],
      path: "M250 411L274 414L286 440L303 468L304 484L292 496L276 489L270 466L254 447Z",
    },
  ],
};
const shienLegs = [
  {
    hip: [167, 484] as P,
    knee: [128, 566] as P,
    ankle: [100, 650] as P,
    upper: "M127 467L190 473L177 522L157 572L138 585L107 574L108 550Z",
    lower: "M107 565L149 577L137 618L122 654L93 661L77 648L87 614Z",
    foot: "M83 640L122 640L128 667L129 681L114 696L79 688L68 673Z",
  },
  {
    hip: [216, 488] as P,
    knee: [226, 552] as P,
    ankle: [237, 612] as P,
    upper: "M189 472L239 470L253 522L248 560L215 570L196 550L180 524Z",
    lower: "M214 550L248 549L255 585L256 613L238 628L211 614Z",
    foot: "M212 602L254 600L262 613L281 630L276 642L244 645L220 633L207 620Z",
  },
];
const mage: Rig = {
  href: "/art/test-caster-v4.png",
  width: 1024,
  height: 1536,
  scale: 0.09,
  origin: [535, 1465],
  hip: [535, 690],
  shoulder: [654, 346],
  joint: [724, 534],
  wrist: [837, 677],
  pieces: [
    {
      name: "legs",
      anchor: [535, 690],
      path: "M435 670L635 670L688 1084L722 1306L804 1383L783 1419L643 1424L583 1390L578 1117L534 920L466 1137L431 1369L449 1435L419 1475L291 1477L286 1449L330 1360L349 1119Z",
    },
    {
      name: "coat",
      anchor: [535, 690],
      path: "M381 276L421 256L436 205L488 224L521 240L579 213L590 259L636 276L660 332L651 450L649 568L675 703L728 890L783 1056L847 1158L837 1230L792 1254L732 1223L665 1104L594 881L585 756L542 733L492 754L459 941L378 1167L327 1212L246 1211L187 1124L263 985L331 796L374 655L391 529L365 417L353 334Z",
    },
    {
      name: "head",
      anchor: [535, 690],
      path: "M425 41L511 35L596 53L614 84L609 107L632 142L611 165L603 210L566 236L524 225L490 202L459 163L435 135L433 102L415 91Z",
    },
    {
      name: "upper",
      anchor: [654, 346],
      end: [724, 534],
      path: "M634 282L673 302L706 359L730 421L765 492L745 540L706 568L668 534L662 484L643 428L630 362Z",
    },
    {
      name: "fore",
      anchor: [724, 534],
      end: [837, 677],
      path: "M696 523L733 521L756 563L790 604L826 631L852 631L890 612L930 618L928 636L902 650L946 664L963 684L950 693L919 683L947 708L935 721L904 706L920 736L904 747L872 724L859 747L842 738L819 706L798 689L762 660L733 623L706 588L688 554Z",
    },
    {
      name: "back-upper",
      anchor: [377, 350],
      end: [294, 528],
      path: "M349 290L387 287L410 333L386 398L357 460L340 520L309 553L262 541L232 509L247 478L284 411L307 347Z",
    },
    {
      name: "back-fore",
      anchor: [294, 528],
      end: [258, 666],
      path: "M262 513L307 526L314 562L297 600L286 636L284 665L302 684L286 699L275 686L275 723L295 741L287 754L266 746L270 770L256 782L238 769L220 742L209 713L211 679L231 634L233 576Z",
    },
  ],
};
const enemyRig = (guard: boolean): Rig => {
  const shift = guard ? 1600 : 1200;
  const base: Rig = {
    href: "/art/units-v2.png",
    width: 2000,
    height: 800,
    scale: 0.3,
    origin: [200 + shift, 680],
    hip: [211 + shift, 489],
    shoulder: [249 + shift, 367],
    joint: [262 + shift, 417],
    wrist: [289 + shift, 477],
    pieces: [],
  };
  const paths = guard
    ? [
        [
          "legs",
          "M118 458L272 458L281 544L298 622L330 653L324 691L278 699L250 674L221 579L190 590L164 652L128 671L89 661L83 638L118 557Z",
        ],
        [
          "coat",
          "M127 323L186 326L256 327L288 353L322 404L363 449L365 541L332 580L279 554L239 541L211 568L161 550L117 559L96 507L98 432L87 377Z",
        ],
        [
          "head",
          "M160 232L208 226L249 254L264 291L247 335L218 355L174 344L148 316L148 270Z",
        ],
      ]
    : [
        [
          "legs",
          "M135 474L267 475L280 549L309 620L336 646L336 681L302 700L273 689L249 636L218 567L181 593L159 641L132 670L96 668L85 646L109 608L126 555Z",
        ],
        [
          "coat",
          "M128 330L183 326L230 340L272 335L302 369L302 423L276 460L302 484L346 515L361 552L344 569L297 535L251 510L239 549L182 557L140 539L108 561L98 521L102 447L91 383Z",
        ],
        [
          "head",
          "M142 254L207 240L244 254L283 275L302 312L280 349L250 371L199 359L176 340L159 308Z",
        ],
      ];
  // Translate the original atlas coordinates into each column without touching bitmap pixels.
  base.pieces = paths.map(([name, path]) => ({
    name,
    anchor: base.hip,
    path: path.replace(
      /(-?\d+) (-?\d+)/g,
      (_m, x, y) => `${Number(x) + shift} ${y}`,
    ),
  }));
  return base;
};
function local(r: Rig, p: P): P {
  return [(p[0] - r.origin[0]) * r.scale, (p[1] - r.origin[1]) * r.scale];
}
function Part({
  rig,
  piece,
  target,
  rotation = 0,
  magnify = 1,
}: {
  rig: Rig;
  piece: Piece;
  target: P;
  rotation?: number;
  magnify?: number;
}) {
  const id = useId().replace(/:/g, "");
  return (
    <g
      data-part={piece.name}
      transform={`translate(${target}) rotate(${rotation}) scale(${rig.scale * magnify}) translate(${-piece.anchor[0]} ${-piece.anchor[1]})`}
    >
      <defs>
        <clipPath id={id}>
          <path d={piece.path} />
        </clipPath>
      </defs>
      <image
        href={rig.href}
        width={rig.width}
        height={rig.height}
        clipPath={`url(#${id})`}
      />
    </g>
  );
}
function PlantedLeg({
  leg,
  index,
  offset,
  gait = [0, 0],
}: {
  leg: (typeof shienLegs)[number];
  index: number;
  offset: P;
  gait?: P;
}) {
  const a = local(soldier, leg.hip),
    b = local(soldier, leg.knee),
    originalFoot = local(soldier, leg.ankle);
  const c: P = [originalFoot[0] + gait[0], originalFoot[1] + gait[1]];
  const hip: P = [a[0] + offset[0], a[1] + offset[1]];
  const joint = elbow(
    hip,
    c,
    Math.hypot(b[0] - a[0], b[1] - a[1]),
    Math.hypot(originalFoot[0] - b[0], originalFoot[1] - b[1]),
    1,
  );
  return (
    <g data-leg={index}>
      <Part
        rig={soldier}
        piece={{ name: `foot-${index}`, path: leg.foot, anchor: leg.ankle }}
        target={c}
      />
      <Part
        rig={soldier}
        piece={{ name: `shin-${index}`, path: leg.lower, anchor: leg.knee }}
        target={joint}
        rotation={angle(joint, c) - angle(b, originalFoot)}
      />
      <Part
        rig={soldier}
        piece={{ name: `thigh-${index}`, path: leg.upper, anchor: leg.hip }}
        target={hip}
        rotation={angle(hip, joint) - angle(a, b)}
      />
    </g>
  );
}
export function rigPose(id: string, clip: Playback | null) {
  const own = clip?.actor === id;
  const hit = !!clip && (clip.targets || [clip.target]).includes(id);
  let body = 0,
    attack = 0,
    recoil = 0,
    casting = 0;
  if (own && clip) {
    const p = ease(clip.progress);
    if (clip.kind === "physical") {
      if (clip.stage === "windup") {
        body = mix(0, -10, p);
        attack = -p;
      }
      if (clip.stage === "release") {
        body = mix(-10, 9, p);
        attack = mix(-1, 1, p);
      }
      if (["contact", "impact", "reaction"].includes(clip.stage)) {
        body = 9;
        attack = 1;
      }
      if (clip.stage === "recovery") {
        body = mix(9, 0, p);
        attack = 1 - p;
      }
    } else {
      casting =
        clip.stage === "windup" ? p : clip.stage === "recovery" ? 1 - p : 1;
      body = casting * 3;
    }
  }
  if (hit && clip) {
    recoil =
      clip.stage === "impact"
        ? 0.12
        : clip.stage === "reaction"
          ? mix(0.12, 1, ease(clip.progress))
          : clip.stage === "recovery"
            ? 1 - ease(clip.progress)
            : 0;
    body = -18 * recoil;
  }
  return { body, attack, recoil, casting };
}
export function AnimatedActor({
  id = "shien",
  clip,
  reduced,
  contact,
  facing = 1,
  children,
}: {
  id?: string;
  clip: Playback | null;
  reduced: boolean;
  contact?: Point;
  facing?: number;
  children?: ReactNode;
}) {
  const isMage = id === "test-wizard",
    isEnemy = /scout|guard/.test(id);
  const rig = isMage
    ? mage
    : isEnemy
      ? enemyRig(id.includes("guard"))
      : soldier;
  const pose = rigPose(id, reduced ? null : clip),
    baseHip = local(rig, rig.hip);
  const walking = !reduced && clip?.actor === id && clip.stage === "move";
  const offset: P =
    !isMage && !isEnemy
      ? walking
        ? [0, 3 + Math.sin(clip.progress * Math.PI * 8) * 1.2]
        : [
            pose.attack < 0 ? pose.attack * 1.5 : pose.attack * 2,
            Math.abs(pose.attack) * 3,
          ]
      : [0, 0];
  const gait = (index: number): P => {
    if (!walking || !clip) return [0, 0];
    const phase = (clip.progress * 2 + index * 0.5) % 1;
    const travel =
      phase < 0.5 ? 0.25 - phase : mix(-0.25, 0.25, ease((phase - 0.5) * 2));
    const blend = Math.min(1, clip.progress * 12, (1 - clip.progress) * 12);
    const dx = (clip.to.x - clip.from.x - (clip.to.y - clip.from.y)) * 50;
    const dy = (clip.to.x - clip.from.x + clip.to.y - clip.from.y) * 25;
    return [
      (dx / 2) * travel * blend,
      (dy / 2) * travel * blend -
        (phase > 0.5 ? Math.sin((phase - 0.5) * Math.PI * 2) * 7 : 0),
    ];
  };
  const hip: P = [baseHip[0] + offset[0], baseHip[1] + offset[1]];
  const torso = (p: P) => {
    const point = local(rig, p);
    return rotate([point[0] + offset[0], point[1] + offset[1]], hip, pose.body);
  };
  const pieces = Object.fromEntries(rig.pieces.map((p) => [p.name, p]));
  const shoulder = torso(rig.shoulder);
  let wrist = torso(rig.wrist),
    swordAngle = 55;
  if (!isMage && !isEnemy) {
    const a = pose.attack;
    const contactPoint: P = contact
      ? [contact.x * facing, contact.y]
      : [90, -80];
    const finalAngle =
      Math.atan2(contactPoint[1] + 80, contactPoint[0] - 48) / rad;
    const impactWrist: P = [
      contactPoint[0] - Math.cos(finalAngle * rad) * 42,
      contactPoint[1] - Math.sin(finalAngle * rad) * 42,
    ];
    if (clip?.actor === id && clip.stage === "release") {
      const p = ease(clip.progress);
      wrist = [mix(-2, impactWrist[0], p), mix(-119, impactWrist[1], p)];
      swordAngle = mix(-147, finalAngle, p);
    } else if (a < 0) {
      wrist = [mix(wrist[0], -2, -a), mix(wrist[1], -119, -a)];
      swordAngle = mix(55, -147, -a);
    } else if (a > 0) {
      wrist = [
        mix(wrist[0], impactWrist[0], a),
        mix(wrist[1], impactWrist[1], a),
      ];
      swordAngle = mix(55, finalAngle, a);
    }
  }
  if (isMage)
    wrist = [
      mix(wrist[0], 39, pose.casting),
      mix(wrist[1], -111, pose.casting),
    ];
  const upper =
    Math.hypot(rig.joint[0] - rig.shoulder[0], rig.joint[1] - rig.shoulder[1]) *
    rig.scale;
  const lower =
    Math.hypot(rig.wrist[0] - rig.joint[0], rig.wrist[1] - rig.joint[1]) *
    rig.scale;
  // Keep bone lengths fixed; clamp unreachable hands instead of stretching the artwork.
  const reach = Math.hypot(wrist[0] - shoulder[0], wrist[1] - shoulder[1]);
  if (reach > upper + lower - 0.05) {
    const s = (upper + lower - 0.05) / reach;
    wrist = [
      shoulder[0] + (wrist[0] - shoulder[0]) * s,
      shoulder[1] + (wrist[1] - shoulder[1]) * s,
    ];
  }
  const joint = elbow(shoulder, wrist, upper, lower, isMage ? 1 : -1);
  const upperRot = angle(shoulder, joint) - angle(rig.shoulder, rig.joint),
    lowerRot = angle(joint, wrist) - angle(rig.joint, rig.wrist);
  const swordTip = {
    x: (wrist[0] + 42 * Math.cos(swordAngle * rad)) * facing,
    y: wrist[1] + 42 * Math.sin(swordAngle * rad),
  };
  const chest = torso([rig.origin[0] + 33, rig.origin[1] - 283]);
  const neck: P = isMage
    ? [535, 225]
    : isEnemy
      ? [rig.origin[0] + 30, 355]
      : [209, 333];
  // Painted L03 figures reuse the move clock and restrained walk bob, without
  // pretending that their single-frame art has the soldier's articulated rig.
  if (children) return (
    <g className="animated-actor" data-pose={clip?.stage || "idle"}
      data-feet={walking ? "walking" : "fixed"}
      transform={`translate(0 ${walking && clip ? Math.sin(clip.progress * Math.PI * 4) * 2 : 0})`}>
      {children}
    </g>
  );
  return (
    <g
      className="animated-actor cutout-actor"
      data-rig={isMage ? "wizard" : isEnemy ? "enemy" : "shien"}
      data-pose={clip?.stage || "idle"}
      data-body-angle={pose.body.toFixed(3)}
      data-recoil={pose.recoil.toFixed(3)}
      data-tip-x={swordTip.x.toFixed(3)}
      data-tip-y={swordTip.y.toFixed(3)}
      data-contact-x={(chest[0] * facing).toFixed(3)}
      data-contact-y={chest[1].toFixed(3)}
      data-feet={walking ? "walking" : "fixed"}
      transform={`scale(${facing} 1)`}
    >
      {!isMage && !isEnemy ? (
        [1, 0].map((index) => (
          <PlantedLeg
            key={index}
            leg={shienLegs[index]}
            index={index}
            offset={offset}
            gait={gait(index)}
          />
        ))
      ) : (
        <Part rig={rig} piece={pieces.legs} target={hip} />
      )}
      {isMage && (
        <g>
          <Part
            rig={rig}
            piece={pieces["back-upper"]}
            target={torso([377, 350])}
            rotation={pose.body + pose.casting * 28}
          />
          <Part
            rig={rig}
            piece={pieces["back-fore"]}
            target={rotate(
              torso([294, 528]),
              torso([377, 350]),
              pose.casting * 28,
            )}
            rotation={pose.body + pose.casting * 75}
          />
        </g>
      )}
      <Part rig={rig} piece={pieces.coat} target={hip} rotation={pose.body} />
      <Part
        rig={rig}
        piece={{ ...pieces.head, anchor: neck }}
        target={torso(neck)}
        rotation={pose.body + (isEnemy ? pose.recoil * 5 : 0)}
        magnify={isMage ? 1.6 : 1}
      />
      {!isMage && !isEnemy && (
        <g
          data-weapon="shortsword"
          data-length="42"
          transform={`translate(${wrist}) rotate(${swordAngle})`}
        >
          <path
            d="M-11 -3H1V3H-11Z"
            fill="#483425"
            stroke="#221e1a"
            strokeWidth="1.5"
          />
          <path d="M1 -8V8" stroke="#b59c62" strokeWidth="3" />
          <path
            d="M4 -4L32 -3L42 0L32 3L4 4Z"
            fill="#c5c9b9"
            stroke="#242d2c"
            strokeWidth="1.2"
          />
          <path d="M5 0H39L31 -2H5Z" fill="#f1edcf" />
          <path d="M-9 -2L-3 2M-5 -2L1 2" stroke="#9b8662" strokeWidth="1" />
        </g>
      )}
      {!isEnemy && (
        <>
          <Part
            rig={rig}
            piece={pieces.upper}
            target={shoulder}
            rotation={upperRot}
          />
          <Part
            rig={rig}
            piece={pieces.fore}
            target={joint}
            rotation={lowerRot}
          />
        </>
      )}
    </g>
  );
}
