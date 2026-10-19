"""Phase 1E2 — enrich the top gap keywords (keyword_overview ≤100, serp for top 20) and score winnability."""
import pandas as pd

import dataforseo_client as c

OUT = "data/processed/"
d = c.DFS()
bal0 = d.balance()["balance_usd"]
gap = pd.read_csv(OUT + "keyword_gap.csv")
auth = pd.read_csv(OUT + "authority_gap.csv").set_index("domain")
fv_rank = auth.loc["fullyvital.com", "rank"]
top = gap.head(100)
ko = d.keyword_overview(top.keyword.tolist())
ko = ko[["keyword", "keyword_info.search_volume", "keyword_properties.keyword_difficulty", "search_intent_info.main_intent",
         "keyword_info.search_volume_trend.yearly", "keyword_info.search_volume_trend.quarterly",
         "avg_backlinks_info.main_domain_rank", "avg_backlinks_info.referring_main_domains"]]
ko.columns = ["keyword", "volume_fresh", "kd_fresh", "intent_fresh", "trend_yearly_pct", "trend_quarterly_pct",
              "top10_avg_domain_rank_fresh", "top10_avg_page_ref_domains_fresh"]
serps = pd.concat([d.serp(k) for k in top.keyword.head(20)], ignore_index=True)
serps["domain"] = serps.domain.str.replace(r"^www\.", "", regex=True)
serps.to_csv(OUT + "dfs_serp_gap_top20.csv", index=False)

# Winnable = a brand competitor whose domain rank is at or below FullyVital's already ranks top 10 for it.
weaker = set(auth[(auth["rank"] <= fv_rank) & (auth.index != "fullyvital.com")].index)
def weaker_top10(r):
    pairs = zip(r.who.split(", "), [int(p) for p in str(r.positions).split(", ")])
    return ", ".join(f"{dom} #{p}" for dom, p in pairs if dom in weaker and p <= 10)
gap["weaker_domains_in_top10"] = gap.apply(weaker_top10, axis=1)
gap["winnable"] = gap.weaker_domains_in_top10 != ""
gap = gap.merge(ko, on="keyword", how="left")
sv = serps.groupby("keyword").agg(serp_organic_results=("domain", "size"),
                                  serp_domains=("domain", lambda s: ", ".join(s)))
gap = gap.merge(sv, on="keyword", how="left")
gap.to_csv(OUT + "keyword_gap.csv", index=False)
print("FV rank", fv_rank, "| weaker-or-equal competitors:", sorted(weaker))
print("gap", len(gap), "winnable", int(gap.winnable.sum()), "winnable volume", int(gap[gap.winnable].volume.sum()))
print(gap.groupby(["cluster", "winnable"]).agg(n=("volume", "size"), vol=("volume", "sum")).to_string())
pd.set_option("display.width", 250, "display.max_colwidth", 70)
print(gap.head(30)[["keyword", "volume", "volume_fresh", "kd", "intent", "trend_yearly_pct", "competitors", "fullyvital_position", "top10_avg_domain_rank", "winnable", "weaker_domains_in_top10"]].to_string())
print(gap[gap.cluster == "gray"].head(25)[["keyword", "volume", "competitors", "fullyvital_position", "winnable", "who"]].to_string())
print(serps.domain.value_counts().head(25).to_dict())
s = d.summary(); s.to_csv(OUT + "dfs_spend_1e2.csv", index=False)
print("spent $%.4f" % s.cost_usd.sum(), "balance", bal0, "->", d.balance()["balance_usd"])
