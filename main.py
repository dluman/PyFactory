from springform import Template

def main():
    template = Template(mod = "Item", cls = "Item")
    template.make("ItemCopy", copy = True)

if __name__ == "__main__":
    main()
