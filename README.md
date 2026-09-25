# Highest Posted CD Rates in the US by Term (2026)

Posted certificate of deposit rates at or above 3.00% APY for 3, 6, 12, 18, 24, 36 and 60 month terms from 203 US banks and credit unions, ranked by term (821 rows). Each rate was read on the institution's own rate page and carries that URL and the date it was read, plus the stated minimum deposit, whether the institution says an account can be opened online, what it says about customers who are not US residents, credit union membership routes and the early withdrawal penalty. Candidates were 595 institutions: the 400 banks paying the highest average rates on time deposits in their June 30, 2026 Call Reports, every Florida-headquartered bank, 59 online banks and 62 large credit unions. Rows read by hand in a browser say so. Compiled 2026-09-24.

Live table: https://stepuplaw.com/data/cd-rates/

| Term | Rates listed | Highest APY | Tenth highest |
|---|---|---|---|
| 3 months | 66 | 4.50% | 3.90% |
| 6 months | 136 | 4.50% | 4.15% |
| 12 months | 164 | 4.75% | 4.35% |
| 18 months | 100 | 4.55% | 4.30% |
| 2 years | 124 | 4.70% | 4.35% |
| 3 years | 113 | 4.80% | 4.35% |
| 5 years | 118 | 4.95% | 4.35% |

## Files

| File | What it holds |
|---|---|
| `data/cd_rates.csv` | One row per institution per term, ranked |
| `data/cd_rates.json` | The same rows as JSON |
| `data/schema.json` | Column definitions and the 3.00% floor |
| `tools/publish_build.py` | Builds the table from the scraper output, applying hand-checked corrections |

## Columns

| Column | Meaning |
|---|---|
| `term_months` | CD term in months |
| `rank` | Rank within the term by APY (ties share a rank), after dropping rates below the floor |
| `institution` | Institution name as marketed |
| `kind` | bank or credit_union |
| `state` | Headquarters state |
| `apy_pct` | Annual percentage yield posted by the institution, percent |
| `min_deposit` | Stated minimum opening deposit in dollars, blank if not stated |
| `promotion` | yes if the institution's own page marks it as a special, promotion or limited-time rate |
| `product_note` | Special product type if any (for example no-penalty or bump-up) |
| `fdic_cert` | FDIC certificate number for banks |
| `ncua_charter` | NCUA charter number for credit unions |
| `remote_opening` | yes if the institution's own pages say an account can be opened online; no if they say in person only; otherwise not stated |
| `nonresident_eligible` | What the institution's own pages say about customers who are not US residents |
| `cu_membership_open_nationwide` | For credit unions, whether anyone in the US can join (usually through a partner organization) |
| `early_withdrawal_penalty` | Early withdrawal penalty as stated, abridged |
| `source_url` | The institution's page where the rate was read |
| `read_note` | How the rate was read when it needed a person (for example a browser read or a homepage banner) |
| `date_checked` | Date the rate was read (YYYY-MM-DD) |

## Method and limits

A script read each candidate's own CD rate page; 252 of 595 institutions posted a rate that could be read. Sites that refused scripted requests or filled rates in by script were read by a person in a browser, and those rows carry a `read_note`. Banks that show rates only after a ZIP code is entered, and sites that present a bot check, are missing; no bot check was bypassed. Only standard terms are ranked; IRA, business and jumbo rates with a minimum over $100,000 are excluded; rates below 3.00% are left out. Rates change often; confirm with the institution. Not financial advice. No institution pays to be listed.

## License and citation

CC BY 4.0. Cite as: Klagge, Kevin D., Highest Posted CD Rates in the US by Term (2026), StepUpLaw, https://stepuplaw.com/data/cd-rates/.
