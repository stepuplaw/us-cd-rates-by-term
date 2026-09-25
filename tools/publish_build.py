#!/usr/bin/env python3
"""Build the published CD rate table from data/top200_<term>m.csv.
Keeps rates at or above FLOOR for each standard term, re-ranks, and writes
publish/cd_rates.csv, publish/cd_rates.json and publish/schema.json.
The site copies these with scripts/sync-cd-rates-dataset.mjs."""
import csv, json, os, re
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLOOR = 3.00
TERMS = [3, 6, 12, 18, 24, 36, 60]
FIELDS = [
 ("term_months","CD term in months"),
 ("rank","Rank within the term by APY (ties share a rank), after dropping rates below the floor"),
 ("institution","Institution name as marketed"),
 ("kind","bank or credit_union"),
 ("state","Headquarters state"),
 ("apy_pct","Annual percentage yield posted by the institution, percent"),
 ("min_deposit","Stated minimum opening deposit in dollars, blank if not stated"),
 ("promotion","yes if the institution's own page marks it as a special, promotion or limited-time rate"),
 ("product_note","Special product type if any (for example no-penalty or bump-up)"),
 ("fdic_cert","FDIC certificate number for banks"),
 ("ncua_charter","NCUA charter number for credit unions"),
 ("remote_opening","yes if the institution's own pages say an account can be opened online; no if they say in person only; otherwise not stated"),
 ("nonresident_eligible","What the institution's own pages say about customers who are not US residents"),
 ("cu_membership_open_nationwide","For credit unions, whether anyone in the US can join (usually through a partner organization)"),
 ("early_withdrawal_penalty","Early withdrawal penalty as stated, abridged"),
 ("source_url","The institution's page where the rate was read"),
 ("read_note","How the rate was read when it needed a person (for example a browser read or a homepage banner)"),
 ("date_checked","Date the rate was read (YYYY-MM-DD)"),
]

# Hand-checked corrections (2026-09-25)
OVERRIDES={
 "United Midwest Savings Bank, National Association":{"read_note":"Rate from the homepage banner '6-12 Month CDs with an APY of 4.75% are here!', which carries no date or minimum; the bank's CD rates page showed no rate table when read in a browser on 2026-09-24. The page says new customers must open their first account in person at a branch.","remote_opening":"no"},
 "Raymond James Bank":{"min_deposit":"1000","read_note":"Rates effective September 18, 2026 per the bank's deposit page. Minimum $1,000, or $2,000 if bought through a Raymond James brokerage account. Rates by phone at 800.718.2265, option 4, or through an advisor."},
}
rows=[]
for t in TERMS:
    src=[r for r in csv.DictReader(open(os.path.join(BASE,"data",f"top200_{t}m.csv"))) if float(r["apy_pct"])>=FLOOR]
    src.sort(key=lambda r:-float(r["apy_pct"]))
    rank=0; prev=None
    for i,r in enumerate(src,1):
        a=float(r["apy_pct"])
        if a!=prev: rank=i; prev=a
        note=r.get("verified_by_hand","").strip()
        note=re.sub(r"^\d{4}-\d{2}-\d{2}\s*","",note)
        rows.append({
         "term_months":t,"rank":rank,"institution":r["institution"].strip(),"kind":r["kind"],"state":r["state"],
         "apy_pct":f"{a:.2f}","min_deposit":r["min_deposit"],"promotion":r["promotion"],"product_note":r["product_note"],
         "fdic_cert":r["fdic_cert"],"ncua_charter":r["ncua_charter"],
         "remote_opening":r["remote_opening"] or "not stated","nonresident_eligible":r["nonresident_eligible"] or "not stated",
         "cu_membership_open_nationwide":r["cu_nationwide_membership"] if r["kind"]=="credit_union" else "",
         "early_withdrawal_penalty":(r["early_withdrawal_penalty"] or "")[:240],
         "source_url":r["source_url"],"read_note":note[:300],"date_checked":r["date_collected"],
        })
for r in rows:
    r.update(OVERRIDES.get(r["institution"],{}))
for r in rows:
    for k,v in r.items():
        if isinstance(v,str): r[k]=v.replace("—"," - ").replace("–","-")
out=os.path.join(BASE,"publish")
with open(os.path.join(out,"cd_rates.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=[k for k,_ in FIELDS]); w.writeheader(); w.writerows(rows)
json.dump(rows,open(os.path.join(out,"cd_rates.json"),"w"),indent=1)
json.dump({"floor_apy_pct":FLOOR,"fields":[{"name":k,"description":d} for k,d in FIELDS]},open(os.path.join(out,"schema.json"),"w"),indent=2)
from collections import Counter
print(len(rows),"rows", dict(Counter(r["term_months"] for r in rows)), "institutions", len({r["institution"] for r in rows}))
