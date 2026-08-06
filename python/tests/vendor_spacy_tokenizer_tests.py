# Vendored spaCy tokenizer test data
#
# These test cases are adapted from the spaCy test suite
# (https://github.com/explosion/spaCy), which is licensed under the MIT License:
#
#     Copyright (c) 2016-present ExplosionAI GmbH, released under the MIT License.
#
# The data is kept as close as possible to the original inputs so that
# interstiCy can be validated against the same real-world tokenization cases
# spaCy uses internally.

SPACY_TOKENIZER_TEXTS = [
    # issue regression texts
    "I went for 40.3, and got home by 10.0.",
    "I like _MATH_ even _MATH_ when _MATH_, except when _MATH_ is _MATH_! but not _MATH_.",
    "880.794.982.218.444.893.023.439.794.626.120.190.780.624.990.275.671 ist eine lange Zahl",
    "oow.jspsearch.eventoracleopenworldsearch.technologyoraclesolarissearch.technologystoragesearch.technologylinuxsearch.technologyserverssearch.technologyvirtualizationsearch.technologyengineeredsystemspcodewwmkmppscem:",
    "I went for 40.3, and got home by 10.0.",
    "a",
    "am",
    "",
    "lorem",
    "Lorem, ipsum.",
    "Lorem, (ipsum).",
    "Lorem ipsum: 1984.",
    "(((_SPECIAL_ A/B, A/B-A/B\")",
    "_SPECIAL_.",
    "the _ID'X_",
    "a b c",
    "a.",
    "a a.",
    "a10.",
    "±10%",
    "No--don't see",
    "id",
    "A'B C",
    "A-B",
    # long texts
    """Lorem ipsum dolor sit amet, consectetur adipiscing elit

Cras egestas orci non porttitor maximus.
Maecenas quis odio id dolor rhoncus dignissim. Curabitur sed velit at orci ultrices sagittis. Nulla commodo euismod arcu eget vulputate.

Phasellus tincidunt, augue quis porta finibus, massa sapien consectetur augue, non lacinia enim nibh eget ipsum. Vestibulum in bibendum mauris.

"Nullam porta fringilla enim, a dictum orci consequat in." Mauris nec malesuada justo.""",
    "Lorem dolor sit amet, consectetur adipiscing elit.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
]

SPACY_URLS_BASIC = [
    "http://www.nytimes.com/2016/04/20/us/politics/new-york-primary-preview.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=a-lede-package-region&region=top-news&WT.nav=top-news&_r=0",
    "www.red-stars.com",
    "mailto:foo.bar@baz.com",
]

SPACY_URLS_FULL = SPACY_URLS_BASIC + [
    "mailto:foo-bar@baz-co.com",
    "mailto:foo-bar@baz-co.com?subject=hi",
    "www.google.com?q=google",
    "http://foo.com/blah_(wikipedia)#cite-1",
]

# URL patterns from https://mathiasbynens.be/demo/url-regex
SPACY_URLS_SHOULD_MATCH = [
    "http://foo.com/blah_blah",
    "http://BlahBlah.com/Blah_Blah",
    "http://foo.com/blah_blah/",
    "http://www.example.com/wpstyle/?p=364",
    "https://www.example.com/foo/?bar=baz&inga=42&quux",
    "http://userid:password@example.com:8080",
    "http://userid:password@example.com:8080/",
    "http://userid@example.com",
    "http://userid@example.com/",
    "http://userid@example.com:8080",
    "http://userid@example.com:8080/",
    "http://userid:password@example.com",
    "http://userid:password@example.com/",
    "http://142.42.1.1/",
    "http://142.42.1.1:8080/",
    "http://foo.com/blah_(wikipedia)#cite-1",
    "http://foo.com/blah_(wikipedia)_blah#cite-1",
    "http://foo.com/unicode_(✪)_in_parens",
    "http://foo.com/(something)?after=parens",
    "http://code.google.com/events/#&product=browser",
    "http://j.mp",
    "ftp://foo.bar/baz",
    "http://foo.bar/?q=Test%20URL-encoded%20stuff",
    "http://-.~_!$&'()*+,;=:%40:80%2f::::::@example.com",
    "http://1337.net",
    "http://a.b-c.de",
    "http://223.255.255.254",
    "http://a.b--c.de/",
    "ssh://login@server.com:12345/repository.git",
    "svn+ssh://user@ssh.yourdomain.com/path",
    "http://foo.com/blah_blah_(wikipedia)",
    "http://foo.com/blah_blah_(wikipedia)_(again)",
    "http://www.foo.co.uk",
    "http://www.foo.co.uk/",
    "http://www.foo.co.uk/blah/blah",
    "http://⌘.ws",
    "http://⌘.ws/",
    "http://☺.damowmow.com/",
    "http://✪df.ws/123",
    "http://➡.ws/䨹",
    "http://مثال.إختبار",
    "http://例子.测试",
    "http://उदाहरण.परीक्षा",
]

SPACY_URLS_SHOULD_NOT_MATCH = [
    "http://",
    "http://.",
    "http://..",
    "http://../",
    "http://?",
    "http://??",
    "http://??/",
    "http://#",
    "http://##",
    "http://##/",
    "http://foo.bar?q=Spaces should be encoded",
    "//",
    "//a",
    "///a",
    "///",
    "http:///a",
    "rdar://1234",
    "h://test",
    "http:// shouldfail.com",
    ":// should fail",
    "http://foo.bar/foo(bar)baz quux",
    "http://-error-.invalid/",
    "http://a.b-.co",
    "http://0.0.0.0",
    "http://10.1.1.0",
    "http://10.1.1.255",
    "http://224.1.1.1",
    "http://123.123.123",
    "http://3628126748",
    "http://.www.foo.bar/",
    "http://.www.foo.bar./",
    "http://10.1.1.1",
    "NASDAQ:GOOG",
    "http://1.1.1.1.1",
    "http://www.foo.bar./",
]

SPACY_URL_PREFIXES = ["(", '"', ">"]
SPACY_URL_SUFFIXES = ['"', ":", ">"]

SPACY_EMOTICONS_TEXT = (
    ":o :/ :'( >:o (: :) >.< XD -__- o.O ;D :-) @_@ :P 8D :1 >:( :D =| :> ...."
)

SPACY_EMOJI_TESTS = [
    "can you still dunk?🍕🍔😵LOL",
    "i💙you",
    "🤘🤘yay!",
]

SPACY_DEGREE_TESTS = [
    "°c.",
    "°f.",
    "°k.",
    "°C.",
    "°F.",
    "°K.",
]

SPACY_WHITESPACE_TESTS = [
    "lorem ipsum",
    "lorem  ipsum",
    "lorem ipsum  ",
    "lorem\nipsum",
    "lorem \nipsum",
    "lorem  \nipsum",
    "lorem \n ipsum",
]

# Examples from the Big List of Naughty Strings
# https://github.com/minimaxir/big-list-of-naughty-strings
SPACY_NAUGHTY_STRINGS = [
    # ASCII punctuation
    r",./;'[]\-=",
    r'<>?:"{}|_+',
    r'!@#$%^&*()`~"',
    # Unicode additional control characters, byte order marks
    r"­؀؁؂؃؄؅؜۝܏᠎​‌‍‎‏‪",
    r"￾",
    # Unicode Symbols
    r"Ω≈ç√∫˜µ≤≥÷",
    r"åß∂ƒ©˙∆˚¬…æ",
    "œ∑´®†¥¨ˆøπ“‘",
    r"¡™£¢∞§¶•ªº–≠",
    r"¸˛Ç◊ı˜Â¯˘¿",
    r"ÅÍÎÏ˝ÓÔÒÚÆ☃",
    r"Œ„´‰ˇÁ¨ˆØ∏”’",
    r"`⁄€‹›ﬁﬂ‡°·‚—±",
    r"⅛⅜⅝⅞",
    r"ЁЂЃЄЅІЇЈЉЊЋЌЍЎЏАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя",
    r"٠١٢٣٤٥٦٧٨٩",
    # Unicode Subscript/Superscript/Accents
    r"⁰⁴⁵",
    r"₀₁₂",
    r"⁰⁴⁵₀₁₂",
    r"ด้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็ ด้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็ ด้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็็้้้้้้้้็็็็็้้้้้็็็็",
    r" ̄  ̄",
    # Two-Byte Characters
    r"田中さんにあげて下さい",
    r"パーティーへ行かないか",
    r"和製漢語",
    r"部落格",
    r"사회과학원 어학연구소",
    r"찦차를 타고 온 펲시맨과 쑛다리 똠방각하",
    r"社會科學院語學研究所",
    r"울란바토르",
    r"𠜎𠜱𠝹𠱓𠱸𠲖𠳏",
    # Japanese Emoticons
    r"ヽ༼ຈل͜ຈ༽ﾉ ヽ༼ຈل͜ຈ༽ﾉ",
    r"(｡◕ ∀ ◕｡)",
    r"｀ｨ(´∀｀∩",
    r"__ﾛ(,_,*)",
    r"・(￣∀￣)・:*:",
    r"ﾟ･✿ヾ╲(｡◕‿◕｡)╱✿･ﾟ",
    r",。・:*:・゜’( ☻ ω ☻ )。・:*:・゜’",
    r"(╯°□°）╯︵ ┻━┻)" "(ﾉಥ益ಥ）ﾉ﻿ ┻━┻",
    r"┬─┬ノ( º _ ºノ)",
    r"( ͡° ͜ʖ ͡°)",
    # Emoji
    r"😍",
    r"👩🏽",
    r"👾 🙇 💁 🙅 🙆 🙋 🙎 🙍",
    r"🐵 🙈 🙉 🙊",
    r"❤️ 💔 💌 💕 💞 💓 💗 💖 💘 💝 💟 💜 💛 💚 💙",
    r"✋🏿 💪🏿 👐🏿 🙌🏿 👏🏿 🙏🏿",
    r"🚾 🆒 🆓 🆕 🆖 🆗 🆙 🏧",
    r"0️⃣ 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟",
    # Regional Indicator Symbols
    r"🇺🇸🇷🇺🇸 🇦🇫🇦🇲🇸",
    r"🇺🇸🇷🇺🇸🇦🇫🇦🇲",
    r"🇺🇸🇷🇺🇸🇦",
    # Unicode Numbers
    r"１２３",
    r"١٢٣",
    # Right-To-Left Strings
    r"ثم نفس سقطت وبالتحديد،, جزيرتي باستخدام أن دنو. إذ هنا؟ الستار وتنصيب كان. أهّل ايطاليا، بريطانيا-فرنسا قد أخذ. سليمان، إتفاقية بين ما, يذكر الحدود أي بعد, معاملة بولندا، الإطلاق عل إيو.",
    r"إيو.",
    r"בְּרֵאשִׁית, בָּרָא אֱלֹהִים, אֵת הַשָּׁמַיִם, וְאֵת הָאָרֶץ",
    r"הָיְתָהtestالصفحات التّحول",
    r"﷽",
    r"ﷺ",
    r"مُنَاقَشَةُ سُبُلِ اِسْتِخْدَامِ اللُّغَةِ فِي النُّظُمِ الْقَائِمَةِ وَفِيم يَخُصَّ التَّطْبِيقَاتُ الْحاسُوبِيَّةُ،",
    # Trick Unicode
    r"‪‪test‪",
    r"‫test",
    r" test ",
    r"test⁠test",
    r"⁦test⁧",
    # Zalgo Text
    r"Ṱ̺̺̕o͞ ̷i̲̬͇̪͙n̝̗͕v̟̜̘̦͟o̶̙̰̠kè͚̮̺̪̹̱̤ ̖t̝͕̳̣̻̪͞h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d̵̼̟͙̩̼̘̳ ̞̥̱̳̭r̛̗̘e͙p͠r̼̞̻̭̗e̺̠̣͟s̘͇̳͍̝͉e͉̥̯̞̲͚̬͜ǹ̬͎͎̟̖͇̤t͍̬̤͓̼̭͘ͅi̪̱n͠g̴͉ ͏͉ͅc̬̟h͡a̫̻̯͘o̫̟̖͍̙̝͉s̗̦̲.̨̹͈̣",
    r"̡͓̞ͅI̗̘̦͝n͇͇͙v̮̫ok̲̫̙͈i̖͙̭̹̠̞n̡̻̮̣̺g̲͈͙̭͙̬͎ ̰t͔̦h̞̲e̢̤ ͍̬̲͖f̴̘͕̣è͖ẹ̥̩l͖͔͚i͓͚̦͠n͖͍̗͓̳̮͎̫̕n͟d̴̪̜̖ ̰͉̩͇͙̲͞ͅT͖̼͓̪͢h͏͓̮̻e̬̝̟ͅ ̤̹̝W͙̞̝͔͇͝ͅa͏͓͔̹̼̣l̴͔̰̤̟͔ḽ̫.͕",
    r"̗̺͖̹̯͓Ṯ̤͍̥͇͈h̲́e͏͓̼̗̙̼̣͔ ͇̜̱̠͓͍ͅN͕͠e̗̱z̘̝̜̺͙p̤̺̹͍̯͚e̠̻̠͜r̨̤͍̺̖͔̖̖d̠̟̭̬̝͟i̦͖̩͓͔̤a̠̗̬͉̙n͚͜ ̻̞̰͚ͅh̵͉i̳̞v̢͇ḙ͎͟ ̯̲͕͞ǫ̟̯̰̲͙̻̝f ̪̰̰̗̖̭̘͘c̦͍̲̞͍̩̙ḥ͚a̮͎̟̙͜ơ̩̹͎s̤.̝̝ ҉Z̡̖̜͖̰̣͉̜a͖̰͙̬͡l̲̫̳͍̩g̡̟̼̱͚̞̬ͅo̗͜.̟",
    r"̦H̬̤̗̤͝e͜ ̜̥̝̻͍̟́w̕h̖̯͓o̝͙̖͎̱̮ ҉̺̙̞̟͈W̷̼̭a̺̪͍į͈͕̭͙̯̜t̶̼̮s̘͙͖̕ ̠̫̠B̻͍͙͉̳ͅe̵h̵̬͇̫͙i̹͓̳̳̮͎̫̕n͟d̴̪̜̖ ̰͉̩͇͙̲͞ͅT͖̼͓̪͢h͏͓̮̻e̬̝̟ͅ ̤̹̝W͙̞̝͔͇͝ͅa͏͓͔̹̼̣l̴͔̰̤̟͔ḽ̫.͕",
    r"Z̮̞̠͙ͅḀ̗̞͈̻̗Ḻ͙͎̯̹̞͓G̻O̭̗̮",
    # Unicode Upsidedown
    r"˙ɐnbᴉlɐ ɐuƃɐɯ ǝɹolop ʇǝ ǝɹoqɐl ʇn ʇunpᴉpᴉɔuᴉ ɹodɯǝʇ poɯsnᴉǝ op pǝs 'ʇᴉlǝ ƃuᴉɔsᴉdᴉpɐ ɹnʇǝʇɔǝsuoɔ 'ʇǝɯɐ ʇᴉs ɹolop ɯnsdᴉ ɯǝɹo˥",
    r"00˙Ɩ$-",
    # Unicode font
    r"Ｔｈｅ ｑｕｉｃｋ ｂｒｏｗｎ ｆｏｘ ｊｕｍｐｓ ｏｖｅｒ ｔｈｅ ｌａｚｙ ｄｏｇ",
    r"𝐓𝐡𝐞 𝐪𝐮𝐢𝐜𝐤 𝐛𝐫𝐨𝐰𝐧 𝐟𝐨𝐱 𝐣𝐮𝐦𝐩𝐬 𝐨𝐯𝐞𝐫 𝐭𝐡𝐞 𝐥𝐚𝐳𝐲 𝐝𝐨𝐠",
    r"𝕿𝖍𝖊 𝖖𝖚𝖎𝖈𝖐 𝖇𝖗𝖔𝖜𝖓 𝖋𝖔𝖝 𝖏𝖚𝖒𝖕𝖘 𝖔𝖛𝖊𝖗 𝖙𝖍𝖊 𝖑𝖆𝖟𝖞 𝖉𝖔𝖌",
    r"𝑻𝒉𝒆 𝒒𝒖𝒊𝒄𝒌 𝒃𝒓𝒐𝒘𝒏 𝒇𝒐𝒙 𝒋𝒖𝒎𝒑𝒔 𝒐𝒗𝒆𝒓 𝒕𝒉𝒆 𝒍𝒂𝒛𝒚 𝒅𝒐𝒈",
    r"𝓣𝓱𝓮 𝓺𝓾𝓲𝓬𝓴 𝓫𝓻𝓸𝔀𝓷 𝓯𝓸𝔁 𝓳𝓾𝓶𝓹𝓼 𝓸𝓿𝓮𝓻 𝓽𝓱𝓮 𝓵𝓪𝔃𝔂 𝓭𝓸𝓰",
    r"𝕋𝕙𝕖 𝕢𝕦𝕚𝕔𝕜 𝕓𝕣𝕠𝕨𝕟 𝕗𝕠𝕩 𝕛𝕦𝕞𝕡𝕤 𝕠𝕧𝕖𝕣 𝕥𝕙𝕖 𝕝𝕒𝕫𝕪 𝕕𝕠𝕘",
    r"𝚃𝚑𝚎 𝚚𝚞𝚒𝚌𝚔 𝚋𝚛𝚘𝚠𝚗 𝚏𝚘𝚡 𝚓𝚞𝚖𝚙𝚜 𝚘𝚟𝚎𝚛 𝚝𝚑𝚎 𝚕𝚊𝚣𝚢 𝚍𝚘𝚐",
    r"⒯⒣⒠ ⒬⒰⒤⒞⒦ ⒝⒭⒪⒲⒩ ⒡⒪⒳ ⒥⒰⒨⒫⒮ ⒪⒱⒠⒭ ⒯⒣⒠ ⒧⒜⒵⒴ ⒟⒪⒢",
    # File paths
    r"../../../../../../../../../../../etc/passwd%00",
    r"../../../../../../../../../../../etc/hosts",
    # iOS Vulnerabilities
    r"Powerلُلُصّبُلُلصّبُررً ॣ ॣh ॣ ॣ冗",
    r"🏳0🌈️",
]

SUN_TEXT = """The Sun is the star at the center of the Solar System. It is almost perfectly spherical and consists of hot plasma interwoven with magnetic fields.[12][13] It has a diameter of about 1,392,684 km (865,374 mi),[5] around 109 times that of Earth, and its mass (1.989×1030 kilograms, approximately 330,000 times the mass of Earth) accounts for about 99.86% of the total mass of the Solar System.[14] Chemically, about three quarters of the Sun's mass consists of hydrogen, while the rest is mostly helium. The remaining 1.69% (equal to 5,600 times the mass of Earth) consists of heavier elements, including oxygen, carbon, neon and iron, among others.[15]

The Sun formed about 4.567 billion[a][16] years ago from the gravitational collapse of a region within a large molecular cloud. Most of the matter gathered in the center, while the rest flattened into an orbiting disk that would become the Solar System. The central mass became increasingly hot and dense, eventually initiating thermonuclear fusion in its core. It is thought that almost all stars form by this process. The Sun is a G-type main-sequence star (G2V) based on spectral class and it is informally designated as a yellow dwarf because its visible radiation is most intense in the yellow-green portion of the spectrum, and although it is actually white in color, from the surface of the Earth it may appear yellow because of atmospheric scattering of blue light.[17] In the spectral class label, G2 indicates its surface temperature, of approximately 5778 K (5505 °C), and V indicates that the Sun, like most stars, is a main-sequence star, and thus generates its energy by nuclear fusion of hydrogen nuclei into helium. In its core, the Sun fuses about 620 million metric tons of hydrogen each second.[18][19]
Once regarded by astronomers as a small and relatively insignificant star, the Sun is now thought to be brighter than about 85% of the stars in the Milky Way, most of which are red dwarfs.[20][21] The absolute magnitude of the Sun is +4.83; however, as the star closest to Earth, the Sun is by far the brightest object in the sky with an apparent magnitude of −26.74.[22][23] This is about 13 billion times brighter than the next brightest star, Sirius, with an apparent magnitude of −1.46. The Sun's hot corona continuously expands in space creating the solar wind, a stream of charged particles that extends to the heliopause at roughly 100 astronomical units. The bubble in the interstellar medium formed by the solar wind, the heliosphere, is the largest continuous structure in the Solar System.[24][25]
"""
