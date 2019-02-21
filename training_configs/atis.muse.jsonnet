{
    "dataset_reader": {
        "type": "bio",
        "token_indexers": {
            "token_characters": {
                "type": "characters"
            },
            "tokens": {
                "type": "single_id",
                "lowercase_tokens": true
            },
        },
        
    },
    "iterator": {
        "type": "basic",
        "batch_size":8
    },
    "validation_iterator": {
        "type": "bucket",
        "sorting_keys": [
            [
                "tokens",
                "num_tokens"
            ]
        ],
        "batch_size":32
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
            "hidden_size": 100,
            "input_size": 300 + 64 ,
            "num_layers": 1
        },
        "include_start_end_transitions": false,
        "label_encoding": "BIO",
        "text_field_embedder": {
            "type": "basic",
            "token_embedders": {
                "tokens": {
                    "type": "embedding",
                    "embedding_dim": 300,
                    "pretrained_file":  "/home/mihirkale815/projects/fasttext/wiki.multi.en_tr.vec",
                    "trainable": true
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
                        "num_filters": 64
                    }
                }
            }
        }
    },
    "train_data_path": std.extVar('TRAIN_DATA_PATH'),
    "validation_data_path": std.extVar('DEV_DATA_PATH'),
    "test_data_path": std.extVar('TEST_DATA_PATH'),
    "evaluate_on_test" : true,
    "trainer": {
        "cuda_device": 0,
        "grad_norm": 5,
        "num_epochs": 50,
        "num_serialized_models_to_keep": 1,
        "optimizer": {
            "type": "adam",
            "lr": 0.001
        },
        "patience": 5,
        "validation_metric": "+f1-measure-overall"
    },
"random_seed": 2, "pytorch_seed": 2, "numpy_seed": 2 }
