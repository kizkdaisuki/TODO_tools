import pyttsx3


def func_say(func_param_text: str):
    local_var_engine = pyttsx3.init()
    local_var_engine.setProperty('rate', 50)
    local_var_engine.setProperty('volume', 0.9)
    local_var_engine.say(func_param_text)
    local_var_engine.runAndWait()


def func_main():
    func_say("time out")
    print("START")


if __name__ == '__main__':
    func_main()