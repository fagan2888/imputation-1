import numpy as np
import argparse
import h5py


# completely randomly spike in missingness
class MCAR():
    def spikein(self, X, rate):
        print('MCAR')
        # @TODO there is definitely a more efficient way to do this
        for idx, row in enumerate(X):
            indices = np.random.random_integers(0, len(row) - 1,
                                                int(len(row) * rate))
            X[idx][indices] = np.nan
        return X


# replace 50% of values in a quartile
class MNAR():
    def spikein(self, X, feature, quartile):
        f_vals = X[:, feature]
        low = np.percentile(f_vals, quartile*25)
        high = np.percentile(f_vals, (quartile+1)*25)

        quartile_vals = np.where(np.logical_and(f_vals >= low,
                                                f_vals < high))
        indices = np.random.random_integers(0, len(quartile_vals[0])-1,
                                            int(len(quartile_vals[0]*0.5)))
        f_vals[quartile_vals[0][indices]] = np.nan
        return X


# replace based on value of another column
class MAR():
    def spikein(self, X, col_a, col_b, quartile):
        col_a_vals = X[:, col_a]
        low = np.percentile(col_a_vals, quartile*25)
        high = np.percentile(col_a_vals, (quartile+1)*25)

        quartile_vals = np.where(np.logical_and(col_a_vals >= low,
                                                col_a_vals < high))
        indices = np.random.random_integers(0, len(quartile_vals[0])-1,
                                            int(len(quartile_vals[0]*0.5)))
        X[quartile_vals[0][indices], col_b] = np.nan
        return X


def run(run_name='test', file_name='completeCasesBoxCox.csv'):
    X = load_file(file_name)

    spike_rate = [0.1, 0.2, 0.3, 0.4, 0.5]
    trials = 10
    # create MCAR
    # mcar = MCAR()
    # for m in spike_rate:
    #     for t in range(trials):
    #         X_corrupt = mcar.spikein(X.copy(), m)
    #         np.savetxt('./data/spikeincsv/MCAR/MCAR_' + str(m) + '_' +
    #                    str(t) + '.csv', X_corrupt,
    #                    delimiter=',', newline='\n')
    #
    # # # create MNAR
    # mar = MAR()
    # print(X.shape[1])
    # for col_a in range(X.shape[1]):
    #     for col_b in range(X.shape[1]):
    #         print(col_a, col_b)
    #         if col_a != col_b and col_a > 0 and col_b > 3:
    #             for q in range(4):
    #                 X_corrupt = mar.spikein(X.copy(), col_a, col_b, q)
    #                 np.savetxt('./data/spikeincsv/MAR/MAR_' + str(col_a) +
    #                            '_' + str(col_b) + '_' + str(q) + '.csv',
    #                            X_corrupt, delimiter=',', newline='\n')
    #
    # #create MNAR
    # mnar = MNAR()
    # for f in range(X.shape[1]):
    #     if f >= 3:
    #         # one trial per quartile
    #         for q in range(4):
    #             X_corrupt = mnar.spikein(X.copy(), f, q)
    #             np.savetxt('./data/spikeincsv/MNAR/MNAR_' + str(f) + '_' +
    #                        str(q) + '.csv', X_corrupt,
    #                        delimiter=',', newline='\n')

    # make test folder
    mcar = MCAR()
    for m in spike_rate:
        X_corrupt = mcar.spikein(X.copy()[:100], m)
        np.savetxt('./data/spikeincsv/TEST/TEST_' + str(m) + '.csv',
                   X_corrupt, delimiter=',', newline='\n')


def load_file(name):
    print(name)
    X = np.genfromtxt('./data/' + name + '.csv', delimiter=',',
                      skip_header=1)[:10000, 1:]
    print(X.shape)
    return X

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="test")
    parser.add_argument("--file_name", type=str, default="completeCasesBoxCox")

    args = parser.parse_args()

    run(args.name, args.file_name)
