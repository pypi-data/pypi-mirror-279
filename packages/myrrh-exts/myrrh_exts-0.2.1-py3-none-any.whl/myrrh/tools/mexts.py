import argparse
import pprint


from myrrh.exts.registry import Registry


def get(uri):
    with Registry().open(uri) as f:
        pprint.pprint(f.read(1))


def push(uri, data):
    with Registry().open(uri) as f:
        pprint.pprint(f.write(data))


def list_(uri):
    pprint.pprint(Registry().findall(uri))


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("method", choices=["push", "get", "list"])
    parser.add_argument("uri")
    parser.add_argument("data", default=None, nargs='?')
    
    args = parser.parse_args()

    if args.method == "push":
        return push(args.uri, args.data)

    if args.method == "get":
        return get(args.uri)

    if args.method == "list":
        return list_(args.uri)


if __name__ == "__main__":
    main()
