"""Interpretation markdown for each use case, written from the executed outputs.

If you change the analysis code in build_use_case_notebook.py, re-run it with
--execute and check these statements still match the printed results.
"""

INTERP = {
    # ------------------------------------------------------------------ UC1
    "uc1_a": r"""
**What the usual approach tells us.** The poorest states (Kebbi, Jigawa, Bauchi, Benue, Zamfara) all average about $-0.24$, while Lagos stands out at $0.81$. The histogram is skewed: most wards sit slightly below zero with a long tail of wealthier wards.

**What it cannot tell us.** Whether poor wards are next to each other or scattered. A state average of $-0.24$ could hide a wealthy town surrounded by very poor villages. If we shuffled the wards randomly across the map, every number above would stay exactly the same.
""",
    "uc1_b": r"""
**Interpretation.**
- **Global Moran's $I = 0.367$** against an expectation of about 0 under randomness, with $z = 56.8$ and pseudo $p = 0.001$ (the smallest possible with 999 permutations). We **reject $H_0$**: purchasing power is strongly clustered.
- **LISA** finds **763 High-High** wards (wealth clusters) and **773 Low-Low** wards (poverty clusters). These are neighbourhoods, not states, and many cross state lines.
- **197 High-Low** wards are relatively wealthy wards surrounded by poorer ones (local economic anchors), and **178 Low-High** wards are poor pockets inside wealthier areas, the households that state averages hide.

**Decision.** Target the cash-transfer programme at the Low-Low clusters (contiguous areas one delivery network can serve) and add the Low-High pockets as a separate list. Do not allocate by state rank alone.
""",
    # ------------------------------------------------------------------ UC2
    "uc2_a": r"""
**What the usual approach tells us.** $r = 0.169$, so $r^2 = 0.028$: church share "explains" under 3% of the variation in purchasing power. A standard analysis would stop here and call the relationship negligible.

**What it cannot tell us.** Whether the relationship is concentrated in particular regions. A weak national correlation can be an average of strong local relationships in some places and none in others.
""",
    "uc2_b": r"""
**Interpretation.**
- **Bivariate Moran's $I = 0.143$, $p = 0.001$**: wards with higher purchasing power tend to be surrounded by wards with a higher church share. The association is weak but it is real, and it is *spatial*.
- Most significant wards are **Low power, low church share nearby (1,747)** and **Low power, high church share nearby (1,566)**. Low purchasing power is common in both mosque-dominated and church-dominated regions, so faith mix is not the driver of poverty.
- **1,096 High-High** wards sit mostly in the wealthier south, which is also where churches dominate; this overlap drives the positive global value.

**Caution.** This is an association between two geographic patterns (both follow the north-south divide), not evidence that faith institutions cause wealth or poverty. For programme design, the useful output is the map: it shows which kind of faith partner is present in each poor cluster.
""",
    # ------------------------------------------------------------------ UC3
    "uc3_a": r"""
**What the usual approach tells us.** State church shares range from 0 to 1 with a median of about 0.71. Sokoto, Zamfara, Jigawa and Kano are almost entirely mosque-dominated; Anambra, Ebonyi, Akwa Ibom and Osun are almost entirely church-dominated.

**What it cannot tell us.** Where, *within* states, the two faiths meet. The mixing happens along a band that cuts across state boundaries.
""",
    "uc3_b": r"""
**Interpretation.**
- **Moran's $I = 0.731$, $p = 0.001$** for church share: one of the strongest spatial patterns in the whole dataset. Faith institutions are highly sorted in space.
- **Getis-Ord $G_i^*$ on Shannon diversity** finds **1,550 mixing-zone wards** (statistically significant clusters of high diversity), led by **Niger, Lagos, Oyo, Nasarawa and Kaduna**: the Middle Belt and the south-west.
- **5,138 wards** fall in single-faith zones.

**Decision.** The mixing-zone clusters are where inter-faith dialogue programmes and early-warning systems for communal tension add the most value, and they span state borders, so programmes should be designed across states.
""",
    # ------------------------------------------------------------------ UC4
    "uc4_a": r"""
**What the usual approach tells us.** **1,675 wards** with more than 17,000 residents have no registered health facility, holding about **69.8 million** people. The list is headed by very large wards such as Mbaapen (Benue), Aheward 9 (Rivers) and Umudim (Imo).

**What it cannot tell us.** Which deserts are next to each other. A mobile clinic that parks in one ward can serve its neighbours too, so a flat list wastes that advantage.

**Data caveat.** "No registered facility" means none in the GRID3 registry. Some dense urban wards will have unregistered private clinics, so treat the list as "where to verify first".
""",
    "uc4_b": r"""
**Interpretation.**
- **957 wards** sit in statistically significant hot spots of unserved population; **537 of the 1,675 deserts** fall inside them. Those 537 are the priority: deserts surrounded by other deserts.
- The most hot-spot wards are in **Lagos, Anambra, Rivers, Imo and Cross River**. Because Lagos is well served in reality, its presence is a strong sign of **registry gaps** (private facilities not mapped) rather than a true desert.

**Decision.** Route mobile clinics through the hot-spot clusters outside the big cities first, and send a facility-mapping team to the urban hot spots to confirm whether the gap is real or a data gap.
""",
    # ------------------------------------------------------------------ UC5
    "uc5_a": r"""
**What the usual approach tells us.** $r = -0.026$: essentially **no relationship** between purchasing power and market density. A standard analysis would conclude that purchasing power is useless for choosing store locations.

**What it cannot tell us.** That "no relationship on average" can hide hundreds of specific places where high purchasing power meets low supply, and exactly those places are the business opportunity.
""",
    "uc5_b": r"""
**Interpretation.**
- The bivariate LISA flags **425 wards with high purchasing power and few markets around them**: the expansion shortlist that the correlation of $-0.03$ completely missed.
- They concentrate in **Kogi, Oyo, Rivers, Kwara, Yobe and Sokoto**.
- **189 wards** are already high power with many markets around (saturated, competitive), and **850** are low power with few markets (low demand).

**Decision.** Scout the 425 High-Low wards first, starting with the states where they cluster, and avoid the 189 saturated High-High wards.
""",
    # ------------------------------------------------------------------ UC6
    "uc6_a": r"""
**What the usual approach tells us.** A **Gini of 0.857** is extreme inequality: **65.8% of wards have no registered water point** at all, and a small share of wards holds most of the infrastructure (the Lorenz curve hugs the bottom axis until the very end).

**What it cannot tell us.** Where the gaps are, and whether they form continuous regions a single programme could cover.
""",
    "uc6_b": r"""
**Interpretation.**
- **Moran's $I = 0.608$, $p = 0.001$**: water provision is strongly clustered, so both good and poor access come in regions.
- **759 Low-Low wards** form contiguous water deserts home to about **21.0 million people**, concentrated in **Kano, Katsina, Borno, Jigawa, Sokoto and Bauchi** (the north).
- **1,408 High-High wards** show where water points are densely clustered.

**Decision.** A borehole programme should be planned per Low-Low cluster rather than per ward, which lets drilling rigs and maintenance teams cover neighbouring wards in one deployment.
""",
    # ------------------------------------------------------------------ UC7
    "uc7_a": r"""
**What the usual approach tells us.** Every coefficient looks highly significant ($p \approx 0$). Purchasing power has a coefficient of **0.279**: wealthier wards have more schools, holding population and area constant. The model explains only **11.6%** of the variation ($R^2 = 0.116$).

**The worry.** Those $p$-values assume every ward is an independent observation. If neighbouring wards share unmeasured factors (state education budgets, history, terrain), the errors are correlated and the $p$-values are too optimistic.
""",
    "uc7_b": r"""
**Interpretation.**
- **Residual Moran's $I = 0.358$ ($z = 56$)**: the OLS errors are strongly clustered, so OLS independence fails and its standard errors cannot be trusted.
- **LM tests**: both LM-lag and LM-error are significant, so we read the robust versions. **Robust LM-error (398.6) is far larger than Robust LM-lag (22.5)**, which points to a **Spatial Error Model**: shared unmeasured regional factors, not schools "spreading" between wards.
- **SEM results**: $\lambda = 0.671$, a strong shared regional component. The purchasing power effect **halves from 0.279 to 0.142**, and the population effect drops from 0.089 to 0.053. OLS was attributing to wealth part of what is really regional context.

**Decision.** Wealth still matters (0.142 remains significant), but a funding rule based on the OLS figure would overstate its effect by about double.
""",
    # ------------------------------------------------------------------ UC8
    "uc8_a": r"""
**What the usual approach tells us.** Urban wards have more markets (coefficient **0.251**, $p < 0.001$); population has no significant effect ($p = 0.48$). But $R^2 = 0.017$: OLS explains almost nothing, and both robust LM tests are significant (lag 79.5, error 281.8). There is spatial structure OLS is missing.
""",
    "uc8_b": r"""
**Interpretation.**
- **$\rho = 0.594$**: a ward's number of markets is strongly tied to the number of markets in its neighbours. Markets attract markets.
- **Spatial multiplier $1/(1-\rho) = 2.46$**: any local change is amplified about 2.5 times once the ripple through neighbours is counted.
- **Impacts for urban status**: direct **0.203** in the ward itself, plus an indirect spillover of **0.297** into neighbouring wards, a total of **0.500**. **More than half of the total effect happens outside the upgraded ward.**

**Decision.** When evaluating an urban upgrade, count the market growth in surrounding wards too. Judging the programme by the upgraded ward alone would miss about 60% of its effect.

*Note: the robust LM-error was also large, so a Spatial Durbin Model would be a good next step; SAR is used here to show how to read impacts.*
""",
    # ------------------------------------------------------------------ UC9
    "uc9_a": r"""
**What the usual approach tells us.** **92.8% of wards have no registered police station** (94.2% of rural wards, 84.6% of urban wards). Coverage is thin almost everywhere.
""",
    "uc9_b": r"""
**Interpretation.**
- **Global Join Counts**: observed 22,557 no-police/no-police neighbour pairs vs 22,542 expected, pseudo **$p = 0.38$**. We **cannot reject $H_0$**. With 93% of wards uncovered, two uncovered wards sitting side by side is exactly what chance produces. This is an important lesson: **not every variable is spatially clustered, and the test protects us from seeing patterns that are not there.**
- **Local join counts** still flag **1,356 wards** (about **34.7 million people**) where a ward *and all of its neighbours* have no station, more than chance allows for those specific neighbourhoods. They are most common in **Osun, Plateau, Lagos, Oyo, Abia and Enugu**.

**Decision.** The national picture is "uniformly thin coverage", not "clustered gaps". The local dark zones are a shortlist for new stations. As with clinics, Lagos appearing here suggests registry gaps to verify.
""",
    # ------------------------------------------------------------------ UC10
    "uc10_a": r"""
**What the usual approach tells us.** Across **774 LGAs**, one national slope says each unit of purchasing power adds about **2.72 schools per 10,000 people** ($p < 0.001$). But the model explains only **13.4%** of the variation, so one line fits the country poorly.
""",
    "uc10_b": r"""
**Interpretation.**
- The optimal **bandwidth is 48 nearest LGAs**: each local regression borrows information from its 48 closest LGAs.
- **GWR fits far better**: $R^2$ rises from **0.134 to 0.571** and AICc drops from **2091 to 1830** (a drop of more than 3 is meaningful). We **reject $H_0$**: the relationship is not the same everywhere.
- The local (standardised) slope ranges from **$-0.77$ to $1.21$**, but after correcting for multiple testing it is **significantly positive in only 48 LGAs** and significantly negative in none. In most of the country, purchasing power adds little once local context is allowed for.

**Decision.** A single national rule ("more wealth, more schools") holds in a minority of LGAs. Education planning should use the local-slope map: where the slope is significant, school supply is tracking wealth, which risks leaving poorer LGAs behind.
""",
    # ------------------------------------------------------------------ UC11
    "uc11_a": r"""
**What the usual approach tells us.** Ward prevalence averages **25%** (from 6.8% to 43.7%). The highest state averages are in the south-east: **Akwa Ibom (33.3%), Abia and Imo (32.3%)**.

The OLS says poorer wards carry slightly more malaria (purchasing power coefficient **$-0.32$, $p = 0.03$**), and urban and denser wards carry less (urban **$-3.3$** percentage points). But $R^2 = 0.13$: these factors explain little, and the model assumes every ward is independent.
""",
    "uc11_b": r"""
**Interpretation.**
- **Moran's $I = 0.933$**: malaria is extremely clustered. Part of this is real (climate, rainfall and ecology change slowly across space) and part comes from the ~5 km MAP surface being shared by small neighbouring wards.
- **LISA finds 2,175 High-High hot-spot wards with about 48.4 million people**, led by **Akwa Ibom, Imo and Abia**, with further clusters in **Niger, Ondo and Kaduna**. These are the contiguous areas where a campaign reaches the most high-burden wards per deployment.
- **The OLS residuals are just as clustered (0.919)**, and Robust LM-error (784) dominates Robust LM-lag (184), so we fit a **Spatial Error Model**.
- In the SEM, **the purchasing power effect disappears (from $-0.32$ to $0.007$)**, and the urban and density effects shrink by about two-thirds. $\lambda = 0.984$: almost all of what OLS attributed to poverty is shared regional geography.

**Decision.** Do not target malaria campaigns by poverty ranking: once geography is accounted for, poverty adds almost nothing. Target the LISA hot-spot clusters directly, and treat urban status as a modest secondary factor.
""",
}
