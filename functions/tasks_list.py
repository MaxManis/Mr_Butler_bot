import config_files.config as config


def create_tasks_file(user_id):
    try:
        f = open(f'{config.tasks_path}tasks-{user_id}.txt', 'r', encoding='utf-8')
        f.close()
    except:
        f = open(f'{config.tasks_path}tasks-{user_id}.txt', 'w', encoding='utf-8')
        f.close()


def create_task(text_task, user_id):
    count_id = len(read_tasks(user_id))
    with open(f'{config.tasks_path}tasks-{user_id}.txt', 'a', encoding='utf-8') as f:
         f.write(str(count_id+1) + ': ' + str(text_task) + "\n")
    f.close()


def read_tasks(user_id):
    with open(f'{config.tasks_path}tasks-{user_id}.txt', 'r', encoding='utf-8') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    f.close()
    return content


def del_tasks(task_id, user_id):
    with open(f'{config.tasks_path}tasks-{user_id}.txt', 'r', encoding='utf-8') as f:
        content = f.readlines()
        f.close()
    content = [x.strip() for x in content]
    new_content = []
    f = open(f'{config.tasks_path}tasks-{user_id}.txt', 'w', encoding='utf-8')
    for i in content:
        if i[:i.find(':')] != task_id:
            new_content.append(i[i.find(' '):])
    c = 1
    for i in new_content:
        f.write(str(c) + ': ' + i + "\n")
        c += 1
    f.close()

