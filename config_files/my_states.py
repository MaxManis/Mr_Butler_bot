from aiogram.dispatcher.filters.state import State, StatesGroup


class TryMySets(StatesGroup):
    set_1 = State()


class WriteToOper(StatesGroup):
    write_1 = State()


class TasksToDo(StatesGroup):
    task_1 = State()
    task_2 = State()


class WriteToUser(StatesGroup):
    write_1 = State()
    write_2 = State()


class GoogTextTS(StatesGroup):
    write_1 = State()


class SportEvents(StatesGroup):
    sport_1 = State()
    sport_2 = State()


