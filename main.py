from Factory import Factory

def main():
    template = Factory(mod = "Item", cls = "Item")
    template.make("TestItem")

if __name__ == "__main__":
    main()
