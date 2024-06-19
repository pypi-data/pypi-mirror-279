from .Configuration.baseconfig import ConfigStruct

config = ConfigStruct()
config.read_config()


def editconfig(key, value):
    from .Input.input_validation import check_inputs

    inputs = check_inputs({"key": key, "value": value}, "edit")
    key, value = inputs["key"], inputs["value"]

    print("Written change to ATKConfig.ini. New Values:\n")
    config.edit_config(key, value)


def openconfig():
    config=ConfigStruct()
    path=config.config_file

    import webbrowser
    webbrowser.open(path)

def outputconfig():
    print("Current ATKConfig.ini values:\n")
    config.read_config()
    config.output_config()


def resetconfig():
    print("Resetting ATKConfig.ini to default values...\n")
    config.set_default_config()
    config.write_config()
