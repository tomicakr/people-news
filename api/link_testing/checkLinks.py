
with open('apiLog.txt', 'r', encoding='utf-8') as found_names:
    with open('links-solved.txt', 'r', encoding='utf-8') as annotated_names:
        found = list(map(lambda x: [x[0], x[1].split(',')], map(lambda x: x.rstrip().split('\t'), found_names.readlines())))
        found_dict = {}
        for link, names in found:
            if names[0] == 'set()':
                found_dict[link] = ['-']
            else:
                fixed_names = []
                for name in names:
                    fixed = name.strip().replace('{', '').replace('}', '')
                    fixed_names.append(fixed[1:-1])
                found_dict[link] = fixed_names

        annotated = list(map(lambda x: [x[0], x[1].split(';')], map(lambda x: x.rstrip().split('\t'), annotated_names.readlines())))
        annotated_dict = {}
        for link, names in annotated:
            fixed_names = list(map(lambda x: x.strip(), names))
            fixed_names = list(filter(lambda x: len(x) != 0, fixed_names))
            annotated_dict[link] = fixed_names

        error_dict = {}

        for link in annotated_dict:
            names_annotated = annotated_dict[link]
            if names_annotated[0] == '-':
                error_dict[link] = ([0, 0], [], [])
                continue

            names_found = found_dict[link]
            total = len(names_annotated)
            really_found = 0

            for name in names_annotated:
                if name in names_found:
                    really_found += 1

            error_dict[link] = ([really_found, total], names_found, names_annotated)
            
        for link in error_dict:
            er = error_dict[link]
            print()
            print()
            print()
            print(link)
            print('Found vs annotated: ', er[0])
            print('Found', er[1])
            print('Annotated', er[2])
