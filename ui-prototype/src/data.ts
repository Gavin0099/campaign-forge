export type Choice = 'residents' | 'grain'
export type Screen = 'menu' | 'journey' | 'camp' | 'story' | 'deploy' | 'battle' | 'result' | 'settings'

export const scenario = {
  title: '界碑之外',
  label: '候選 A 展示情境，非正式設定',
  chapter: '第一章・名冊之外',
  mission: '渡口的最後一趟',
  premise: '軍糧與低地居民都在等船。裂潮將在下一次往返後抵達渡口。',
  narrator: '席恩',
  known: [
    '低地仍有居民，官方名冊卻記為「已撤空」。',
    '現有船隻與時間只夠完整護送其中一邊。',
    '留下的一邊會自行撤離；目前無法確定能帶出多少人或物資。'
  ],
  choices: {
    residents: {
      title: '先護送居民',
      gain: '更多低地居民可搭上這趟船。',
      cost: '部分糧車與工事器材留在低地，後續防線補給吃緊。',
      objective: '護送居民抵達北岸出口',
      support: '瑪芮提供渡口船訊',
      camp: '莉妲已在北岸搭起臨時救護所；奧倫要求重新計算守線天數。',
      outcome: '居民登上北岸，糧車仍困在低地。奧倫接受改令，但要求席恩親自承擔接下來的補給缺口。',
      next: '下一次行動：在補給不足下徵集糧車、縮短防線。'
    },
    grain: {
      title: '先護送軍糧',
      gain: '營地保住糧食與工事材料。',
      cost: '部分居民錯過軍方護送，渡口留下失散者。',
      objective: '護送糧隊抵達北岸出口',
      support: '奧倫的工事小隊可用',
      camp: '營地糧倉仍滿；莉妲要求安排回渡口尋人的行動。',
      outcome: '糧隊抵達北岸，低地居民只能自行尋路。莉妲留下照護後來的傷者，要求席恩記下失散者姓名。',
      next: '下一次行動：回收落單者與渡口遺物。'
    }
  },
  dialogue: [
    { speaker: '瑪芮', line: '名冊說這裡空了。那岸邊等船的人，是誰算進去的？' },
    { speaker: '奧倫', line: '糧車若留在低地，北岸的守軍只夠撐更短時間。我會守，但你得明說這個代價。' },
    { speaker: '莉妲', line: '救護所能接住一批人，接不住一張把他們當空白的名冊。' }
  ],
  party: [
    { id: 'shien', name: '席恩', role: '測繪與軍需副官', mark: '席', why: '想用自己的功績換取父親案件重審。', worry: '怕再次把後果交給別人的簽名。', wish: '讓受影響的人知道自己的命令。', limit: '若命令只剩數字，必須重新詢問現場的人。', leave: '仍會整理撤離路線與責任紀錄。' },
    { id: 'lida', name: '莉妲', role: '醫療者', mark: '莉', why: '想讓臨時救護所成為可交接的醫療路線。', worry: '傷患的運力被軍令徵走。', wish: '讓每個被帶走的人有名字。', limit: '若救護車遭違諾徵用，她留下照護，退出戰鬥隊伍。', leave: '在後方救護所照護傷者；主線仍可用普通補給。' },
    { id: 'olun', name: '奧倫', role: '重裝軍官', mark: '奧', why: '要帶手下活著回家。', worry: '士兵被當成沒有盡頭的掩護隊。', wish: '每次守線都有明確撤退時限。', limit: '若明知超時仍強迫留守，他會帶所部撤離。', leave: '縮短自己的防線，率兵退出當前部署。' },
    { id: 'marui', name: '瑪芮', role: '渡船斥候', mark: '瑪', why: '替渡口居民取得席位，也尋找炸橋死者證詞。', worry: '軍方再次用名冊抹去居民。', wish: '帶自己的船做能交代的救援。', limit: '若證詞遭扣留，她會離隊救人。', leave: '帶船行動；主線改走陸路或軍方運力。' }
  ],
  chapters: ['名冊之外', '誰被帶走', '橋下的名字', '誰先知道', '把名字簽上去', '撤離之後']
} as const

export const mapRows = [
  '...~~.R....',
  '..F~~.R....',
  '..F~~.R.FF.',
  '....~~..FF.',
  '.F..~~.....',
  '....RR.F...',
  '....~~.F...',
  '.....~~....',
  '.....~~~...'
]

export const unitSeeds = [
  { id: 'shien', name: '席恩', x: 1, y: 6, hp: 9, side: 'ally' as const, mark: '席' },
  { id: 'lida', name: '莉妲', x: 1, y: 7, hp: 7, side: 'ally' as const, mark: '莉' },
  { id: 'olun', name: '奧倫', x: 2, y: 7, hp: 12, side: 'ally' as const, mark: '奧' },
  { id: 'scout', name: '追兵', x: 2, y: 3, hp: 6, side: 'enemy' as const, mark: '敵' },
  { id: 'guard', name: '封路兵', x: 8, y: 5, hp: 8, side: 'enemy' as const, mark: '敵' }
]

export const artwork = { party: "/art/party-v2.png", units: "/art/units-v2.png", battlefield: "/art/ferry-scene-v2.png", campaign: "/art/campaign-v1.png" } as const
