class UserExists(Exception):
    pass


class UserDoesntExist(Exception):
    pass


class UserIsBlocked(Exception):
    pass


class CompanyDoesntExist(Exception):
    pass


class CompanyExists(Exception):
    pass


class PasswordIsIncorrect(Exception):
    pass


class InviteCodeIsIncorrect(Exception):
    pass


class ItemDoesntExist(Exception):
    pass


class ItemInUse(Exception):
    pass


class ActivationCodeIsIncorrect(Exception):
    pass


class NoEnoughRights(Exception):
    pass


class ItemNotInUse(Exception):
    pass


class TokenExpired(Exception):
    pass


class TokenIsAlreadyRequested(Exception):
    pass


class TokenIsIncorrect(Exception):
    pass
