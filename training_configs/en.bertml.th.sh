TRAIN_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/en/train-en.conllu \
DEV_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/eval-th.conllu \
TEST_DATA_PATH=data/multilingual_task_oriented_dialog_slotfilling/th/test-th.conllu \
allennlp train -s saved_models/en.bertml.th training_configs/en .bertml.th.jsonnet --include-package augment.dataset_readers
