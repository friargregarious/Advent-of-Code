import os

log = open("Words B.log").read().split("\n")

allrecords = len(log)
for row_num, row in enumerate(log):
    os.system("cls")
    print("\n\n\n\n\n")
    print("\t\t\t\t\tA Nums\t\t\t     WORD\t\t\t   B Nums")

    print(f"{(row_num+1)/allrecords:.2f}%", row)
    _ = input("\n\n\nPress <ENTER> to continue...")
