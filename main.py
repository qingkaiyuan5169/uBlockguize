from datetime import datetime
import urllib.request


def convert_url_domains_to_ublock(
    url="https://dfcloud.qzz.io/f/MJTE/fake.txt", output_file="yinhu.txt"
):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        print(f"正在从网络读取域名列表: {url} ...")
        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode("utf-8")

        lines = content.splitlines()
        rules = []

        for line in lines:
            domain = line.strip()
            # 过滤空行以及注释行（! 或 # 开头）
            if domain and not domain.startswith("!") and not domain.startswith("#"):
                # 避免重复添加 || 和 ^ 符号
                if not (domain.startswith("||") and domain.endswith("^")):
                    rule = f"||{domain}^"
                else:
                    rule = domain
                rules.append(rule)

        # 获取当前系统时间并格式化
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 写入目标文件 yinhu.txt
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write("! Title: 银狐木马监测\n")
            outfile.write(f"! Source: {url}\n")
            outfile.write(f"! Updated: {current_time}\n\n")
            outfile.write("\n".join(rules))

        print(
            f"转换成功！共处理 {len(rules)} 条域名规则，已保存至文件: {output_file}"
        )

    except Exception as e:
        print(f"读取或转换失败，错误信息: {e}")


if __name__ == "__main__":
    convert_url_domains_to_ublock()
