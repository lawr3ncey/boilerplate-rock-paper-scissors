def player(prev_play, opponent_history=[], play_history=[]):
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    
    # Reset history when a new game starts (prev_play is empty and we have history)
    if not prev_play and len(opponent_history) > 0:
        opponent_history.clear()
        play_history.clear()
    
    # Only append actual opponent moves, not the default
    if prev_play:
        opponent_history.append(prev_play)
    
    n = len(opponent_history)
    
    guess = "R"  # default
    
    # Quincy detection and strategy (cycles R, R, P, P, S)
    # Note: opponent_history[0] is from round 2, so we need to offset by 1
    if n >= 4:
        quincy_pattern = ["R", "R", "P", "P", "S"]
        matches = sum(1 for i in range(min(n, 10)) if opponent_history[i] == quincy_pattern[(i + 1) % 5])
        if matches >= min(n, 10) * 0.9:
            # Predict quincy's next move (round n+1)
            next_quincy = quincy_pattern[(n + 1) % 5]
            guess = ideal_response[next_quincy]
            play_history.append(guess)
            return guess
    
    # Kris detection and strategy (plays counter to our last move)
    if len(play_history) >= 1:
        kris_matches = sum(
            1 for i in range(1, min(len(play_history) + 1, n))
            if opponent_history[i] == ideal_response.get(play_history[i-1], "R")
        )
        total_checks = min(len(play_history), n - 1)
        if total_checks > 0 and kris_matches / total_checks >= 0.75:  # Lower threshold
            # Kris plays ideal_response[our_last_move]
            # We play what beats that
            guess = ideal_response[ideal_response[play_history[-1]]]
            play_history.append(guess)
            return guess
    
    # Abbey strategy (predicts based on our 2-move patterns)
    if len(play_history) >= 15:
        # Build frequency table of what we play after each 2-move sequence
        play_order = {}
        for i in range(2, len(play_history)):
            last_two = "".join(play_history[i-2:i])
            next_play = play_history[i]
            if last_two not in play_order:
                play_order[last_two] = {"R": 0, "P": 0, "S": 0}
            play_order[last_two][next_play] += 1
        
        last_two = "".join(play_history[-2:])
        if last_two in play_order and sum(play_order[last_two].values()) > 0:
            # Predict what we'll play
            my_prediction = max(play_order[last_two], key=play_order[last_two].get)
            # Abbey will play counter to that prediction
            abbey_play = ideal_response[my_prediction]
            # We play counter to abbey
            guess = ideal_response[abbey_play]
            play_history.append(guess)
            return guess
    
    # Mrugesh strategy (counters our most frequent in last 10)
    if len(play_history) >= 10:
        last_ten = play_history[-10:]
        most_frequent = max(set(last_ten), key=last_ten.count)
        mrugesh_move = ideal_response[most_frequent]
        guess = ideal_response[mrugesh_move]
        play_history.append(guess)
        return guess
    
    # Default: try kris strategy (works well against kris and is neutral against others)
    if len(play_history) > 0:
        guess = ideal_response[ideal_response[play_history[-1]]]
    else:
        guess = "R"
    
    play_history.append(guess)
    return guess
