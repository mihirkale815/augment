from typing import Dict, List, Sequence, Iterable
import itertools
import logging
from overrides import overrides
from allennlp.common.checks import ConfigurationError
from allennlp.common.file_utils import cached_path
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import TextField, SequenceLabelField, Field, MetadataField
from allennlp.data.instance import Instance
from allennlp.data.token_indexers import TokenIndexer, SingleIdTokenIndexer
from allennlp.data.tokenizers import Token
from augment.data.instance import Instance as CustomInstance



logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _is_divider(line: str) -> bool:
    empty_line = line.strip() == ''
    if empty_line: return True
    if line.startswith("#") : return True
    return False

@DatasetReader.register("fb_xling")
class FacebookCrossLingualDialogueReader(DatasetReader):
    """
    Parameters
    ----------
    token_indexers : ``Dict[str, TokenIndexer]``, optional (default=``{"tokens": SingleIdTokenIndexer()}``)
        We use this to define the input representation for the text.  See :class:`TokenIndexer`.
    tag_label: ``str``, optional (default=``ner``)
        Specify `ner`, `pos`, or `chunk` to have that tag loaded into the instance field `tag`.
    feature_labels: ``Sequence[str]``, optional (default=``()``)
        These labels will be loaded as features into the corresponding instance fields:
        ``pos`` -> ``pos_tags``, ``chunk`` -> ``chunk_tags``, ``ner`` -> ``ner_tags``
        Each will have its own namespace: ``pos_tags``, ``chunk_tags``, ``ner_tags``.
        If you want to use one of the tags as a `feature` in your model, it should be
        specified here.
    coding_scheme: ``str``, optional (default=``IOB1``)
        Specifies the coding scheme for ``ner_labels`` and ``chunk_labels``.
        Valid options are ``IOB1`` and ``BIOUL``.  The ``IOB1`` default maintains
        the original IOB1 scheme in the CoNLL 2003 NER data.
        In the IOB1 scheme, I is a token inside a span, O is a token outside
        a span and B is the beginning of span immediately following another
        span of the same type.
    label_namespace: ``str``, optional (default=``labels``)
        Specifies the namespace for the chosen ``tag_label``.
    """
    _VALID_LABELS = {'ner', 'pos', 'chunk'}

    def __init__(self,
                 token_indexers: Dict[str, TokenIndexer] = None,
                 tag_label: str = "ner",
                 feature_labels: Sequence[str] = (),
                 lazy: bool = False,
                 coding_scheme: str = "BIO",
                 label_namespace: str = "labels",
                 domain_identifier: str = None) -> None:
        super().__init__(lazy)
        self._token_indexers = token_indexers or {'tokens': SingleIdTokenIndexer()}
        if tag_label is not None and tag_label not in self._VALID_LABELS:
            raise ConfigurationError("unknown tag label type: {}".format(tag_label))
        for label in feature_labels:
            if label not in self._VALID_LABELS:
                raise ConfigurationError("unknown feature label type: {}".format(label))
        if coding_scheme not in ("BIO"):
            raise ConfigurationError("unknown coding_scheme: {}".format(coding_scheme))

        self.tag_label = tag_label
        self.feature_labels = set(feature_labels)
        self.coding_scheme = coding_scheme
        self.label_namespace = label_namespace
        self._original_coding_scheme = "BIO"
        self.domain_identifier = domain_identifier

    @overrides
    def _read(self, file_path: str) -> Iterable[Instance]:
        # if `file_path` is a URL, redirect to the cache
        file_path = cached_path(file_path)
        num_yielded = 0
        counter = 0
        with open(file_path, "r") as data_file: #encoding='ISO-8859-1'
            logger.info("Reading instances from lines in file at: %s", file_path)
            if self.domain_identifier is not None:
                logger.info("Filtering to only include instances containing the %s domain", self.domain_identifier.upper())
            # Group into alternative divider / sentence chunks.
            for is_divider, lines in itertools.groupby(data_file, _is_divider):
                # Ignore the divider chunks, so that `lines` corresponds to the words
                # of a single sentence.
                if not is_divider:
                    counter+=1
                    fields = [line.strip().split("\t") for line in lines]
                    # unzipping trick returns tuples, but our Fields need lists
                    fields = [list(field) for field in zip(*fields)]
                    indices,tokens_,domain_intent,ner_tags = fields
                    domain,intent = domain_intent[0].strip(" ").split("/")
                    if self.domain_identifier is not None and self.domain_identifier != domain:
                        continue
                    ner_tags = [tag if tag!='NoLabel' else 'O' for tag in ner_tags ]
                    #instance = CustomInstance.from_lines([line for line in lines])
                    #ner_tags = instance.slot_labels
                    #tokens_ = instance.tokens
                    tokens = [Token(token.lower()) for token in tokens_]
                    num_yielded += 1
                    yield self.text_to_instance(tokens,ner_tags)
        print("num yielded = ",counter,num_yielded)
        #exit(-1)


    def text_to_instance(self, # type: ignore
                         tokens: List[Token],
                         ner_tags: List[str] = None) -> Instance:
        """
        We take `pre-tokenized` input here, because we don't have a tokenizer in this class.
        """
        # pylint: disable=arguments-differ
        sequence = TextField(tokens, self._token_indexers)
        instance_fields: Dict[str, Field] = {'tokens': sequence}
        instance_fields["metadata"] = MetadataField({"words": [x.text for x in tokens]})


        #print(ner_tags)
        coded_ner = ner_tags
        instance_fields['ner_tags'] = SequenceLabelField(coded_ner, sequence, "ner_tags")

        # Add "tag label" to instance
        if self.tag_label == 'ner' and coded_ner is not None:
            instance_fields['tags'] = SequenceLabelField(coded_ner, sequence,
                                                         self.label_namespace)
        return Instance(instance_fields)