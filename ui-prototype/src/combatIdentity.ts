import type { Clip } from "./combatPlayback";

// Presentation cast is separate from unitSeeds, deployment and story identities.
export const rehearsalCast = [
  {
    id: "demo-shien",
    name: "席恩・近戰排練",
    x: 1,
    y: 4,
    hp: 9,
    side: "ally" as const,
    mark: "席",
  },
  {
    id: "test-wizard",
    name: "測試法師",
    x: 1,
    y: 6,
    hp: 1,
    side: "ally" as const,
    mark: "法",
  },
  {
    id: "demo-scout",
    name: "目標 A",
    x: 2,
    y: 3,
    hp: 6,
    side: "enemy" as const,
    mark: "A",
  },
  {
    id: "demo-guard",
    name: "目標 B",
    x: 6,
    y: 2,
    hp: 8,
    side: "enemy" as const,
    mark: "B",
  },
];
export const demonstrationProfiles = {
  "demo-shien": {
    identity: "非魔法軍官近戰",
    classReference: null,
    abilities: ["physical"],
  },
  "test-wizard": {
    identity: "獨立測試法師",
    classReference: "Wizard",
    abilities: ["magicMissile"],
    prepared: ["magicMissile"],
  },
} as const;
export const magicMissileReference = {
  id: "magicMissile",
  name: "Magic Missile",
  spellLevel: 1,
  school: "Evocation",
  components: ["V", "S"],
  darts: 3,
  simultaneous: true,
  concentration: false,
  source: "SRD 5.2.1 p.146",
} as const;
export function permitsClip(clip: Clip) {
  if (![clip.from.x, clip.from.y, clip.to.x, clip.to.y].every(Number.isFinite))
    return false;
  if (clip.kind === "magicMissile") {
    const caster =
      clip.actor === "test-wizard" ? demonstrationProfiles[clip.actor] : null;
    return (
      !!caster &&
      caster.classReference === "Wizard" &&
      caster.prepared.includes(clip.kind) &&
      !clip.committed &&
      clip.targets?.length === magicMissileReference.darts &&
      clip.target === clip.targets[0] &&
      clip.targets.every((id) => id === "demo-scout" || id === "demo-guard")
    );
  }
  if (clip.kind !== "physical") return false;
  if (clip.actor === "demo-shien")
    return !clip.committed && clip.target === "demo-scout";
  return (
    clip.committed &&
    ["shien", "lida", "olun"].includes(clip.actor) &&
    ["scout", "guard"].includes(clip.target)
  );
}
