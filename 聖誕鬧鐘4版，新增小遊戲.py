import streamlit as st
import random
import datetime
import base64

# 頁面基本設定
st.set_page_config(
    page_title="🌿 綠意天地・聖誕鬧鐘 🎄",
    page_icon="🌲",
    layout="centered"
)

# 輔助函數：將本地檔案（圖片/音樂）轉為 Base64 格式
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# 讀取本地圖片與音樂
green_bg_base64 = get_base64_of_bin_file("bg_green.jpg")
xmas_bg_base64 = get_base64_of_bin_file("bg_xmas.png")
xmas_tree_bg_base64 = get_base64_of_bin_file("bg_xmas_tree.jpg")

happy_audio_base64 = get_base64_of_bin_file("bgm_happy.mp3")
xmas_audio_base64 = get_base64_of_bin_file("bgm_xmas.mp3")

# 初始化 session_state
if "show_tree_bg" not in st.session_state:
    st.session_state.show_tree_bg = False
if "auto_xmas_bgm" not in st.session_state:
    st.session_state.auto_xmas_bgm = False
if "night_mode" not in st.session_state:
    st.session_state.night_mode = False
if "plant_growth" not in st.session_state:
    st.session_state.plant_growth = 0
if "plant_action_note" not in st.session_state:
    st.session_state.plant_action_note = ""
if "quest_idx" not in st.session_state:
    st.session_state.quest_idx = 0
if "quest_done" not in st.session_state:
    st.session_state.quest_done = False
if "picked_food" not in st.session_state:
    st.session_state.picked_food = None
if "picked_drink" not in st.session_state:
    st.session_state.picked_drink = None
if "xmas_voucher" not in st.session_state:
    st.session_state.xmas_voucher = None
if "xmas_picked_box" not in st.session_state:
    st.session_state.xmas_picked_box = None
if "xmas_wish_card" not in st.session_state:
    st.session_state.xmas_wish_card = ""

# ==================== 多國語言資料字典 ====================
translations = {
    "繁體中文": {
        "nav_title": "🌿 導覽選單",
        "nav_select": "選擇一個溫馨小天地：",
        "menu_1": "🏠 綠意森林與倒數",
        "menu_2": "🌸 吉祥花語與解憂籤詩",
        "menu_3": "🎄 聖誕限定彩蛋專區",
        "music_title": "🎵 療癒音樂播放器",
        "music_toggle": "開啟背景音樂",
        "night_toggle": "🌙 夜間星光模式",
        "sidebar_info": "💡 專屬於你的無壓力療癒空間，隨時為你加油打氣！",
        "home_title": "🌿 歡迎來到你的專屬綠意小天地",
        "home_desc": "這裡是那位大人送給你的領地，此處沒有惱人的壓力，也沒有煩人的雜音，只有屬於你的空間、好心情與溫暖陪伴，靜靜等待那位大人的出現吧！",
        "quote_title": "✨ 那位大人對你說",
        "quote_text": "「不管是面對此時的困境，亦是未來的星辰大海，慢慢來、照著自己的節奏，你一直都很棒，也很有才華。」",
        "timer_title": "⏳ 距離那位沉睡的大人甦醒還有...",
        "timer_unit_d": "天", "timer_unit_h": "小時", "timer_unit_m": "分",
        "timer_footer": "讓我們一起期待接下來溫馨的冬日時光吧！",
        "advent_title": "📅 十二月聖誕倒數日曆",
        "advent_desc": "每天一格小驚喜（依台北時間解鎖），點開已經解鎖的日子看看今天藏了什麼吧！",
        "quest_title": "🎯 今日小任務 / 療癒挑戰",
        "quest_change": "🔄 換一個小任務",
        "quest_done_btn": "✅ 今天做到了！",
        "food_title": "🍽️ 不知道該吃什麼時",
        "food_style_label": "選擇料理風格：",
        "food_any_style": "不限風格",
        "food_btn": "🎲 幫我挑一道料理",
        "drink_title": "🥤 不知道該喝什麼時",
        "drink_btn": "💧 幫我挑一杯飲品",
        "flower_title": "🌸 吉祥花語與解憂籤詩",
        "flower_desc": "此地種滿各種具有深刻意義的花朵，請挑選一株帶著美好寓意與吉祥花語的植物，為你今天的生活帶來滿滿的好運！",
        "flower_btn": "🎲 抽取今日的花朵",
        "flower_result": "抽到的是：",
        "flower_lang": "✨ 吉祥花語",
        "flower_fortune": "運勢",
        "flower_msg": "專屬祝福小語",
        "plant_title": "🌱 每日專屬小植栽養成",
        "plant_desc": "給小植栽一點水、陽光或鼓勵，陪它一步步長大開花吧！",
        "plant_water": "💧 澆水",
        "plant_sun": "☀️ 曬太陽",
        "plant_cheer": "✨ 輕輕鼓勵",
        "plant_reset": "🔁 重新種下一盆",
        "xmas_lock_title": "🔒 聖誕限定彩蛋尚在冬眠封印中",
        "xmas_lock_desc": "這份專屬聖誕驚喜預計在 **12 月 25 日** 準時解鎖（依台北時間）。在那之前，先在綠意森林與花語小天地裡好好放鬆吧！",
        "xmas_title": "🎄 聖誕節限定 BONUS",
        "xmas_desc": "歡迎來到冬日限定的雪景森林！點擊下方按鈕，點亮屬於妳的聖誕節與聖誕佬的祝福。",
        "xmas_btn": "🌟 點亮聖誕節的祝願",
        "xmas_snow_btn": "❄️ 再下一次雪",
        "xmas_reset_btn": "🌙 回到靜謐夜空",
        "xmas_box_title": "🎁 來自 聖誕佬 的通知",
        "xmas_box_text": "「喔吼吼吼吼！是你把我喚醒的吧！希望這座專屬於你的綠意森林與這些玩意，能在這個冬日為你帶來暖洋洋的陪伴。喔吼吼吼吼！不管是想安穩度日，亦或是未來的任何旅途，聖誕佬一定會大力支持你噠！Merry Christmas & Happy Every Day My child！ 🌲❄️✨」",
        "xmas_placeholder": "👆 點擊上方按鈕，喚醒雪花、聖誕鈴聲與那位沉睡中的大人吧！",
        "gift_title": "🧦 拆開你的聖誕禮物盒（每人限挑一份）",
        "gift_desc": "聖誕老公公的禮物每個孩子都只有一份，挑一個最有緣分的禮物盒拆開吧（記得截圖保存喔）：",
        "gift_red": "🎁 紅色禮物盒",
        "gift_gold": "🎁 金色禮物盒",
        "gift_green": "🎁 綠色禮物盒",
        "wish_title": "💌 許下今年的聖誕心願",
        "wish_placeholder": "在這裡寫下一個小願望，或給聖誕節的自己一句話...",
        "wish_btn": "✨ 生成專屬聖誕紀念卡"
    },
    "简体中文": {
        "nav_title": "🌿 导航菜单",
        "nav_select": "选择一个温馨小天地：",
        "menu_1": "🏠 绿意森林与倒数",
        "menu_2": "🌸 吉祥花语与解忧签诗",
        "menu_3": "🎄 圣诞限定彩蛋专区",
        "music_title": "🎵 疗愈音乐播放器",
        "music_toggle": "开启背景音乐",
        "night_toggle": "🌙 夜间星光模式",
        "sidebar_info": "💡 专属于你的无压力疗愈空间，随时为你加油打气！",
        "home_title": "🌿 欢迎来到你的专属绿意小天地",
        "home_desc": "这里是那位大人送给你的领地，此处没有恼人的压力，也没有烦人的杂音，只有属于你的空间、好心情与温暖陪伴，静静等待那位大人的出现吧！",
        "quote_title": "✨ 那位大人对你说",
        "quote_text": "「不管是面对此时的困境，亦是未来的星辰大海，慢慢来、照着自己的节奏，你一直都很棒，也很有才华。」",
        "timer_title": "⏳ 距离那位沉睡的大人苏醒还有...",
        "timer_unit_d": "天", "timer_unit_h": "小时", "timer_unit_m": "分",
        "timer_footer": "让我们一起期待接下来温馨的冬日时光吧！",
        "advent_title": "📅 十二月圣诞倒数日历",
        "advent_desc": "每天一格小惊喜（依台北时间解锁），点开已经解锁的日子看看今天藏了什么吧！",
        "quest_title": "🎯 今日小任务 / 疗愈挑战",
        "quest_change": "🔄 换一个小任务",
        "quest_done_btn": "✅ 今天做到了！",
        "food_title": "🍽️ 不知道该吃什么时",
        "food_style_label": "选择料理风格：",
        "food_any_style": "不限风格",
        "food_btn": "🎲 帮我挑一道料理",
        "drink_title": "🥤 不知道该喝什么时",
        "drink_btn": "💧 帮我挑一杯饮品",
        "flower_title": "🌸 吉祥花语与解忧签诗",
        "flower_desc": "此地种满各种具有深刻意义的花朵，请挑选一株带着美好寓意与吉祥花语的植物，为你今天的生活带来满满的好运！",
        "flower_btn": "🎲 抽取今日的花朵",
        "flower_result": "抽到的是：",
        "flower_lang": "✨ 吉祥花语",
        "flower_fortune": "运势",
        "flower_msg": "专属祝福小语",
        "plant_title": "🌱 每日专属小植栽养成",
        "plant_desc": "给小植栽一点水、阳光或鼓励，陪它一步步长大开花吧！",
        "plant_water": "💧 浇水",
        "plant_sun": "☀️ 晒太阳",
        "plant_cheer": "✨ 轻轻鼓励",
        "plant_reset": "🔁 重新种下一盆",
        "xmas_lock_title": "🔒 圣诞限定彩蛋尚在冬眠封印中",
        "xmas_lock_desc": "这份专属圣诞惊喜预计在 **12 月 25 日** 准时解锁（依台北时间）。在那之前，先在绿意森林与花语小天地里好好放松吧！",
        "xmas_title": "🎄 圣诞节限定 BONUS",
        "xmas_desc": "欢迎来到冬日限定的雪景森林！点击下方按钮，点亮属于妳的圣诞节与圣诞佬的祝福。",
        "xmas_btn": "🌟 点亮圣诞节的祝愿",
        "xmas_snow_btn": "❄️ 再下一次雪",
        "xmas_reset_btn": "🌙 回到静谧夜空",
        "xmas_box_title": "🎁 来自 圣诞佬 的通知",
        "xmas_box_text": "「哦吼吼吼吼！是你把我唤醒的吧！希望这座专属于你的绿意森林与这些玩意，能在这个冬日为你带来暖洋洋的陪伴。哦吼吼吼吼！不管是想安稳度日，亦或是未来的任何旅途，圣诞佬一定会大力支持你哒！Merry Christmas & Happy Every Day My child！ 🌲❄️✨」",
        "xmas_placeholder": "👆 点击上方按钮，唤醒雪花、圣诞铃声与那位沉睡中的大人吧！",
        "gift_title": "🧦 拆开你的圣诞礼物盒（每人限挑一份）",
        "gift_desc": "圣诞老公公的礼物每个孩子都只有一份，挑一个最有缘分的礼物盒拆开吧（记得截图保存哦）：",
        "gift_red": "🎁 红色礼物盒",
        "gift_gold": "🎁 金色礼物盒",
        "gift_green": "🎁 绿色礼物盒",
        "wish_title": "💌 许下今年的圣诞心愿",
        "wish_placeholder": "在这里写下一个小愿望，或给圣诞节的自己一句话...",
        "wish_btn": "✨ 生成专属圣诞纪念卡"
    },
    "English": {
        "nav_title": "🌿 Navigation",
        "nav_select": "Select a cozy space:",
        "menu_1": "🏠 Green Forest & Countdown",
        "menu_2": "🌸 Floral Language & Fortune",
        "menu_3": "🎄 Christmas Special Easter Egg",
        "music_title": "🎵 Healing Music Player",
        "music_toggle": "Enable Background Music",
        "night_toggle": "🌙 Night Starlight Mode",
        "sidebar_info": "💡 Your stress-free healing space, cheering you on anytime!",
        "home_title": "🌿 Welcome to Your Exclusive Green Haven",
        "home_desc": "This is the territory given to you by that person. Here, there is no annoying pressure or noise—only your own space, good vibes, and warm companionship. Quietly wait for their arrival!",
        "quote_title": "✨ Words from That Person",
        "quote_text": "\"Whether facing current hardships or the sea of stars in the future, take your time and follow your own rhythm. You've always been amazing and incredibly talented.\"",
        "timer_title": "⏳ Time until the sleeping VIP awakens...",
        "timer_unit_d": "days", "timer_unit_h": "hrs", "timer_unit_m": "mins",
        "timer_footer": "Let's look forward to the cozy winter time ahead together!",
        "advent_title": "📅 December Advent Calendar",
        "advent_desc": "A little surprise every day (Taipei time). Open unlocked days to see what's inside!",
        "quest_title": "🎯 Daily Cozy Quest",
        "quest_change": "🔄 New Quest",
        "quest_done_btn": "✅ Done Today!",
        "food_title": "🍽️ When You Don't Know What to Eat",
        "food_style_label": "Choose cuisine style:",
        "food_any_style": "Any Style",
        "food_btn": "🎲 Pick a Meal",
        "drink_title": "🥤 When You Don't Know What to Drink",
        "drink_btn": "💧 Pick a Drink",
        "flower_title": "🌸 Floral Language & Fortune",
        "flower_desc": "Filled with deeply meaningful blooms, pick a plant with a wonderful blessing and floral language to bring you great luck today!",
        "flower_btn": "🎲 Draw Today's Flower",
        "flower_result": "You drew: ",
        "flower_lang": "✨ Floral Meaning",
        "flower_fortune": "Fortune",
        "flower_msg": "Exclusive Blessing",
        "plant_title": "🌱 Daily Little Plant Care",
        "plant_desc": "Give your little plant water, sunlight, or encouragement and watch it bloom!",
        "plant_water": "💧 Water",
        "plant_sun": "☀️ Sunlight",
        "plant_cheer": "✨ Cheer Up",
        "plant_reset": "🔁 Plant a New One",
        "xmas_lock_title": "🔒 Christmas Easter Egg Still Hibernating",
        "xmas_lock_desc": "This special Christmas surprise unlocks on **December 25** (Taipei time). Until then, relax in the green forest and floral haven!",
        "xmas_title": "🎄 Christmas Limited BONUS",
        "xmas_desc": "Welcome to the winter snow-covered forest! Click the button below to light up your Christmas tree and Santa's blessings.",
        "xmas_btn": "🌟 Light Up Christmas Wishes",
        "xmas_snow_btn": "❄️ Let It Snow Again",
        "xmas_reset_btn": "🌙 Back to Starry Night",
        "xmas_box_title": "🎁 Notice from Santa",
        "xmas_box_text": "\"Ho ho ho ho! You woke me up, didn't you! May this exclusive green forest and these little wonders bring you cozy warmth this winter. Ho ho ho ho! Whether you want a peaceful life or adventures on any future journey, Santa will always strongly support you! Merry Christmas & Happy Every Day My child! 🌲❄️✨\"",
        "xmas_placeholder": "👆 Click the button above to awaken the snowflakes, Christmas bells, and the sleeping VIP!",
        "gift_title": "🧦 Unbox Your Christmas Gift (One per child)",
        "gift_desc": "Santa gives one gift per child—pick the gift box meant for you (take a screenshot to redeem!):",
        "gift_red": "🎁 Red Gift Box",
        "gift_gold": "🎁 Gold Gift Box",
        "gift_green": "🎁 Green Gift Box",
        "wish_title": "💌 Make a Christmas Wish",
        "wish_placeholder": "Write down a wish or a note to yourself for Christmas...",
        "wish_btn": "✨ Create Christmas Keepsake Card"
    },
    "日本語": {
        "nav_title": "🌿 メニュー",
        "nav_select": "癒しの空間を選択：",
        "menu_1": "🏠 緑の森とカウントダウン",
        "menu_2": "🌸 花言葉とおみくじ",
        "menu_3": "🎄 クリスマス限定イースターエッグ",
        "music_title": "🎵 ヒーリング音楽プレーヤー",
        "music_toggle": "BGMを再生する",
        "night_toggle": "🌙 ナイトモード",
        "sidebar_info": "💡 あなただけのストレスフリーな癒しの空間。いつでも応援しています！",
        "home_title": "🌿 あなた専用の緑の楽園へようこそ",
        "home_desc": "ここは「あの人」から贈られた領地。嫌なプレッシャーも雑音もなく、あなただけの空間、良い気分、そして温かな陪伴だけがあります。あの人の登場を静かに待ちましょう！",
        "quote_title": "✨ あの人からのメッセージ",
        "quote_text": "「今の困難に直面するときも、未来の星の海に向かうときも、ゆっくり自分のペースで進んで。あなたはいつだって素晴らしく、才能に溢れています。」",
        "timer_title": "⏳ 眠っているあの人が目覚めるまで...",
        "timer_unit_d": "日", "timer_unit_h": "時間", "timer_unit_m": "分",
        "timer_footer": "温かな冬の時間を一緒に楽しみにしましょう！",
        "advent_title": "📅 12月アドベントカレンダー",
        "advent_desc": "毎日ひとつ小さなサプライズ（台湾時間基準）。解禁された日を開いてみましょう！",
        "quest_title": "🎯 今日の癒やしクエスト",
        "quest_change": "🔄 別のクエストにする",
        "quest_done_btn": "✅ できたよ！",
        "food_title": "🍽️ 何を食べるか迷ったとき",
        "food_style_label": "料理のジャンルを選ぶ：",
        "food_any_style": "おまかせ",
        "food_btn": "🎲 料理を選ぶ",
        "drink_title": "🥤 何を飲むか迷ったとき",
        "drink_btn": "💧 ドリンクを選ぶ",
        "flower_title": "🌸 花言葉とおみくじ",
        "flower_desc": "深い意味を持つ花々が咲き誇る場所。素敵な意味を持つ植物を選んで、今日の幸運を引き寄せましょう！",
        "flower_btn": "🎲 本日の花を引く",
        "flower_result": "引いた花：",
        "flower_lang": "✨ 花言葉",
        "flower_fortune": "運勢",
        "flower_msg": "専用の祝福メッセージ",
        "plant_title": "🌱 毎日のミニ植物そだて",
        "plant_desc": "お水や日差しや応援をあげて、お花を咲かせてみましょう！",
        "plant_water": "💧 お水",
        "plant_sun": "☀️ 日差し",
        "plant_cheer": "✨ 応援",
        "plant_reset": "🔁 もう一度植える",
        "xmas_lock_title": "🔒 クリスマス限定シークレットは冬眠中",
        "xmas_lock_desc": "このクリスマスサプライズは **12月25日** に解禁されます（台湾時間）。それまでは緑の森とおみくじでゆっくり過ごしてね！",
        "xmas_title": "🎄 クリスマス限定 BONUS",
        "xmas_desc": "冬限定の雪景色へようこそ！下のボタンをクリックして、あなただけのクリスマスとサンタからの祝福を灯しましょう。",
        "xmas_btn": "🌟 クリスマスの願いを灯す",
        "xmas_snow_btn": "❄️ もう一度雪を降らす",
        "xmas_reset_btn": "🌙 静かな夜空に戻る",
        "xmas_box_title": "🎁 サンタクロースからの通知",
        "xmas_box_text": "「ホっホっホっ！私を目覚めさせたのは君だな！この緑の森とサプライズが、この冬君に温かい癒やしをもたらしますように。ホっホっホっ！平穏な日々を望むも、未来のどんな旅路も、サンタは全力で君を応援するぞ！Merry Christmas & Happy Every Day My child！ 🌲❄️✨」",
        "xmas_placeholder": "👆 上のボタンをクリックして、雪とクリスマスの鈴と眠るあの人を起こしましょう！",
        "gift_title": "🧦 クリスマスギフトを開けよう（お一人様1つまで）",
        "gift_desc": "サンタからのプレゼントは一人ひとつ。ご縁のあるギフトボックスをひとつ選んでね（スクショで保存！）：",
        "gift_red": "🎁 赤いギフト",
        "gift_gold": "🎁 金のギフト",
        "gift_green": "🎁 緑のギフト",
        "wish_title": "💌 今年のクリスマスウィッシュ",
        "wish_placeholder": "お願いごとや、自分へのメッセージを書いてね...",
        "wish_btn": "✨ クリスマス記念カードを作る"
    },
    "한국어": {
        "nav_title": "🌿 네비게이션",
        "nav_select": "아늑한 공간 선택:",
        "menu_1": "🏠 초록 숲과 카운트다운",
        "menu_2": "🌸 꽃말과 위로의 운세",
        "menu_3": "🎄 크리스마스 한정 이스터에그",
        "music_title": "🎵 힐링 음악 플레이어",
        "music_toggle": "배경음악 켜기",
        "night_toggle": "🌙 야간 모드",
        "sidebar_info": "💡 당신만을 위한 스트레스 없는 힐링 공간, 언제나 응원합니다!",
        "home_title": "🌿 전용 초록 쉼터에 오신 것을 환영합니다",
        "home_desc": "여기는 그분이 당신에게 준 영지입니다. 번거로운 압박이나 소음 없이 오직 당신만의 공간, 좋은 기분, 따뜻한 동행만 있으니 그분이 나타나기를 조용히 기다려보세요!",
        "quote_title": "✨ 그분이 당신에게 건네는 말",
        "quote_text": "\"지금의 시련이든 미래의 별바다이든 천천히 자신의 페이스대로 가세요. 당신은 언제나 멋지고 재능이 넘쳐요.\"",
        "timer_title": "⏳ 잠들어 있는 그분이 깨어날 때까지...",
        "timer_unit_d": "일", "timer_unit_h": "시간", "timer_unit_m": "분",
        "timer_footer": "다가올 따뜻한 겨울을 함께 기대해 봐요!",
        "advent_title": "📅 12월 크리스마스 달력",
        "advent_desc": "매일 하나씩 열리는 작은 선물 (대만 시간 기준).",
        "quest_title": "🎯 오늘의 힐링 퀘스트",
        "quest_change": "🔄 다른 퀘스트 뽑기",
        "quest_done_btn": "✅ 오늘 완료!",
        "food_title": "🍽️ 뭘 먹을지 모를 때",
        "food_style_label": "요리 스타일 선택:",
        "food_any_style": "상관없음",
        "food_btn": "🎲 메뉴 추천",
        "drink_title": "🥤 뭘 마실지 모를 때",
        "drink_btn": "💧 음료 추천",
        "flower_title": "🌸 꽃말과 위로의 운세",
        "flower_desc": "깊은 뜻을 가진 꽃들로 가득한 곳. 아름다운 의미가 담긴 식물을 골라 오늘 하루 행운을 더해보세요!",
        "flower_btn": "🎲 오늘의 꽃 뽑기",
        "flower_result": "뽑은 꽃: ",
        "flower_lang": "✨ 꽃말",
        "flower_fortune": "운세",
        "flower_msg": "전용 축복 메시지",
        "plant_title": "🌱 나만의 작은 식물 키우기",
        "plant_desc": "물과 햇빛, 응원을 주며 예쁜 꽃을 피워보세요!",
        "plant_water": "💧 물 주기",
        "plant_sun": "☀️ 햇빛 쬐기",
        "plant_cheer": "✨ 응원하기",
        "plant_reset": "🔁 새로 심기",
        "xmas_lock_title": "🔒 크리스마스 이스터에그 잠금 중",
        "xmas_lock_desc": "이 특별한 크리스마스 서프라이즈는 **12월 25일** 에 열립니다(대만 시간). 그때까지 초록 숲과 꽃말 공간에서 편히 쉬어요!",
        "xmas_title": "🎄 크리스마스 한정 BONUS",
        "xmas_desc": "겨울 한정 눈 덮인 숲에 오신 것을 환영합니다! 아래 버튼을 눌러 당신만의 크리스마스와 산타의 축복을 밝혀보세요.",
        "xmas_btn": "🌟 크리스마스 소원 밝히기",
        "xmas_snow_btn": "❄️ 눈 다시 내리기",
        "xmas_reset_btn": "🌙 밤하늘로 돌아가기",
        "xmas_box_title": "🎁 산타클로스의 알림",
        "xmas_box_text": "\"오호호호! 나를 깨운 건 너구나! 이 초록 숲과 작은 선물들이 이번 겨울 너에게 따뜻한 위로가 되길 바란다. 오호호호! 평온한 삶을 원하든 미래의 어떤 여정이든 산타가 든든하게 응원할게! Merry Christmas & Happy Every Day My child! 🌲❄️✨\"",
        "xmas_placeholder": "👆 위 버튼을 눌러 눈꽃, 크리스마스 종소리, 잠든 그분을 깨워주세요!",
        "gift_title": "🧦 크리스마스 선물 상자 열기（1인 1개 선택）",
        "gift_desc": "산타 선물은 한 사람당 하나씩만! 가장 끌리는 선물 상자 하나를 열어보세요（스크린샷으로 저장!）：",
        "gift_red": "🎁 빨간 선물 상자",
        "gift_gold": "🎁 황금 선물 상자",
        "gift_green": "🎁 초록 선물 상자",
        "wish_title": "💌 올해의 크리스마스 소원 빌기",
        "wish_placeholder": "작은 소원이나 나에게 해주고 싶은 말을 적어보세요...",
        "wish_btn": "✨ 크리스마스 기념 카드 만들기"
    },
    "Tiếng Việt": {
        "nav_title": "🌿 Menu điều hướng",
        "nav_select": "Chọn một không gian ấm áp:",
        "menu_1": "🏠 Rừng xanh & Đếm ngược",
        "menu_2": "🌸 Ngôn ngữ hoa & Lời chúc",
        "menu_3": "🎄 Trứng Phục Sinh Giáng Sinh",
        "music_title": "🎵 Trình phát nhạc thư giãn",
        "music_toggle": "Bật nhạc nền",
        "night_toggle": "🌙 Chế độ ban đêm",
        "sidebar_info": "💡 Không gian chữa lành không áp lực dành riêng cho bạn!",
        "home_title": "🌿 Chào mừng đến với không gian xanh của bạn",
        "home_desc": "Đây là vùng đất mà người ấy trao cho bạn. Nơi đây không có áp lực hay tạp âm phiền muộn, chỉ có không gian, tâm trạng vui vẻ và sự đồng hành ấm áp của riêng bạn!",
        "quote_title": "✨ Người ấy nói với bạn",
        "quote_text": "“Dù đối mặt với khó khăn hiện tại hay biển sao trong tương lai, hãy cứ từ từ, theo nhịp điệu của riêng bạn. Bạn luôn rất tuyệt vời và tài năng.”",
        "timer_title": "⏳ Thời gian người ấy thức dậy còn...",
        "timer_unit_d": "ngày", "timer_unit_h": "giờ", "timer_unit_m": "phút",
        "timer_footer": "Hãy cùng mong chờ khoảng thời gian mùa đông ấm áp sắp tới nhé!",
        "advent_title": "📅 Lịch đếm ngược Giáng Sinh tháng 12",
        "advent_desc": "Mỗi ngày một bất ngờ nhỏ (theo giờ Đài Loan).",
        "quest_title": "🎯 Thử thách chữa lành hôm nay",
        "quest_change": "🔄 Đổi thử thách",
        "quest_done_btn": "✅ Đã hoàn thành!",
        "food_title": "🍽️ Khi không biết ăn gì",
        "food_style_label": "Chọn phong cách ẩm thực:",
        "food_any_style": "Bất kỳ",
        "food_btn": "🎲 Chọn món ăn",
        "drink_title": "🥤 Khi không biết uống gì",
        "drink_btn": "💧 Chọn đồ uống",
        "flower_title": "🌸 Ngôn ngữ hoa & Lời chúc",
        "flower_desc": "Nơi đây tràn ngập những loài hoa ý nghĩa. Hãy chọn một loại cây mang ý nghĩa tốt đẹp để mang lại may mắn cho ngày mới!",
        "flower_btn": "🎲 Rút hoa hôm nay",
        "flower_result": "Bạn đã rút được: ",
        "flower_lang": "✨ Ý nghĩa hoa",
        "flower_fortune": "Vận may",
        "flower_msg": "Lời chúc độc quyền",
        "plant_title": "🌱 Chăm sóc cây xanh mỗi ngày",
        "plant_desc": "Tưới nước, đón nắng và cổ vũ để cây nở hoa nhé!",
        "plant_water": "💧 Tưới nước",
        "plant_sun": "☀️ Đón nắng",
        "plant_cheer": "✨ Cổ vũ",
        "plant_reset": "🔁 Trồng chậu mới",
        "xmas_lock_title": "🔒 Trứng Phục Sinh Giáng Sinh đang khóa",
        "xmas_lock_desc": "Bất ngờ Giáng Sinh này sẽ mở khóa vào **25 tháng 12** (giờ Đài Loan). Trước đó, hãy thư giãn ở rừng xanh và vườn hoa nhé!",
        "xmas_title": "🎄 Giáng Sinh Đặc Biệt BONUS",
        "xmas_desc": "Chào mừng bạn đến với khu rừng tuyết mùa đông! Nhấp vào nút bên dưới để thắp sáng cây thông Noel và nhận lời chúc từ ông già Noel.",
        "xmas_btn": "🌟 Thắp sáng điều ước Giáng Sinh",
        "xmas_snow_btn": "❄️ Tuyết rơi thêm lần nữa",
        "xmas_reset_btn": "🌙 Về lại đêm sao",
        "xmas_box_title": "🎁 Thông báo từ Ông Già Noel",
        "xmas_box_text": "“Ho ho ho ho! Chính cháu đã đánh thức ta phải không! Mong rằng khu rừng xanh và những điều kỳ diệu này sẽ sưởi ấm trái tim cháu trong mùa đông này. Ho ho ho ho! Dù cháu muốn một cuộc sống bình yên hay những chuyến phiêu lưu trong tương lai, ông già Noel sẽ luôn ủng hộ cháu hết mình! Merry Christmas & Happy Every Day My child! 🌲❄️✨”",
        "xmas_placeholder": "👆 Nhấp vào nút phía trên để đánh thức bông tuyết, tiếng chuông Giáng Sinh và người ấy nhé!",
        "gift_title": "🧦 Mở Hộp Quà Giáng Sinh（Chỉ chọn một hộp）",
        "gift_desc": "Ông già Noel chỉ tặng mỗi bé một món quà—hãy chọn hộp quà hợp duyên nhất nhé（nhớ chụp màn hình nhé）：",
        "gift_red": "🎁 Hộp quà Đỏ",
        "gift_gold": "🎁 Hộp quà Vàng",
        "gift_green": "🎁 Hộp quà Xanh",
        "wish_title": "💌 Gửi Điều Ước Giáng Sinh",
        "wish_placeholder": "Viết một điều ước nhỏ hoặc lời nhắn cho bản thân...",
        "wish_btn": "✨ Tạo Thiệp Kỷ Niệm Giáng Sinh"
    },
    "Bahasa Indonesia": {
        "nav_title": "🌿 Menu Navigasi",
        "nav_select": "Pilih ruang nyaman:",
        "menu_1": "🏠 Hutan Hijau & Hitung Mundur",
        "menu_2": "🌸 Makna Bunga & Pesan Harapan",
        "menu_3": "🎄 Spesial Natal",
        "music_title": "🎵 Pemutar Musik Relaksasi",
        "music_toggle": "Nyalakan Musik Latar",
        "night_toggle": "🌙 Mode Malam",
        "sidebar_info": "💡 Ruang pemulihan bebas stres khusus untukmu!",
        "home_title": "🌿 Selamat Datang di Surga Hijau Eksklusifmu",
        "home_desc": "Ini adalah wilayah yang diberikan oleh orang itu untukmu. Di sini tidak ada tekanan atau kebisingan—hanya ruangmu sendiri, suasana hati yang baik, dan kehangatan!",
        "quote_title": "✨ Kata Orang Itu Kepadamu",
        "quote_text": "\"Baik saat menghadapi kesulitan saat ini maupun lautan bintang di masa depan, perlahan saja dan ikuti ritmemu sendiri. Kamu selalu hebat dan sangat berbakat.\"",
        "timer_title": "⏳ Waktu hingga orang spesial itu terbangun...",
        "timer_unit_d": "hari", "timer_unit_h": "jam", "timer_unit_m": "menit",
        "timer_footer": "Mari kita nantikan waktu musim dingin yang hangat bersama!",
        "advent_title": "📅 Kalender Advent Desember",
        "advent_desc": "Kejutan kecil setiap hari (waktu Taipei).",
        "quest_title": "🎯 Tantangan Santai Hari Ini",
        "quest_change": "🔄 Ganti Tantangan",
        "quest_done_btn": "✅ Selesai!",
        "food_title": "🍽️ Saat Bingung Mau Makan Apa",
        "food_style_label": "Pilih gaya kuliner:",
        "food_any_style": "Bebas",
        "food_btn": "🎲 Pilih Makanan",
        "drink_title": "🥤 Saat Bingung Mau Minum Apa",
        "drink_btn": "💧 Pilih Minuman",
        "flower_title": "🌸 Makna Bunga & Pesan Harapan",
        "flower_desc": "Penuh dengan bunga bermakna mendalam. Pilih tanaman dengan berkah indah untuk membawa keberuntungan besar hari ini!",
        "flower_btn": "🎲 Ambil Bunga Hari Ini",
        "flower_result": "Kamu mendapatkan: ",
        "flower_lang": "✨ Arti Bunga",
        "flower_fortune": "Keberuntungan",
        "flower_msg": "Pesan Berkat Eksklusif",
        "plant_title": "🌱 Rawat Tanaman Kecil Harian",
        "plant_desc": "Beri air, sinar matahari, dan semangat hingga berbunga!",
        "plant_water": "💧 Siram",
        "plant_sun": "☀️ Jemur",
        "plant_cheer": "✨ Semangat",
        "plant_reset": "🔁 Tanam Ulang",
        "xmas_lock_title": "🔒 Kejutan Natal Masih Terkunci",
        "xmas_lock_desc": "Kejutan spesial Natal ini terbuka pada **25 Desember** (waktu Taipei). Sambil menunggu, bersantailah di hutan hijau dan ruang bunga!",
        "xmas_title": "🎄 BONUS Spesial Natal",
        "xmas_desc": "Selamat datang di hutan salju musim dingin! Klik tombol di bawah untuk menyalakan pohon Natal dan berkah dari Sinterklas.",
        "xmas_btn": "🌟 Nyalakan Harapan Natal",
        "xmas_snow_btn": "❄️ Turunkan Salju Lagi",
        "xmas_reset_btn": "🌙 Kembali ke Malam Berbintang",
        "xmas_box_title": "🎁 Pesan dari Sinterklas",
        "xmas_box_text": "\"Ho ho ho ho! Kamu yang membangunkanku, ya! Semoga hutan hijau eksklusif ini memberimu kehangatan di musim dingin. Ho ho ho ho! Baik kamu ingin hidup tenang atau berpetualang di masa depan, Sinterklas akan selalu mendukungmu penuh! Merry Christmas & Happy Every Day My child! 🌲❄️✨\"",
        "xmas_placeholder": "👆 Klik tombol di atas untuk membangunkan salju, lonceng Natal, dan orang spesial itu!",
        "gift_title": "🧦 Buka Kotak Hadiah Natalmu（Pilih satu saja）",
        "gift_desc": "Sinterklas hanya memberi satu hadiah untuk setiap anak—pilih satu kotak hadiah yang paling cocok（jangan lupa screenshot!）：",
        "gift_red": "🎁 Kotak Merah",
        "gift_gold": "🎁 Kotak Emas",
        "gift_green": "🎁 Kotak Hijau",
        "wish_title": "💌 Buat Harapan Natal Tahun Ini",
        "wish_placeholder": "Tulis harapan kecil atau pesan untuk dirimu sendiri...",
        "wish_btn": "✨ Buat Kartu Kenangan Natal"
    },
    "ไทย": {
        "nav_title": "🌿 เมนูนำทาง",
        "nav_select": "เลือกพื้นที่อบอุ่นของคุณ:",
        "menu_1": "🏠 ป่าสีเขียวและการนับถอยหลัง",
        "menu_2": "🌸 ความหมายของดอกไม้และคำทำนาย",
        "menu_3": "🎄 โบนัสพิเศษคริสต์มาส",
        "music_title": "🎵 เครื่องเล่นเพลงบำบัด",
        "music_toggle": "เปิดเพลงพื้นหลัง",
        "night_toggle": "🌙 โหมดกลางคืน",
        "sidebar_info": "💡 พื้นที่พักผ่อนไร้ความเครียดสำหรับคุณ คอยให้กำลังใจเสมอ!",
        "home_title": "🌿 ยินดีต้อนรับสู่ดินแดนสีเขียวส่วนตัวของคุณ",
        "home_desc": "นี่คือดินแดนที่คนสำคัญมอบให้คุณ ที่นี่ไม่มีความกดดันหรือเสียงรบกวน มีเพียงพื้นที่ของคุณ อารมณ์ดีๆ และความอบอุ่น รอคอยการปรากฏตัวของเขาคนนั้น!",
        "quote_title": "✨ ข้อความถึงคุณ",
        "quote_text": "\"ไม่ว่าจะเผชิญกับความยากลำบากหรืออนาคตที่กว้างไกล ค่อยๆ ก้าวไปตามจังหวะของคุณเอง คุณเก่งและมีความสามารถเสมอ\"",
        "timer_title": "⏳ เวลาจนกว่าคนสำคัญจะตื่นขึ้น...",
        "timer_unit_d": "วัน", "timer_unit_h": "ชม.", "timer_unit_m": "นาที",
        "timer_footer": "มาตั้งตารอช่วงเวลาฤดูหนาวที่อบอุ่นด้วยกันเถอะ!",
        "advent_title": "📅 ปฏิทินนับถอยหลังคริสต์มาสเดือนธันวาคม",
        "advent_desc": "เซอร์ไพรส์เล็กๆ ในแต่ละวัน (อ้างอิงเวลาไทเป)",
        "quest_title": "🎯 ภารกิจผ่อนคลายประจำวัน",
        "quest_change": "🔄 เปลี่ยนภารกิจ",
        "quest_done_btn": "✅ ทำสำเร็จแล้ว!",
        "food_title": "🍽️ ตอนที่ไม่รู้จะกินอะไรดี",
        "food_style_label": "เลือกสไตล์อาหาร:",
        "food_any_style": "ได้หมด",
        "food_btn": "🎲 สุ่มเมนูอาหาร",
        "drink_title": "🥤 ตอนที่ไม่รู้จะดื่มอะไรดี",
        "drink_btn": "💧 สุ่มเครื่องดื่ม",
        "flower_title": "🌸 ความหมายของดอกไม้และคำทำนาย",
        "flower_desc": "สถานที่เต็มไปด้วยดอกไม้ที่มีความหมาย เลือกพืชพรรณที่มีความหมายดีๆ เพื่อนำพาโชค 1 วันเต็มมาให้คุณ!",
        "flower_btn": "🎲 สุ่มดอกไม้ประจำวัน",
        "flower_result": "คุณได้ดอก: ",
        "flower_lang": "✨ ความหมาย",
        "flower_fortune": "โชคลาภ",
        "flower_msg": "คำอวยพรพิเศษ",
        "plant_title": "🌱 ปลูกต้นไม้จิ๋วประจำวัน",
        "plant_desc": "รดน้ำ รับแดด และให้กำลังใจจนต้นไม้เบ่งบาน!",
        "plant_water": "💧 รดน้ำ",
        "plant_sun": "☀️ รับแดด",
        "plant_cheer": "✨ ให้กำลังใจ",
        "plant_reset": "🔁 ปลูกกระถางใหม่",
        "xmas_lock_title": "🔒 โบนัสคริสต์มาสยังไม่ปลดล็อก",
        "xmas_lock_desc": "เซอร์ไพรส์คริสต์มาสนี้จะเปิดในวันที่ **25 ธันวาคม** (เวลาไทเป) ระหว่างนี้พักผ่อนในป่าสีเขียวและสวนดอกไม้ไปก่อนนะ!",
        "xmas_title": "🎄 โบนัสพิเศษคริสต์มาส",
        "xmas_desc": "ยินดีต้อนรับสู่ป่าหิมะฤดูหนาว! คลิกปุ่มด้านล่างเพื่อเปิดไฟต้นคริสต์มาสและรับคำอวยพรจากซานตาคลอส",
        "xmas_btn": "🌟 จุดประกายความปรารถนาคริสต์มาส",
        "xmas_snow_btn": "❄️ โปรยหิมะอีกครั้ง",
        "xmas_reset_btn": "🌙 กลับสู่ท้องฟ้ายามค่ำคืน",
        "xmas_box_title": "🎁 ประกาศจากซานตาคลอส",
        "xmas_box_text": "\"โฮ โฮ โฮ โฮ! เธอปลุกฉันสินะ! หวังว่าป่าสีเขียวแห่งนี้จะนำความอบอุ่นมาให้เธอในฤดูหนาวนี้นะ ไม่ว่าจะอยากใช้ชีวิตสงบๆ หรือผจญภัยในอนาคต ซานตาคลอสจะคอยสนับสนุนเธอเต็มที่แน่นอน! Merry Christmas & Happy Every Day My child！ 🌲❄️✨\"",
        "xmas_placeholder": "👆 คลิกปุ่มด้านข้างเพื่อปลุกเกล็ดหิมะ กระดิ่งคริสต์มาส และคนสำคัญคนนั้น!",
        "gift_title": "🧦 เปิดกล่องของขวัญคริสต์มาส（เลือกได้กล่องเดียว）",
        "gift_desc": "ซานตามีของขวัญให้เด็กๆ คนละชิ้นเท่านั้น เลือกกล่องที่ถูกใจที่สุดเพียงกล่องเดียว（อย่าลืมแคปหน้าจอเก็บไว้นะ）：",
        "gift_red": "🎁 กล่องสีแดง",
        "gift_gold": "🎁 กล่องสีทอง",
        "gift_green": "🎁 กล่องสีเขียว",
        "wish_title": "💌 อธิษฐานขอพรคริสต์มาสปีนี้",
        "wish_placeholder": "เขียนคำอธิษฐานเล็กๆ หรือข้อความถึงตัวเอง...",
        "wish_btn": "✨ สร้างการ์ดที่ระลึกคริสต์มาส"
    }
}

# 時間與解鎖狀態計算（依台北時間 UTC+8，12/25 00:00 正式解鎖聖誕彩蛋）
taipei_tz = datetime.timezone(datetime.timedelta(hours=8))
now = datetime.datetime.now(taipei_tz)
xmas_unlock_dt = datetime.datetime(now.year, 12, 25, 0, 0, 0, tzinfo=taipei_tz)
is_xmas_unlocked = (now.month == 12 and now.day >= 25)

if not is_xmas_unlocked:
    st.session_state.show_tree_bg = False
    st.session_state.auto_xmas_bgm = False

# ==================== 側邊欄導覽、語言與日夜模式 ====================
selected_lang = st.sidebar.selectbox("🌍 選擇語言 / Language", list(translations.keys()), index=0)
t = translations[selected_lang]

st.sidebar.markdown(f"## {t['nav_title']}")
menu = st.sidebar.radio(
    t["nav_select"],
    [t["menu_1"], t["menu_2"], t["menu_3"]]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['music_title']}")
bgm_toggle = st.sidebar.toggle(t["music_toggle"], value=False)
st.session_state.night_mode = st.sidebar.toggle(t["night_toggle"], value=st.session_state.night_mode)

st.sidebar.markdown("---")
st.sidebar.info(t["sidebar_info"])

# ==================== 音樂播放控制 ====================
can_auto_xmas = is_xmas_unlocked and (menu == t["menu_3"]) and st.session_state.show_tree_bg and st.session_state.auto_xmas_bgm
should_play_bgm = bgm_toggle or can_auto_xmas

if should_play_bgm:
    is_xmas_active = is_xmas_unlocked and (menu == t["menu_3"]) and st.session_state.show_tree_bg
    if not is_xmas_active:
        if happy_audio_base64:
            st.markdown(f"""
                <audio autoplay loop controls style="display:none;">
                    <source src="data:audio/mp3;base64,{happy_audio_base64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)
    else:
        if xmas_audio_base64:
            st.markdown(f"""
                <audio autoplay loop controls style="display:none;">
                    <source src="data:audio/mp3;base64,{xmas_audio_base64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)

# 依日夜模式動態決定卡片與文字色系
is_night = st.session_state.night_mode
card_bg = "rgba(18, 30, 24, 0.88)" if is_night else "rgba(255, 255, 255, 0.94)"
card_border = "rgba(167, 243, 208, 0.22)" if is_night else "rgba(255, 255, 255, 0.9)"
text_main = "#f1f5f9" if is_night else "#2d3748"
text_accent = "#86efac" if is_night else "#2e5a44"
title_color = "#ecfdf5" if is_night else "#1e3d2f"
title_shadow = "0 2px 8px rgba(0,0,0,0.85)" if is_night else "0 2px 4px rgba(255,255,255,0.9)"
timer_card_bg = "rgba(20, 38, 29, 0.92)" if is_night else "rgba(230, 242, 236, 0.96)"
timer_box_bg = "rgba(12, 24, 18, 0.92)" if is_night else "rgba(255, 255, 255, 0.92)"
overlay_darkness = 0.42 if is_night else 0.20

# 自訂精美溫馨風格 CSS + 植栽動畫 + 倒數日曆格線 + 聖誕燈串動畫
st.markdown(f"""
    <style>
    [data-testid="stSidebar"] {{
        background-color: #16241b;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}
    [data-testid="stSidebar"] * {{
        color: #e2e8f0 !important;
    }}
    .stButton>button {{
        background-color: #2e5a44;
        color: white;
        border-radius: 12px;
        padding: 0.55rem 1.0rem;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        transition: all 0.25s ease;
    }}
    .stButton>button:hover:not(:disabled) {{
        background-color: #3b7458;
        color: #fff;
        transform: translateY(-1px);
    }}
    .stButton>button:disabled {{
        opacity: 0.45;
        cursor: not-allowed;
    }}
    .card {{
        background-color: {card_bg};
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        margin-bottom: 18px;
        border: 1px solid {card_border};
        backdrop-filter: blur(10px);
        color: {text_main};
    }}
    .christmas-card {{
        background: rgba(15, 23, 42, 0.90);
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.6);
        margin-bottom: 20px;
        border: 2px dashed #f6e05e;
        backdrop-filter: blur(10px);
        color: #f8fafc;
    }}
    .voucher-card {{
        background: linear-gradient(135deg, rgba(127, 29, 29, 0.92), rgba(15, 23, 42, 0.95));
        padding: 22px;
        border-radius: 16px;
        border: 2px solid #fbbf24;
        box-shadow: 0 0 22px rgba(251, 191, 36, 0.35);
        text-align: center;
        margin: 14px 0;
        color: #fef3c7;
    }}
    .wish-card {{
        background: linear-gradient(135deg, rgba(20, 83, 45, 0.90), rgba(15, 23, 42, 0.94));
        padding: 22px;
        border-radius: 16px;
        border: 1.5px solid #86efac;
        box-shadow: 0 0 18px rgba(134, 239, 172, 0.28);
        margin-top: 12px;
        color: #ecfdf5;
    }}
    .title-text {{
        color: {title_color};
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-shadow: {title_shadow};
    }}
    .timer-box {{
        background: {timer_box_bg};
        padding: 15px 25px;
        border-radius: 14px;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(0,0,0,0.12);
        border: 2px solid #2e5a44;
        margin: 10px 0;
    }}
    .advent-grid {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 6px;
        margin-top: 12px;
    }}
    .advent-cell {{
        border-radius: 10px;
        padding: 8px 4px;
        text-align: center;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(46, 90, 68, 0.25);
    }}
    .advent-unlocked {{
        background: rgba(74, 222, 128, 0.22);
        color: {text_main};
    }}
    .advent-locked {{
        background: rgba(148, 163, 184, 0.16);
        color: #94a3b8;
    }}
    @keyframes swayPlant {{
        0%, 100% {{ transform: rotate(-3deg) scale(1); }}
        50% {{ transform: rotate(3deg) scale(1.04); }}
    }}
    @keyframes bloomPulse {{
        0%, 100% {{ transform: scale(1); filter: drop-shadow(0 0 4px rgba(250, 204, 21, 0.35)); }}
        50% {{ transform: scale(1.12); filter: drop-shadow(0 0 12px rgba(250, 204, 21, 0.75)); }}
    }}
    @keyframes twinkleBulbA {{
        0%, 100% {{ opacity: 1; transform: scale(1.15); box-shadow: 0 0 12px #f87171; }}
        50% {{ opacity: 0.35; transform: scale(0.9); box-shadow: none; }}
    }}
    @keyframes twinkleBulbB {{
        0%, 100% {{ opacity: 0.35; transform: scale(0.9); box-shadow: none; }}
        50% {{ opacity: 1; transform: scale(1.15); box-shadow: 0 0 12px #facc15; }}
    }}
    @keyframes twinkleBulbC {{
        0%, 100% {{ opacity: 0.85; transform: scale(1.08); box-shadow: 0 0 12px #4ade80; }}
        50% {{ opacity: 0.35; transform: scale(0.9); box-shadow: none; }}
    }}
    .lights-bar {{
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 10px 8px;
        margin-bottom: 12px;
        background: rgba(15, 23, 42, 0.65);
        border-radius: 999px;
        border: 1px solid rgba(250, 204, 21, 0.35);
    }}
    .bulb {{
        width: 14px;
        height: 14px;
        border-radius: 50%;
        display: inline-block;
    }}
    .bulb-red {{ background: #ef4444; animation: twinkleBulbA 1.6s infinite; }}
    .bulb-gold {{ background: #facc15; animation: twinkleBulbB 1.6s infinite; }}
    .bulb-green {{ background: #22c55e; animation: twinkleBulbC 1.6s infinite; }}
    .plant-anim-stage-0 {{
        font-size: 4rem;
        display: inline-block;
        animation: swayPlant 3.2s ease-in-out infinite;
    }}
    .plant-anim-stage-1 {{
        font-size: 4.3rem;
        display: inline-block;
        animation: swayPlant 2.4s ease-in-out infinite;
    }}
    .plant-anim-stage-2 {{
        font-size: 4.6rem;
        display: inline-block;
        animation: swayPlant 2.0s ease-in-out infinite;
    }}
    .plant-anim-bloom {{
        font-size: 5rem;
        display: inline-block;
        animation: bloomPulse 1.8s ease-in-out infinite;
    }}
    </style>
""", unsafe_allow_html=True)

# ==================== 1. 首頁：綠意森林與倒數 + 聖誕月曆 + 小任務 + 吃喝轉盤 ====================
if menu == t["menu_1"]:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, {overlay_darkness}), rgba(0, 0, 0, {overlay_darkness})),
                        url("data:image/jpeg;base64,{green_bg_base64}");
            background-size: cover;
            background-position: center bottom;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<h1 class='title-text'>{t['home_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #fff; font-size: 1.05rem; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.9);'>{t['home_desc']}</p>", unsafe_allow_html=True)

    st.markdown(f"""
        <div class='card'>
            <h3 style='color: {text_accent}; margin-top: 0;'>{t['quote_title']}</h3>
            <p style='font-size: 1.1rem; color: {text_main}; line-height: 1.6;'>
            {t['quote_text']}
            </p>
        </div>
    """, unsafe_allow_html=True)

    christmas = datetime.datetime(now.year, 12, 25, 0, 0, 0, tzinfo=taipei_tz)
    if now > christmas:
        christmas = datetime.datetime(now.year + 1, 12, 25, 0, 0, 0, tzinfo=taipei_tz)
    delta = christmas - now
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    st.markdown(f"""
        <div class='card' style='background: {timer_card_bg}; text-align: center;'>
            <h3 style='color: {text_accent}; margin-top: 0;'>{t['timer_title']}</h3>
            <div class="timer-box">
                <h2 style='color: {title_color}; margin: 0; font-size: 1.8rem;'>🎁 {days} {t['timer_unit_d']} {hours} {t['timer_unit_h']} {minutes} {t['timer_unit_m']} 🎄</h2>
            </div>
            <p style='color: {text_main}; font-weight: 650; margin-top: 10px;'>{t['timer_footer']}</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 聖誕倒數日曆（12/1 ~ 12/25 月曆型式） ---
    advent_notes = {
        1: "12/1 冬日序曲：把今天的步調放慢半拍，給自己一個好心情。",
        2: "12/2 暖心提醒：有在好好吃飯與喝水嗎？照顧好自己最重要。",
        3: "12/3 綠意小語：路邊看到綠色植物或小花時，停下來看一眼吧。",
        4: "12/4 輕鬆一下：今天不需要完美，只要有往前一點點就很棒了。",
        5: "12/5 悄悄打氣：你的細心與眼光一直都在發光，只是有時候自己沒發現。",
        6: "12/6 週末小憩：挑一段喜歡的音樂，讓腦袋放空一下。",
        7: "12/7 節氣叮嚀：大雪時節，注意保暖，別讓手腳冷冰冰的。",
        8: "12/8 好運累積：今天遇到的每件小事，都可能藏著之後的驚喜。",
        9: "12/9 呼吸練習：肩膀如果緊繃了，深呼吸三次再放下。",
        10: "12/10 靈感收集：看到喜歡的畫面或配色，先記在心裡吧。",
        11: "12/11 溫柔陪伴：就算今天什麼都不想做，這裡也永遠歡迎你。",
        12: "12/12 甜度補給：允許自己今天來一點喜歡的點心或飲料。",
        13: "12/13 節奏由你：照著自己的步調走，不用跟別人賽跑。",
        14: "12/14 森林微風：想像自己走在安靜的樹林裡，空氣很清新。",
        15: "12/15 自我肯定：回想一下這陣子撐過的大小事，你真的做得很棒。",
        16: "12/16 睡前放空：睡前把煩惱留在門外，今晚好好睡一覺。",
        17: "12/17 小確幸預告：說不定今天就會遇到讓人會心一笑的小事。",
        18: "12/18 步步踏實：每一份累積都不會白費，慢慢開花就好。",
        19: "12/19 溫暖冬陽：有陽光的時候，去窗邊或戶外曬幾分鐘吧。",
        20: "12/20 倒數五天：聖誕節的氣息越來越近囉！",
        21: "12/21 冬至祝福：冬至快樂！吃一碗熱呼呼的湯圓，迎接白晝漸長。",
        22: "12/22 倒數三天：森林裡的燈泡好像開始閃閃發亮了。",
        23: "12/23 倒數兩天：準備好迎接溫馨的節日氛圍了嗎？",
        24: "12/24 平安夜前夕：願今晚的你被滿滿的安心與溫暖包圍。",
        25: "12/25 聖誕快樂！Merry Christmas & Happy Every Day！🎄✨"
    }

    st.markdown(f"""
        <div class='card'>
            <h3 style='color: {text_accent}; margin-top: 0;'>{t['advent_title']}</h3>
            <p style='color: {text_main}; margin-bottom: 8px;'>{t['advent_desc']}</p>
    """, unsafe_allow_html=True)

    is_december = (now.month == 12)
    unlocked_max_day = now.day if is_december else 0

    grid_html = "<div class='advent-grid'>"
    for d in range(1, 26):
        if d <= unlocked_max_day:
            icon = "🎄" if d == 25 else "✨"
            grid_html += f"<div class='advent-cell advent-unlocked'>{icon}<br>12/{d}</div>"
        else:
            grid_html += f"<div class='advent-cell advent-locked'>🔒<br>12/{d}</div>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

    unlocked_days = [d for d in range(1, 26) if d <= unlocked_max_day]
    if unlocked_days:
        chosen_day = st.selectbox(
            "選擇已解鎖的日期查看內容：",
            unlocked_days,
            index=len(unlocked_days) - 1,
            format_func=lambda x: f"12月{x}日"
        )
        st.info(f"🎁 **12月{chosen_day}日**：{advent_notes[chosen_day]}")
    else:
        st.caption("目前尚未進入 12 月，12/1 起每天都會依序解鎖一格喔！")

    st.markdown("</div>", unsafe_allow_html=True)

    # --- 今日小任務 / 療癒挑戰 ---
    cozy_quests = [
        "💧 喝一杯溫水或喜歡的常溫飲品，幫身體補補水。",
        "🌿 離開螢幕 3 分鐘，看看窗外的天空、樹葉或綠色植物。",
        "🙆 伸個大懶腰，轉動一下肩膀與脖子，把緊繃感放掉。",
        "📸 拍一張今天覺得順眼的小角落、光影或可愛小東西。",
        "🎧 聽一首最近喜歡或能讓心情平靜的歌，專心聽完它。",
        "📝 在心裡寫下一件今天做得不錯的小事，誇誇自己。",
        "🍵 泡一杯熱茶或熱可可，享受安靜喝完的幾分鐘。",
        "🚶 到戶外走走或陽台吹吹風，感受一下空氣溫度。",
        "🧹 整理桌面或包包裡的一小塊地方，讓視線清爽一點。",
        "🌙 今晚早一點放下手機，給眼睛與大腦好好休息的時間。"
    ]

    st.markdown(f"""
        <div class='card'>
            <h3 style='color: {text_accent}; margin-top: 0;'>{t['quest_title']}</h3>
            <p style='font-size: 1.08rem; color: {text_main}; font-weight: 600;'>{cozy_quests[st.session_state.quest_idx]}</p>
    """, unsafe_allow_html=True)

    q_col1, q_col2 = st.columns(2)
    with q_col1:
        if st.button(t["quest_change"], key="btn_change_quest"):
            st.session_state.quest_idx = (st.session_state.quest_idx + 1) % len(cozy_quests)
            st.session_state.quest_done = False
            st.rerun()
    with q_col2:
        if st.button(t["quest_done_btn"], key="btn_done_quest"):
            st.session_state.quest_done = True

    if st.session_state.quest_done:
        st.success("🎉 太棒了！完成一件小小的療癒事，今天也很值得被溫柔對待！")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- 不知道該吃什麼時 / 不知道該喝什麼時（上下排列 + 八國翻譯） ---
    food_options = {
        "西式": ["帕瑪森起司烤雞潛艇堡", "奶油蘑菇燉飯與烤時蔬", "香煎鮭魚沙拉佐油醋醬", "經典起司牛肉漢堡與薯條"],
        "中式": ["熱騰騰牛肉麵或陽春麵", "蔥油雞腿飯配清爽青菜", "手工水餃或鍋貼配酸辣湯", "家常麻婆豆腐蓋飯"],
        "義式": ["番茄羅勒瑪格麗特披薩", "蒜香白酒蛤蠣義大利麵", "青醬雞肉筆管麵", "松露野菇燉飯"],
        "日式": ["親子丼或壽喜燒牛丼", "鮭魚酪梨丼飯配味增湯", "日式咖哩豬排飯", "讚岐烏龍麵與天婦羅"],
        "韓式": ["韓式拌飯配海帶湯", "起司辣炒年糕與魚板串", "韓式泡菜嫩豆腐鍋", "酥脆韓式炸雞"],
        "泰式": ["泰式打拋豬飯配半熟蛋", "酸辣海鮮河粉", "綠咖哩雞肉飯", "泰式蝦醬空心菜與炒河粉"],
        "越式": ["清爽越式生春捲與河粉", "越式烤肉米線", "香茅豬排越式法國麵包", "越式牛肉河粉"]
    }

    drink_options = [
        ("💧 常溫水 / 氣泡水", "最純粹的補水選擇，身體會很喜歡！"),
        ("🧋 珍珠奶茶 / 鮮奶茶", "今天想來點療癒甜味，半糖微冰剛剛好。"),
        ("🍵 四季春 / 青茶", "清爽不膩口，配餐點或下午放空都很搭。"),
        ("🍋 蜂蜜檸檬 / 鮮果茶", "酸酸甜甜的果香，替今天提提神。"),
        ("☕ 拿鐵 / 摩卡", "需要一點溫柔陪伴或清醒感時的好夥伴。"),
        ("🍃 烏龍茶 / 綠茶", "溫潤茶香，喝完覺得整個人都輕盈了。"),
        ("🍫 濃郁可可", "冬日裡暖呼呼的幸福滋味。")
    ]

    # 上：不知道該吃什麼時
    st.markdown(f"""
        <div class='card'>
            <h3 style='color: {text_accent}; margin-top: 0;'>{t['food_title']}</h3>
    """, unsafe_allow_html=True)

    any_label = t["food_any_style"]
    cuisine_choice = st.selectbox(
        t["food_style_label"],
        [any_label] + list(food_options.keys()),
        key="cuisine_select"
    )
    if st.button(t["food_btn"], key="btn_pick_food"):
        if cuisine_choice == any_label:
            cat = random.choice(list(food_options.keys()))
        else:
            cat = cuisine_choice
        dish = random.choice(food_options[cat])
        st.session_state.picked_food = f"【{cat}】{dish}"
    if st.session_state.picked_food:
        st.info(f"✨ {st.session_state.picked_food}")

    st.markdown("</div>", unsafe_allow_html=True)

    # 下：不知道該喝什麼時
    st.markdown(f"""
        <div class='card'>
            <h3 style='color: {text_accent}; margin-top: 0;'>{t['drink_title']}</h3>
    """, unsafe_allow_html=True)

    if st.button(t["drink_btn"], key="btn_pick_drink"):
        st.session_state.picked_drink = random.choice(drink_options)
    if st.session_state.picked_drink:
        d_name, d_tip = st.session_state.picked_drink
        st.info(f"✨ **{d_name}**\n\n{d_tip}")

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 2. 吉祥花語與解憂籤詩 + 每日專屬小植栽養成 ====================
elif menu == t["menu_2"]:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, {overlay_darkness}), rgba(0, 0, 0, {overlay_darkness})),
                        url("data:image/jpeg;base64,{green_bg_base64}");
            background-size: cover;
            background-position: center bottom;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<h1 class='title-text'>{t['flower_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #fff; font-size: 1.05rem; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.9);'>{t['flower_desc']}</p>", unsafe_allow_html=True)

    lucky_plants = [
        {"plant": "🌸 蝴蝶蘭", "flower_language": "幸福向你靠近、高潔典雅、事事順心", "fortune": "大吉", "msg": "蝴蝶蘭象徵幸福到來與好運連連。今天的你散發著獨特而高雅的魅力，自信往前走，機會就在轉角！"},
        {"plant": "🌻 向日葵", "flower_language": "信念、光輝、勇敢追夢、充滿朝氣", "fortune": "超吉", "msg": "永遠朝向陽光生長的向日葵！不管外在環境如何，你內心始終有一股溫暖而堅定的力量，勇敢去發光吧。"},
        {"plant": "🌿 桂花", "flower_language": "崇高、吉祥、迎風飄香、貴人相助", "fortune": "吉上加吉", "msg": "桂花開口，清香自來。這陣子你的努力與才華會像桂花香一樣悄悄傳開，遇到欣賞你的溫暖貴人！"},
        {"plant": "🌷 鬱金香", "flower_language": "永恆的祝福、慈愛、名譽與美滿", "fortune": "大發", "msg": "典雅的鬱金香代表著美好的成果。你過去在景觀設計上的累積與美感，都是無價的寶藏，靜待花開即可。"},
        {"plant": "🍀 四葉幸運草", "flower_language": "幸運、希望、真愛與健康", "fortune": "平安喜樂", "msg": "尋獲四葉草需要一點緣分，正如美好的契合。今天的你被幸運溫柔包圍，放鬆心情，一切都會順心如意！"},
        {"plant": "🌿 虎尾蘭", "flower_language": "堅韌不拔、強大保護力、步步高升", "fortune": "穩健大吉", "msg": "具有強大淨化與適應力的虎尾蘭。你擁有面對挑戰時的過人韌性，一步一腳印，絕對能達成心中的理想目標。"},
        {"plant": "🌺 繡球花", "flower_language": "希望、團聚、美滿、永恆的幸福", "fortune": "福氣滿滿", "msg": "繡球花圓滿的花型象徵著圓滿與好人緣。今天適合展現親和力，周遭的溫暖會回饋到你身上！"},
        {"plant": "🌹 茶花", "flower_language": "可愛、謙遜、理想的愛、謹慎而堅定", "fortune": "事事如意", "msg": "茶花在寒冬中依然綻放。這代表著你內心擁有非常扎實的底蘊與實力，冷靜應對，絕對能驚豔全場。"},
        {"plant": "🌿 琴葉榕", "flower_language": "和平、長久、高大挺拔、清新文藝", "fortune": "大吉大利", "msg": "姿態優雅大方的琴葉榕，能為空間帶來安定的氣場。今天適合靜心規劃未來，每一步都在往好的方向前進。"},
        {"plant": "🌾 薰衣草", "flower_language": "等待愛情、心想事成、寧靜與療癒", "fortune": "心曠神怡", "msg": "帶著浪漫香氣的薰衣草，為你洗去內心的疲憊。給自己一杯茶的時間放空，好靈感隨之而來。"},
        {"plant": "🌼 雛菊", "flower_language": "純潔、天真、和平、希望與暗戀的幸福", "fortune": "喜事連連", "msg": "像小太陽一樣樸實而溫暖的雛菊。保持赤子之心與對未來的熱情，簡單的小確幸今天就會找上門！"},
        {"plant": "🎋 翠竹", "flower_language": "正直、高風亮節、節節高升、平安吉祥", "fortune": "步步高升", "msg": "竹子虛心有節、韌性極強。面對任何挑戰你總能迎刃而解，未來的每一步都會穩扎穩打、節節高升！"}
    ]

    if st.button(t["flower_btn"]):
        picked = random.choice(lucky_plants)
        st.markdown(f"""
            <div class='card' style='border-left: 6px solid #2e5a44;'>
                <h3 style='color: {text_accent}; margin-top: 0;'>🌿 {t['flower_result']}{picked['plant']}</h3>
                <p style='color: {text_main};'><strong>{t['flower_lang']}</strong>：<span style='color: #d97706; font-weight: bold;'>{picked['flower_language']}</span>（{t['flower_fortune']}：{picked['fortune']}）</p>
                <hr style='border: none; border-top: 1px solid rgba(148,163,184,0.35); margin: 12px 0;'>
                <p style='color: {text_main}; line-height: 1.6;'>💬 <strong>{t['flower_msg']}</strong>：{picked['msg']}</p>
            </div>
        """, unsafe_allow_html=True)

    # --- 每日專屬小植栽養成（CSS 動畫呈現） ---
    growth_stages = [
        ("🌰", "沉睡的小種子", "plant-anim-stage-0", "靜靜躺在土裡，等著你給它第一份照顧。"),
        ("🌱", "剛冒出的嫩芽", "plant-anim-stage-1", "探出小小的綠芽了！看起來充滿好奇心。"),
        ("🌿", "綠意盎然的小苗", "plant-anim-stage-2", "葉片舒展開來，在微風裡輕輕搖曳。"),
        ("🌺", "盛開的療癒花朵", "plant-anim-bloom", "開出漂亮的花囉！把這份好運與溫暖送給你。")
    ]
    stage_idx = min(st.session_state.plant_growth, 3)
    p_emoji, p_name, p_anim_class, p_desc = growth_stages[stage_idx]

    st.markdown(f"""
        <div class='card' style='text-align: center;'>
            <h3 style='color: {text_accent}; margin-top: 0;'>{t['plant_title']}</h3>
            <p style='color: {text_main};'>{t['plant_desc']}</p>
            <div class='{p_anim_class}'>{p_emoji}</div>
            <h4 style='color: {text_main}; margin: 8px 0 4px 0;'>{p_name}（成長值：{st.session_state.plant_growth} / 3）</h4>
            <p style='color: {text_main}; font-size: 0.98rem;'>{p_desc}</p>
    """, unsafe_allow_html=True)

    if st.session_state.plant_action_note:
        st.caption(st.session_state.plant_action_note)

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button(t["plant_water"], key="btn_water"):
            st.session_state.plant_growth = min(st.session_state.plant_growth + 1, 3)
            st.session_state.plant_action_note = "💧 咕嚕咕嚕，小植栽喝到清爽的水分了！"
            if st.session_state.plant_growth == 3:
                st.balloons()
            st.rerun()
    with b2:
        if st.button(t["plant_sun"], key="btn_sun"):
            st.session_state.plant_growth = min(st.session_state.plant_growth + 1, 3)
            st.session_state.plant_action_note = "☀️ 暖洋洋的陽光灑下來，葉子亮晶晶的！"
            if st.session_state.plant_growth == 3:
                st.balloons()
            st.rerun()
    with b3:
        if st.button(t["plant_cheer"], key="btn_cheer"):
            st.session_state.plant_growth = min(st.session_state.plant_growth + 1, 3)
            st.session_state.plant_action_note = "✨ 收到溫柔的鼓勵，小植栽更有力量長大了！"
            if st.session_state.plant_growth == 3:
                st.balloons()
            st.rerun()

    if st.session_state.plant_growth >= 3:
        if st.button(t["plant_reset"], key="btn_reset_plant"):
            st.session_state.plant_growth = 0
            st.session_state.plant_action_note = ""
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 3. 聖誕限定彩蛋專區（12/25 時間鎖 + 點燈自動播放 bgm_xmas + 禮物盒擇一抽券 + 心願卡） ====================
elif menu == t["menu_3"]:
    if not is_xmas_unlocked:
        st.markdown(f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(0, 0, 0, {overlay_darkness}), rgba(0, 0, 0, {overlay_darkness})),
                            url("data:image/jpeg;base64,{green_bg_base64}");
                background-size: cover;
                background-position: center bottom;
                background-attachment: fixed;
            }}
            </style>
        """, unsafe_allow_html=True)

        rem = xmas_unlock_dt - now
        rem_d = max(0, rem.days)
        rem_h = max(0, rem.seconds // 3600)
        rem_m = max(0, (rem.seconds % 3600) // 60)

        st.markdown(f"""
            <div class='card' style='text-align: center; margin-top: 20px;'>
                <div style='font-size: 3.2rem; margin-bottom: 8px;'>🎄🔒✨</div>
                <h2 style='color: {text_accent}; margin-top: 0;'>{t['xmas_lock_title']}</h2>
                <p style='color: {text_main}; font-size: 1.05rem; line-height: 1.7;'>{t['xmas_lock_desc']}</p>
                <div class='timer-box'>
                    <h3 style='color: {title_color}; margin: 0;'>⏳ {rem_d} {t['timer_unit_d']} {rem_h} {t['timer_unit_h']} {rem_m} {t['timer_unit_m']}</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        current_bg = xmas_tree_bg_base64 if st.session_state.show_tree_bg and xmas_tree_bg_base64 else xmas_bg_base64
        bg_mime = "image/jpeg" if st.session_state.show_tree_bg else "image/png"

        st.markdown(f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)),
                            url("data:{bg_mime};base64,{current_bg}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            .christmas-title {{
                color: #f6e05e !important;
                text-shadow: 0 2px 6px rgba(0,0,0,0.9);
            }}
            .christmas-desc {{
                color: #edf2f7 !important;
                text-shadow: 0 1px 4px rgba(0,0,0,0.9);
                font-size: 1.05rem;
            }}
            </style>
        """, unsafe_allow_html=True)

        # 頂部閃爍聖誕燈串
        bulbs_html = "<div class='lights-bar'>" + "".join([
            "<span class='bulb bulb-red'></span>"
            "<span class='bulb bulb-gold'></span>"
            "<span class='bulb bulb-green'></span>"
            for _ in range(5)
        ]) + "</div>"
        st.markdown(bulbs_html, unsafe_allow_html=True)

        st.markdown(f"<h1 class='title-text christmas-title'>{t['xmas_title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='christmas-desc'>{t['xmas_desc']}</p>", unsafe_allow_html=True)

        # 點燈按鈕與重置按鈕
        if not st.session_state.show_tree_bg:
            if st.button(t["xmas_btn"], key="btn_light_xmas"):
                st.session_state.show_tree_bg = True
                st.session_state.auto_xmas_bgm = True
                st.rerun()
        else:
            col_x1, col_x2 = st.columns(2)
            with col_x1:
                if st.button(t["xmas_snow_btn"], key="btn_snow_again"):
                    st.snow()
            with col_x2:
                if st.button(t["xmas_reset_btn"], key="btn_reset_xmas"):
                    st.session_state.show_tree_bg = False
                    st.session_state.auto_xmas_bgm = False
                    st.session_state.xmas_voucher = None
                    st.session_state.xmas_picked_box = None
                    st.rerun()

        if st.session_state.show_tree_bg:
            st.snow()
            st.markdown(f"""
                <div class='christmas-card'>
                    <h3 style='color: #f6e05e; margin-top: 0;'>{t['xmas_box_title']}</h3>
                    <p style='font-size: 1.1rem; color: #fff; font-weight: 500; line-height: 1.7;'>
                    {t['xmas_box_text']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            # --- 聖誕禮物盒擇一抽專屬兌換券（每人只能挑一份） ---
            vouchers = {
                "red": ("🧋 暖心飲料無限暢飲券", "隨時指定想喝的手搖飲或熱飲一杯，使命必達！"),
                "gold": ("🍽️ 任選一頓聖誕大餐券", "想吃西式、日式、韓式或任何料理，憑截圖隨時兌換！"),
                "green": ("🎧 專屬樹洞陪聊 / 放空券", "想吐槽、想分享日常或單純安靜待著，隨時召喚陪伴！")
            }

            already_picked = st.session_state.xmas_picked_box is not None

            st.markdown(f"""
                <div class='christmas-card'>
                    <h3 style='color: #f6e05e; margin-top: 0;'>{t['gift_title']}</h3>
                    <p style='color: #e2e8f0; margin-bottom: 12px;'>{t['gift_desc']}</p>
            """, unsafe_allow_html=True)

            g1, g2, g3 = st.columns(3)
            with g1:
                if st.button(t["gift_red"], key="btn_gift_red", disabled=already_picked):
                    st.session_state.xmas_picked_box = "red"
                    st.session_state.xmas_voucher = vouchers["red"]
                    st.rerun()
            with g2:
                if st.button(t["gift_gold"], key="btn_gift_gold", disabled=already_picked):
                    st.session_state.xmas_picked_box = "gold"
                    st.session_state.xmas_voucher = vouchers["gold"]
                    st.rerun()
            with g3:
                if st.button(t["gift_green"], key="btn_gift_green", disabled=already_picked):
                    st.session_state.xmas_picked_box = "green"
                    st.session_state.xmas_voucher = vouchers["green"]
                    st.rerun()

            if st.session_state.xmas_voucher:
                box_labels = {
                    "red": t["gift_red"],
                    "gold": t["gift_gold"],
                    "green": t["gift_green"]
                }
                chosen_label = box_labels.get(st.session_state.xmas_picked_box, "")
                v_title, v_desc = st.session_state.xmas_voucher
                st.markdown(f"""
                    <div class='voucher-card'>
                        <div style='font-size: 0.85rem; letter-spacing: 2px; color: #fde68a;'>★ {chosen_label}・專屬禮物已選定 ★</div>
                        <h3 style='color: #fef08a; margin: 8px 0;'>{v_title}</h3>
                        <p style='color: #fffbeb; margin: 0; font-size: 1rem;'>{v_desc}</p>
                    </div>
                """, unsafe_allow_html=True)
                st.caption("🎄 聖誕老人的規矩：每人只能挑一份禮物，這份就是你的專屬驚喜囉！")

            st.markdown("</div>", unsafe_allow_html=True)

            # --- 許下今年的聖誕心願（生成專屬紀念卡） ---
            st.markdown(f"""
                <div class='christmas-card'>
                    <h3 style='color: #f6e05e; margin-top: 0;'>{t['wish_title']}</h3>
            """, unsafe_allow_html=True)

            wish_input = st.text_input(
                label="Christmas Wish",
                placeholder=t["wish_placeholder"],
                label_visibility="collapsed",
                key="xmas_wish_input"
            )
            if st.button(t["wish_btn"], key="btn_make_wish"):
                if wish_input.strip():
                    st.session_state.xmas_wish_card = wish_input.strip()

            if st.session_state.xmas_wish_card:
                st.markdown(f"""
                    <div class='wish-card'>
                        <div style='font-size: 0.85rem; color: #bbf7d0;'>🎄 {now.year} CHRISTMAS WISH KEEPSAKE</div>
                        <p style='font-size: 1.15rem; font-weight: 600; color: #ffffff; margin: 10px 0; line-height: 1.6;'>
                        「{st.session_state.xmas_wish_card}」
                        </p>
                        <div style='font-size: 0.85rem; color: #86efac; text-align: right;'>✨ 願這個冬天的所有美好都如期而至</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown(f"""
                <div style='padding: 25px; background: rgba(15, 23, 42, 0.85); border-radius: 16px; text-align: center; border: 2px dashed #f6e05e; backdrop-filter: blur(8px);'>
                    <p style='color: #f6e05e; margin: 0; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.8);'>{t['xmas_placeholder']}</p>
                </div>
            """, unsafe_allow_html=True)