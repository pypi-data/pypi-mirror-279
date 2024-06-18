import os


def gci(filepath, results=[]):
    files = os.listdir(filepath)
    for fi in files:
        fi_d = os.path.join(os.path.abspath(filepath), fi)
        if os.path.isdir(fi_d):
            results = gci(fi_d, results)
        else:
            results.append(os.path.join(os.path.abspath(filepath), fi_d))

    return results


if __name__ == '__main__':
    results = gci('..')
    print(results)
