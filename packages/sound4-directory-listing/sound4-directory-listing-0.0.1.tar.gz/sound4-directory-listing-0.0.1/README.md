
<div align="center">
  <img src="https://blogs.cappriciosec.com/uploaders/sound4-directory-listing-tool.png" alt="logo">
</div>


## Badges



[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![PyPI - Version](https://img.shields.io/pypi/v/sound4-directory-listing)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sound4-directory-listing)
![GitHub all releases](https://img.shields.io/github/downloads/Cappricio-Securities/sound4-directory-listing/total)
<a href="https://github.com/Cappricio-Securities/CVE-2023-27524/releases/"><img src="https://img.shields.io/github/release/Cappricio-Securities/sound4-directory-listing"></a>![Profile_view](https://komarev.com/ghpvc/?username=Cappricio-Securities&label=Profile%20views&color=0e75b6&style=flat)
[![Follow Twitter](https://img.shields.io/twitter/follow/cappricio_sec?style=social)](https://twitter.com/cappricio_sec)
<p align="center">

<p align="center">







## License

[MIT](https://choosealicense.com/licenses/mit/)



## Installation 

1. Install Python3 and pip [Instructions Here](https://www.python.org/downloads/) (If you can't figure this out, you shouldn't really be using this)

   - Install via pip
     - ```bash
          pip install sound4-directory-listing 
        ```
   - Run bellow command to check
     - `sound4-directory-listing -h`

## Configurations 
2. We integrated with the Telegram API to receive instant notifications for vulnerability detection.
   
   - Telegram Notification
     - ```bash
          sound4-directory-listing --chatid <YourTelegramChatID>
        ```
   - Open your telegram and search for [`@CappricioSecuritiesTools_bot`](https://web.telegram.org/k/#@CappricioSecuritiesTools_bot) and click start

## Usages 
3. This tool has multiple use cases.
   
   - To Check Single URL
     - ```bash
          sound4-directory-listing -u http://example.com 
        ```
   - To Check List of URL 
      - ```bash
          sound4-directory-listing -i urls.txt 
        ```
   - Save output into TXT file
      - ```bash
          sound4-directory-listing -i urls.txt -o out.txt
        ```
   - Want to Learn about [`sound4-directory-listing`](https://blogs.cappriciosec.com/cve/187/%22Sound4%20Directory%20Listing%22%20and%20Potential%20File%20Write%20Vulnerability)? Then Type Below command
      - ```bash
         sound4-directory-listing -b
        ```
     
<p align="center">
  <b>🚨 Disclaimer</b>
  
</p>
<p align="center">
<b>This tool is created for security bug identification and assistance; Cappricio Securities is not liable for any illegal use. 
  Use responsibly within legal and ethical boundaries. 🔐🛡️</b></p>


## Working PoC Video

[![asciicast](https://blogs.cappriciosec.com/uploaders/Screenshot%202024-06-17%20at%204.08.48%20PM.png)](https://asciinema.org/a/XPDWZXoq966q1JVMaFSq5pmqw)




## Help menu

#### Get all items

```bash
👋 Hey Hacker
                                                                             v1.0
                               ____ __            ___                __                         __           __
   _________  __  ______  ____/ / // /       ____/ (_)_______  _____/ /_____  _______  __      / /__  ____ _/ /_______
  / ___/ __ \/ / / / __ \/ __  / // /_______/ __  / / ___/ _ \/ ___/ __/ __ \/ ___/ / / /_____/ / _ \/ __ `/ //_/ ___/
 (__  ) /_/ / /_/ / / / / /_/ /__  __/_____/ /_/ / / /  /  __/ /__/ /_/ /_/ / /  / /_/ /_____/ /  __/ /_/ / ,< (__  )
/____/\____/\__,_/_/ /_/\__,_/  /_/        \__,_/_/_/   \___/\___/\__/\____/_/   \__, /     /_/\___/\__,_/_/|_/____/
                                                                                /____/

                              Developed By https://cappriciosec.com


sound4-directory-listing : Bug scanner for WebPentesters and Bugbounty Hunters

$ sound4-directory-listing [option]

Usage: sound4-directory-listing [options]
```


| Argument | Type     | Description                | Examples |
| :-------- | :------- | :------------------------- | :------------------------- |
| `-u` | `--url` | URL to scan | sound4-directory-listing -u https://target.com |
| `-i` | `--input` | filename Read input from txt  | sound4-directory-listing -i target.txt | 
| `-o` | `--output` | filename Write output in txt file | sound4-directory-listing -i target.txt -o output.txt |
| `-c` | `--chatid` | Creating Telegram Notification | sound4-directory-listing --chatid yourid |
| `-b` | `--blog` | To Read about sound4-directory-listing Bug | sound4-directory-listing -b |
| `-h` | `--help` | Help Menu | sound4-directory-listing -h |



## 🔗 Links
[![Website](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://cappriciosec.com/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/karthikeyan--v/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/karthithehacker)



## Author

- [@karthithehacker](https://github.com/karthi-the-hacker/)



## Feedback

If you have any feedback, please reach out to us at contact@karthithehacker.com