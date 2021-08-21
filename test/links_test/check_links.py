
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
                error_dict[link] = ([0, 0, 0, 0, 0, 0], [], [])
                continue

            names_found = found_dict[link]
            n_annotated = len(names_annotated)
            total_found = len(names_found)
            true_positives = 0
            true_negatives = 0
            false_positives = 0
            false_negatives = 0

            for name in names_annotated:
                if name in names_found:
                    true_positives += 1
                else:
                    false_negatives += 1

            for name in names_found:
                if name not in names_annotated:
                    false_positives += 1

            perc = 0 if n_annotated == 0 or true_positives == 0 else float(true_positives)/n_annotated
            error_dict[link] = ([true_positives, true_negatives, false_positives, false_negatives, n_annotated, perc], names_found, names_annotated)


        true_positives_total = 0
        true_negatives_total = 0
        false_positives_total = 0
        false_negatives_total = 0
        annotated_total = 0
        for link in error_dict:
            [true_positives, true_negatives, false_positives, false_negatives, n_annotated, perc], names_found, names_annotated = error_dict[link]
            true_positives_total += true_positives
            true_negatives_total += true_negatives
            false_positives_total += false_positives
            false_negatives_total += false_negatives
            annotated_total += n_annotated
            print()
            print()
            print()
            print('Poveznica:', link)
            print('P/O: \t\t{}/{} ({:.2f})'.format(true_positives, n_annotated, perc))
            print('Pronađeni:\t', names_found)
            print('Označeni:\t', names_annotated)

        precision = float(true_positives_total)/(true_positives_total+false_positives_total)
        recall = float(true_positives_total)/(true_positives_total+false_negatives_total)
        f1_score = 2*(precision*recall)/(precision+recall)

        print('---------------------------------------')
        print('---------------------------------------')
        print('Matrica konfuzije: ')
        print('\tPOZ    NEG')
        print('POZ \t{}    {}'.format(true_positives_total, false_negatives_total))
        print('NEG \t{}    {}'.format(false_positives_total, true_negatives_total))

        perc_total = float(true_positives_total)/annotated_total
        print('---------------------------------------')
        print('---------------------------------------')
        print('Ukupno:')
        print('     P/O:        {}/{} ({:.2f})'.format(true_positives_total, annotated_total, perc_total))
        print('     PRECIZNOST: {:.2f}'.format(precision))
        print('     ODZIV:      {:.2f}'.format(recall))
        print('     F1:         {:.2f}'.format(f1_score))
        print('---------------------------------------')
        print('---------------------------------------')
