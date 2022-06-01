def run_tests(strategies, cases, cases_expected):
    num_tests = len(cases)
    results = {name: 0 for name, _ in strategies}

    for name, strategy in strategies:
        print(name)
        print()
        for index, case in enumerate(cases):
            n, m, blocked = case
            got = strategy(n, m, blocked)
            expected = cases_expected[index]

            print(f"case {index} ({case})")
            print(f"got {strategy(n, m, blocked)}")
            if got == expected:
                results[name] += 1
                print("same!")
            else:
                print(f"expected {cases_expected[index]}")
            print()

    for name, result in results.items():
        formatted_result = "passed" if result // num_tests >= 1 else "failed"
        print(f"{name}: {formatted_result} ({result}/{num_tests})")
