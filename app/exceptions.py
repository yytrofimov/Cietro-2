class UserEmailExists(Exception):
    pass


class UserEmailDoesntExist(Exception):
    pass


class UserIsBlocked(Exception):
    pass


class UserIdDoesntExist(Exception):
    pass


class CompanyDoesntExist(Exception):
    pass


class CompanyExists(Exception):
    pass


class IncorrectPassword(Exception):
    pass


class IncorrectInviteCode(Exception):
    pass


class IncorrectToken(Exception):
    pass


class ItemDoesntExist(Exception):
    pass

class ItemInUse(Exception):
    pass


class IncorrectActivationCode(Exception):
    pass

class NoEnoughRigths(Exception):
    pass


class ItemNotInUse(Exception):
    pass

class TokenExpired(Exception):
    pass

class WrongType(Exception):
    pass