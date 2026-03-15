import sys

DATA_FILE = "data.db"


class Node:
    """
    Node for linked list key-value storage.
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class KeyValueStore:
    """
    Custom key-value store using a linked list.
    No built-in dict/map is used.
    """

    def __init__(self):
        self.head = None

    def find(self, key):
        """
        Search for a node by key.
        """
        current = self.head

        while current:
            if current.key == key:
                return current
            current = current.next

        return None

    def set(self, key, value):
        """
        Insert or update a key-value pair.
        """
        node = self.find(key)

        if node:
            node.value = value
        else:
            new_node = Node(key, value)
            new_node.next = self.head
            self.head = new_node

    def get(self, key):
        """
        Retrieve value by key.
        """
        node = self.find(key)

        if node:
            return node.value

        return None


def load_database(store):
    """
    Replay the append-only log to rebuild memory index.
    """

    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split()

                if len(parts) == 3 and parts[0] == "SET":
                    key = parts[1]
                    value = parts[2]
                    store.set(key, value)

    except FileNotFoundError:
        # Database does not exist yet
        pass


def command_loop(store):
    """
    CLI loop for STDIN commands.
    """

    db_file = open(DATA_FILE, "a")

    for line in sys.stdin:

        parts = line.strip().split()

        if not parts:
            continue

        command = parts[0]

        if command == "SET" and len(parts) == 3:

            key = parts[1]
            value = parts[2]

            store.set(key, value)

            # Persist immediately
            db_file.write(f"SET {key} {value}\n")
            db_file.flush()

        elif command == "GET" and len(parts) == 2:

            key = parts[1]
            result = store.get(key)

            if result is not None:
                 print(result)
            else:
                 print()  # prints empty line

            sys.stdout.flush()

        elif command == "EXIT":
            break

    db_file.close()


def main():

    store = KeyValueStore()

    # Load previous data
    load_database(store)

    # Start CLI
    command_loop(store)


if __name__ == "__main__":
    main()