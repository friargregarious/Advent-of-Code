from pathlib import Path



def parse_input(input_path:Path)->list:
    text = input_path.read_text(encoding="utf-8")
    test_list = text.split("\n")
    
    return [list(map(int, row.split(" "))) for row in test_list]

def rules(item):
    test_asc_dec = item == sorted(item, reverse=True) or item == sorted(item, reverse=False)
    test_differences = all([ 1<= abs(a-b) <= 3 for a, b in zip(item[:-1], item[1:])])
    
    return test_asc_dec and test_differences


def problem_dampener(item)->bool:
    # item = [66, 67, 70, 73, 74, 76, 78, 80]
    versions = [item[:i] + item[i+1:] for i, _ in enumerate(item)] 
    for r in versions:
        if rules(r): return True    
        

def solve_a(data):
    safe_reports = 0
    # item = [66, 67, 70, 73, 74, 76, 78, 80]
    for item in data:
        if rules(item): safe_reports += 1
    
    print(f"There are {safe_reports} safe reports.")
    return safe_reports

def solve_b(data):
    safe_reports = solve_a(data)
    
    safe_dampened_reports = 0
    for row in data:
        if problem_dampener(row): safe_dampened_reports += 1
    
    print(f"There are {safe_dampened_reports} safe dampened reports.")
    print(f"There are {safe_reports} safe reports.")


if __name__ == "__main__":

    input_path = Path.cwd() / "input.txt"
    input_data = parse_input(input_path)
    # solve_a(input_data)
    solve_b(input_data)    
            
