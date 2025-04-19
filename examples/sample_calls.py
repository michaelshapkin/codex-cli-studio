# examples/sample_calls.py
def func_a():
    print("In A")
    func_b()

def func_b():
    print("In B")
    func_c()
    func_d()

def func_c():
    print("In C")

def func_d():
    print("In D")
    # Maybe call func_a again for a cycle?
    # func_a() # Uncomment for cycle

def main():
    print("Starting main")
    func_a()
    print("Finished main")

if __name__ == "__main__":
    main()