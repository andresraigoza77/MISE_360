
def read_chunks():
    with open("search_q3.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 20):
            print("".join(lines[i:i+20]))
            print("--- CHUNK ---")

if __name__ == "__main__":
    read_chunks()
