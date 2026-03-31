#!/usr/bin/env python3
"""
Add 均一課綱風格題目 to each grade/subject JSON.
Questions are self-authored but follow the same topics and style
as Junyi Academy (junyiacademy.org) curriculum.
"""
import json, os, random

ROOT = os.path.join(os.path.dirname(__file__), '..', 'questions')

def load(grade, sub):
    path = os.path.join(ROOT, grade, f'{sub}.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f), path

def save(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'  saved {path} ({len(data["questions"])} 題)')

def add(data, new_qs):
    existing_ids = {q['id'] for q in data['questions']}
    added = 0
    for q in new_qs:
        if q['id'] not in existing_ids:
            data['questions'].append(q)
            added += 1
    data['meta']['count'] = len(data['questions'])
    return added

# ── helpers ────────────────────────────────────────────────────────
def mcq(id_, q, opts, a, tags):
    return {'id': id_, 'type': 'mcq', 'q': q, 'opts': opts, 'a': a, 'tags': tags}

def tf(id_, q, a, tags):
    return {'id': id_, 'type': 'tf', 'q': q, 'opts': ['正確', '錯誤'], 'a': a, 'tags': tags}

# ================================================================
# KINDER MATH  km0110+
# ================================================================
kinder_math = [
    mcq('km0110','小明有 3 個蘋果，媽媽又給他 2 個，小明現在共有幾個蘋果？',['3','4','5','6'],2,['addition','word-problem']),
    mcq('km0111','盤子上有 6 顆糖果，小花吃掉 2 顆，還剩幾顆？',['2','3','4','5'],2,['subtraction','word-problem']),
    mcq('km0112','教室裡有 4 張桌子，再搬來 3 張，現在共有幾張桌子？',['5','6','7','8'],2,['addition','word-problem']),
    mcq('km0113','樹上有 5 隻鳥，飛走了 2 隻，樹上剩幾隻？',['1','2','3','4'],2,['subtraction','word-problem']),
    mcq('km0114','籃子裡有 2 顆橘子和 4 顆芭樂，籃子裡共有幾顆水果？',['4','5','6','7'],2,['addition','word-problem']),
    mcq('km0115','小英有 7 枝鉛筆，送給妹妹 3 枝，還剩幾枝？',['2','3','4','5'],2,['subtraction','word-problem']),
    mcq('km0116','草地上有 3 隻兔子，又跑來 5 隻，現在共有幾隻兔子？',['6','7','8','9'],2,['addition','word-problem']),
    mcq('km0117','圓形、三角形、正方形，哪一個沒有角？',['三角形','正方形','圓形','都有角'],2,['shape']),
    mcq('km0118','哪個數字比 5 大、比 8 小？',['4','6','8','9'],1,['comparison','number']),
    mcq('km0119','1、2、3、4、__，下一個數字是？',['4','5','6','7'],1,['counting','sequence']),
    mcq('km0120','小狗有 4 條腿，2 隻小狗共有幾條腿？',['6','7','8','9'],2,['multiplication','counting']),
    tf('km0121','10 比 9 大。',0,['comparison','number']),
    tf('km0122','三角形有 4 個角。',1,['shape','tf']),
    mcq('km0123','花園裡有紅花 3 朵、黃花 4 朵，共有幾朵花？',['5','6','7','8'],2,['addition','word-problem']),
    mcq('km0124','書架上有 9 本書，借走 4 本，還剩幾本？',['3','4','5','6'],2,['subtraction','word-problem']),
    mcq('km0125','6 和 3，哪個數字比較小？',['6','3','一樣大','無法比較'],1,['comparison']),
    mcq('km0126','小朋友排隊，小明排第 3 個，他前面有幾個人？',['1','2','3','4'],1,['ordinal','counting']),
    tf('km0127','5 + 4 = 9。',0,['addition','tf']),
    mcq('km0128','積木有 5 塊紅色和 2 塊藍色，共有幾塊積木？',['5','6','7','8'],2,['addition','word-problem']),
    mcq('km0129','媽媽買了 8 顆雞蛋，打破了 1 顆，還有幾顆？',['6','7','8','9'],1,['subtraction','word-problem']),
]

# ================================================================
# KINDER CHINESE  kc043+
# ================================================================
kinder_chinese = [
    mcq('kc043','下面哪個字的意思是「很開心」？',['哭','笑','跑','睡'],1,['emotion','character']),
    mcq('kc044','「大」的相反是什麼？',['小','高','多','長'],0,['antonym']),
    mcq('kc045','下面哪個是動物？',['桌子','蘋果','貓咪','鉛筆'],2,['category','animal']),
    mcq('kc046','「上」的相反是什麼？',['前','後','下','左'],2,['antonym','direction']),
    mcq('kc047','爸爸的媽媽叫什麼？',['阿姨','奶奶','姑姑','媽媽'],1,['family']),
    mcq('kc048','哪一個字和「水」有關？',['火','海','山','土'],1,['radical','water']),
    mcq('kc049','下面哪個是顏色？',['跑步','綠色','蘋果','快樂'],1,['color']),
    tf('kc050','「貓」是動物。',0,['animal','tf']),
    mcq('kc051','「快」的相反是什麼？',['跑','慢','高','多'],1,['antonym']),
    mcq('kc052','太陽從哪裡升起？',['西邊','南邊','東邊','北邊'],2,['nature','direction']),
    tf('kc053','天空是藍色的。',0,['nature','tf']),
    mcq('kc054','下面哪個字代表數量最多？',['一','三','七','九'],3,['number','character']),
    mcq('kc055','媽媽的哥哥叫什麼？',['叔叔','舅舅','伯伯','爺爺'],1,['family']),
    tf('kc056','魚生活在水裡。',0,['animal','nature','tf']),
    mcq('kc057','下面哪個字是水果？',['桌子','椅子','香蕉','書包'],2,['food','category']),
]

# ================================================================
# KINDER ENGLISH  ke043+
# ================================================================
kinder_english = [
    mcq('ke043','Which animal says "moo"?',['Dog','Cat','Cow','Bird'],2,['animal','sound']),
    mcq('ke044','What color is the sky?',['Red','Green','Blue','Yellow'],2,['color']),
    mcq('ke045','How many fingers do you have on one hand?',['3','4','5','6'],2,['number','body']),
    mcq('ke046','Which is a fruit?',['Chair','Apple','Book','Pen'],1,['food','category']),
    tf('ke047','A cat has four legs.',0,['animal','tf']),
    mcq('ke048','What do you say in the morning?',['Good night','Good morning','Goodbye','Thank you'],1,['greeting']),
    mcq('ke049','Which letter comes after "B"?',['A','C','D','E'],1,['alphabet']),
    mcq('ke050','What color is the sun?',['Blue','Green','Yellow','Purple'],2,['color','nature']),
    tf('ke051','A fish can fly.',1,['animal','tf']),
    mcq('ke052','Which is a body part?',['Table','Nose','Apple','Rain'],1,['body']),
    mcq('ke053','How do you say 再見 in English?',['Hello','Sorry','Goodbye','Thank you'],2,['greeting']),
    tf('ke054','There are 7 days in a week.',0,['time','tf']),
    mcq('ke055','Which animal lives in the ocean?',['Dog','Horse','Fish','Cat'],2,['animal']),
    mcq('ke056','What comes after 4?',['3','5','6','7'],1,['number']),
    tf('ke057','Red, blue, and yellow are colors.',0,['color','tf']),
]

# ================================================================
# GRADE 1 MATH  g1m0088+
# ================================================================
grade1_math = [
    mcq('g1m0088','小柔有 13 顆糖，小剛有 7 顆糖，兩人共有幾顆糖？',['18','19','20','21'],2,['addition','word-problem']),
    mcq('g1m0089','媽媽買了 20 個紅豆餅，吃掉 6 個，還剩幾個？',['12','13','14','15'],2,['subtraction','word-problem']),
    mcq('g1m0090','小明有 8 枝鉛筆，小華有 5 枝，小明比小華多幾枝？',['2','3','4','5'],1,['subtraction','comparison']),
    mcq('g1m0091','教室有 3 排座位，每排 6 個，共有幾個座位？',['15','16','17','18'],3,['multiplication','counting']),
    mcq('g1m0092','小如撈到 3 條魚，小莉撈到 5 條魚，小柔撈到 6 條魚，三人共撈到幾條魚？',['12','13','14','15'],2,['addition','word-problem']),
    mcq('g1m0093','花園裡有 16 朵花，風吹落了 9 朵，剩幾朵？',['6','7','8','9'],1,['subtraction','word-problem']),
    mcq('g1m0094','一盒有 10 顆餅乾，2 盒共有幾顆？',['10','15','20','25'],2,['multiplication','counting']),
    tf('g1m0095','15 + 5 = 20。',0,['addition','tf']),
    mcq('g1m0096','小剛有貼紙 15 張，他送出 5 張後和小柔一樣多，小柔有幾張貼紙？',['8','9','10','11'],2,['subtraction','word-problem']),
    mcq('g1m0097','一條繩子長 18 公分，剪掉 7 公分，還剩幾公分？',['9','10','11','12'],2,['subtraction','word-problem']),
    tf('g1m0098','20 減 8 等於 11。',1,['subtraction','tf']),
    mcq('g1m0099','停車場有 9 輛車，開走 4 輛，又來了 3 輛，現在有幾輛？',['7','8','9','10'],1,['mixed','word-problem']),
    mcq('g1m0100','小朋友有 17 個，男生 9 個，女生有幾個？',['7','8','9','10'],1,['subtraction','word-problem']),
    tf('g1m0101','9 + 8 = 18。',1,['addition','tf']),
    mcq('g1m0102','書架上原來有 12 本書，借走 7 本，又還回來 3 本，現在有幾本？',['7','8','9','10'],1,['mixed','word-problem']),
    mcq('g1m0103','2、4、6、8、__，下一個數字是？',['9','10','11','12'],1,['counting','pattern']),
    mcq('g1m0104','5、10、15、__，下一個數字是？',['18','19','20','21'],2,['counting','pattern']),
    tf('g1m0105','10 + 10 = 21。',1,['addition','tf']),
    mcq('g1m0106','一個班有 20 個學生，今天有 3 個請假，出席幾人？',['15','16','17','18'],2,['subtraction','word-problem']),
    mcq('g1m0107','河流兩岸各有 8 棵樹，共有幾棵樹？',['14','15','16','17'],2,['addition','word-problem']),
]

# ================================================================
# GRADE 1 CHINESE  g1c041+
# ================================================================
grade1_chinese = [
    mcq('g1c041','「冷」的相反詞是什麼？',['涼','熱','暖','凍'],1,['antonym']),
    mcq('g1c042','哪個詞語描述心情很好？',['難過','生氣','開心','害怕'],2,['emotion']),
    mcq('g1c043','「天空」中的「天」是指什麼？',['地面','雲朵','天氣','天空'],3,['vocabulary']),
    mcq('g1c044','「春夏秋冬」裡，哪個季節最熱？',['春','夏','秋','冬'],1,['season']),
    tf('g1c045','「貓」和「狗」都是動物。',0,['animal','tf']),
    mcq('g1c046','下面哪個字和「山」相關？',['岩石','海洋','沙漠','城市'],0,['nature','character']),
    mcq('g1c047','「上學」的相反是什麼？',['讀書','放學','休息','玩耍'],1,['antonym','school']),
    mcq('g1c048','哪個句子是問句？',['今天天氣好。','小明吃飯了。','你叫什麼名字？','我喜歡玩。'],2,['sentence','punctuation']),
    tf('g1c049','一年有 12 個月。',0,['time','tf']),
    mcq('g1c050','「大樹」裡的「大」是形容什麼？',['顏色','大小','重量','形狀'],1,['adjective']),
    mcq('g1c051','下面哪個字可以填入「___色的花」？',['黑','紅','重','快'],1,['color','adjective']),
    tf('g1c052','「月亮」晚上才看得到。',0,['nature','tf']),
    mcq('g1c053','「手」的部首是什麼？',['木','水','手','人'],2,['radical']),
    mcq('g1c054','下面哪個詞語表示方向？',['快樂','東西','吃飯','看書'],1,['direction']),
    mcq('g1c055','「吃飯、喝水、睡覺」都屬於什麼？',['玩耍','動作','顏色','地方'],1,['verb','category']),
]

# ================================================================
# GRADE 1 ENGLISH  g1e041+
# ================================================================
grade1_english = [
    mcq('g1e041','What is 6 + 4?',['8','9','10','11'],2,['math','number']),
    mcq('g1e042','Which day comes after Monday?',['Sunday','Wednesday','Tuesday','Friday'],2,['days']),
    mcq('g1e043','How do you say 謝謝 in English?',['Sorry','Please','Thank you','Hello'],2,['greeting']),
    tf('g1e044','A mother is a woman.',0,['family','tf']),
    mcq('g1e045','Which is a classroom object?',['Apple','River','Desk','Mountain'],2,['school','noun']),
    mcq('g1e046','What color is grass?',['Blue','Red','Green','Yellow'],2,['color','nature']),
    mcq('g1e047','How many days are in a week?',['5','6','7','8'],2,['time','number']),
    tf('g1e048','Sister is a girl.',0,['family','tf']),
    mcq('g1e049','Which word means the opposite of "big"?',['Tall','Small','Heavy','Fast'],1,['antonym']),
    mcq('g1e050','What do you use to write?',['Fork','Pencil','Spoon','Cup'],1,['school','noun']),
    tf('g1e051','February comes before January.',1,['months','tf']),
    mcq('g1e052','Which animal can swim?',['Cat','Dog','Fish','Bird'],2,['animal']),
    mcq('g1e053','How do you greet someone in the evening?',['Good morning','Good afternoon','Good evening','Good night'],2,['greeting','time']),
    tf('g1e054','There are 26 letters in the English alphabet.',0,['alphabet','tf']),
    mcq('g1e055','Which word is a verb (動作)?',['Run','Happy','Blue','Book'],0,['verb','grammar']),
]

# ================================================================
# GRADE 2 MATH  g2m0134+
# ================================================================
grade2_math = [
    mcq('g2m0134','小明有一條長 245 公分的繩子，小華有一條長 138 公分的繩子，兩人共有多長？',['373','383','383','393'],1,['addition','word-problem','3-digit']),
    mcq('g2m0135','學校有 325 本故事書，借出去 147 本，還剩幾本？',['168','178','188','198'],1,['subtraction','word-problem','3-digit']),
    mcq('g2m0136','一包餅乾重 256 公克，一包糖果重 183 公克，兩包共重幾公克？',['429','439','449','459'],1,['addition','word-problem','3-digit']),
    mcq('g2m0137','4 × 7 = ?',['24','27','28','32'],2,['multiplication','times-table']),
    mcq('g2m0138','6 × 8 = ?',['42','46','48','56'],2,['multiplication','times-table']),
    mcq('g2m0139','9 × 3 = ?',['24','27','30','33'],1,['multiplication','times-table']),
    mcq('g2m0140','現在是 3 點鐘，2 小時後是幾點？',['4點','5點','6點','7點'],1,['time','clock']),
    tf('g2m0141','5 × 6 = 30。',0,['multiplication','tf']),
    mcq('g2m0142','媽媽買了 3 盒雞蛋，每盒 8 顆，共有幾顆雞蛋？',['21','22','23','24'],3,['multiplication','word-problem']),
    mcq('g2m0143','火車有 6 節車廂，每節有 52 個座位，共有幾個座位？',['302','312','322','332'],1,['multiplication','word-problem']),
    tf('g2m0144','7 × 8 = 54。',1,['multiplication','tf']),
    mcq('g2m0145','一個長方形長 8 公分、寬 5 公分，周長是多少公分？',['24','26','28','30'],1,['geometry','perimeter']),
    mcq('g2m0146','現在是 10:30，半小時後是幾點幾分？',['10:00','10:30','11:00','11:30'],2,['time','clock']),
    mcq('g2m0147','農場有雞 4 隻和牛 3 頭，動物的腳共有幾條？',['20','22','24','26'],2,['multiplication','word-problem']),
    tf('g2m0148','400 + 300 = 700。',0,['addition','3-digit','tf']),
    mcq('g2m0149','一個正方形的邊長是 6 公分，周長是幾公分？',['18','22','24','28'],2,['geometry','perimeter']),
    mcq('g2m0150','書店原有書 500 本，賣出 237 本，還剩幾本？',['253','263','273','283'],1,['subtraction','word-problem','3-digit']),
    mcq('g2m0151','2 × 3 × 4 = ?',['12','18','24','36'],2,['multiplication','multi-step']),
    tf('g2m0152','一個星期有 7 天。',0,['time','tf']),
    mcq('g2m0153','小柔有 48 元，買了一枝 15 元的鉛筆，還剩多少元？',['31','33','35','37'],1,['subtraction','word-problem','money']),
]

# ================================================================
# GRADE 2 CHINESE  g2c0041+
# ================================================================
grade2_chinese = [
    mcq('g2c0041','「快樂」的近義詞是？',['難過','開心','生氣','害怕'],1,['synonym']),
    mcq('g2c0042','「寬廣」的反義詞是？',['廣大','遼闊','狹窄','平坦'],2,['antonym']),
    mcq('g2c0043','下列哪個詞語和「昆蟲」有關？',['大象','蝴蝶','鯨魚','老虎'],1,['category','animal']),
    mcq('g2c0044','「春天來了，花開了。」這句話表達了什麼？',['秋天的景色','春天的景色','夏天的景色','冬天的景色'],1,['sentence','season']),
    tf('g2c0045','「喜」字的部首是「口」。',0,['radical','tf']),
    mcq('g2c0046','「他跑得___快」，空格應填入什麼？',['非常','一下','什麼','那麼'],0,['adverb','fill-blank']),
    mcq('g2c0047','「日出而作，日落而息」這句話中「作」是什麼意思？',['睡覺','工作','玩耍','讀書'],1,['idiom','vocabulary']),
    mcq('g2c0048','下列哪個詞語是動詞？',['美麗','書本','奔跑','紅色'],2,['verb','grammar']),
    tf('g2c0049','「雨」的部首是「雨」。',0,['radical','tf']),
    mcq('g2c0050','「海洋」中的「洋」字，三點水代表與什麼有關？',['火','木','水','土'],2,['radical','water']),
    mcq('g2c0051','「___的天空，白白的雲。」空格應填什麼顏色？',['紅紅','綠綠','藍藍','黃黃'],2,['adjective','color']),
    mcq('g2c0052','以下哪個句子沒有錯誤？',['我去了公園昨天。','昨天我去了公園。','公園我去了昨天。','昨天公園我去了。'],1,['sentence','order']),
    tf('g2c0053','「蝴蝶」是一種昆蟲。',0,['animal','tf']),
    mcq('g2c0054','「她每天早上__起床，__刷牙，__吃早餐。」空格最適合填入什麼？',['先...再...然後','因為...所以...但是','雖然...但是...所以','如果...就...那麼'],0,['conjunction','sequence']),
    mcq('g2c0055','「光」字加上三點水旁，變成什麼字？',['炸','洗','沙','洸'],3,['radical','character']),
]

# ================================================================
# GRADE 2 ENGLISH  g2e0041+
# ================================================================
grade2_english = [
    mcq('g2e0041','Which sentence is correct?',['I am happy.','I is happy.','I are happy.','I be happy.'],0,['grammar','be-verb']),
    mcq('g2e0042','What day is after Wednesday?',['Monday','Tuesday','Thursday','Friday'],2,['days']),
    mcq('g2e0043','I ___ a student.',['am','is','are','be'],0,['be-verb','fill-blank']),
    tf('g2e0044','There are 12 months in a year.',0,['months','tf']),
    mcq('g2e0045','Which word means 教室?',['Library','Kitchen','Classroom','Bedroom'],2,['school','noun']),
    mcq('g2e0046','She ___ a teacher.',['am','is','are','be'],1,['be-verb','fill-blank']),
    mcq('g2e0047','What is the opposite of "old"?',['Big','New','Small','Long'],1,['antonym']),
    tf('g2e0048','Sunday is the first day of the week.',0,['days','tf']),
    mcq('g2e0049','Which word is an animal?',['Book','Pencil','Tiger','Table'],2,['animal','noun']),
    mcq('g2e0050','I like ___ apples. (我喜歡吃蘋果)',['eat','eating','ate','eats'],1,['verb','grammar']),
    tf('g2e0051','"They are" is correct grammar.',0,['be-verb','tf']),
    mcq('g2e0052','Which sentence asks a question?',['I am happy.','She likes cats.','Are you okay?','He runs fast.'],2,['question','grammar']),
    mcq('g2e0053','What month comes after June?',['May','August','July','September'],2,['months']),
    mcq('g2e0054','We ___ students.',['am','is','are','be'],2,['be-verb','fill-blank']),
    mcq('g2e0055','Which word means 圖書館?',['Hospital','Library','School','Park'],1,['place','noun']),
]

# ================================================================
# GRADE 3 MATH  g3m0123+
# ================================================================
grade3_math = [
    mcq('g3m0123','一個長方形長 12 公分、寬 8 公分，面積是幾平方公分？',['80','88','96','104'],2,['geometry','area']),
    mcq('g3m0124','一個正方形邊長 9 公分，面積是幾平方公分？',['72','81','90','99'],1,['geometry','area']),
    mcq('g3m0125','56 ÷ 8 = ?',['6','7','8','9'],1,['division']),
    mcq('g3m0126','72 ÷ 9 = ?',['7','8','9','10'],1,['division']),
    mcq('g3m0127','一班有 35 個學生，分成 5 組，每組幾人？',['5','6','7','8'],2,['division','word-problem']),
    mcq('g3m0128','48 個橘子平分給 6 個小朋友，每人幾個？',['6','7','8','9'],2,['division','word-problem']),
    mcq('g3m0129','1234 + 567 = ?',['1791','1801','1811','1821'],1,['addition','4-digit']),
    mcq('g3m0130','2000 - 875 = ?',['1025','1125','1225','1325'],1,['subtraction','4-digit']),
    tf('g3m0131','63 ÷ 7 = 9。',0,['division','tf']),
    mcq('g3m0132','一本書有 248 頁，小明每天讀 8 頁，幾天可以讀完？',['29','31','33','35'],1,['division','word-problem']),
    mcq('g3m0133','三角形三個角加起來共幾度？',['90°','180°','270°','360°'],1,['geometry','angle']),
    tf('g3m0134','正方形的四個邊一樣長。',0,['geometry','tf']),
    mcq('g3m0135','4567 + 2345 = ?',['6802','6902','6912','7012'],2,['addition','4-digit']),
    mcq('g3m0136','一個長方形周長 28 公分，長是 8 公分，寬是幾公分？',['4','5','6','7'],2,['geometry','perimeter']),
    mcq('g3m0137','25 × 4 = ?',['80','90','100','110'],2,['multiplication','2-digit']),
    mcq('g3m0138','36 × 3 = ?',['96','100','108','116'],2,['multiplication','2-digit']),
    tf('g3m0139','100 ÷ 5 = 20。',0,['division','tf']),
    mcq('g3m0140','一公里等於幾公尺？',['10','100','1000','10000'],2,['measurement','unit']),
    mcq('g3m0141','圖書館有 1500 本書，借出 378 本，還剩幾本？',['1112','1122','1132','1142'],1,['subtraction','word-problem','4-digit']),
    mcq('g3m0142','一個長方形面積 60 平方公分，長 10 公分，寬是幾公分？',['4','5','6','7'],2,['geometry','area']),
]

# ================================================================
# GRADE 3 CHINESE  g3c0046+
# ================================================================
grade3_chinese = [
    mcq('g3c0046','「勤儉節約」這個成語的意思是？',['努力讀書','節省不浪費','助人為樂','待人和善'],1,['idiom','vocabulary']),
    mcq('g3c0047','「木」字旁的字通常與什麼有關？',['水','火','樹木','金屬'],2,['radical']),
    mcq('g3c0048','「蟬噪林逾靜，鳥鳴山更幽。」這句話描述的是什麼場景？',['熱鬧的市集','安靜的山林','忙碌的農場','美麗的海邊'],1,['poem','comprehension']),
    mcq('g3c0049','下面哪個詞語是反義詞對？',['高興—快樂','寒冷—炎熱','美麗—漂亮','聰明—智慧'],1,['antonym']),
    tf('g3c0050','「氵」（三點水）通常與水有關。',0,['radical','tf']),
    mcq('g3c0051','「水到渠成」這個成語的意思最接近？',['努力必有成果','隨波逐流','水往低處流','灌溉農田'],0,['idiom']),
    mcq('g3c0052','「他跑得比我___。」空格最適合填入什麼？',['很快','非常','更快','快樂'],2,['comparison','adjective']),
    mcq('g3c0053','下面哪個字的部首是「心」？',['海','想','樹','跑'],1,['radical']),
    tf('g3c0054','「因為…所以…」是表示因果關係的句型。',0,['conjunction','tf']),
    mcq('g3c0055','「交通工具」包含以下哪個選項？',['蘋果','汽車','課本','鉛筆'],1,['category','transportation']),
    mcq('g3c0056','「雨過天晴」最適合比喻什麼？',['下雨之後天氣變好','努力後得到好結果','困難過後迎來希望','學習之後變聰明'],2,['idiom','metaphor']),
    mcq('g3c0057','「足」字旁的字通常與什麼有關？',['手','腳或走路','眼睛','嘴巴'],1,['radical']),
    mcq('g3c0058','以下哪個句子使用了比喻？',['他很高。','她唱歌唱得好。','他的聲音像雷聲一樣響亮。','今天天氣很好。'],2,['figure-of-speech','metaphor']),
    tf('g3c0059','「口」字旁的字大多與嘴巴或說話有關。',0,['radical','tf']),
    mcq('g3c0060','「___而不捨」這個成語空格應填什麼？',['堅','繼','持','學'],0,['idiom','fill-blank']),
]

# ================================================================
# GRADE 3 ENGLISH  g3e0017+  (boost from 16 to ~46)
# ================================================================
grade3_english = [
    mcq('g3e0017','She ___ to school every day.',['go','goes','going','went'],1,['present-tense','verb']),
    mcq('g3e0018','They ___ playing basketball now.',['is','am','are','be'],2,['present-continuous','be-verb']),
    mcq('g3e0019','What does "beautiful" mean?',['Ugly','Pretty','Small','Fast'],1,['vocabulary']),
    mcq('g3e0020','___ is your favorite color?',['Who','What','Where','When'],1,['question-word']),
    tf('g3e0021','"He don\'t like cats" is correct.',1,['grammar','tf']),
    mcq('g3e0022','___ does he live?',['What','Who','Where','When'],2,['question-word']),
    mcq('g3e0023','I ___ my homework yesterday.',['do','does','did','done'],2,['past-tense','verb']),
    mcq('g3e0024','Which word means 圖書館?',['Hospital','Library','Post office','Police station'],1,['noun','place']),
    tf('g3e0025','"She goes" is correct present tense.',0,['present-tense','tf']),
    mcq('g3e0026','___ many students are in your class?',['What','Who','How','Where'],2,['question-word']),
    mcq('g3e0027','The opposite of "happy" is ___.',['Sad','Angry','Tired','Hungry'],0,['antonym']),
    mcq('g3e0028','We ___ eat lunch at noon.',['usually','is','am','were'],0,['adverb','grammar']),
    tf('g3e0029','"They was happy" is correct.',1,['grammar','tf']),
    mcq('g3e0030','___ do you go to school?',['What','Who','How','Which'],2,['question-word']),
    mcq('g3e0031','She has ___ apple and ___ orange.',['a / a','an / an','an / a','a / an'],2,['article','grammar']),
    mcq('g3e0032','Which word is an adjective?',['Run','Beautiful','Book','Quickly'],1,['adjective','grammar']),
    tf('g3e0033','"I am going to the park" means 我要去公園。',0,['translation','tf']),
    mcq('g3e0034','He ___ play soccer on Sundays.',['do','does','is','are'],1,['present-tense','verb']),
    mcq('g3e0035','What is the plural of "child"?',['Childs','Children','Childrens','Child'],1,['plural','grammar']),
    mcq('g3e0036','___ old are you?',['What','Who','How','Where'],2,['question-word']),
    tf('g3e0037','"We are friends" is correct.',0,['grammar','tf']),
    mcq('g3e0038','I drink water ___ I am thirsty.',['so','but','because','and'],2,['conjunction']),
    mcq('g3e0039','Which sentence is in the past tense?',['She eats rice.','She ate rice.','She is eating rice.','She will eat rice.'],1,['past-tense','grammar']),
    mcq('g3e0040','The book is ___ the desk. (書在桌子上)',['in','on','under','beside'],1,['preposition']),
    tf('g3e0041','"Does she like cats?" is a correct question.',0,['question','tf']),
    mcq('g3e0042','Which word means 安靜?',['Noisy','Loud','Quiet','Happy'],2,['vocabulary']),
    mcq('g3e0043','I have ___ umbrella.',['a','an','the','some'],1,['article','grammar']),
    tf('g3e0044','"I goes to school" is correct.',1,['grammar','tf']),
    mcq('g3e0045','What is 7 × 6?',['36','40','42','48'],2,['math','number']),
    mcq('g3e0046','___ season comes after winter?',['Which','What','Where','Who'],0,['question-word','season']),
]

# ================================================================
# MAIN
# ================================================================
batches = [
    ('kinder', 'math',    kinder_math),
    ('kinder', 'chinese', kinder_chinese),
    ('kinder', 'english', kinder_english),
    ('grade1', 'math',    grade1_math),
    ('grade1', 'chinese', grade1_chinese),
    ('grade1', 'english', grade1_english),
    ('grade2', 'math',    grade2_math),
    ('grade2', 'chinese', grade2_chinese),
    ('grade2', 'english', grade2_english),
    ('grade3', 'math',    grade3_math),
    ('grade3', 'chinese', grade3_chinese),
    ('grade3', 'english', grade3_english),
]

total_added = 0
for grade, sub, new_qs in batches:
    data, path = load(grade, sub)
    n = add(data, new_qs)
    save(data, path)
    total_added += n
    print(f'  +{n} 題')

print(f'\n總計新增 {total_added} 題')
