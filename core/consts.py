DIRECTION_TO_RUS = 'на русский'
DIRECTION_FROM_RUS = 'с русского'
DIRECTION_CHOICES = (
    (DIRECTION_TO_RUS, DIRECTION_TO_RUS),
    (DIRECTION_FROM_RUS, DIRECTION_FROM_RUS),
)

TRAINING_MODE_ALL_WORDS = 'все слова'
TRAINING_MODE_UNKNOWN_WORDS = 'неизученные'
TRAINING_MODE_CHOICES = (
    (TRAINING_MODE_ALL_WORDS, TRAINING_MODE_ALL_WORDS),
    (TRAINING_MODE_UNKNOWN_WORDS, TRAINING_MODE_UNKNOWN_WORDS),
)