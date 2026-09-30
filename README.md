# Signal Desk — Reddit integration review

Signal Desk is a local personal desktop/browser prototype for stock and defined-risk options analysis. This repository contains the relevant read-only Reddit adapter, ticker/sentiment processing, and retention excerpts for review. It is not the full application and does not claim Reddit endorsement or approved access.

## Intended use

Subject to explicit approval, periodically read public posts from r/stocks and r/options through the official OAuth API. Extract ticker mentions and aggregate lexicon sentiment and mention frequency over successive 24-hour windows. Combine those indicators with independently sourced market/options data to rank defined-risk simulated trades and evaluate timestamped outcomes. Initial use is paper trading; the intended eventual purpose is informing the owner's investment decisions.

The application runs outside Reddit. It does not provide a direct in-Reddit service. Guidance is requested on whether this workflow can be supported through Devvit or needs separate Data API approval. No permission is inferred from an account, OAuth token or creation of this repository.

## Code included

* `reddit_adapter.py`: exact adapter logic extracted from the prototype, with standalone imports. Uses only read requests to `oauth.reddit.com/r/{subreddit}/new`. Requests at most 100 recent posts per subreddit per poll, bounded retries, and an identifying user agent. It requires `reddit_permitted` to be explicitly enabled and an authorized token to be supplied locally. No runnable collection command is provided in this review package.
* `features.py`: the prototype's ticker extraction and simple sentiment lexicon. No language model or AI training. Multiple tickers in a post receive the same post-level sentiment, a known limitation.
* `retention.py`: the prototype's timestamp-based community retention purge. This requires the application's SQLite schema and is provided for inspection, not standalone execution. It removes older community text and mention rows; signal aggregates remain.
* `test_review.py`: offline tests with invented text. Does not contact Reddit.

## Data and behavior

The adapter returns post identifiers, subreddit/source, text, publication time and observation time. It does not return usernames, private messages or user profiles. The application deduplicates by source/post ID and ticker, stores ticker-level aggregates, and distinguishes observed market data from model estimates. It performs no posting, commenting, voting, messaging or moderation actions.

Default proposed scope is r/stocks and r/options. The prototype's continuous mode currently polls no more often than every five minutes and retains raw community text/mentions for seven days. These are provisional configuration defaults, not asserted Reddit permissions; approved frequency, retention and deletion requirements take precedence.

The prototype skips items marked removed/deleted at collection and supports age-based purging. It **does not yet implement deletion-event synchronization**. Necessary deletion compliance, authorization/token refresh and any other conditions must be completed before collection begins. The adapter currently accepts a manually supplied OAuth access token; it does not automate account login or collect passwords.

Any future AI processing, additional communities, commercial use or redistribution would be subject to separately confirmed permission. No live trading execution or automatic orders exist in this review package. Lexicon sentiment and simulated results do not establish profitability.

## Offline verification

Requires Python 3.11 or newer; no external dependencies.

```sh
python -m unittest -v test_review.py
```

This repository contains no API tokens, passwords, account details, downloaded Reddit content, market data, databases or local machine paths. It is intended to support an access review, not to bypass approval.
