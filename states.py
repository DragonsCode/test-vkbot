from vkbottle import CtxStorage, BaseStateGroup

ctx = CtxStorage()

class RegData(BaseStateGroup):

    NAME = 0
    AGE = 1
    CATEGORY = 2
    ABOUT = 3


class ChangeProfileData(BaseStateGroup):

    WHAT = 0
    CHANGE = 1


class PostData(BaseStateGroup):

    CATEGORY = 0
    TITLE = 1
    TEXT = 2