from collections import namedtuple

import spacy

from sovrinxplore import utils
from sovrinxplore.strats.base import Base


class Spacy(Base):
    def train(self, silent: bool):
        """ Spacy is pre-trained, we load the English pre-trained pipeline """
        self.schemas = utils.load_schemas(self.ledger, silent)
        self.norm = utils.normalize_schemas([schema['value'] for schema in self.schemas])
        
        # exclude ner and parser reduces the time to query in 50% and apparently doesn't affect f-score
        self.nlp = spacy.load('en_core_web_md', exclude=['ner', 'parser'])

    def predict(self, query: str, limit: int, min_score: float, seq_only: bool = False):
        columns = ['seqNo', 'values'] if limit == 0 else ['score', 'seqNo', 'values']
        named = namedtuple('Result', columns)
        
        if limit == 0:
            schemas = sorted(self.schemas, key=lambda i: i['key'])
            results = [s['key'] if seq_only else named(s['key'], s['value']) for s in schemas]
        else:
            query = self.nlp(query)

            sims = self.nlp.pipe(i for i in self.norm)
            sims = (i.similarity(query) if i.vector_norm else 0 for i in sims)
            sims = enumerate(sims)
            sims = sorted(sims, key=lambda i: i[1], reverse=True)

            results = []
            for i in range(min(limit, len(self.schemas))):
                idx, score = sims[i]
                
                if score < min_score:
                    continue
                     
                sch = self.schemas[idx]

                results.append(sch['key'] if seq_only else named(score, sch['key'], sch['value']))
                
        return results
