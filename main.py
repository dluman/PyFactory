from springform import Template

def __dumb(self):
    print("it rly is")

def main():
    template = Template(mod = "Item")
    template.make("ItemCopy", copy = True, __dumb = __dumb)

if __name__ == "__main__":
    main()
