"""Four-play copy for the how-a-vote-works walkthrough."""

from __future__ import annotations

from collections.abc import Callable
from html import escape

ClaimFn = Callable[[str, str, str], str]
StackFn = Callable[[tuple[tuple[str, int, str], ...]], str]

CONTEXT_MD = "https://raw.githubusercontent.com/IlhamKassim/live-political-analysis/main/CONTEXT.md"


def _wiki_raw(title: str, section: int) -> str:
    """A single article section as wikitext.

    ``/w/api.php`` extracts are disallowed by Wikipedia's robots.txt, and a
    full ``?action=raw`` page often spends the 8k fetch cap on the infobox.
    """
    return f"https://en.wikipedia.org/wiki/{title}?action=raw&section={section}"


POLITICS_LEAD = _wiki_raw("Politics_of_Malaysia", 0)
DUN_LEAD = _wiki_raw("State_legislative_assemblies_of_Malaysia", 0)
DEWAN_NEGARA_LEAD = _wiki_raw("Dewan_Negara", 0)
DEWAN_NEGARA_MEMBERSHIP = _wiki_raw("Dewan_Negara", 1)
DEWAN_RAKYAT_LEAD = _wiki_raw("Dewan_Rakyat", 0)
DEWAN_RAKYAT_POWERS = _wiki_raw("Dewan_Rakyat", 3)
ELECTIONS_LEAD = _wiki_raw("Elections_in_Malaysia", 0)
ELECTIONS_FEDERAL = _wiki_raw("Elections_in_Malaysia", 2)
GE15_RESULT = "https://en.wikipedia.org/wiki/2022_Malaysian_general_election?action=render"
STATES_WIKI = "https://en.wikipedia.org/wiki/States_and_federal_territories_of_Malaysia?action=raw"
UNDI18_WIKI = "https://en.wikipedia.org/wiki/UNDI18?action=raw"
GE13_WIKI = "https://en.wikipedia.org/wiki/2013_Malaysian_general_election?action=raw"
GE14_WIKI = "https://en.wikipedia.org/wiki/2018_Malaysian_general_election?action=raw"
GE15_WIKI = "https://en.wikipedia.org/wiki/2022_Malaysian_general_election?action=raw"
PH_WIKI = "https://en.wikipedia.org/wiki/Pakatan_Harapan?action=raw"
PN_WIKI = "https://en.wikipedia.org/wiki/Perikatan_Nasional?action=raw"
BN_WIKI = "https://en.wikipedia.org/wiki/Barisan_Nasional?action=raw"
GPS_WIKI = "https://en.wikipedia.org/wiki/Gabungan_Parti_Sarawak?action=raw"
GRS_WIKI = "https://en.wikipedia.org/wiki/Gabungan_Rakyat_Sabah?action=raw"
CONSTITUTION_ARTICLE_62 = "https://mylaw.my/legislation/federal-constitution-1957/article-62"
CONSTITUTION_ARTICLE_66 = "https://mylaw.my/legislation/federal-constitution-1957/article-66"


def _color_style(colors: dict[str, str]) -> str:
    return ";".join(
        f"--vote-{code.lower()}:{escape(color, quote=True)}" for code, color in colors.items()
    )


def _journey_next(
    *,
    eyebrow: str,
    title: str,
    href: str,
    description: str,
    links: tuple[tuple[str, str], ...],
) -> str:
    extra_links = "".join(
        f'<a href="{escape(link_href, quote=True)}">{escape(label)} →</a>'
        for link_href, label in links
    )
    return f"""<aside class="journey-next" aria-label="{escape(eyebrow, quote=True)}">
      <div class="pk-eyebrow">{escape(eyebrow)}</div>
      <h3><a href="{escape(href, quote=True)}">{escape(title)} →</a></h3>
      <p>{escape(description)}</p>
      <div class="journey-links">{extra_links}</div>
    </aside>"""


def _speech(role: str, text: str) -> str:
    return (
        f'<figure class="bill-speech">'
        f"<figcaption>{role}</figcaption>"
        f"<blockquote><p>{text}</p></blockquote>"
        f"</figure>"
    )


def _bill_play(*, language: str, c: dict[str, str]) -> str:
    """Staged teaching Bill. Speeches are fiction. Claims sit in the coda."""
    if language == "ms":
        fiction = (
            "Ini permainan pengajaran. Rang Undang-Undang Undi Kampus bukan "
            "di hadapan dewan. Ucapan watak direka. Ia bukan rekod Hansard."
        )
        stake = (
            "Rang Undang-Undang Undi Kampus — suatu Rang Undang-Undang "
            "pengajaran — membenarkan pelajar mengundi di Kerusi tempat "
            "mereka belajar, bukan hanya Kerusi pada kad pengenalan. "
            "Kerusi ialah salah satu daripada 222 kawasan parlimen persekutuan."
        )
        path = (
            "Bacaan",
            "Perbahasan",
            "Belah bahagian",
            "Dewan Negara",
            "Agong",
            "Tamat",
        )
        minister, speaker, clerk = "Menteri", "Yang di-Pertua", "Setiausaha"
        back, opp = "Ahli kerajaan", "Ahli pembangkang"
        president, senator = "Yang di-Pertua Dewan Negara", "Senator"
        s1 = "Bacaan pertama — Dewan Rakyat"
        s2 = "Bacaan kedua — hujah kerajaan"
        s3 = "Bacaan kedua — hujah pembangkang"
        s4 = "Belah bahagian — dewan berpecah"
        s5 = "Dewan Negara"
        s6 = "Perkenan — Yang di-Pertuan Agong"
        s7 = "Rang Undang-Undang menjadi undang-undang"
        s8 = "Rang Undang-Undang gagal"
        s9 = "Ini benar-benar berlaku"
        reading = (
            _speech(
                minister,
                "Tuan Yang di-Pertua, saya membentang sebuah Rang Undang-Undang. "
                "Pelajar tinggal di suatu Kerusi selama bertahun. Ramai tidak "
                "dapat pulang pada hari mengundi. Rang ini membenarkan mereka "
                "mengundi di tempat mereka belajar.",
            )
            + _speech(
                speaker,
                "Setiausaha, bacakan tajuk Rang Undang-Undang. Tiada perbahasan "
                "pada bacaan pertama.",
            )
            + _speech(
                clerk,
                "Bacaan pertama. Rang Undang-Undang Undi Kampus. Suatu Rang "
                "Undang-Undang untuk membenarkan pelajar mengundi di Kerusi "
                "tempat mereka belajar.",
            )
        )
        gov = _speech(
            minister,
            "Orang berumur 18 tahun sudah boleh mengundi. Ramai duduk di kolej, "
            "jauh dari Kerusi pada kad mereka. Tiket bas pulang ialah cukai "
            "pada hak yang sudah ada. Sewa, bas dan klinik ada di Kerusi "
            "tempat mereka tinggal sekarang.",
        ) + _speech(
            back,
            "Kerusi ialah orang yang tinggal di situ dalam penggal ini. "
            "Bukan hanya orang yang membesar di situ.",
        )
        opposition = _speech(
            opp,
            "Kerusi ialah komuniti yang hidup dengan keputusan itu selama "
            "bertahun. Kebanyakan pelajar pergi selepas diploma. Bandar "
            "kampus akan berayun kerana orang yang tidak akan tinggal untuk "
            "longkang, klinik, atau sekolah.",
        ) + _speech(
            opp,
            "Seseorang tidak boleh mengundi dua kali. Dua alamat menjadikan "
            "itu lebih sukar dikawal. Kerusi luar bandar sudah nipis. Ini "
            "menarik pengundi muda ke beberapa bandar yang ada kampus.",
        )
        division_copy = (
            _speech(
                speaker,
                "Soalannya ialah Rang Undang-Undang dibaca kali kedua. Yang "
                "setuju, ke kanan saya. Yang tidak, ke kiri saya. Kita akan "
                "kira.",
            )
            + '<p class="bill-note">Anda menonton. Satu orang tidak memusingkan '
            "belah bahagian. Permainan ini menganggap semua 222 Ahli Parlimen "
            "mengundi dan setiap Ahli daripada Gabungan Kerajaan yang dipilih "
            "mengundi ya. Dengan 222 undi, 112 undi ya mengatasi 110 undi "
            f"tidak. {c['bill-vote-rule']} Menganggap seluruh Gabungan mengundi "
            "bersama ialah andaian whip, bukan undang-undang.</p>"
        )
        senate = (
            _speech(
                president,
                "Rang Undang-Undang kini di Dewan Negara.",
            )
            + _speech(
                senator,
                "Pilihan raya umum tidak menghantar saya pulang.",
            )
            + f'<p class="prose-claim">{c["senate-term"]}</p>'
            + f'<p class="more">{c["senate-70"]}</p>'
        )
        assent = (
            _speech(
                clerk,
                "Jika kedua-dua dewan lulus, Rang Undang-Undang pergi kepada "
                "Yang di-Pertuan Agong.",
            )
            + f'<p class="prose-claim">{c["assent"]}</p>'
            + f'<p class="more">{c["ydpa-head"]}</p>'
        )
        law = (
            "<p>Jika pihak ya mendapat sekurang-kurangnya 112 undi dalam "
            "permainan yang mengira semua 222 Ahli ini, inilah laluannya.</p>"
            "<p>Dalam permainan ini, Rang Undang-Undang Undi Kampus menjadi "
            "undang-undang. Umur mengundi sebenar negara ini tidak berubah di "
            "sini.</p>"
        )
        failed = (
            "<p>Jika pihak ya tidak mendapat 112 undi dalam permainan yang "
            "mengira semua 222 Ahli ini, inilah laluannya.</p>"
            "<p>Pihak ya tidak sampai 112 undi. Rang Undang-Undang mati di "
            "Dewan Rakyat. Peraturan kekal seperti sedia ada.</p>"
            "<p>Menteri ada tiga pilihan:</p>"
            '<ol class="bill-choices">'
            "<li>Tinggalkan Rang Undang-Undang.</li>"
            "<li>Cuba lagi, dan pujuk lebih banyak Kerusi.</li>"
            "<li>Ubah teks, kemudian cuba lagi.</li>"
            "</ol>"
        )
        coda = (
            "<p>Permainan itu fiksyen. Tulisan semula siapa boleh mengundi "
            "benar-benar berlaku.</p>"
            f'<p class="prose-claim">{c["undi18-unanimous"]} '
            "Tiada pecahan.</p>"
            f'<p class="prose-claim">{c["undi18-age"]}</p>'
            f'<p class="prose-claim">{c["undi18-avr"]}</p>'
            '<p class="more">Permainan ini menggunakan 112 kerana ia mengira '
            "semua 222 Ahli Parlimen sebagai mengundi. Pindaan perlembagaan "
            "boleh mempunyai ambang berbeza. Dua pertiga daripada 222 "
            f"Kerusi ialah 148. {c['undi18-two-thirds']}</p>"
        )
        cont = "Teruskan"
        divide = "Pecahkan dewan"
        open_fail = "Buka Rang Undang-Undang yang gagal"
        if_pass = "Lihat laluan jika 112 mengundi ya"
        yes_lab, no_lab = "Ya", "Tidak"
        pool_lab = "Dewan — 222 Kerusi"
        live0 = "Belum dikira. Tekan untuk memecahkan 222 Kerusi."
    else:
        fiction = (
            "This is a teaching play. The Campus Vote Bill is not before the "
            "house. The speeches are invented. They are not a Hansard record."
        )
        stake = (
            "The Campus Vote Bill — a teaching Bill — would let a student vote "
            "in the Seat where they study, not only the Seat on their identity "
            "card. A Seat is one of the 222 federal constituencies."
        )
        path = (
            "Reading",
            "Debate",
            "Division",
            "Dewan Negara",
            "Agong",
            "End",
        )
        minister, speaker, clerk = "The Minister", "Speaker", "Clerk"
        back, opp = "A Government backbencher", "An Opposition MP"
        president, senator = "President of the Dewan Negara", "A Senator"
        s1 = "First reading — Dewan Rakyat"
        s2 = "Second reading — the government case"
        s3 = "Second reading — the opposition case"
        s4 = "Division — the floor splits"
        s5 = "Dewan Negara"
        s6 = "Assent — Yang di-Pertuan Agong"
        s7 = "The Bill becomes law"
        s8 = "The Bill fails"
        s9 = "This really happened"
        reading = (
            _speech(
                minister,
                "Speaker, I present a Bill. Students live in a Seat for years. "
                "Many cannot get home on polling day. This Bill lets them vote "
                "where they study.",
            )
            + _speech(
                speaker,
                "Clerk, read the title of the Bill. There is no debate at first reading.",
            )
            + _speech(
                clerk,
                "First reading. The Campus Vote Bill. A Bill to let a student "
                "vote in the Seat where they study.",
            )
        )
        gov = _speech(
            minister,
            "Eighteen-year-olds can already vote. A lot of them are at college, "
            "far from the Seat on their card. A bus home is a tax on a right "
            "they already have. Rent, buses and clinics are in the Seat they "
            "live in now.",
        ) + _speech(
            back,
            "A Seat is the people who live there this term. Not only the people who grew up there.",
        )
        opposition = _speech(
            opp,
            "A Seat is a community that lives with the result for years. Most "
            "students leave after a diploma. Campus towns would swing on people "
            "who will not stay for the drain, the clinic, or the school.",
        ) + _speech(
            opp,
            "A person must not vote twice. Two addresses make that harder to "
            "police. Rural Seats are already thin. This pulls young voters into "
            "a few towns with campuses.",
        )
        division_copy = (
            _speech(
                speaker,
                "The question is that the Bill be read a second time. Those "
                "who agree, to my right. Those who do not, to my left. We "
                "will count.",
            )
            + '<p class="bill-note">You are watching. One person does not swing '
            "a Division. This play assumes all 222 MPs vote and every MP in "
            "the selected Government Coalition votes yes. With 222 votes, "
            f"112 yes votes beat 110 no votes. {c['bill-vote-rule']} Treating "
            "a whole Coalition as voting together is a whip assumption, not "
            "a law.</p>"
        )
        senate = (
            _speech(
                president,
                "The Bill is in the Dewan Negara now.",
            )
            + _speech(
                senator,
                "A general election does not send me home.",
            )
            + f'<p class="prose-claim">{c["senate-term"]}</p>'
            + f'<p class="more">{c["senate-70"]}</p>'
        )
        assent = (
            _speech(
                clerk,
                "If both houses pass the Bill, it goes to the Yang di-Pertuan Agong.",
            )
            + f'<p class="prose-claim">{c["assent"]}</p>'
            + f'<p class="more">{c["ydpa-head"]}</p>'
        )
        law = (
            "<p>If the yes side has at least 112 votes in this all-222-vote "
            "play, this is that path.</p>"
            "<p>In this play, the Campus Vote Bill is now a law. The real "
            "voting age in this country was not changed here.</p>"
        )
        failed = (
            "<p>If the yes side does not have 112 votes in this all-222-vote "
            "play, this is that path.</p>"
            "<p>The yes side did not reach 112 votes. The Bill dies in the "
            "Dewan Rakyat. The rule stays as it is.</p>"
            "<p>The Minister has three choices:</p>"
            '<ol class="bill-choices">'
            "<li>Leave the Bill.</li>"
            "<li>Try again, and persuade more Seats.</li>"
            "<li>Change the text, then try again.</li>"
            "</ol>"
        )
        coda = (
            "<p>That play was fiction. A real rewrite of who can vote did "
            "happen.</p>"
            f'<p class="prose-claim">{c["undi18-unanimous"]} '
            "There was no split.</p>"
            f'<p class="prose-claim">{c["undi18-age"]}</p>'
            f'<p class="prose-claim">{c["undi18-avr"]}</p>'
            '<p class="more">This play uses 112 because it counts all 222 MPs '
            "as voting. Constitutional amendments can have a different "
            "threshold. Two-thirds of 222 "
            f"Seats is 148. {c['undi18-two-thirds']}</p>"
        )
        cont = "Continue"
        divide = "Divide the house"
        open_fail = "Open the failed bill"
        if_pass = "See the path if 112 had voted yes"
        yes_lab, no_lab = "Yes", "No"
        pool_lab = "The house — 222 Seats"
        live0 = "Not yet counted. Press to split the 222 Seats."

    def stage(sid: str, title: str, body: str) -> str:
        on = " is-on" if sid == "reading" else ""
        return (
            f'<section class="bill-stage{on}" data-bill-stage="{sid}" tabindex="-1">'
            f"<h3>{title}</h3>{body}</section>"
        )

    floor = f"""
        <div class="div-floor" data-div-floor data-split="false" role="img" aria-labelledby="bill-div-live">
          <div class="div-pool">
            <p>{pool_lab}</p>
            <div class="sim-chamber" data-div-pool-dots></div>
          </div>
          <div class="div-yes">
            <p>{yes_lab} <span data-div-yes-n>0</span></p>
            <div class="sim-chamber" data-div-yes-dots></div>
          </div>
          <div class="div-mark" aria-hidden="true"><span>112</span></div>
          <div class="div-no">
            <p>{no_lab} <span data-div-no-n>0</span></p>
            <div class="sim-chamber" data-div-no-dots></div>
          </div>
        </div>
        <p class="div-live" id="bill-div-live" data-div-live aria-live="polite">{live0}</p>
    """
    return f"""
    <div class="bill-play" id="vote-bill">
      <p class="caveat">{fiction}</p>
      <p class="more">{stake}</p>
      <ol class="bill-path" aria-label="Bill path">
        <li data-bill-chip="reading" data-on="true" aria-current="step">{path[0]}</li>
        <li data-bill-chip="debate" data-on="false">{path[1]}</li>
        <li data-bill-chip="division" data-on="false">{path[2]}</li>
        <li data-bill-chip="senate" data-on="false">{path[3]}</li>
        <li data-bill-chip="assent" data-on="false">{path[4]}</li>
        <li data-bill-chip="end" data-on="false">{path[5]}</li>
      </ol>
      <div class="bill-window">
        {stage("reading", s1, reading)}
        {stage("gov", s2, gov)}
        {stage("opp", s3, opposition)}
        {stage("division", s4, division_copy + floor)}
        {stage("senate", s5, senate)}
        {stage("assent", s6, assent)}
        {stage("law", s7, law)}
        {stage("failed", s8, failed)}
        {stage("coda", s9, coda)}
        <div class="bill-dock">
          <button type="button" class="bill-continue" data-bill-next data-label-continue="{cont}" data-label-divide="{divide}">{cont}</button>
          <button type="button" class="bill-alt" data-bill-fail hidden>{open_fail}</button>
          <button type="button" class="bill-alt" data-bill-if-pass hidden>{if_pass}</button>
        </div>
      </div>
    </div>
    """.strip()


def _ge15_bar(stack_bar: StackFn, colors: dict[str, str]) -> str:
    return stack_bar(
        (
            ("PH", 82, colors["PH"]),
            ("PN", 74, colors["PN"]),
            ("BN", 30, colors["BN"]),
            ("GPS", 23, colors["GPS"]),
            ("GRS", 6, colors["GRS"]),
            ("Others", 7, colors["OTHER"]),
        )
    )


def body_en(claim: ClaimFn, stack_bar: StackFn, colors: dict[str, str]) -> str:
    c = {
        "seat-unit": claim(
            "claim-seat-unit",
            CONTEXT_MD,
            "A Seat is one of the 222 parliamentary constituencies in the "
            "Dewan Rakyat — the unit an election is actually won or lost in.",
        ),
        "seat-222": claim("claim-222", CONTEXT_MD, "The Dewan Rakyat has 222 Seats."),
        "street": claim(
            "claim-street-in-seat",
            CONTEXT_MD,
            "A Malaysian postcode maps to every Seat it could fall in, and a "
            "postcode can straddle two Seats.",
        ),
        "dun": claim(
            "claim-dun-is-state-assembly",
            DUN_LEAD,
            "In Malaysia, a state legislative assembly, officially Dewan "
            "Undangan Negeri (DUN), is the legislative branch of the state "
            "governments in each of the 13 Malaysian states.",
        ),
        "two-rolls": claim(
            "claim-two-rolls",
            ELECTIONS_LEAD,
            "Federal level elections are those for membership in the Dewan "
            "Rakyat, the lower house of Parliament, while state level "
            "elections are for membership in the various State Legislative "
            "Assemblies.",
        ),
        "ft-names": claim(
            "claim-ft-names",
            STATES_WIKI,
            "The three federal territories—Kuala Lumpur, Labuan and "
            "Putrajaya—were created later from land separated from existing "
            "states.",
        ),
        "ft-direct": claim(
            "claim-ft-direct",
            STATES_WIKI,
            "The federal territories are directly governed by the federal government.",
        ),
        "fptp": claim(
            "claim-fptp",
            DEWAN_RAKYAT_LEAD,
            "The Dewan Rakyat is a directly elected body consisting of 222 "
            "members known as Members of Parliament (MPs). Members are "
            "elected by first-past-the-post voting with one member from "
            "each federal constituency.",
        ),
        "westminster": claim(
            "claim-westminster",
            POLITICS_LEAD,
            "The system of government is based on the Westminster system.",
        ),
        "majority": claim(
            "claim-majority",
            CONTEXT_MD,
            "A Majority means holding more than half of the 222 seats (112+).",
        ),
        "coalitions": claim(
            "claim-coalitions",
            CONTEXT_MD,
            "The five Coalitions this site tracks are PH, BN, PN, GPS and GRS.",
        ),
        "hung": claim(
            "claim-hung-ge15",
            GE15_RESULT,
            "The elections resulted in a hung parliament, the first federal "
            "election to have had such a result in the nation's history.",
        ),
        "ge13-bn": claim(
            "claim-ge13-bn-133",
            GE13_WIKI,
            "Barisan Nasional won 133 seats in the 2013 general election.",
        ),
        "ge13-pr": claim(
            "claim-ge13-pr-89",
            GE13_WIKI,
            "Pakatan Rakyat won 89 of the 222 seats.",
        ),
        "ge14-ph": claim(
            "claim-ge14-ph-113",
            GE14_WIKI,
            "Pakatan Harapan won 113 seats in the 2018 general election.",
        ),
        "ge14-bn": claim(
            "claim-ge14-bn-79",
            GE14_WIKI,
            "Barisan Nasional won 79 seats in the 2018 general election.",
        ),
        "ge15-ph": claim(
            "claim-ge15-ph-82",
            GE15_WIKI,
            "Pakatan Harapan won 82 seats in the 2022 general election, a "
            "figure that includes MUDA.",
        ),
        "ge15-pn": claim(
            "claim-ge15-pn-74",
            GE15_WIKI,
            "Perikatan Nasional won 74 seats in the 2022 general election.",
        ),
        "ge15-bn": claim(
            "claim-ge15-bn-30",
            GE15_WIKI,
            "Barisan Nasional won 30 seats in the 2022 general election.",
        ),
        "ge15-gps": claim(
            "claim-ge15-gps-23",
            GE15_WIKI,
            "Gabungan Parti Sarawak won 23 seats in the 2022 general election.",
        ),
        "ge15-grs": claim(
            "claim-ge15-grs-6",
            GE15_WIKI,
            "Gabungan Rakyat Sabah won 6 seats in the 2022 general election.",
        ),
        "ph-founded": claim(
            "claim-ph-founded",
            PH_WIKI,
            "Pakatan Harapan was founded on 22 September 2015.",
        ),
        "gps-founded": claim(
            "claim-gps-founded",
            GPS_WIKI,
            "Gabungan Parti Sarawak was founded on 12 June 2018.",
        ),
        "pn-founded": claim(
            "claim-pn-founded",
            PN_WIKI,
            "Perikatan Nasional was founded on 29 February 2020.",
        ),
        "grs-founded": claim(
            "claim-grs-founded",
            GRS_WIKI,
            "Gabungan Rakyat Sabah was established in September 2020, when "
            "Hajiji Noor set up an informal alliance of that name.",
        ),
        "bill": claim(
            "claim-bill",
            CONTEXT_MD,
            "A Bill is a piece of legislation before the Dewan Rakyat.",
        ),
        "division": claim(
            "claim-division",
            CONTEXT_MD,
            "A Division is a counted vote in the Dewan Rakyat, in which "
            "Hansard names every Member as agreeing, disagreeing, abstaining "
            "or absent.",
        ),
        "bill-vote-rule": claim(
            "claim-bill-vote-rule",
            CONSTITUTION_ARTICLE_62,
            "Except where the Federal Constitution provides otherwise, each "
            "House decides by a simple majority of Members voting, and absent "
            "Members cannot vote.",
        ),
        "assent": claim(
            "claim-royal-assent",
            CONSTITUTION_ARTICLE_66,
            "The Yang di-Pertuan Agong has 30 days to assent to a Bill. If "
            "it is not assented to within that period, it becomes law as if "
            "assent had been given.",
        ),
        "senate-70": claim(
            "claim-senate-70",
            DEWAN_NEGARA_LEAD,
            "The Dewan Negara is the upper house of the Parliament of "
            "Malaysia, consisting of 70 senators of whom 26 are elected by "
            "the state legislative assemblies, with two senators for each "
            "state, while the other 44 are appointed by the Yang di-Pertuan "
            "Agong, including four who are appointed to represent the "
            "federal territories.",
        ),
        "senate-term": claim(
            "claim-senate-undissolved",
            DEWAN_NEGARA_MEMBERSHIP,
            "The Dewan Negara is not affected by the elections for the "
            "Dewan Rakyat, and senators continue to hold office despite the "
            "Dewan Rakyat's dissolution for an election.",
        ),
        "ydpa-head": claim(
            "claim-ydpa-head",
            POLITICS_LEAD,
            "The Yang di-Pertuan Agong is head of state and the Prime "
            "Minister of Malaysia is the head of government.",
        ),
        "pm-practice": claim(
            "claim-pm-practice",
            DEWAN_RAKYAT_POWERS,
            "If the Prime Minister loses the confidence of the Dewan Rakyat, "
            "whether by losing a no-confidence vote or failing to pass a "
            "budget, he must either advise the King to dissolve Parliament "
            "and hold a general election or submit his resignation to the "
            "King.",
        ),
        "undi18-two-thirds": claim(
            "claim-undi18-two-thirds",
            ELECTIONS_FEDERAL,
            "A two-thirds majority is the majority required to pass most "
            "constitutional amendments.",
        ),
        "undi18-unanimous": claim(
            "claim-undi18-unanimous",
            UNDI18_WIKI,
            "On 16 July 2019, the Constitution (Amendment) Bill 2019 was "
            "passed unanimously by all present members of the Dewan Rakyat.",
        ),
        "undi18-age": claim(
            "claim-undi18-age",
            UNDI18_WIKI,
            "The Constitution (Amendment) Act 2019 changed the minimum age "
            "for voting from 21 years old to 18 years old.",
        ),
        "undi18-avr": claim(
            "claim-undi18-avr",
            UNDI18_WIKI,
            "The Constitution (Amendment) Bill 2019 included provisions "
            "relating to automatic voter registration for all Malaysian "
            "citizens.",
        ),
        "ph-position": claim(
            "claim-ph-position",
            PH_WIKI,
            "Pakatan Harapan's political position is centre to centre-left.",
        ),
        "bn-position": claim(
            "claim-bn-position",
            BN_WIKI,
            "Barisan Nasional's political position is centre-right to right-wing.",
        ),
        "pn-position": claim(
            "claim-pn-position",
            PN_WIKI,
            "Perikatan Nasional's political position is right-wing to far-right.",
        ),
        "gps-position": claim(
            "claim-gps-position",
            GPS_WIKI,
            "Gabungan Parti Sarawak's political position is centre-right to right-wing.",
        ),
        "gps-sarawak": claim(
            "claim-gps-sarawak",
            GPS_WIKI,
            "Gabungan Parti Sarawak is a Sarawak-based political alliance in Malaysia.",
        ),
        "grs-position": claim(
            "claim-grs-position",
            GRS_WIKI,
            "Gabungan Rakyat Sabah's political position is centre to centre-right.",
        ),
        "grs-sabah": claim(
            "claim-grs-sabah",
            GRS_WIKI,
            "Gabungan Rakyat Sabah is a Malaysian coalition of Sabah-based parties.",
        ),
    }
    bar = _ge15_bar(stack_bar, colors)
    color_style = _color_style(colors)
    place_next = _journey_next(
        eyebrow="Next on PolitikKu",
        title="Find your Seat",
        href="/#find",
        description="Enter your postcode, or browse all 222 Seats on the map.",
        links=(("/app/", "Explore the Seat map"),),
    )
    seat_next = _journey_next(
        eyebrow="From one Seat to the national count",
        title="Meet the Coalitions",
        href="/learn/coalitions.html",
        description="See how PH, BN, PN, GPS and GRS fit into the Seat count.",
        links=(("/learn/glossary.html#term-seat", "Read the Seat definition"),),
    )
    majority_next = _journey_next(
        eyebrow="From the teaching house to the current estimate",
        title="Read the GE16 Projection",
        href="/projection/",
        description="See the Seat Calls behind the projected Majority and the model caveat beside them.",
        links=(("/learn/glossary.html#term-majority", "Read the Majority definition"),),
    )
    bill_next = _journey_next(
        eyebrow="From the teaching Bill to the public record",
        title="Follow current Bills",
        href="/bills/",
        description="Read each Bill's current parliamentary stage and its source.",
        links=(
            ("/dewan/", "Explore Dewan Rakyat activity"),
            ("/learn/ge16-process.html", "See the GE16 process"),
        ),
    )
    return f"""
<div class="pk-scroll" style="{color_style}">
  <section class="scene" id="open">
    <div class="pk-eyebrow">Four short plays</div>
    <h1>Where does a vote go?</h1>
    <p class="line">Into a Seat. Then a Majority. Then a Bill.</p>
    <nav class="act-nav" aria-label="Plays">
      <a href="#play-1">1 · Place</a>
      <a href="#play-2">2 · Seat</a>
      <a href="#play-3">3 · Majority</a>
      <a href="#play-4">4 · Bill</a>
      <a href="#play-compass">Compass</a>
    </nav>
  </section>
  <section class="scene" id="play-1">
    <div class="pk-eyebrow">01 · Your place</div>
    <h2>One street. One federal Seat.</h2>
    <p class="prose-claim">{c["seat-unit"]} {c["seat-222"]} {c["street"]}</p>
    <div class="split">
      <article class="split-card">
        <div class="tag">Federal</div>
        <h3>Seat</h3>
        <p>You choose an MP for the Dewan Rakyat.</p>
      </article>
      <article class="split-card">
        <div class="tag">State</div>
        <h3>DUN</h3>
        <p>If you live in a state, you also choose an ADUN. {c["dun"]}</p>
      </article>
    </div>
    <p class="caveat">
      <strong>The exclusion.</strong>
      {c["ft-names"]} {c["ft-direct"]}
    </p>
    <details class="why-tap">
      <summary>Why two rolls</summary>
      <p>{c["two-rolls"]}</p>
    </details>
    {place_next}
  </section>

  <section class="scene" id="play-2">
    <div class="pk-eyebrow">02 · Win one Seat</div>
    <h2>Most votes in this Seat win it.</h2>
    <p class="prose-claim">{c["fptp"]}</p>
    <div class="race" id="vote-race">
      <p class="more">This Seat is made up. Tap who wins.</p>
      <div class="race-picks">
        <button type="button" data-race="amina" aria-pressed="false">Amina · 4,200</button>
        <button type="button" data-race="rizal" aria-pressed="false">Rizal · 5,100</button>
        <button type="button" data-race="siti" aria-pressed="false">Siti · 3,900</button>
      </div>
      <p class="sim-status" data-race-result data-state="warn">Three people. One Seat. Tap a name.</p>
    </div>
    <details class="why-tap">
      <summary>Why this count</summary>
      <p>{c["westminster"]} Government is built from Seats, not from adding every vote nationwide.</p>
    </details>
    {seat_next}
  </section>

  <section class="scene" id="play-3">
    <div class="pk-eyebrow">03 · Build a Majority</div>
    <h2>Can you make 112?</h2>
    <p class="prose-claim">{c["majority"]} {c["coalitions"]} {c["hung"]}</p>
    <div class="vote-sim" id="vote-sim">
      <p class="more">This is a teaching house, not today’s Dewan Rakyat. Tick who sits in government. Try another year.</p>
      <div class="sim-presets">
        <button type="button" data-sim-year="ge15" aria-pressed="true">2022 · GE15</button>
        <button type="button" data-sim-year="ge14" aria-pressed="false">2018 · GE14</button>
        <button type="button" data-sim-year="ge13" aria-pressed="false">2013 · GE13</button>
      </div>
      <div class="sim-rows">
        <label class="sim-choice" data-sim-row="PH">
          <b>PH</b><span data-sim-count="PH">82</span>
          <span class="sim-gov"><input data-sim-gov="PH" type="checkbox"> In government</span>
          <input data-sim-seats="PH" type="hidden" value="82">
        </label>
        <label class="sim-choice" data-sim-row="PN">
          <b>PN</b><span data-sim-count="PN">74</span>
          <span class="sim-gov"><input data-sim-gov="PN" type="checkbox"> In government</span>
          <input data-sim-seats="PN" type="hidden" value="74">
        </label>
        <label class="sim-choice" data-sim-row="BN">
          <b>BN</b><span data-sim-count="BN">30</span>
          <span class="sim-gov"><input data-sim-gov="BN" type="checkbox"> In government</span>
          <input data-sim-seats="BN" type="hidden" value="30">
        </label>
        <label class="sim-choice" data-sim-row="GPS">
          <b>GPS</b><span data-sim-count="GPS">23</span>
          <span class="sim-gov"><input data-sim-gov="GPS" type="checkbox"> In government</span>
          <input data-sim-seats="GPS" type="hidden" value="23">
        </label>
        <label class="sim-choice" data-sim-row="GRS">
          <b>GRS</b><span data-sim-count="GRS">6</span>
          <span class="sim-gov"><input data-sim-gov="GRS" type="checkbox"> In government</span>
          <input data-sim-seats="GRS" type="hidden" value="6">
        </label>
        <label class="sim-choice" data-sim-row="OTHER">
          <b data-sim-other-name>Others</b><span data-sim-count="OTHER">7</span>
          <span class="sim-gov"><input data-sim-gov="OTHER" type="checkbox"> In government</span>
          <input data-sim-seats="OTHER" type="hidden" value="7">
        </label>
      </div>
      <p class="sim-status" data-sim-status data-state="hung">Tick Coalitions until you hold 112.</p>
      <div data-sim-stack>{bar}</div>
      <div class="sim-chamber" data-sim-chamber aria-hidden="true"></div>
    </div>
    <details class="why-tap">
      <summary>The numbers on each year</summary>
      <p>{c["ge15-ph"]} {c["ge15-pn"]} {c["ge15-bn"]} {c["ge15-gps"]} {c["ge15-grs"]}</p>
      <p>{c["ge14-ph"]} {c["ge14-bn"]}</p>
      <p>{c["ge13-bn"]} {c["ge13-pr"]}</p>
      <p>{c["ph-founded"]} {c["gps-founded"]} {c["pn-founded"]} {c["grs-founded"]}</p>
    </details>
    {majority_next}
  </section>

  <section class="scene" id="play-4">
    <div class="pk-eyebrow">04 · Pass one Bill</div>
    <h2>Walk one Bill out.</h2>
    {_bill_play(language="en", c=c)}
    <details class="why-tap">
      <summary>More info</summary>
      <p>{c["bill"]}</p>
      <p>{c["division"]}</p>
      <p>{c["pm-practice"]}</p>
    </details>
    <p class="finish">
      What GE16 projects on this site is the next Dewan Rakyat — 222 Seats,
      and whether a Coalition holds a Majority.
    </p>
    {bill_next}
  </section>

  <section class="scene" id="play-compass">
    <div class="pk-eyebrow">Optional</div>
    <h2>A political compass</h2>
    <p class="caveat">
      This is a teaching sketch, not a scientific score. Wikipedia does not
      publish x and y numbers. A click is your mark only. This page will not
      name a Coalition for you.
    </p>
    <div class="compass-panel">
      <div class="compass-board" id="vote-compass" role="img" aria-label="Political compass teaching sketch">
        <span class="compass-label top">Peninsula</span>
        <span class="compass-label bottom">East Malaysia</span>
        <span class="compass-label left">Left</span>
        <span class="compass-label right">Right</span>
        <span class="compass-dot" data-c="PH" title="PH">PH</span>
        <span class="compass-dot" data-c="BN" title="BN">BN</span>
        <span class="compass-dot" data-c="PN" title="PN">PN</span>
        <span class="compass-dot" data-c="GPS" title="GPS">GPS</span>
        <span class="compass-dot" data-c="GRS" title="GRS">GRS</span>
        <span class="compass-you" id="vote-compass-you" hidden>You</span>
      </div>
      <div class="compass-tools">
        <label>Left to right
          <input id="vote-compass-x" type="range" min="2" max="98" value="50">
        </label>
        <label>Peninsula to East Malaysia
          <input id="vote-compass-y" type="range" min="2" max="98" value="50">
        </label>
        <p class="more" id="vote-compass-note">Place a mark if you want one.</p>
      </div>
      <div class="compass-legend prose-claim">
        {c["ph-position"]} {c["bn-position"]} {c["pn-position"]}
        {c["gps-position"]} {c["gps-sarawak"]} {c["grs-position"]} {c["grs-sabah"]}
      </div>
    </div>
  </section>
</div>
""".strip()


def body_ms(claim: ClaimFn, stack_bar: StackFn, colors: dict[str, str]) -> str:
    c = {
        "seat-unit": claim(
            "claim-seat-unit",
            CONTEXT_MD,
            "Kerusi ialah unit yang dimenangi atau kalah dalam pilihan raya.",
        ),
        "seat-222": claim(
            "claim-222",
            CONTEXT_MD,
            "Dewan Rakyat mempunyai 222 Kerusi.",
        ),
        "street": claim(
            "claim-street-in-seat",
            CONTEXT_MD,
            "Poskod Malaysia dipetakan kepada setiap Kerusi yang mungkin termasukinya, dan satu poskod boleh merentasi dua Kerusi.",
        ),
        "dun": claim(
            "claim-dun-is-state-assembly",
            DUN_LEAD,
            "Di Malaysia, dewan undangan negeri, rasminya Dewan Undangan "
            "Negeri (DUN), ialah cabang perundangan kerajaan negeri di "
            "setiap 13 negeri Malaysia.",
        ),
        "two-rolls": claim(
            "claim-two-rolls",
            ELECTIONS_LEAD,
            "Pilihan raya peringkat persekutuan ialah untuk keahlian Dewan "
            "Rakyat, dewan rendah Parlimen, manakala pilihan raya peringkat "
            "negeri ialah untuk keahlian Dewan Undangan Negeri.",
        ),
        "ft-names": claim(
            "claim-ft-names",
            STATES_WIKI,
            "Tiga wilayah persekutuan—Kuala Lumpur, Labuan dan Putrajaya—dicipta kemudian daripada tanah yang dipisahkan daripada negeri sedia ada.",
        ),
        "ft-direct": claim(
            "claim-ft-direct",
            STATES_WIKI,
            "Wilayah persekutuan ditadbir secara langsung oleh kerajaan persekutuan.",
        ),
        "fptp": claim(
            "claim-fptp",
            DEWAN_RAKYAT_LEAD,
            "Dewan Rakyat ialah badan yang dipilih secara langsung, terdiri "
            "daripada 222 ahli yang dikenali sebagai Ahli Parlimen. Ahli "
            "dipilih melalui undian first-past-the-post dengan seorang ahli "
            "daripada setiap kawasan persekutuan.",
        ),
        "westminster": claim(
            "claim-westminster",
            POLITICS_LEAD,
            "Sistem kerajaan berasaskan sistem Westminster.",
        ),
        "majority": claim(
            "claim-majority",
            CONTEXT_MD,
            "Majoriti bermaksud memegang lebih daripada separuh daripada 222 kerusi (112+).",
        ),
        "coalitions": claim(
            "claim-coalitions",
            CONTEXT_MD,
            "Lima Gabungan yang dijejaki laman ini ialah PH, BN, PN, GPS dan GRS.",
        ),
        "hung": claim(
            "claim-hung-ge15",
            GE15_RESULT,
            "Pilihan raya itu menghasilkan parlimen tergantung, pilihan raya "
            "persekutuan pertama dengan keputusan begitu dalam sejarah negara.",
        ),
        "ge13-bn": claim(
            "claim-ge13-bn-133",
            GE13_WIKI,
            "Barisan Nasional memenangi 133 kerusi dalam pilihan raya umum 2013.",
        ),
        "ge13-pr": claim(
            "claim-ge13-pr-89",
            GE13_WIKI,
            "Pakatan Rakyat memenangi 89 daripada 222 kerusi.",
        ),
        "ge14-ph": claim(
            "claim-ge14-ph-113",
            GE14_WIKI,
            "Pakatan Harapan memenangi 113 kerusi dalam pilihan raya umum 2018.",
        ),
        "ge14-bn": claim(
            "claim-ge14-bn-79",
            GE14_WIKI,
            "Barisan Nasional memenangi 79 kerusi dalam pilihan raya umum 2018.",
        ),
        "ge15-ph": claim(
            "claim-ge15-ph-82",
            GE15_WIKI,
            "Pakatan Harapan memenangi 82 kerusi dalam pilihan raya umum 2022, angka yang merangkumi MUDA.",
        ),
        "ge15-pn": claim(
            "claim-ge15-pn-74",
            GE15_WIKI,
            "Perikatan Nasional memenangi 74 kerusi dalam pilihan raya umum 2022.",
        ),
        "ge15-bn": claim(
            "claim-ge15-bn-30",
            GE15_WIKI,
            "Barisan Nasional memenangi 30 kerusi dalam pilihan raya umum 2022.",
        ),
        "ge15-gps": claim(
            "claim-ge15-gps-23",
            GE15_WIKI,
            "Gabungan Parti Sarawak memenangi 23 kerusi dalam pilihan raya umum 2022.",
        ),
        "ge15-grs": claim(
            "claim-ge15-grs-6",
            GE15_WIKI,
            "Gabungan Rakyat Sabah memenangi 6 kerusi dalam pilihan raya umum 2022.",
        ),
        "ph-founded": claim(
            "claim-ph-founded",
            PH_WIKI,
            "Pakatan Harapan ditubuhkan pada 22 September 2015.",
        ),
        "gps-founded": claim(
            "claim-gps-founded",
            GPS_WIKI,
            "Gabungan Parti Sarawak ditubuhkan pada 12 Jun 2018.",
        ),
        "pn-founded": claim(
            "claim-pn-founded",
            PN_WIKI,
            "Perikatan Nasional ditubuhkan pada 29 Februari 2020.",
        ),
        "grs-founded": claim(
            "claim-grs-founded",
            GRS_WIKI,
            "Gabungan Rakyat Sabah ditubuhkan pada September 2020, apabila Hajiji Noor menubuhkan pakatan tidak rasmi dengan nama itu.",
        ),
        "bill": claim(
            "claim-bill",
            CONTEXT_MD,
            "Rang Undang-Undang ialah suatu undang-undang yang dibawa ke Dewan Rakyat.",
        ),
        "division": claim(
            "claim-division",
            CONTEXT_MD,
            "Belah bahagian ialah undian yang dikira di Dewan Rakyat, di mana Hansard menamakan setiap Ahli sebagai setuju, tidak setuju, berkecuali atau tidak hadir.",
        ),
        "bill-vote-rule": claim(
            "claim-bill-vote-rule",
            CONSTITUTION_ARTICLE_62,
            "Kecuali jika Perlembagaan Persekutuan memperuntukkan selainnya, "
            "setiap Dewan membuat keputusan dengan majoriti mudah Ahli yang "
            "mengundi, dan Ahli yang tidak hadir tidak boleh mengundi.",
        ),
        "assent": claim(
            "claim-royal-assent",
            CONSTITUTION_ARTICLE_66,
            "Yang di-Pertuan Agong mempunyai 30 hari untuk memperkenankan "
            "sesuatu Rang Undang-Undang. Jika ia tidak diperkenankan dalam "
            "tempoh itu, ia menjadi undang-undang seolah-olah perkenan telah "
            "diberikan.",
        ),
        "senate-70": claim(
            "claim-senate-70",
            DEWAN_NEGARA_LEAD,
            "Dewan Negara ialah dewan atasan Parlimen Malaysia, terdiri "
            "daripada 70 senator; 26 dipilih oleh dewan undangan negeri, dua "
            "senator bagi setiap negeri, manakala 44 yang lain dilantik oleh "
            "Yang di-Pertuan Agong, termasuk empat yang mewakili wilayah "
            "persekutuan.",
        ),
        "senate-term": claim(
            "claim-senate-undissolved",
            DEWAN_NEGARA_MEMBERSHIP,
            "Dewan Negara tidak terjejas oleh pilihan raya Dewan Rakyat, dan "
            "senator terus memegang jawatan walaupun Dewan Rakyat dibubarkan "
            "untuk suatu pilihan raya.",
        ),
        "ydpa-head": claim(
            "claim-ydpa-head",
            POLITICS_LEAD,
            "Yang di-Pertuan Agong ialah ketua negara dan Perdana Menteri Malaysia ialah ketua kerajaan.",
        ),
        "pm-practice": claim(
            "claim-pm-practice",
            DEWAN_RAKYAT_POWERS,
            "Jika Perdana Menteri hilang kepercayaan Dewan Rakyat, sama ada "
            "kerana kalah undian tidak percaya atau gagal meluluskan belanjawan, "
            "beliau mesti menasihati Raja untuk membubarkan Parlimen dan "
            "mengadakan pilihan raya umum atau menyerahkan peletakan jawatan "
            "kepada Raja.",
        ),
        "undi18-two-thirds": claim(
            "claim-undi18-two-thirds",
            ELECTIONS_FEDERAL,
            "Majoriti dua pertiga ialah majoriti yang diperlukan untuk "
            "meluluskan kebanyakan pindaan perlembagaan.",
        ),
        "undi18-unanimous": claim(
            "claim-undi18-unanimous",
            UNDI18_WIKI,
            "Pada 16 Julai 2019, Rang Undang-Undang Pindaan Perlembagaan 2019 "
            "diluluskan sebulat suara oleh semua ahli Dewan Rakyat yang hadir.",
        ),
        "undi18-age": claim(
            "claim-undi18-age",
            UNDI18_WIKI,
            "Akta Pindaan Perlembagaan 2019 menukar umur minimum mengundi "
            "daripada 21 tahun kepada 18 tahun.",
        ),
        "undi18-avr": claim(
            "claim-undi18-avr",
            UNDI18_WIKI,
            "Rang Undang-Undang Pindaan Perlembagaan 2019 merangkumi peruntukan "
            "berkaitan pendaftaran pengundi automatik bagi semua warganegara "
            "Malaysia.",
        ),
        "ph-position": claim(
            "claim-ph-position",
            PH_WIKI,
            "Kedudukan politik Pakatan Harapan ialah tengah hingga tengah kiri.",
        ),
        "bn-position": claim(
            "claim-bn-position",
            BN_WIKI,
            "Kedudukan politik Barisan Nasional ialah tengah kanan hingga sayap kanan.",
        ),
        "pn-position": claim(
            "claim-pn-position",
            PN_WIKI,
            "Kedudukan politik Perikatan Nasional ialah sayap kanan hingga jauh kanan.",
        ),
        "gps-position": claim(
            "claim-gps-position",
            GPS_WIKI,
            "Kedudukan politik Gabungan Parti Sarawak ialah tengah kanan hingga sayap kanan.",
        ),
        "gps-sarawak": claim(
            "claim-gps-sarawak",
            GPS_WIKI,
            "Gabungan Parti Sarawak ialah pakatan politik berasaskan Sarawak di Malaysia.",
        ),
        "grs-position": claim(
            "claim-grs-position",
            GRS_WIKI,
            "Kedudukan politik Gabungan Rakyat Sabah ialah tengah hingga tengah kanan.",
        ),
        "grs-sabah": claim(
            "claim-grs-sabah",
            GRS_WIKI,
            "Gabungan Rakyat Sabah ialah gabungan Malaysia yang terdiri daripada parti berasaskan Sabah.",
        ),
    }
    bar = _ge15_bar(stack_bar, colors)
    color_style = _color_style(colors)
    place_next = _journey_next(
        eyebrow="Seterusnya di PolitikKu",
        title="Cari Kerusi anda",
        href="/ms/#find",
        description="Masukkan poskod anda, atau teroka kesemua 222 Kerusi pada peta.",
        links=(("/app/", "Teroka peta Kerusi"),),
    )
    seat_next = _journey_next(
        eyebrow="Daripada satu Kerusi kepada kiraan negara",
        title="Kenali Gabungan",
        href="/ms/learn/coalitions.html",
        description="Lihat bagaimana PH, BN, PN, GPS dan GRS termasuk dalam kiraan Kerusi.",
        links=(("/ms/learn/glossary.html#term-seat", "Baca takrif Kerusi"),),
    )
    majority_next = _journey_next(
        eyebrow="Daripada dewan pengajaran kepada anggaran semasa",
        title="Baca Unjuran PRU16",
        href="/ms/projection/",
        description="Lihat Keputusan Kerusi di sebalik Majoriti yang diunjurkan dan batas model di sisinya.",
        links=(("/ms/learn/glossary.html#term-majority", "Baca takrif Majoriti"),),
    )
    bill_next = _journey_next(
        eyebrow="Daripada Rang Undang-Undang pengajaran kepada rekod awam",
        title="Ikuti Rang Undang-Undang semasa",
        href="/bills/",
        description="Baca peringkat semasa setiap Rang Undang-Undang dan sumbernya.",
        links=(
            ("/dewan/", "Teroka aktiviti Dewan Rakyat"),
            ("/ms/learn/ge16-process.html", "Lihat proses PRU16"),
        ),
    )
    return f"""
<div class="pk-scroll" style="{color_style}">
  <section class="scene" id="open">
    <div class="pk-eyebrow">Empat permainan pendek</div>
    <h1>Ke mana undi pergi?</h1>
    <p class="line">Ke suatu Kerusi. Kemudian suatu Majoriti. Kemudian suatu Rang Undang-Undang.</p>
    <nav class="act-nav" aria-label="Permainan">
      <a href="#play-1">1 · Tempat</a>
      <a href="#play-2">2 · Kerusi</a>
      <a href="#play-3">3 · Majoriti</a>
      <a href="#play-4">4 · Rang undang-undang</a>
      <a href="#play-compass">Kompas</a>
    </nav>
  </section>
  <section class="scene" id="play-1">
    <div class="pk-eyebrow">01 · Tempat anda</div>
    <h2>Satu jalan. Satu Kerusi persekutuan.</h2>
    <p class="prose-claim">{c["seat-unit"]} {c["seat-222"]} {c["street"]}</p>
    <div class="split">
      <article class="split-card">
        <div class="tag">Persekutuan</div>
        <h3>Kerusi</h3>
        <p>Anda memilih Ahli Parlimen untuk Dewan Rakyat.</p>
      </article>
      <article class="split-card">
        <div class="tag">Negeri</div>
        <h3>DUN</h3>
        <p>Jika anda tinggal di sebuah negeri, anda juga memilih ADUN. {c["dun"]}</p>
      </article>
    </div>
    <p class="caveat">
      <strong>Pengecualian.</strong>
      {c["ft-names"]} {c["ft-direct"]}
    </p>
    <details class="why-tap">
      <summary>Mengapa dua daftar</summary>
      <p>{c["two-rolls"]}</p>
    </details>
    {place_next}
  </section>

  <section class="scene" id="play-2">
    <div class="pk-eyebrow">02 · Menang satu Kerusi</div>
    <h2>Undi terbanyak dalam Kerusi ini memenanginya.</h2>
    <p class="prose-claim">{c["fptp"]}</p>
    <div class="race" id="vote-race">
      <p class="more">Kerusi ini dibuat-buat. Ketik siapa menang.</p>
      <div class="race-picks">
        <button type="button" data-race="amina" aria-pressed="false">Amina · 4,200</button>
        <button type="button" data-race="rizal" aria-pressed="false">Rizal · 5,100</button>
        <button type="button" data-race="siti" aria-pressed="false">Siti · 3,900</button>
      </div>
      <p class="sim-status" data-race-result data-state="warn">Tiga orang. Satu Kerusi. Ketik satu nama.</p>
    </div>
    <details class="why-tap">
      <summary>Mengapa kiraan ini</summary>
      <p>{c["westminster"]} Kerajaan dibina daripada Kerusi, bukan daripada jumlah setiap undi di seluruh negara.</p>
    </details>
    {seat_next}
  </section>

  <section class="scene" id="play-3">
    <div class="pk-eyebrow">03 · Bina Majoriti</div>
    <h2>Bolehkah anda buat 112?</h2>
    <p class="prose-claim">{c["majority"]} {c["coalitions"]} {c["hung"]}</p>
    <div class="vote-sim" id="vote-sim">
      <p class="more">Ini dewan pengajaran, bukan Dewan Rakyat hari ini. Tanda siapa duduk dalam kerajaan. Cuba tahun lain.</p>
      <div class="sim-presets">
        <button type="button" data-sim-year="ge15" aria-pressed="true">2022 · PRU15</button>
        <button type="button" data-sim-year="ge14" aria-pressed="false">2018 · PRU14</button>
        <button type="button" data-sim-year="ge13" aria-pressed="false">2013 · PRU13</button>
      </div>
      <div class="sim-rows">
        <label class="sim-choice" data-sim-row="PH">
          <b>PH</b><span data-sim-count="PH">82</span>
          <span class="sim-gov"><input data-sim-gov="PH" type="checkbox"> Dalam kerajaan</span>
          <input data-sim-seats="PH" type="hidden" value="82">
        </label>
        <label class="sim-choice" data-sim-row="PN">
          <b>PN</b><span data-sim-count="PN">74</span>
          <span class="sim-gov"><input data-sim-gov="PN" type="checkbox"> Dalam kerajaan</span>
          <input data-sim-seats="PN" type="hidden" value="74">
        </label>
        <label class="sim-choice" data-sim-row="BN">
          <b>BN</b><span data-sim-count="BN">30</span>
          <span class="sim-gov"><input data-sim-gov="BN" type="checkbox"> Dalam kerajaan</span>
          <input data-sim-seats="BN" type="hidden" value="30">
        </label>
        <label class="sim-choice" data-sim-row="GPS">
          <b>GPS</b><span data-sim-count="GPS">23</span>
          <span class="sim-gov"><input data-sim-gov="GPS" type="checkbox"> Dalam kerajaan</span>
          <input data-sim-seats="GPS" type="hidden" value="23">
        </label>
        <label class="sim-choice" data-sim-row="GRS">
          <b>GRS</b><span data-sim-count="GRS">6</span>
          <span class="sim-gov"><input data-sim-gov="GRS" type="checkbox"> Dalam kerajaan</span>
          <input data-sim-seats="GRS" type="hidden" value="6">
        </label>
        <label class="sim-choice" data-sim-row="OTHER">
          <b data-sim-other-name>Lain-lain</b><span data-sim-count="OTHER">7</span>
          <span class="sim-gov"><input data-sim-gov="OTHER" type="checkbox"> Dalam kerajaan</span>
          <input data-sim-seats="OTHER" type="hidden" value="7">
        </label>
      </div>
      <p class="sim-status" data-sim-status data-state="hung">Tanda Gabungan sampai anda pegang 112.</p>
      <div data-sim-stack>{bar}</div>
      <div class="sim-chamber" data-sim-chamber aria-hidden="true"></div>
    </div>
    <details class="why-tap">
      <summary>Nombor pada setiap tahun</summary>
      <p>{c["ge15-ph"]} {c["ge15-pn"]} {c["ge15-bn"]} {c["ge15-gps"]} {c["ge15-grs"]}</p>
      <p>{c["ge14-ph"]} {c["ge14-bn"]}</p>
      <p>{c["ge13-bn"]} {c["ge13-pr"]}</p>
      <p>{c["ph-founded"]} {c["gps-founded"]} {c["pn-founded"]} {c["grs-founded"]}</p>
    </details>
    {majority_next}
  </section>

  <section class="scene" id="play-4">
    <div class="pk-eyebrow">04 · Lulus satu Rang Undang-Undang</div>
    <h2>Bawa satu Rang Undang-Undang keluar.</h2>
    {_bill_play(language="ms", c=c)}
    <details class="why-tap">
      <summary>Lagi maklumat</summary>
      <p>{c["bill"]}</p>
      <p>{c["division"]}</p>
      <p>{c["pm-practice"]}</p>
    </details>
    <p class="finish">
      Apa yang PRU16 unjurkan di laman ini ialah Dewan Rakyat yang seterusnya
      — 222 Kerusi, dan sama ada suatu Gabungan memegang Majoriti.
    </p>
    {bill_next}
  </section>

  <section class="scene" id="play-compass">
    <div class="pk-eyebrow">Pilihan</div>
    <h2>Kompas politik</h2>
    <p class="caveat">
      Ini lakaran pengajaran, bukan skor saintifik. Wikipedia tidak
      menerbitkan nombor x dan y. Klik ialah tanda anda sahaja. Laman ini
      tidak akan menamakan Gabungan untuk anda.
    </p>
    <div class="compass-panel">
      <div class="compass-board" id="vote-compass" role="img" aria-label="Lakaran pengajaran kompas politik">
        <span class="compass-label top">Semenanjung</span>
        <span class="compass-label bottom">Malaysia Timur</span>
        <span class="compass-label left">Kiri</span>
        <span class="compass-label right">Kanan</span>
        <span class="compass-dot" data-c="PH" title="PH">PH</span>
        <span class="compass-dot" data-c="BN" title="BN">BN</span>
        <span class="compass-dot" data-c="PN" title="PN">PN</span>
        <span class="compass-dot" data-c="GPS" title="GPS">GPS</span>
        <span class="compass-dot" data-c="GRS" title="GRS">GRS</span>
        <span class="compass-you" id="vote-compass-you" hidden>Anda</span>
      </div>
      <div class="compass-tools">
        <label>Kiri ke kanan
          <input id="vote-compass-x" type="range" min="2" max="98" value="50">
        </label>
        <label>Semenanjung ke Malaysia Timur
          <input id="vote-compass-y" type="range" min="2" max="98" value="50">
        </label>
        <p class="more" id="vote-compass-note">Letakkan tanda jika anda mahu.</p>
      </div>
      <div class="compass-legend prose-claim">
        {c["ph-position"]} {c["bn-position"]} {c["pn-position"]}
        {c["gps-position"]} {c["gps-sarawak"]} {c["grs-position"]} {c["grs-sabah"]}
      </div>
    </div>
  </section>
</div>
""".strip()
