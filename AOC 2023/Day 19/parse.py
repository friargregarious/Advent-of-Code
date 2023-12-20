import os

os.system("cls")


__on_example__ = True

source = "input.txt"
if __on_example__:
    source = "example.txt"

raw = open(source).read().split("\n")

# Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}.
# This workflow is named ex and contains four rules.
# If workflow ex were considering a specific part,
# it would perform the following steps in order:

# Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named one.
# Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the workflow named two.
# Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately rejected (R).
# Rule "A": Otherwise, because no other rules matched the part, the part is immediately accepted (A).

# ans = eval()


class MyPart:
    """simple object to represent a gear and it's XMAS rating"""

    def __init__(self, inputs: dict) -> None:
        # these are likely unnessessary
        self.x = 0
        self.m = 0
        self.a = 0
        self.s = 0

        # assigns values to properties
        self.__dict__.update(inputs)


# class Decider:
#     """awesome machine for running workflows on parts lists."""

#     rules = {}
#     queues = {}

#     def __init__(self, rules) -> None:
#         self.rules = rules

#     def analyze(self, part_item: MyPart):
#         """compare part given to workflows"""
#         target_queue = ""
#         for key in self.rules:
#             for _, rule in self.rules[key].items():
#                 if isinstance(rule, str):
#                     target_queue = rule

#                 elif eval(f"part_item.{rule}") is True:


#     def report(self):
#         report, incomplete_msgs, completed_msgs = [], [], []
#         total_incompete, total_completed = 0, 0

#         for queue, content in self.queues.items():
#             if queue in ["R", "A"]:
#                 total_completed += len(content)
#                 completed_msgs.append(f"{queue}: {len(content)}")
#             else:
#                 total_incompete += len(content)
#                 incomplete_msgs.append(f"{queue}: {len(content)}")

#         report.extend(sorted(incomplete_msgs))
#         report.extend(sorted(completed_msgs))
#         report_msg = "Decide_a_Tron Report\n"
#         report_msg += "\n".join(report)
#         total_parts = total_completed + total_incompete
#         if total_completed == 0:
#             percent_done = 0.0
#         else:
#             percent_done = total_completed / total_parts

#         report_msg += f"\nThe Decider is {percent_done:.1}% complete."

#         print()


class WorkFlow:
    rules = {}  # key is rule to eval, val is target to send to
    default = ""  # default target if no other rules apply

    def __init__(self) -> None:
        pass

    def test(self, gear: dict) -> str:
        if gear.true:
            return True
        else:
            return self.default


workflow_queue = {}


def build_work_flow(line):
    my_name, parts = rules.split("{")
    workflow_queue[my_name] = WorkFlow()
    parts.strip("}").split(",")
    workflow_queue[my_name].default_target = parts[-1]
    # ..... need more lines here to finish the rules


work_flows, work_queues = {}, {}
accepted, rejected = [], []

for row in raw:
    if len(row) > 0:
        if row[0].isalpha():  # this is a workflow
            obrack = row.find("{")
            cbrack = row.find("}")
            key = row[:obrack]
            work_flows[key] = []
            work_queues[key] = []

            raw_rules = row[obrack + 1 : cbrack].split(",")
            for rule in raw_rules:
                if ":" in rule:  # comparison
                    work_flows[key].append(tuple(rule.split(":")))
                else:
                    work_flows[key].append(rule)
            print(work_flows[key])

        elif row.startswith("{"):  # these are parts
            new_part = {}
            for pair in row.strip("}{").split(","):
                key, val = pair.split("=")
                new_part[key] = int(val)
            print(new_part)
            work_queues["in"].append(MyPart(new_part))

        else:
            print(f"Didn't find case for [{row}]")
# print(unsorted_parts)

current_queue = "in"  # we always start in "in":
