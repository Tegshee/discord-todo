from needhelp.config import EMOJI_NUMBERS

def calculate_emoji_number(number):
    # if number is less than 10 return emoji number
    # else calculate the number emoji with + symbol like if 11 then 10 + 1
    msg = ""
    if number <= 10:
        msg =  EMOJI_NUMBERS[number]
    elif number <= 20:
        #calculate the number emoji with + symbol like if 11 then 10 + 1
        msg =  EMOJI_NUMBERS[10] + EMOJI_NUMBERS[number - 10]
    elif number > 20:
        while number <= 10:
            number -= 10
            msg += EMOJI_NUMBERS[10]
        msg = msg + EMOJI_NUMBERS[number]

    return msg

def show_todo(todo):
    # set message to todos header message with category emoji todos['category']
    msg = ""
    # loop todos task and show in a nice way with numbers and emoji categories
    # for todo in todos:
    print(todo)
    msg += f"{todo.category.emoji} - {todo.id} - {todo.title}\n"
    #after task x emoji or checkmark emoji conditionally if task is done
    count = 1
    for task in todo.tasks:
        header_emoji = calculate_emoji_number(count)
        if task.status == 'done':
            msg += f"\t\t{header_emoji} - {task.title} ✅\n"
        elif task.status == 'in_progress':
            msg += f"\t\t{header_emoji} - {task.title} ⏳\n"
        else: #emoji X 
            msg += f"\t\t{header_emoji} - {task.title} ❌\n"
        count += 1

    return msg

def parse_todo_id(message):
    first_line = message.split('\n')[0]
    str_list = first_line.split(' ')
    if len(str_list) > 3 and str_list[2].isdigit():
        return int(str_list[2])
    
    return None

