import os, complex_main, single_main, Correlation


def menu():
    print("\n======== dwi处理 ========")
    print("1. 选项一：单一被试处理")
    print("2. 选项二：批量被试处理")
    print("3. 选项三：结果查看(mrview)")
    print("4. 选项四：结构功能耦合相关分析")
    print("0. 选项零：退出程序")
    print("===========================")

def main():
    while True:
        menu()
        choice = input("请输入选项（0-8）：")
        if choice == "1":
            single_main.main()
        elif choice == "2":
            complex_main.main()
        elif choice == "3":
            process = os.popen(
                'mrview')
            output = process.read()
            print(output)
            process.close()
        elif choice == "4":
            Correlation.main()
        elif choice == "0":
            break
        else:
            print("无效的选项，请重新输入！")

if __name__ == "__main__":
    main()