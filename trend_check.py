def check_trend_heat(posts_count):
    """
    מחזיר דירוג חום לטרנד לפי כמות הפוסטים שנמצאו.
    """
    if posts_count > 30:
        return "חמה"
    elif posts_count > 10:
        return "בינונית"
    else:
        return "חלשה"
