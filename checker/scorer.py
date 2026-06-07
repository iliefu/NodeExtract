def score(
    delay,
    speed,
    success
):

    if not success:

        return 0

    return round(

        1000/max(delay,1)

        + speed*3,

        2
    )
