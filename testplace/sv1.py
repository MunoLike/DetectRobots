import sv2
import sv3



def showA():
    print(sv3.A)


def main():
    sv3.A = 50
    sv2.showA()
    showA()


if __name__ == "__main__":
    main()
