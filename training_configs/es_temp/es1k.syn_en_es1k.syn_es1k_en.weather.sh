TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/train.es1k.syn_en_es.syn_es_en.1.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/eval-es.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/test-es.conllu \
allennlp train -s saved_models/es1k.syn_en_es..syn_es._en.weather training_configs/es_master.weather.jsonnet --include-package augment.dataset_readers
