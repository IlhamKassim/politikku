# 0002: Predictive Forecasting vs Swing Model

**Date:** 2026-08-28
**Topic:** What a "paid" predictive model looks like

## What was learned
*   A true "paid" predictive model would likely use **MRP (Multilevel Regression and Poststratification)**. This requires expensive polling and granular census data to predict shifts based on specific demographic groups per constituency.
*   It would use **Probabilistic simulations** (Monte Carlo) requiring paid cloud compute, generating probabilities (e.g. 80% chance to win) rather than deterministic arithmetic margins.
*   It would rely on **Proprietary data APIs** (social media firehoses, daily tracking polls) instead of open-source news scraping.
*   **Why we avoid it:** Aside from violating the zero recurring cost rule (ADR 0002), these complex models reduce transparency. The current Swing Model's deterministic arithmetic ensures that any user can audit exactly why a Seat Call was made (ADR 0005).

## Future implications
*   If the user suggests using demographics to tweak a seat, I can remind them that we intentionally do not use an MRP approach to preserve transparency and zero cost.
