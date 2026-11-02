# Judge file r2-langchain-1.4.3

## PUBLISHED RELEASE NOTES (written by the maintainers)

Changes since langchain==1.4.2

release(langchain): 1.4.3 (#40888)
fix(langchain): sanitize cache settings for fallback models (#40886)
feat(langchain): support Bedrock Mantle chat models in `init_chat_model` (#40837)
fix(langchain): recognize GPT-6 structured output without profiles (#40844)
docs(infra): fix AGENTS.md root setup guidance and package doc accuracy (#40794)
fix(langchain): repair invalid tool calls in `create_agent` (#40530)
chore(langchain): remove commented-out cohere extra (#40713)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/langchain_v1 (#40626)

## COMMIT SUBJECTS between the previous tag and the release

chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/huggingface (#40637)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/fireworks (#40639)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/deepseek (#40641)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/chroma (#40642)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/exa (#40640)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/groq (#40638)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/openai (#40629)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/mistralai (#40636)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/nomic (#40635)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/perplexity (#40633)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/ollama (#40632)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/qdrant (#40631)
chore(deps): bump anyio from 4.13.0 to 4.14.2 in /libs/partners/openrouter (#40627)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/anthropic (#40643)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/partners/xai (#40628)
chore(deps): bump anyio from 4.12.0 to 4.14.2 in /libs/core (#40634)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/langchain (#40630)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/langchain_v1 (#40626)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/text-splitters (#40624)
chore(deps): bump anyio from 4.11.0 to 4.14.2 in /libs/model-profiles (#40623)
chore(deps): bump anyio from 4.12.0 to 4.14.2 in /libs/standard-tests (#40625)
chore(deps): bump anyio from 4.14.2 to 4.15.1 in /libs/model-profiles (#40647)
chore(deps): bump anyio from 4.14.2 to 4.15.1 in /libs/text-splitters (#40645)
chore(deps): bump anyio from 4.14.2 to 4.15.1 in /libs/standard-tests (#40646)
chore(model-profiles): refresh model profile data (#40665)
feat(anthropic): send mid-conversation `SystemMessage`s in place (#40622)
feat(typesafe): make classifier questions invocation-scoped (#40659)
chore(model-profiles): refresh model profile data (#40685)
release(typesafe): 0.0.1a3 (#40693)
chore(model-profiles): refresh model profile data (#40705)
chore(core): deprecate chat message history (#40711)
chore(langchain): remove commented-out cohere extra (#40713)
fix(openai): expose inferred Responses API routing at initialization (#40715)
release(core): 1.6.4 (#40718)
docs: update OpenWiki (#40359)
release(openai): 1.6.3 (#40719)
release(openrouter): 0.2.9 (#40736)
release(fireworks): 1.6.2 (#40735)
release(deepseek): 1.1.1 (#40734)
hotfix(fireworks): use available model in LLM tests (#40737)
fix(deepseek,infra): resolve compatible minimum OpenAI dependencies, bump min ver (#40738)
fix(fireworks): use current completions model in LLM tests (#40740)
chore(model-profiles): refresh model profile data (#40747)
chore(anthropic): update docs for Opus 5.5 (#40765)
fix(anthropic): auto-route `with_structured_output` to `method="json_schema"` for fable and opus 5.5 (#40766)
fix(langchain): repair invalid tool calls in `create_agent` (#40530)
chore(model-profiles): refresh anthropic model profile data (#40772)
release(anthropic): 1.7.3 (#40773)
chore(model-profiles): refresh openai model profile data (#40774)
release(openai): 1.6.4 (#40775)
docs: update OpenWiki (#40750)
chore(infra): remove Claude instructions and sync workflow (#40779)
chore(model-profiles): refresh model profile data (#40780)
feat(anthropic,openai): mid-conversation tool changes on `SystemMessage` (#40758)
fix(anthropic): add Opus 5.5 and GPT-6 profile augmentations (#40785)
release(anthropic): 1.7.4 (#40786)
release(openai): 1.6.5 (#40787)
chore(anthropic): fix integration test cassette (#40790)
fix(core): abbreviate long tool IDs in XML buffer strings (#40792)
fix(openai): raise on error events in stream path (#40791)
docs(infra): fix AGENTS.md root setup guidance and package doc accuracy (#40794)
release(openai): 1.6.6 (#40800)
chore(model-profiles): refresh model profile data (#40804)
release(core): 1.6.5 (#40816)
fix(fireworks): preserve malformed tool arguments as diagnostic JSON (#40818)
feat(openai): discover Azure workload identity (#40532)
fix(fireworks): declare native PDF inputs unsupported (#40814)
release(fireworks): 1.6.3 (#40834)
fix(langchain): recognize GPT-6 structured output without profiles (#40844)
docs(core): fix docstring examples that don't run as copied (#40815)
feat(langchain): support Bedrock Mantle chat models in `init_chat_model` (#40837)
fix(anthropic): serialize invalid tool calls as tool use on replay (#40864)
chore(model-profiles): refresh model profile data (#40833)
chore(model-profiles): refresh model profile data (#40869)
docs: update OpenWiki (#40781)
fix(fireworks): classify mid-stream read timeouts (#40874)
feat(fireworks): add prompt caching middleware (#38823)
fix(langchain): sanitize cache settings for fallback models (#40886)
release(langchain): 1.4.3 (#40888)

# CANDIDATE A

## What's changed in langchain 1.4.3

### New features

- `init_chat_model` now supports AWS Bedrock Mantle through two new providers, `bedrock_mantle_openai` and `bedrock_mantle_anthropic`; this requires `langchain-aws>=1.7.9`. ([#40837](https://github.com/langchain-ai/langchain/pull/40837))

### Bug fixes

- `create_agent` now adds an error tool result for each malformed tool call, so conversations can be resumed and replayed safely. ([#40530](https://github.com/langchain-ai/langchain/pull/40530))
- `create_agent` now uses provider-native structured output for GPT-6 Sol, Luna, and Astra models when no model profile is available. ([#40844](https://github.com/langchain-ai/langchain/pull/40844))
- `ModelFallbackMiddleware` now strips cache settings the fallback model doesn't support, so fallbacks no longer fail on them. ([#40886](https://github.com/langchain-ai/langchain/pull/40886))

### Other

- Removed a commented-out `cohere` extra from the package metadata. ([#40713](https://github.com/langchain-ai/langchain/pull/40713))
- Routine dependency bumps, release housekeeping, and test updates.
- Related changes in partner packages (Anthropic, OpenAI, Fireworks, and others) and `langchain-core` ship in their own releases.


# CANDIDATE B

## What's changed

### Features

- `init_chat_model` now supports AWS Bedrock Mantle through two new providers, `bedrock_mantle_openai` and `bedrock_mantle_anthropic`; requires `langchain-aws>=1.7.9`. ([#40837](https://github.com/langchain-ai/langchain/pull/40837))

### Fixes

- `create_agent` now adds an error tool result for each malformed tool call, so conversations can be safely resumed and replayed with providers. ([#40530](https://github.com/langchain-ai/langchain/pull/40530))
- Agents using GPT-6 Sol, Luna, or Astra without model profiles now default to provider-native structured output. ([#40844](https://github.com/langchain-ai/langchain/pull/40844))
- `ModelFallbackMiddleware` now removes cache settings (`prompt_cache_key`, `x-session-affinity`) that a fallback model doesn't support, so fallbacks no longer fail on them. ([#40886](https://github.com/langchain-ai/langchain/pull/40886))

### Other

- Removed a commented-out `cohere` extra from package metadata. ([#40713](https://github.com/langchain-ai/langchain/pull/40713))
- Updated `AGENTS.md` setup guidance and package docs. ([#40794](https://github.com/langchain-ai/langchain/pull/40794))
- Version bump to 1.4.3. ([#40888](https://github.com/langchain-ai/langchain/pull/40888))

