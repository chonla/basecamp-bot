from ...bc3bot.config import Config


def test_getting_config_data():
    yaml_str = '''
    bot:
        name: Bot name
    '''

    conf = Config()
    conf.load(yaml_str)

    result = conf.get('bot.name')

    assert result == 'Bot name'

def test_getting_config_data_array():
    yaml_str = '''
    bot:
        name: Bot name
        alias:
        - hello
        - book
    '''

    conf = Config()
    conf.load(yaml_str)

    result = conf.get('bot.alias')

    assert result == ['hello', 'book']
