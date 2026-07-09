# Review Ledger

Generated: 2026-07-10
Source packet generated: 2026-07-10
Source trend generated: 2026-07-10
Source scenario generated: 2026-07-10

## Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.

## Summary

- Total items: 14
- By status: new: 11, open: 1, resolved: 1, watch: 1
- By severity: high: 7, medium: 4, severe: 3
- Stale items: GOOGL|persistent_warning|hist-regulatory-ads-2026-06-12, MSFT|scenario_stress|scn-cloud-margin-compression

## Ticker Summary

| Ticker | Total | Status | Severity |
| --- | ---: | --- | --- |
| AAPL | 1 | new: 1 | high: 1 |
| GOOGL | 5 | new: 4, open: 1 | high: 1, medium: 1, severe: 3 |
| META | 1 | resolved: 1 | high: 1 |
| MSFT | 4 | new: 3, watch: 1 | high: 2, medium: 2 |
| NVDA | 3 | new: 3 | high: 2, medium: 1 |

## Review Items

### GOOGL - persistent_warning - hist-regulatory-ads-2026-06-12

- Key: `GOOGL|persistent_warning|hist-regulatory-ads-2026-06-12`
- Status: open
- Severity: severe
- First seen: 2026-07-03
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 7
- Stale: true
- Next action: Resolve the repeated GOOGL warning with updated local evidence or mark why it remains valid.

Evidence links:
- `demo/trend/trend_history.json` [2026-06-26_packet, 2026-07-03_packet, 2026-07-10_packet]: hist-regulatory-ads-2026-06-12: source remained stale across 3 periods

### GOOGL - scenario_stress - scn-cloud-margin-compression

- Key: `GOOGL|scenario_stress|scn-cloud-margin-compression`
- Status: new
- Severity: severe
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 7
- Stale: false
- Next action: Document whether the GOOGL thesis still holds under the static scn-cloud-margin-compression stress case.

Evidence links:
- `demo/scenario/scenario_stress.json` [scn-cloud-margin-compression]: severe risk; stress score 100: Check whether matched stress shocks add a separate reason for GOOGL thesis pressure or duplicate an existing concern.

### GOOGL - scenario_stress - scn-regulatory-ad-tightening

- Key: `GOOGL|scenario_stress|scn-regulatory-ad-tightening`
- Status: new
- Severity: severe
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 7
- Stale: false
- Next action: Document whether the GOOGL thesis still holds under the static scn-regulatory-ad-tightening stress case.

Evidence links:
- `demo/scenario/scenario_stress.json` [scn-regulatory-ad-tightening]: severe risk; stress score 100: Check whether matched stress shocks add a separate reason for GOOGL thesis pressure or duplicate an existing concern.

### AAPL - scenario_stress - scn-premium-device-demand

- Key: `AAPL|scenario_stress|scn-premium-device-demand`
- Status: new
- Severity: high
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 14
- Stale: false
- Next action: Document whether the AAPL thesis still holds under the static scn-premium-device-demand stress case.

Evidence links:
- `demo/scenario/scenario_stress.json` [scn-premium-device-demand]: high risk; stress score 88: Clarify whether matched stress shocks turn the current AAPL read into a directional thesis question.

### GOOGL - packet_warning - evt-regulatory-ads-2026-06-20

- Key: `GOOGL|packet_warning|evt-regulatory-ads-2026-06-20`
- Status: new
- Severity: high
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 14
- Stale: false
- Next action: Refresh or document the static source behind evt-regulatory-ads-2026-06-20 before relying on this review packet.

Evidence links:
- `demo/impact_packet.json` [evt-regulatory-ads-2026-06-20]: evt-regulatory-ads-2026-06-20: source is 20 days old

### META - attention_review - impact_packet_review_queue

- Key: `META|attention_review|impact_packet_review_queue`
- Status: resolved
- Severity: high
- First seen: 2026-07-03
- Latest seen: 2026-07-03
- Resolved at: 2026-07-10
- Expiry days: 14
- Stale: false
- Next action: Keep prior evidence for audit trail; no current packet, trend, or scenario evidence matched this issue.

Evidence links:
- `demo/impact_packet.json` [review_queue]: attention score 64: Review whether META thesis sensitivities still match events old-social-ads-review.

### MSFT - scenario_stress - scn-ai-capex-digestion

- Key: `MSFT|scenario_stress|scn-ai-capex-digestion`
- Status: new
- Severity: high
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 14
- Stale: false
- Next action: Document whether the MSFT thesis still holds under the static scn-ai-capex-digestion stress case.

Evidence links:
- `demo/scenario/scenario_stress.json` [scn-ai-capex-digestion]: high risk; stress score 100: Test whether the current positive read for MSFT still holds under the matched stress shocks.

### MSFT - scenario_stress - scn-cloud-margin-compression

- Key: `MSFT|scenario_stress|scn-cloud-margin-compression`
- Status: watch
- Severity: high
- First seen: 2026-06-26
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 14
- Stale: true
- Next action: Document whether the MSFT thesis still holds under the static scn-cloud-margin-compression stress case.

Evidence links:
- `demo/scenario/scenario_stress.json` [scn-cloud-margin-compression]: high risk; stress score 100: Test whether the current positive read for MSFT still holds under the matched stress shocks.

### NVDA - attention_review - impact_packet_review_queue

- Key: `NVDA|attention_review|impact_packet_review_queue`
- Status: new
- Severity: high
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 14
- Stale: false
- Next action: Re-read the current NVDA thesis claims and record whether the static catalyst changes the research note.

Evidence links:
- `demo/impact_packet.json` [review_queue]: attention score 67: Review whether NVDA thesis sensitivities still match events evt-supply-chain-2026-07-03, evt-cloud-margin-2026-07-08.

### NVDA - scenario_stress - scn-ai-capex-digestion

- Key: `NVDA|scenario_stress|scn-ai-capex-digestion`
- Status: new
- Severity: high
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 14
- Stale: false
- Next action: Document whether the NVDA thesis still holds under the static scn-ai-capex-digestion stress case.

Evidence links:
- `demo/scenario/scenario_stress.json` [scn-ai-capex-digestion]: high risk; stress score 100: Test whether the current positive read for NVDA still holds under the matched stress shocks.

### GOOGL - trend_change - changed

- Key: `GOOGL|trend_change|changed`
- Status: new
- Severity: medium
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 21
- Stale: false
- Next action: Compare the latest GOOGL packet against prior periods and update the research note if the change is material.

Evidence links:
- `demo/trend/trend_history.json` [next_review_queue]: changed; score increased; exposure decreased

### MSFT - attention_review - impact_packet_review_queue

- Key: `MSFT|attention_review|impact_packet_review_queue`
- Status: new
- Severity: medium
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 21
- Stale: false
- Next action: Re-read the current MSFT thesis claims and record whether the static catalyst changes the research note.

Evidence links:
- `demo/impact_packet.json` [review_queue]: attention score 60: Review whether MSFT thesis sensitivities still match events evt-cloud-margin-2026-07-08.

### MSFT - trend_change - changed

- Key: `MSFT|trend_change|changed`
- Status: new
- Severity: medium
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 21
- Stale: false
- Next action: Compare the latest MSFT packet against prior periods and update the research note if the change is material.

Evidence links:
- `demo/trend/trend_history.json` [next_review_queue]: changed; score increased; exposure increased

### NVDA - trend_change - changed

- Key: `NVDA|trend_change|changed`
- Status: new
- Severity: medium
- First seen: 2026-07-10
- Latest seen: 2026-07-10
- Resolved at: not resolved
- Expiry days: 21
- Stale: false
- Next action: Compare the latest NVDA packet against prior periods and update the research note if the change is material.

Evidence links:
- `demo/trend/trend_history.json` [next_review_queue]: changed; score increased; exposure increased
