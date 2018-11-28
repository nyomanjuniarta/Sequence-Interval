import itertools

def pattern_parser(raw_entry='', separator='-1'):
    if len(raw_entry) > 0:
        try:
            # THIS IS THE PARSE FOR SPMF FILES
            return [[float(j) for j in i.strip().split()] for i in raw_entry.replace('-1 -2', '').strip().split(separator)]
        except:
            print 'ERROR: Trying to parse :{}'.format(raw_entry)
            exit()
    else:
        return []


def spmf2tuple(atts):
    # print 'pattern parser = ', atts
    # return {(i+1,): j for i, j in enumerate(atts)}
    sequence = []
    sequences = []
    for j in atts:
        sequence.append([j[0], j[0], j[1], j[1]])
    sequences.append(sequence)
    return sequences


class PatternConfig:
    def __init__(self, theta=1):
        self.theta = theta


class Pattern:
    def __init__(self, atts={}, dirty=True, config=None, separator=' ', object=-1):
        self.objects = []
        self.sequences = []
        if not config:
            self.cfg = PatternConfig(1)
        else:
            self.cfg = config

        if dirty:
            self.sequences = spmf2tuple(pattern_parser(atts))
            self.objects.append(object)
        else:
            if len(atts) != 0:
                print("!!!@@!#" * 10)
            self.sequences = []

    def intersect(self, p):
        pi = Pattern(atts={}, config=self.cfg, dirty=False)
        pi.sequences = []

        for seq1 in self.sequences:
            for seq2 in p.sequences:
                #print seq1, 'dan', seq2
                self.common(seq1, seq2, pi.sequences)
        return pi

    def common(self, seq1, seq2, common_sequences):
        same = set()
        for i, item1 in enumerate(seq1):
            for j, item2 in enumerate(seq2):
                if max(item1[1], item2[1]) - min(item1[0], item2[0]) <= self.cfg.theta and max(item1[3], item2[3]) - min(item1[2], item2[2]) <= self.cfg.theta and (i, j) not in same:
                    same.add((i,j))
                    common_sequences.append(self.iterate_sequence(seq1, seq2, i, j, same))
        same.clear()
        #print 'common', common_sequences
        return common_sequences

    def iterate_sequence(self, seq1, seq2, start1, start2, same):
        common_sequence = [self.convex(seq1[start1], seq2[start2])]
        counter = 1
        for item1, item2 in itertools.izip(seq1[start1+1:], seq2[start2+1:]):
            if max(item1[1], item2[1]) - min(item1[0], item2[0]) <= self.cfg.theta and max(item1[3], item2[3]) - min(item1[2], item2[2]) <= self.cfg.theta and (start1+counter, start2+counter) not in same:
                same.add((start1+counter, start2+counter))
                common_sequence.append(self.convex(item1, item2))
            else:
                break
            counter += 1
        #print 'iterate_sequence', common_sequence
        return common_sequence

    def convex(self, itemset1, itemset2):
        return [min(itemset1[0], itemset2[0]), max(itemset1[1], itemset2[1]), min(itemset1[2], itemset2[2]), max(itemset1[3], itemset2[3])]

    def __eq__(self, p):
        for seq1 in self.sequences:
            equal = False
            for seq2 in p.sequences:
                if seq1 == seq2:
                    equal = True
                    break
            if not equal:
                return False
        return True

    def __le__(self, p):
        for seq1 in self.sequences:
            subsumed = False
            for seq2 in p.sequences:
                if self.subsequence_of(seq1, seq2):
                    subsumed = True
                    break
            if not subsumed:
                return False
        return True

    def subsequence_of(self, seq1, seq2):
        if len(seq1) > len(seq2):
            return False
        for idx2 in xrange(0, len(seq2) - len(seq1) + 1):
            subseq = True
            for idx1 in xrange(0, len(seq1)):
                if seq1[idx1][0] < seq2[idx2+idx1][0] or seq1[idx1][1] > seq2[idx2+idx1][1] or seq1[idx1][2] < seq2[idx2+idx1][2] or seq1[idx1][3] > seq2[idx2+idx1][3]:
                    subseq = False
                    break
            if subseq:
                return subseq
        return False

    def size(self):
        return len(self.sequences)

    def __repr__(self):
        output = ""
        for s in self.sequences:
            output += str(s) + '@'
        return str(output[:-1])
