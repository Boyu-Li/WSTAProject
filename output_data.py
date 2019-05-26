import os
import pickle
import csv
import json

class Outputing(object):
    def __init__(self):
        self.outputdir = './output'
        self.pickledir = './pickles'
        self.labels = ['SUPPORTS', 'REFUTES', 'NOT ENOUGH INFO']

    def output_test(self):
        def maxf(a):
            b = []
            for i in a:
                b.append(float(i))
            return b.index(max(b))
        labels = []
        with open(os.path.join(self.outputdir, 'test_results.tsv')) as f:
            output = csv.reader(f, delimiter='\t')
            for line in output:
                label = self.labels[maxf(line)]
                labels.append(label)

        #labels = [labels[i: i + 10] for i in range(0, len(labels) - 9, 3)]
        pickle_file_dir = os.path.join(self.pickledir, 'test-5-24-randomdev.txt')
        with open(pickle_file_dir, 'rb') as f:
            df = pickle.load(f)
        output = {}
        for i in range(0, len(labels) - 9, 10):
            sub = labels[i: i + 10]
            scores = [df.loc[[i + j], 'score'].values[0] for j in range(10)]
            s = list(filter(lambda x: x[1] == 'SUPPORTS', enumerate(sub)))
            r = list(filter(lambda x: x[1] == 'REFUTES', enumerate(sub)))
            n = list(filter(lambda x: x[1] == 'NOT ENOUGH INFO', enumerate(sub)))
            sc = [float(df.loc[[i+j[0]], 'score']) for j in s]
            rc = [float(df.loc[[i+j[0]], 'score']) for j in r]
            nc = [float(df.loc[[i+j[0]], 'score']) for j in n]
            if len(sc)==0:
                sc.append(0)
            if len(rc) == 0:
                rc.append(0)
            maxc = float(df.loc[i, 'score'])
            if sc[0] >= rc[0] and (sc[0] >= maxc-11 or len(s) >= 2):
                evidences = []
                for j in s:
                    es = df.loc[[i + j[0]], 'docname'].values[0].split(' ')
                    cf = []
                    cf.append(es[0])
                    cf.append(int(es[1]))
                    evidences.append(cf)

                output[df.loc[[i], ['id']].values[0][0]] = {'claim': df.loc[[i], ['claim']].values[0][0],
                                                                 'label': 'SUPPORTS',
                                                                 'evidence': evidences}
            elif rc[0] >= maxc-11 or len(r) >= 2:
                evidences = []
                for j in r:
                    es = df.loc[[i + j[0]], 'docname'].values[0].split(' ')
                    cf = []
                    cf.append(es[0])
                    cf.append(int(es[1]))
                    evidences.append(cf)
                output[df.loc[[i], ['id']].values[0][0]] = {'claim': df.loc[[i], ['claim']].values[0][0],
                                                                     'label': 'REFUTES',
                                                                     'evidence': evidences}
            else:
                output[df.loc[[i], ['id']].values[0][0]] = {'claim': df.loc[[i], ['claim']].values[0][0],
                                                                     'label': 'NOT ENOUGH INFO',
                                                                     'evidence': []}

        with open(os.path.join(self.outputdir, 'test_results.json'), 'w') as f:
            json.dump(output, f)

    def output_test_all(self):
        def maxf(a):
            b = []
            for i in a:
                b.append(float(i))
            return b.index(max(b))
        labels = []
        with open(os.path.join(self.outputdir, 'test_results.tsv')) as f:
            output = csv.reader(f, delimiter='\t')
            for line in output:
                label = self.labels[maxf(line)]
                labels.append(label)

        #labels = [labels[i: i + 10] for i in range(0, len(labels) - 9, 3)]
        pickle_file_dir = os.path.join(self.pickledir, 'test.txt')
        with open(pickle_file_dir, 'rb') as f:
            df = pickle.load(f)
        output = {}
        n = 0
        for i in range(0, len(labels) - 9, 10):
            sub = labels[i: i + 10]
            for j in range(10):
                if labels[i+j]=='SUPPORTS':
                    r = list(filter(lambda x: x[1] == 'REFUTES', enumerate(sub)))
                    evidences = [df.loc[[i + j[0]], 'docname'].values[0] for j in r]
                    d = {'claim': df.loc[[i], ['claim']].values[0][0],
                                                            'label': 'SUPPORTS','score':df.loc[[i+j], ['score']].values[0][0],
                                                            'evidence': df.loc[[i+j], ['docname']].values[0][0]}
                elif labels[i+j]=='REFUTES':
                    r = list(filter(lambda x: x[1] == 'REFUTES', enumerate(sub)))
                    evidences = [df.loc[[i + j[0]], 'docname'].values[0] for j in r]
                    d = {'claim': df.loc[[i], ['claim']].values[0][0],
                                                            'label': 'REFUTES','score':df.loc[[i+j], ['score']].values[0][0],
                                                            'evidence': df.loc[[i+j], ['docname']].values[0][0]}
                else:
                    d = {'claim': df.loc[[i], ['claim']].values[0][0],
                         'label': 'NOT ENOUGH INFO', 'score': df.loc[[i+j], ['score']].values[0][0],
                         'evidence': []}
                print(d)

outputformatting = Outputing()
#outputformatting.output_test_all()
outputformatting.output_test()

