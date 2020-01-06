def main():
    types = ["string", "int", "pointer"]
    for fact_type in types:
        index = read_facts(fact_type)
        write_rules(index, fact_type)

def read_facts(fact_type):
    index = []
    file_path = "./pages/" + fact_type
    with open(file_path, 'r') as output:
        line = output.readline()
        while line:
            tmp = line.strip().split('\t')
            if len(tmp) == 2:
                index.append(tmp[0])
                print tmp   
            line = output.readline()
    return index



def write_rules(index, rule_type):
    file_path = "./pages/rules.pl"
    with open(file_path, 'a') as output:
        for fact in index:
            rule = "is" + rule_type + "(" + str(fact) + ")" + "." + "\n"
            output.write(rule)

if __name__ == "__main__":
    main()