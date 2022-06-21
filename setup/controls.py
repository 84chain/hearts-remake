# Weights for passing
diamond_weights = [0, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, -0.5, -1, -1.5, -2]
hearts_weights = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1.5, 2, 2.5, 3]

# Preference for which suits to pass away, e is the rating bonus (additive) for getting rid of a suit
suits_preference = {
    "c": 1,
    "d": 1,
    "s": 1,
    "h": 1,
    "e": 1
}

# risk_tolerance is from [0, 1], 0 meaning always avoiding taking, and 1 always taking.
risk_tolerance = 1

# minimum_takes is from [0-13], minimum number of guaranteed takes to trigger shooting
minimum_takes = 10

# taking_point_threshold is maximum number of points on the table when taking with d_jack is triggered
taking_point_threshold = 100

# blocking_point_threshold is the maximum number of points on the table when blocking shoot is triggered
blocking_point_threshold = 40

# loss and gain on L change how likely/unlikely a player is on team
loss_on_L = 1 / 13
gain_on_L = 1 / 13