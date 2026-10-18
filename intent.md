# Product Intent: TrendFlow

## Purpose

TrendFlow (awesome_trading) aims to be a trading decision-support platform
for stocks and cryptocurrencies. It should help me understand market
conditions, identify potential trading opportunities, and evaluate strategies
before deciding whether to act.

The goal is to support informed, disciplined decisions, not to predict markets
with certainty or guarantee profits. This document describes the intended
product, not a claim that every capability is already available.

## Intended User

The primary user is an individual trader who wants to combine visual market
analysis, relevant alerts, and historical strategy evaluation in one platform
while retaining control over every trading decision.

## Core Capabilities

### Trading Charts and Financial Indicators

Provide trading charts that bring price movements, volume, and financial
indicators together. Indicators such as MM30 should help the user understand
trends and assess potential entry or exit conditions in context.

The user should be able to understand what an indicator represents and how it
contributes to a strategy signal, rather than treating it as an unexplained
instruction to buy or sell.

### Trading Alerts

Notify the user when relevant market or strategy conditions are met, through
a communication channel such as Telegram. Alerts should help the user notice
opportunities without continuously watching the charts.

An alert should identify the asset, the triggering condition, and the time of
the observation so the user can review the signal in context before deciding
whether to act. An alert is a prompt for analysis, not an order.

### Strategy Backtesting

Allow the user to evaluate a trading strategy against historical market data
before relying on its signals. Backtesting should help assess both potential
returns and risk, with results such as total return, maximum drawdown, and
win rate.

Results should make the evaluated period and assumptions clear. Historical
performance is evidence for analysis, not a promise of future results.

MM30 and Telegram are illustrative examples, not mandatory indicator or
channel choices.

## Decision-Support Workflow

1. Explore an asset through its chart and indicators to understand market
   conditions and form a strategy idea.
2. Backtest the strategy to examine its historical behavior and risks.
3. Use alerts to notice when relevant conditions occur, then return to the
   chart to review the current context.
4. Decide independently whether to trade, wait, or take no action.

## Principles and Boundaries

- **Human control:** The user makes every trading decision. Automated order
  execution and broker integration for placing trades are outside this scope.
- **Transparency:** Indicators, signals, alerts, and backtest results should
  be understandable and traceable to their underlying data and assumptions.
- **Data awareness:** Missing, stale, or insufficient data should be visible,
  rather than presented as reliable analysis.
- **Responsible evaluation:** Backtesting should avoid using future
  information and make limitations, including trading-cost assumptions and
  the risk of overfitting, clear.
- **Focused scope:** This intent defines the product's purpose and core
  capabilities, not a technical architecture, fixed provider, or detailed
  implementation roadmap.

## What Success Looks Like

The platform succeeds when the user can:

- Understand an asset's price behavior using charts and indicators together.
- Receive a relevant alert and understand why it was triggered.
- Evaluate a strategy's historical returns and downside before using it.
- Connect visual analysis, historical evidence, and alerts to make a
  deliberate decision, including choosing not to trade.
