MESSAGES = {
    'weather_for_location_retrieval_failed': 'Нет инфы, другалек,' +
    'пойди траву потрогай. \n\n /help - инструкция по использованию бота.',

    'general_failure': 'Я анскил, у меня нет таких возможностей.\n\n /help - инструкция по использованию бота.',

    'weather_in_city_message': 'Погода в {}:\n{}\nтемпература: {:.1f}°C.',

    'weather_in_location_message': 'Погода в указанной локации:\n{}\nтемпература: {:.1f}°C.',

    'help': 'Погода в вашем городе, введите название города или отправьте местоположение.'
}


def get_message(message_key: str):
    return MESSAGES[message_key]
