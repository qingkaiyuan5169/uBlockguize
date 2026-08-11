import urllib.request
import urllib.error
from datetime import datetime

def convert_url_domains_to_ublock(
    url: str = "https://dfcloud.qzz.io/f/MJTE/fake.txt", 
    output_file: str = "yinhu.txt"
) -> None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        print(f"正在从网络读取域名列表: {url} ...")
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode("utf-8")

        lines = content.splitlines()
        rules = set()  # 使用 set() 自动处理去重

        for line in lines:
            domain = line.strip()
            
            # 过滤空行以及注释行
            if domain and not domain.startswith(("!", "#")):
                # 提取纯域名，防止源文件中有行内注释 (例如: "evil.com # 恶意域名")
                domain = domain.split()[0]
                
                # 避免重复添加 || 和 ^ 符号
                if not (domain.startswith("||") and domain.endswith("^")):
                    rule = f"||{domain}^"
                else:
                    rule = domain
                
                rules.add(rule)

        # 转换为排序后的列表，保证输出文件内容的稳定性
        sorted_rules = sorted(list(rules))
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 写入目标文件
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write("! Title: 银狐木马监测\n")
            outfile.write(f"! Source: {url}\n")
            outfile.write(f"! Updated: {current_time}\n")
            outfile.write(f"! Total Count: {len(sorted_rules)}\n\n")
            outfile.write("\n".join(sorted_rules))

        print(
            f"转换成功！共处理 {len(sorted_rules)} 条独立域名规则，已保存至文件: {output_file}"
        )

    except urllib.error.URLError as e:
        print(f"网络请求失败，请检查 URL 或网络连接: {e}")
    except Exception as e:
        print(f"读取或转换失败，错误信息: {e}")

if __name__ == "__main__":
    convert_url_domains_to_ublock()
