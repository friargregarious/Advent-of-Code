import sys


test_row = "345  591   73"

SAMPLE = "sample" in sys.argv

if SAMPLE:
    source = list(open("sample.txt").readlines())
else:
    source = list(open("input.txt").readlines())

part_2_source = []


if __name__ == "__main__":

    # tri_add = {True: [], False: []}
    # tri_add_nosort = {True: [], False: []}
    # tri_pythagorus = {True: [], False: []}
    # tri_reddit_answer = {True: [], False: []}

    print("Part 1: Add nosort:", sum([vals[0] + vals[1] > vals[2]
          for vals in [sorted([int(x) for x in line.split()]) for line in source]]))

    xcross = iter(source)

    breakhere = False
    while not breakhere:
        nums1, nums2, nums3 = [], [], []

        for x in range(3):
            try:
                a, b, c = next(xcross).split()
                nums1.append(int(a))
                nums2.append(int(b))
                nums3.append(int(c))
                print([nums1, nums2, nums3])
                part_2_source.extend([nums1, nums2, nums3])
            except StopIteration as e:
                if SAMPLE:
                    print("Part 1: Add vertical sort:", sum([vals[0] + vals[1] > vals[2]
                        for vals in [sorted([int(x) for x in line]) for line in sample]]))
                else:
                    print("Part 1: Add vertical sort:", sum([vals[0] + vals[1] > vals[2]
                        for vals in [sorted([int(x) for x in line]) for line in part_2_source]]))

                breakhere = True 
                break
