def get_commands_client(menu):

    cmnds = []

    for option in menu:

        _name = option['name']

        for keyboard in option['keyboards']:

            _handler = keyboard['handler']

            if _handler != 'dat_ukaz' and _handler != None:

                for button in keyboard['buttons']:

                    text = button['text']

                    cmnds.append(text)

    return (cmnds)