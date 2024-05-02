import csv

with open('elections.csv', newline='') as csvfile:
    fieldnames = ["ID","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th","13th","14th","15th"]
    electionsreader = csv.DictReader(csvfile, fieldnames=fieldnames)
    ballots = []
    for d in electionsreader:
        for k, v in d.copy().items():
            if not v:
                d.pop(k)
        ballots.append(d)
    for ballot in ballots.copy():
        try:
            int(ballot.get(fieldnames[0]))
        except:
            ballots.pop(ballots.index(ballot))

    # convert dicts to lists
    headers = []
    for ballot in ballots:
        for header in ballot:
            headers.append(header)
        break

    for ballot in ballots.copy():
        i = ballots.index(ballot)
        temp_list = list(ballot.values())
        ballots[i] = temp_list

    # make list of candidates
    candidates = ballots[0][1:]

    # get round totals for each candidate
    roundresults = []
    ballotslist = []
    elim_list = []
    winner = None
    while not winner:
        for header in headers:
            if header == headers[0]:
                continue

            roundresults = []
            i = 1
            ordinal = headers.index(header)
            init_string = f"{headers[ordinal]} round"
            resultslist = [init_string]

            for candidate in candidates:
                votetotal = 0
                for ballot in ballots:
                    if ballot[i] == candidate:
                        votetotal = votetotal + 1
                roundresults.append(votetotal)
                resultslist.append(f"{candidate} - {roundresults[candidates.index(candidate)]}")
            results_string = '\n'.join(map(str, resultslist))
            print(results_string + "\n")

            # check for winner
            for candidate in candidates:
                if roundresults[candidates.index(candidate)]/sum(roundresults) >= 0.5:
                    winner = candidate
                    print(f"Winner in the {init_string}: {winner}")
                    break

            if winner:
                break

            if i < len(headers) - 1:
                min_val = min(v for v in roundresults if v>0)
                elim_index = [v for v, x in enumerate(roundresults) if x <= min_val]
                for name in [name for name in candidates if candidates.index(name) in elim_index]:
                    if name not in elim_list:
                        elim_list.append(name)
            # print(elim_list)

            for ballot in ballots:
                valid = False
                check_ballot = ballot.copy()[:len(ballot) - 1]
                while not valid:
                    # print(ballot)
                    # print(elim_list)
                    for name in check_ballot[:len(ballot)]:
                        check_i = check_ballot.index(name)
                        if name in elim_list:
                            check_ballot[check_i] = True
                        else:
                            check_ballot[check_i] = False
                    # print(check_ballot)
                    if not any(check_ballot):
                        valid = True
                        # print(ballot)
                        # print("checked")
                        continue
                    for name in check_ballot[:len(ballot)]:
                        replace_i = check_ballot.index(name)
                        if name:
                            # print(ballot[replace_i])
                            try:
                                zindex = ballot.index(ballot[replace_i])
                                # print(zindex)
                                xcount = 0
                                for x in check_ballot[zindex:len(ballot) + 1]:
                                    y = ballot[zindex + xcount]
                                    replacement = y
                                    if replacement in elim_list:
                                        xcount = xcount + 1
                                        continue
                                    else:
                                        replacement = y
                                        check_ballot[replace_i] = False
                                        xcount = xcount + 1
                                        break
                            except:
                                check_ballot[replace_i] = False

                            ballot[replace_i] = replacement
                            # print(name)
                            # print(replacement)
                            # print(check_ballot)
                            # print(ballot)