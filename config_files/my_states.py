from aiogram.dispatcher.filters.state import State, StatesGroup


class TryMySets(StatesGroup):
    set_1 = State()


class WriteToOper(StatesGroup):
    write_1 = State()


class TasksToDo(StatesGroup):
    task_1 = State()
    task_2 = State()
