
with open('links_with_found_names.txt', 'r', encoding='utf-8') as found_names:
    with open('links_annotated.txt', 'r', encoding='utf-8') as annotated_names:
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
                error_dict[link] = ([0, 0, 0], [], [])
                continue

            names_found = found_dict[link]
            total = len(names_annotated)
            really_found = 0

            for name in names_annotated:
                if name in names_found:
                    really_found += 1

            perc = 0 if total == 0 or really_found == 0 else float(really_found)/total
            error_dict[link] = ([really_found, total, perc], names_found, names_annotated)


        really_found_total = 0
        annotated_total = 0  
        for link in error_dict:
            [really_found, total, perc], names_found, names_annotated = error_dict[link]
            really_found_total += really_found
            annotated_total += total
            print()
            print()
            print()
            print('Poveznica:', link)
            print('P/O: \t\t{}/{} ({:.2f})'.format(really_found, total, perc))
            print('Pronađeni:\t', names_found)
            print('Označeni:\t', names_annotated)

        perc_total = float(really_found_total)/annotated_total
        print()
        print()
        print('Ukupno:')
        print('     P/O: \t\t{}/{} ({:.2f})'.format(really_found_total, annotated_total, perc_total))
