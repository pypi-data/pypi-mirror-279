# # NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# # All trademark and other rights reserved by their respective owners
# # Copyright 2008-2021 Neongecko.com Inc.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import lingua_franca.config

from typing import List, Optional
from lingua_franca.parse import normalize
from ovos_config import Configuration

from neon_transformers import UtteranceTransformer
from neon_transformers.tasks import UtteranceTask


class UtteranceNormalizer(UtteranceTransformer):
    task = UtteranceTask.TRANSFORM

    def __init__(self, name: str = "neon_utterance_normalizer_plugin",
                 priority: int = 1,
                 config: Optional[dict] = None):
        super().__init__(name, priority, config)
        self.config_core = Configuration()
        lingua_franca.config.load_langs_on_demand = True

    def transform(self, utterances: List[str],
                  context: Optional[dict] = None) -> (list, dict):
        """
        Normalize and return an ordered list of utterances
        @param utterances: List of utterances to be normalized
        @param context: Utterance context (unused)
        @returns: Ordered list of normalized + raw utterances, dict context
        """
        context = context or {}
        lang = context.get("lang") or self.config_core.get("lang", "en-us")
        remove_punctuation = self.config.get("remove_punctuation", True)
        remove_articles = self.config.get("remove_articles", True)
        clean = []
        norm = []
        norm2 = []
        for utt in utterances:
            # Strip any enclosing quotes
            utt = utt.strip('"')
            # Strip punctuation first and add NEW strings to clean
            if remove_punctuation:
                utt = self._strip_punctuation(utt)
                if not any((utt in utterances, utt in clean)):
                    clean.append(utt)

            # Do basic normalization next and add NEW strings to norm
            normal = normalize(utt, lang=lang, remove_articles=False)
            if not any((normal in utterances, normal in norm)):
                norm.append(normal)

            # Remove articles and add NEW strings to norm2
            if remove_articles:
                normal = normalize(utt, lang=lang, remove_articles=True)
                if normal not in utterances:
                    norm2.append(normal)

        # Append no-article normalization and punctuation cleaned to end of list
        norm += [u for u in norm2 + clean if u not in norm]
        return (norm + utterances,
                {"normalization": {"remove_punctuation": remove_punctuation,
                                   "remove_articles": remove_articles}})

    @staticmethod
    def _strip_punctuation(utterance: str):
        return utterance.rstrip('.').rstrip('?').rstrip('!')
