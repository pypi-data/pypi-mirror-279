import string


def seed_none(*args):
    return None


def seed_many_empty(args, guesser, data, value, model, index, instance):
    return []


def seed_default_number(args, guesser, value, model):
    return value


def seed_default_auto_add(args, guesser, value, model):
    return value


def seed_variable_name(args, guesser, data, value, model, index):
    args = args or (10, 20)
    return ''.join(guesser.random_sample(string.ascii_lowercase, guesser.random.randint(*args)))


def seed_class_name(args, guesser, data, value, model, index):
    args = args or (10, 20)
    return ''.join(guesser.random_sample(string.ascii_uppercase) + guesser.random_sample(string.ascii_lowercase,
                                                                                         guesser.random.randint(*args)))
