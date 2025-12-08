import base64  # import decode library # 引入解码库

# 1. Define the name of the file be solved
# 1. 定义我们要处理的文件名
filename = "server_log.txt"

print(f"[*] Analyzing {filename}...")

try:
    # 2. Try to open  the file
    with open(filename, "r") as f:
        for line in f:
            # Search target line
            # 3. 寻找包含线索的行
            if "EXFILTRATED_DATA:" in line:
                # Extract string after :(colon)
                # 提取冒号后面的那串乱码
                # we use split to cut string, we need the last part
                # split() 会把字符串按空格切分，我们需要最后一部分
                encoded_string = line.strip().split(" ")[-1]

                print(f"[+] Found encoded string: {encoded_string}")

                # 4. [Key Step] decoding with Base64
                # 4. 【关键步骤】进行 Base64 解码
                # The base library of Python need bytes type, so we need to use .encode() transcript first, then use .decode() turn it back.
                # Python 的 base64 库需要字节(bytes)类型，所以要先 .encode() 转一下，解完再 .decode() 回来
                # ---------------------------------------------------------
                
                decoded_bytes = base64.b64decode(encoded_string)
                flag = decoded_bytes.decode('utf-8')
    
                # ---------------------------------------------------------

                # 5. print final result
                # 5. 打印最终结果
                print(f"[SUCCESS] The Flag is: {flag}") 
except FileNotFoundError:
    # If the file is missing, run this code instead of crashing
    print(f"[-] Error: the file '{filename}'was not found.")
    print("[-] Please make sure the file exists in the same folder.")