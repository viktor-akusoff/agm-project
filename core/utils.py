from functools import wraps

def coordinates_eval(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        cleaned_result = []
        for element in result:
            cleaned_element = element
            cleaned_element.coordinates = eval(element.coordinates) # type: ignore
            cleaned_result.append(cleaned_element)
        return cleaned_result
    return wrapper