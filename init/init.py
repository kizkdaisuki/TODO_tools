import json

def func_read_json(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())
def func_write_json(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))

def main():
    pass
if __name__ == '__main__':
    main()

