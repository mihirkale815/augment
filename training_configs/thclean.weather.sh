TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th_clean/train-th.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th_clean/eval-th.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th_clean/test-th.conllu \
allennlp train -s saved_models/thclean.weather training_configs/th_master.weather.jsonnet --include-package augment.dataset_readers
