# Weights for passing
diamond_weights = [0, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, -0.5, -1, -1.5, -2]
hearts_weights = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1.5, 2, 2.5, 3]

# Preference for which suits to pass away, e is the rating bonus (additive) for getting rid of a suit
suits_preference = {
    "c": 1,
    "d": 1,
    "s": 1,
    "h": 1,
    "e": 10
}

# risk_tolerance is from [0, 1], 0 meaning always avoiding taking, and 1 always taking.
risk_tolerance = 1

# minimum_takes is from [0-13], minimum number of guaranteed takes to trigger shooting
minimum_takes = 10
