{
    "dataset_reader": {
        "type": "conll2003",
        "token_indexers": {
            "token_characters": {
                "type": "characters"
            },
            "tokens": {
                "type": "single_id",
                "lowercase_tokens": true
            }
        }
    },
    "iterator": {
        "type": "basic",
        "batch_size": 8
    },
    "validation_iterator": {
        "type": "basic",
        "batch_size": 128
    },
    "model": {
        "type": "crf_tagger",
        "calculate_span_f1": true,
        "constrain_crf_decoding": true,
        "dropout": 0.5,
        "encoder": {
            "type": "lstm",
            "bidirectional": true,
            "dropout": 0.5,
            "hidden_size": 200,
            "input_size": 300 + 128 ,
            "num_layers": 1
        },
        "include_start_end_transitions": false,
        "label_encoding": "IOB1",
        "text_field_embedder": {
            "type": "basic",
            "token_embedders": {
                "tokens": {
                    "type": "embedding",
                    "embedding_dim": 300,
                    "pretrained_file": "/Users/mihirkale.s/Downloads/fasttext/wiki.multi.vec",
                    "trainable": false
                },
                "token_characters": {
                    "type": "character_encoding",
                    "embedding": {
                        "embedding_dim": 16
                    },
                    "encoder": {
                        "type": "cnn",
                        "conv_layer_activation": "relu",
                        "embedding_dim": 16,
                        "ngram_filter_sizes": [
                            3
                        ],
                        "num_filters": 128
                    }
                }
            }
        }
    },
    "train_data_path": std.extVar('NER_TRAIN_DATA_PATH'),
    "validation_data_path": std.extVar('NER_TEST_A_DATA_PATH'),
    "test_data_path": std.extVar('NER_TEST_B_DATA_PATH'),
    "trainer": {
        "cuda_device": -1,
        "grad_norm": 5,
        "num_epochs": 25,
        "num_serialized_models_to_keep": 3,
        "optimizer": {
            "type": "adam",
            "lr": 0.001
        },
        "patience": 25,
        "validation_metric": "+f1-measure-overall"
    },
    "validation_dataset_reader": {
        "type": "conll2003",
        "coding_scheme": "IOB1",
        "token_indexers": {
            "token_characters": {
                "type": "characters"
            },
            "tokens": {
                "type": "single_id",
                "lowercase_tokens": true
            }
        }
    }
}