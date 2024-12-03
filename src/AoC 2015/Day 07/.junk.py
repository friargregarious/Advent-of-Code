from solution import parse_input, AND_OR, SHIFT, PUT_NOT

inputs = parse_input("example_input.txt")

tree = {}
for row in inputs:
    # print(row)
    # parts = row.split(" ")
    
    tree[parts[-1]] = {"answer": None, "children": parts[:-2],}
    
    if "AND" in row:
        tree[parts[-1]]["answer"] = parts

    elif "OR" in row:
        tree[parts[-1]]["answer"] = parts


    elif "SHIFT" in row:
        if "RSHIFT" in row:
            subject >>= pos

        else:  # "LSHIFT"
            subject <<= pos
    
   
    
    elif "NOT" in row:
        pass
        # a = ("0" * 16 + bin(subject)[2:])[-16:]
        # b = "0b"
        # for i in a:
        #     if i == "1":
        #         b += "0"
        #     else:
        #         b += "1"
        
        # ans[target] = int(b, base=2)
        
    else:
        # ans[target] = subject
        pass
        
        
for key, val in tree.items():
    print(key, val.__str__())
