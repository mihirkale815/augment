import allennlp.data.dataset_readers.dataset_utils.span_utils as span_utils

class Instance():
    def __init__(self,text,lines,tokens,domain,intent,spans,slot_labels,slot_type_labels,slot_pos_labels,id):
        self.text = text
        self.lines = lines
        self.tokens = tokens
        self.domain = domain
        self.intent = intent
        self.spans = spans
        self.slot_labels = slot_labels
        self.slot_type_labels = slot_type_labels
        self.slot_pos_labels = slot_pos_labels
        self.id = id

    def to_lines(self,domain,intent,spans):
        if self.id == 'fb' : return FBDataUtils.to_lines(domain,intent,spans)
        elif self.id == 'snips': return BIODataUtils.to_lines(domain, intent, spans)

class FBDataUtils:

    @classmethod
    def extract_spans_old(cls,text,line):
        slots = line.strip("\n").split(" ")[2].strip(" ").split(",")
        spans = []
        prev_start_idx, prev_end_idx = 0, 0
        if slots == ['']: return spans
        for slot in slots:
            start_idx, end_idx, slot_type = slot.split(":")
            start_idx, end_idx = int(start_idx), int(end_idx)
            if start_idx - (prev_end_idx - 1) >= 3:
                span = text[prev_end_idx:start_idx].strip(" ")
                spans.append([span, "O"])
            spans.append([text[start_idx:end_idx].strip(), slot_type])
            prev_start_idx, prev_end_idx = start_idx, end_idx
        if prev_end_idx <= len(text) - 1: spans.append([text[prev_end_idx:].strip(), "O"])
        return spans

    @classmethod
    def extract_spans(cls,tokens,labels):
        spans = []
        labels = [label if label!='O' else 'B-O' for label in labels]
        span_labels = span_utils.bio_tags_to_spans(labels)
        span_labels = sorted(span_labels,key=lambda x:x[1])
        #print(tokens,labels,span_labels)
        for span_label,indices in span_labels:
            start_idx,end_idx = indices
            spans.append([" ".join(tokens[start_idx:end_idx+1]),span_label])
        return spans

    @classmethod
    def from_lines(cls,lines):
        text = lines[0].strip("\n").split(":")[1].strip(" ")

        tokens = []
        slot_type_labels = []
        slot_pos_labels = []
        slot_labels = []
        for line in lines[3:]:
            idx, token, domain_intent, slot_label = line.strip("\n").split("\t")
            domain,intent = domain_intent.strip().split("/")
            slot_label = slot_label.strip()
            if slot_label == 'NoLabel':
                slot_label,slot_pos_label, slot_type_label = "O", "O","O"
            else :
                slot_pos_label, slot_type_label = slot_label.split("-")

            tokens.append(token)
            slot_labels.append(slot_label)
            slot_type_labels.append(slot_type_label)
            slot_pos_labels.append(slot_pos_label)
        lines = [line.strip("\n") for line in lines]

        # spans = Instance.extract_spans(text,lines[2])
        spans = FBDataUtils.extract_spans(tokens,slot_labels)
        return Instance(text,lines,tokens,domain,intent,spans,slot_labels,slot_type_labels,slot_pos_labels,"fb")


    def to_lines_b(self):
        lines = self.lines[:3]
        for idx in range(len(self.tokens)):
            line = "\t".join([str(idx+1),self.tokens[idx],self.domain+"/"+self.intent,self.slot_labels[idx]])
            lines.append(line)
        lines = "\n".join(lines)
        return lines

    @classmethod
    def instance_gen(cls,path):
        f = open(path)
        elements = []
        for line in f:
            if line == "\n" and len(elements) > 0:
                yield cls.from_lines(elements)
                elements = []
            else:
                if line != "\n":
                    elements.append(line)

    @classmethod
    def to_lines(cls,domain, intent, spans):
        tokens = []
        slot_labels = []
        domain_intent = domain + "/" + intent
        slot_texts = []
        text = ""
        for span_text, span_label in spans:
            span_start_idx = len(text)
            for pos, token in enumerate(span_text.split()):
                if span_label != 'O':
                    if pos == 0:
                        slot_label = 'B-' + span_label
                    else:
                        slot_label = 'I-' + span_label
                else:
                    slot_label = 'NoLabel'
                text += token + " "
                tokens.append(token)
                slot_labels.append(slot_label)
            span_end_idx = len(text) - 1
            if span_label != 'O':
                slot_texts += [str(span_start_idx) + ":" + str(span_end_idx) + ":" + span_label]
        slot_text = "# slots: " + ",".join(slot_texts)

        lines = []
        lines.append("# text: " + text)
        lines.append("# intent: " + domain_intent)
        lines.append(slot_text)
        for idx in range(len(tokens)):
            line = "\t".join([str(idx + 1), tokens[idx], domain_intent, slot_labels[idx]])
            lines.append(line)

        return lines


class BIODataUtils:

    @classmethod
    def extract_spans(cls,tokens,labels):
        spans = []
        labels = [label if label!='O' else 'B-O' for label in labels]
        span_labels = span_utils.bio_tags_to_spans(labels)
        span_labels = sorted(span_labels,key=lambda x:x[1])
        for span_label,indices in span_labels:
            start_idx,end_idx = indices
            spans.append([" ".join(tokens[start_idx:end_idx+1]),span_label])
        return spans

    @classmethod
    def from_lines(cls,lines):
        tokens = []
        slot_type_labels = []
        slot_pos_labels = []
        slot_labels = []
        for line in lines:
            slot_label,token = line.strip("\n").split("\t")
            slot_label = slot_label.strip().upper()
            if slot_label == 'O':
                slot_label,slot_pos_label, slot_type_label = "O", "O","O"
            else :
                slot_pos_label, slot_type_label = slot_label.split("-")

            tokens.append(token)
            slot_labels.append(slot_label)
            slot_type_labels.append(slot_type_label)
            slot_pos_labels.append(slot_pos_label)
        lines = [line.strip("\n") for line in lines]

        spans = BIODataUtils.extract_spans(tokens,slot_labels)
        text =  " ".join(tokens)
        return Instance(text,lines,tokens,"","",spans,slot_labels,slot_type_labels,slot_pos_labels,'snips')

    @classmethod
    def to_lines(cls,domain,intent,spans):
        tokens = []
        slot_labels = []
        slot_texts = []
        text = ""
        for span_text, span_label in spans:
            for pos, token in enumerate(span_text.split()):
                if span_label != 'O':
                    if pos == 0:
                        slot_label = 'B-' + span_label
                    else:
                        slot_label = 'I-' + span_label
                else:
                    slot_label = 'O'
                tokens.append(token)
                slot_labels.append(slot_label)

        lines = []
        for idx in range(len(tokens)):
            line = "\t".join([slot_labels[idx],tokens[idx]])
            lines.append(line)

        return lines

    @classmethod
    def instance_gen(cls,path):
        f = open(path)
        elements = []
        for line in f:
            if line == "\n" and len(elements) > 0:
                yield cls.from_lines(elements)
                elements = []
            else:
                if line != "\n":
                    elements.append(line)







#igen = instance_gen("data/multilingual_task_oriented_dialog_slotfilling/th/train-th.conllu")
#for instance in igen:
#    print(instance.text,instance.spans)