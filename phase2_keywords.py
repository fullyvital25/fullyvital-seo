"""
Phase 2A: keyword universe and topic clusters from cached Phase 1 data (no API calls).

Outputs:
    data/processed/phase2_keyword_universe.csv   one row per keyword
    data/processed/phase2_clusters.csv           one row per cluster

Usage:
    python phase2_keywords.py
"""

import re

import numpy as np
import pandas as pd

import dataforseo_client as c

O, RAW, D = "data/processed/", "data/raw/", "2026-10-12"
FV_RANK = 317  # FullyVital Backlinks domain rank (Phase 1)
norm = lambda u: re.sub(r"^https?://(www\.)?", "https://", str(u).split("?")[0].split("#")[0].rstrip("/")).lower()

# ---------- taxonomy: first matching rule wins ----------
GRAY = r"\bgr[ae]y|\bwhite hair|\bgr[ae]ying|\bsilver hair|salt and pepper|canities|\bwhite hairs"
RULES = [
    # (line, cluster, regex, product_fit, compliance)
    ("both", "Off-scope: beard, brows, lashes, body, pets", r"\bbeard|eyebrow|eyelash|\blash|facial hair|body hair|\bcats?\b|\bdogs?\b|\bpubic|chest hair|leg hair|anime|cartoon|character|cosplay|costume|\bwig\b|\bart\b|drawing|\bkpop\b|celebrit|actor|actress", "none", ""),
    ("gray", "Gray: competitor brands", r"particle|\barey\b|mayraki|heyhair|\biles\b|greyverse|grey ?ban|nutrafol|viviscal|\bari grey", "Anti-Gray System", ""),
    ("gray", "Gray: coverage, dye & styling", r"\bdye|dyed|dying|color|colour|cover|blending|blend|highlight|transition|hairstyle|haircut|\bstyl|\bcuts?\b|\btint|bleach|ideas|toning|toner|purple shampoo|silver fox|look|dark|roots?\b|frizzy|\bgo gr[ae]y|going gr[ae]y|embrac|hiding|hide|\bgrey x|black and white|full gr[ae]y|how to get gr[ae]y|\bwig|ombre|balayage|lowlight|platinum|\bash\b|\bbob\b|pixie|layer", "none", ""),
    ("gray", "Gray: care for gray hair", r"\bcare\b|mask|conditioning|conditioner|\bwash|shampoo|yellow|brassy|soft|dry|texture|wiry", "none", ""),
    ("gray", "Gray: reversal, slowing & stopping", r"revers|stop|prevent|get rid|restore|repigment|cure|turn .* back|naturally black|slow|delay|avoid|combat|\bno gr[ae]y|fight", "Anti-Gray System", "reverse/prevent wording"),
    ("gray", "Gray: nutrients & deficiencies", r"vitamin|b12|b-12|copper|deficien|catalase|glutathione|\biron\b|zinc|biotin|melanin|mineral|\bfood|diet|\beat|peptide", "Anti-Gray Supplements", ""),
    ("gray", "Gray: supplements & products", r"supplement|pill|tablet|capsule|gumm|serum|product|treatment|best|anti[- ]?gr[ae]y|\boils?\b|medicine", "Anti-Gray System", ""),
    ("gray", "Gray: natural remedies", r"natural|home|remed|onion|curry|amla|rosemary|coconut|henna|black tea|coffee", "Anti-Gray Serum", ""),
    ("gray", "Gray: causes", r"cause|why|reason|stress|genetic|turn|getting|smok|thyroid|disease|anxiety|what makes", "Anti-Gray Supplements", ""),
    ("gray", "Gray: questions, myths & meaning", r"pluck|pull|patch|meaning|\bmean|bulb|follicle|silver vs|vs gr[ae]y|chemo|one gr[ae]y|single|myth|true|normal", "Anti-Gray System", ""),
    ("gray", "Gray: by age & early graying", r"\bat \d\d|\b\d\d\b|\d0s|twent|thirt|when do|when does|1st|first|young|early|premature|teen|\bage\b|\bages\b|kid|child", "Anti-Gray System", ""),
    ("gray", "Gray: causes", r"cause|why|reason|stress|genetic|turn|start|getting|smok|thyroid|disease|anxiety", "Anti-Gray Supplements", ""),
    ("gray", "Gray: men", r"\bmen\b|\bmens?\b|men's|\bmale|\bguys?\b|\bman\b", "Anti-Gray System", ""),
    ("gray", "Gray: general", r".", "Anti-Gray System", ""),
    ("growth", "Drugs: minoxidil, finasteride & Rx", r"minoxidil|finasteride|rogaine|dutasteride|spironolactone|ketoconazole|kirkland|propecia|clascoterone|\brx\b|prescription|\bhims\b|for hims|\bkeeps\b|roman\b", "none", "drug topic"),
    ("growth", "Medications that cause hair loss", r"metformin|wellbutrin|accutane|\bmeds?\b|medication|ozempic|semaglutide|birth control|antidepress|lexapro|adderall|statin|levothyroxine|lisinopril|zoloft|gabapentin|\bdrugs?\b", "none", "drug topic"),
    ("growth", "Styling for thinning hair", r"hairstyle|haircut|\bcuts?\b|\bstyl|buzz|bangs|\bwigs?\b|topper|extension|volumiz|thicker looking|\bbob\b|pixie|layer|updo|braid|ponytail|part line", "none", ""),
    ("growth", "Competitor brands (growth)", r"nutrafol|viviscal|pura d.?or|vegamour|hairmax|keranique|bosley|olaplex|sugarbear|hairburst|\bols?ly\b|\bhum\b|neofollics|theradome|mdhair|kerotin|happy head", "Hair Revival System", ""),
    ("growth", "Conditions: alopecia, TE, PCOS, thyroid…", r"alopecia|areata|androgenetic|telogen|effluvium|pcos|thyroid|psoriasis|dandruff|chemo|lupus|scarring|traction|seborrh|fungal|ringworm|tinea|lichen|covid|anemia|disease|disorder|syndrome", "Hair Revival System", "disease topic"),
    ("growth", "Life stages: postpartum, pregnancy, menopause", r"postpartum|pregnan|menopaus|perimenopaus|breastfeed|after baby|hormon", "Hair Revival System", ""),
    ("growth", "Procedures & devices", r"transplant|\bprp\b|platelet|laser|light therapy|red light|\bled\b|lllt|microneedl|derma ?roll|dermaroll|derma ?stamp|stem cell|injection|\bcap\b|helmet|exosome|micropig|scalp massager|massager", "Derma roller", ""),
    ("growth", "Peptides & copper peptides", r"peptide|copper", "Hair Revival Serum", ""),
    ("growth", "Topical oils & natural ingredients", r"\boils?\b|rosemary|castor|onion|aloe|coconut|batana|essential|tea tree|peppermint|jojoba|argan|rice water|caffeine|ginseng|herb", "Hair Revival Serum", ""),
    ("growth", "Supplement myths: creatine, protein shakes", r"creatine|protein shake|protein powder|whey|pre.?workout|\bsteroid", "Hair Revival Supplements", ""),
    ("growth", "Protein & food for hair", r"protein|\bfoods?\b|\bdiet\b|\beat|eggs?\b|rich in|fruit|vegetable|smoothie|juice", "Hair Revival Supplements", ""),
    ("growth", "Biotin", r"biotin", "Hair Revival Supplements", ""),
    ("growth", "Collagen", r"collagen|keratin supplement", "Hair Skin Gut Collagen", ""),
    ("growth", "Prenatal vitamins & hair", r"prenatal", "Hair Revival Supplements", ""),
    ("growth", "Iron, vitamin D & deficiencies", r"\biron\b|ferritin|vitamin d|\bb12\b|deficien|lack of|zinc|magnesium|folic|folate|selenium|omega|fish oil", "Hair Revival Supplements", ""),
    ("growth", "Saw palmetto & DHT blockers", r"saw palmetto|\bdht\b|testosterone|androgen|pumpkin seed|beta.?sitosterol", "Hair Revival Supplements", ""),
    ("growth", "Hair, skin & nails vitamins", r"(skin|nail).*(hair|skin|nail)|beauty vitamin", "Hair Skin Gut Collagen", ""),
    ("growth", "Hair vitamins & supplements (commercial)", r"vitamin|supplement|pills?\b|tablet|gumm|capsule|nutrient|multivitamin|amino|silica|quercetin|melatonin|ashwagandha", "Hair Revival Supplements", ""),
    ("growth", "Growth products: serums, shampoos, kits", r"serum|shampoo|conditioner|products?\b|\bbest\b|\bkit\b|foam|topical|spray|tonic|mask|regimen|routine|fibers", "Hair Revival Kit / System", ""),
    ("growth", "Hairline, crown & bald spots", r"hairline|receding|crown|temple|widow|\bpart\b|bald spot|balding|bald\b|thin spot|cowlick|\bv shape|shav", "Hair Revival System", ""),
    ("growth", "Shedding & how much is normal", r"shed|normal|how much|falling out|fall out|hair fall|clumps|in the shower|brush", "Hair Revival System", ""),
    ("growth", "Signs & symptoms of thinning", r"sign|look like|is my hair|tender|pain|itch|sore|hurt|sticks? up|sticking up", "Hair Revival System", ""),
    ("growth", "Hair growth cycle & biology", r"cycle|phase|stage|anagen|catagen|follicle|how does hair grow|how do hair|biology|calculator", "Hair Revival System", ""),
    ("growth", "Remedies & how to stop hair loss", r"how to (stop|prevent|reduce|avoid|slow)|\bstop\b|prevent|remed|medicine|solution|natural|therapy|encourage|stimulate|massag|treatment|cure|fix", "Hair Revival System", "treat/prevent wording"),
    ("growth", "Causes of hair loss & thinning", r"cause|why|reason|stress|anxiety|genetic|\bage\b|weight loss|losing weight|sleep", "Hair Revival System", ""),
    ("growth", "Men's thinning & hair loss", r"\bmen\b|\bmens?\b|men's|\bmale|\bguys?\b|\bman\b|beard", "Hair Revival System", ""),
    ("growth", "Women's thinning & hair loss", r"women|woman|female|ladies|\bgirls?\b", "Hair Revival System", ""),
    ("growth", "Speed & regrowth timelines", r"fast|faster|quick|how long|grow back|regrow|week|month|timeline|per day|inch|longer", "Hair Revival System", ""),
    ("growth", "Hair growth: general", r".", "Hair Revival System", ""),
]
COMPILED = [(l, n, re.compile(p, re.I), f, k) for l, n, p, f, k in RULES]


def classify(kw: str):
    gray = bool(re.search(GRAY, kw, re.I))
    for line, name, rx, fit, risk in COMPILED:
        if line == "gray" and not gray:
            continue
        if line == "growth" and gray:
            continue
        if rx.search(kw):
            return ("gray" if gray else "growth") if line == "both" else line, name, fit, risk
    return "growth", "Hair growth: general", "Hair Revival System", ""


def main():
    fv = pd.read_csv(O + "dfs_ranked_keywords_in_scope_fullyvital.csv")
    ck = pd.read_csv(O + "dfs_competitor_keywords_in_scope_top20.csv")
    gap = pd.read_csv(O + "keyword_gap.csv")
    auth = pd.read_csv(O + "authority_gap.csv").set_index("domain")
    pq = pd.read_csv(RAW + f"gsc_page_query_{D}.csv").dropna(subset=["query"])
    q = pd.read_csv(RAW + f"gsc_query_{D}.csv").dropna(subset=["query"])
    rev = pd.read_csv(O + "blog_cleanup_review.csv")
    queue = set(pd.read_csv(O + "refresh_queue.csv").path)

    # keyword-level metrics
    sug = pd.read_csv(O + "phase2_dfs_keyword_suggestions.csv")
    kw = pd.concat([fv[["keyword", "volume", "kd", "intent"]], ck[["keyword", "volume", "kd", "intent"]],
                    gap[["keyword", "volume", "kd", "intent"]], sug[["keyword", "volume", "kd", "intent"]]]
                   ).sort_values("volume", ascending=False).drop_duplicates("keyword")
    top10_dr = pd.concat([gap.set_index("keyword").top10_avg_domain_rank, sug.set_index("keyword").top10_avg_domain_rank]).groupby(level=0).first()
    fvpos = fv.groupby("keyword").position.min().rename("fv_position")
    fvurl = fv.sort_values("position").drop_duplicates("keyword").set_index("keyword").url.rename("fv_url")
    weaker = set(auth[(auth["rank"] <= FV_RANK) & (auth.index != "fullyvital.com")].index)
    cagg = ck.groupby("keyword").agg(competitors_top20=("domain", "nunique"), best_comp_position=("position", "min"))
    cweak = ck[ck.domain.isin(weaker) & (ck.position <= 10)].groupby("keyword").domain.apply(lambda s: ", ".join(sorted(set(s)))).rename("weaker_comp_top10")
    kw = kw.set_index("keyword").join([fvpos, fvurl, cagg, cweak, top10_dr.rename("top10_avg_domain_rank")])
    gsc_q = q[~q["query"].str.contains("fully ?vital", case=False)].set_index("query")[["clicks", "impressions", "position"]]
    gsc_q.columns = ["gsc_clicks_16m", "gsc_impressions_16m", "gsc_position"]
    pat = "|".join(c.TOPIC_TERMS)
    gsc_q = gsc_q[gsc_q.index.str.contains(pat, case=False)]
    gsc_q = gsc_q[gsc_q.gsc_impressions_16m >= 50]  # keep GSC-only queries with meaningful impressions
    uni = kw.join(gsc_q, how="outer")
    uni.index.name = "keyword"
    uni = uni.reset_index()
    uni["source"] = np.where(uni.volume.notna(), "dataforseo", "gsc_only")
    uni[["line", "cluster", "product_fit", "compliance"]] = uni.keyword.apply(lambda k: pd.Series(classify(k)))
    # winnable: a lower-authority brand already ranks top 10, or the top 10's average domain rank is at or below FullyVital's
    uni["winnable"] = uni.weaker_comp_top10.notna() | (uni.top10_avg_domain_rank <= FV_RANK)
    uni["fv_top10"] = uni.fv_position <= 10
    uni["fv_top20"] = uni.fv_position <= 20

    # current best FullyVital page per keyword (GSC, by impressions), and its clean-up status
    pq["url"] = pq.page.map(norm)
    best = pq.sort_values("impressions", ascending=False).drop_duplicates("query").set_index("query").url.rename("gsc_best_url")
    uni = uni.merge(best, left_on="keyword", right_index=True, how="left")
    uni["current_url"] = uni.gsc_best_url.fillna(uni.fv_url.map(norm))
    status = dict(zip("https://fullyvital.com" + rev.path, rev.decision))
    redirect = {("https://fullyvital.com" + p): ("https://fullyvital.com" + t) for p, t in zip(rev.path, rev.redirect_to) if isinstance(t, str)}
    uni["current_url"] = uni.current_url.map(lambda u: redirect.get(u, u) if isinstance(u, str) else u)

    def page_status(u):
        if not isinstance(u, str):
            return "no page"
        p = u.replace("https://fullyvital.com", "")
        if "/products/" in p or "/collections/" in p:
            return "product/collection page"
        if p in queue:
            return "in refresh queue"
        s = status.get(u)
        return s or ("page" if "/pages/" in p else "other")
    uni["page_status"] = uni.current_url.map(page_status)
    uni.to_csv(O + "phase2_keyword_universe.csv", index=False)

    # ---------- clusters ----------
    def top_kw(x, n=5):
        x = x.sort_values(["volume", "gsc_impressions_16m"], ascending=False, na_position="last")
        return " | ".join(x.keyword.head(n))

    def top_page(x):
        y = x.dropna(subset=["current_url"]).groupby("current_url").gsc_impressions_16m.sum().sort_values(ascending=False)
        return y.index[0].replace("https://fullyvital.com", "") if len(y) else ""

    STOPW = set("for the and of to in a is with on does do can how what your my are it be from at by an you i".split())
    uni["variant_key"] = uni.keyword.map(lambda k: " ".join(sorted({re.sub(r"(ies|es|s)$", "", t) for t in re.findall(r"[a-z0-9]+", k.lower()) if t not in STOPW})))

    SYN = {"grey": "gray", "greying": "gray", "graying": "gray", "white": "gray", "hairstyle": "style", "haircut": "style", "cut": "style",
           "styling": "style", "vitamin": "vitamin", "supplement": "vitamin", "pill": "vitamin", "women": "woman", "female": "woman",
           "men": "man", "male": "man", "regrow": "grow", "growth": "grow", "growing": "grow", "thinning": "thin", "loss": "loss"}

    def stems(k):
        return {SYN.get(t, t) for t in (re.sub(r"(ies|es|s)$", "", w) for w in re.findall(r"[a-z0-9]+", k.lower())) if t not in STOPW}

    def dedup_volume(x):
        """Count a search family once: keywords with the same volume and >=50% token overlap are variants."""
        kept, total = [], 0.0
        for k, v in x.dropna(subset=["volume"]).sort_values("volume", ascending=False)[["keyword", "volume"]].itertuples(index=False):
            st = stems(k)
            if any(v == kv and len(st & ks) / max(1, len(st | ks)) >= 0.5 for kv, ks in kept):
                continue
            kept.append((v, st))
            total += v
        return total

    cl = uni.groupby(["line", "cluster"]).apply(lambda x: pd.Series({
        "keywords": len(x), "volume": x.volume.sum(), "volume_dedup": dedup_volume(x),
        "head_term": x.sort_values("volume", ascending=False).keyword.iat[0], "head_volume": x.volume.max(),
        "dfs_keywords": int(x.volume.notna().sum()),
        "fv_top10": int(x.fv_top10.sum()), "fv_top20": int(x.fv_top20.sum()),
        "fv_top10_volume": x.loc[x.fv_top10, "volume"].sum(),
        "winnable_keywords": int(x.winnable.sum()), "winnable_volume": x.loc[x.winnable, "volume"].sum(),
        "gsc_clicks_16m": x.gsc_clicks_16m.sum(), "gsc_impressions_16m": x.gsc_impressions_16m.sum(),
        "commercial_share": (x.intent.isin(["commercial", "transactional"]) * x.volume.fillna(0)).sum() / max(1, x.volume.fillna(0).sum()),
        "product_fit": x.product_fit.mode().iat[0], "compliance": x.compliance.mode().iat[0] if x.compliance.ne("").any() else "",
        "top_keywords": top_kw(x), "fv_main_page": top_page(x),
        "pages_ranking": x.current_url.nunique(),
    })).reset_index().sort_values(["line", "volume_dedup"], ascending=[True, False])
    cl.to_csv(O + "phase2_clusters.csv", index=False)
    pd.set_option("display.width", 260, "display.max_colwidth", 60)
    print(uni.groupby("source").size().to_dict(), "| keywords:", len(uni))
    print(cl[["line", "cluster", "keywords", "volume", "fv_top10", "winnable_volume", "gsc_clicks_16m", "commercial_share", "product_fit", "pages_ranking"]]
          .round(2).to_string())


if __name__ == "__main__":
    main()
