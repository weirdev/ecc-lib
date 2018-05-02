if __name__ == "__main__":
     with open("tesbin", 'wb') as binf:
        # num rows, num columns
        for i in range(5):
            binf.write(i.to_bytes(1, byteorder='little'))