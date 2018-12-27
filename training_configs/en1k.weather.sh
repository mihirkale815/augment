TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en1k/train-en1k.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en1k/eval-en.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en1k/test-en.conllu \
allennlp train -s saved_models/en1k.weather training_configs/en_master.weather.jsonnet --include-package augment.dataset_readers
