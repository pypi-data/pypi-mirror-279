# Utterance Normalizer Plugin
Normalizes utterances by stripping quotes, trailing punctuation, normalization 
(numeric substitutions, expanded contractions), and removing articles.
Original utterances are preserved and returned utterances are returned in order:
1. No Punctuation, Normalized
2. No Punctuation, Normalized, Removed Articles
3. No Punctuation
4. Original Utterances
> Wrapping `"` symbols are removed from all normalized strings
## Configuration
This plugin can be enabled and configured as described below. By default, all
normalization is completed.

```yaml
utterance_transformers:
  neon_utterance_normalizer_plugin:
    remove_punctuation: True
    remove_articles: False
```