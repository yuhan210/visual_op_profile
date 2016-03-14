import numpy as np

if __name__ == "__main__":

    with open('out') as fh:
        lines = [float(x.strip().split(' ')[1]) for x in fh.readlines() if x.find('got_output:1') >= 0]

        print np.mean(lines), np.std(lines)
