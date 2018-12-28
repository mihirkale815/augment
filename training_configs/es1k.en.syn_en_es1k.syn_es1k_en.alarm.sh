TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/train.es1k.en.syn_en_es.syn_es_en.1.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/eval-es.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/es1k/test-es.conllu \
allennlp train -s saved_models/es1k.en.syn_en_es..syn_es._en.alarm training_configs/es_master.alarm.jsonnet --include-package augment.dataset_readers
