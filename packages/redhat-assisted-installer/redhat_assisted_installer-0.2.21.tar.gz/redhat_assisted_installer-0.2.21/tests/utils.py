

def get_input(prompt, cast_func=None):
    value = input(prompt)
    if value == "":
        return None
    return cast_func(value) if cast_func else value
