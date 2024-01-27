import os

def install_modules():
    # Cài đặt các module Node.js
    os.system('npm install axios cheerio gradient-string colors random-useragent')

    # Cài đặt module Python
    os.system('pip install colored')

    print("Cài đặt thành công các module.")

if __name__ == "__main__":
    install_modules()
