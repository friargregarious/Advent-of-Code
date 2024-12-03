from itertools import count
import aocd
from pathlib import Path


input_data_path = Path("input.txt")
if input_data_path.exists() and input_data_path.read_text() != "":
    data = input_data_path.read_text()
else:
    data = aocd.get_data(day=1, year=2024)

def parse_data(data):
    list_a = []
    list_b = []
    
    for row in data.split("\n"):
        a, b = row.split("   ")
        list_a.append(int(a))
        list_b.append(int(b))

    return sorted(list_a), sorted(list_b)               

def solve_a(data):
    list_a, list_b = parse_data(data)
    sum_distances = 0
    for a, b in zip(list_a, list_b):
        dist = abs(a-b)
        sum_distances += dist
        print(a, b, dist, sum_distances)

    return sum_distances

def solve_b(data):
    list_a, list_b = parse_data(data)
    
    counts = {
        a: list_b.count(a)   for a in list_a
    }

    sums = 0    
    for k, v in counts.items():
        sums += k*v
        if v > 1:
            print(f"k:{k}, v:{v}, prod: {k*v}, running: {sums}")

    print(f"sums: {sums}")
    return sums
    
    
        
if __name__ == "__main__":

    # solve_a(data)
    solve_b(data)
