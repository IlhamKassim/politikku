# 0001: The Election Model (Swing Model)

**Date:** 2026-08-28
**Topic:** The `live-political-analysis` Election Model

## What was learned
*   The model used is the **Swing Model**.
*   It operates by taking the **Baseline** (GE15 results) and applying a **uniform state swing**.
*   The swing is derived from **Sentiment** (News + Poll Calibration).
*   The constants used to convert Sentiment to Swing (`sentiment_sensitivity`, `state_signal_weight`) are provisional and uncalibrated because mapping news to vote share is a research-grade problem (ADR 0003).
*   **Why this model?** It guarantees transparency (pure arithmetic, not subjective judgement per constituency), operates at zero recurring cost, and allows for seat-level projections (ADR 0005) without needing unavailable, granular demographic polling.
*   Because the model is arithmetic and uncalibrated, its outputs must always be framed as **Projections**, never Predictions.

## Future implications
*   If the user asks to "tweak the model for a specific seat", this must be rejected. The model is intentionally uniform at the state level.
*   Future lessons could cover how Sentiment is calculated, or how state election signals are blended in.
