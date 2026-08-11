import urllib.request
import urllib.error
from datetime import datetime
from typing import List

def convert_url_domains_to_ublock(output_file: str = "yinhu.txt") -> None:
    # 1. 定义多镜像 URL 列表
    urls: List[str] = [
        "https://deepformat.top/yh/fake.txt",          # 主域名
        "https://fyh.johnnyblog.top/fake.txt",
        "https://dfcloud.qzz.io/f/MJTE/fake.txt",
        "http://anti-silverfox.wpidc.top/fake.txt",
        "https://cloud.mcnan.top/fake.txt",
        "https://sysbbs.cn/fake.txt"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    content = None
    successful_url = ""

    # 2. 轮询尝试获取内容
    for url in urls:
        print(f"🔄 尝试从镜像获取数据: {url} ...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status == 200:
                    temp_content = response.read().decode("utf-8")
                    # 确保获取到的内容不是空文件
                    if temp_content.strip(): 
                        content = temp_content
                        successful_url = url
                        print(f"✅ 成功从 {url} 获取数据！")
                        break  # 只要成功一个，立刻终止循环
                    else:
                        print(f"⚠️ {url} 返回了空内容，继续尝试下一个镜像...")
                        
        except urllib.error.URLError as e:
            # e.reason 可能不存在，这里做个安全获取
            error_msg = getattr(e, 'reason', e)
            print(f"❌ 请求失败 {url}: {error_msg}")
        except Exception as e:
            print(f"❌ 未知错误 {url}: {e}")

    # 3. 检查是否所有链接都失败
    if not content:
        print("🚨 所有镜像链接均获取失败或内容为空，程序终止。")
        return

    # 4. 解析和转换规则
    try:
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
        
        # 增加一道防线：确保解析出了有效的规则
        if not sorted_rules:
            print("🚨 成功下载文件，但未解析出任何有效的域名规则，程序终止。")
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 5. 写入目标文件
        with open(output_file, "w", encoding="utf-8") as outfile:
            outfile.write("! Title: 银狐木马监测\n")
            outfile.write(f"! Source: {successful_url}\n")  # 记录这次成功获取的来源
            outfile.write(f"! Updated: {current_time}\n")
            outfile.write(f"! Total Count: {len(sorted_rules)}\n\n")
            outfile.write("\n".join(sorted_rules))

        print(f"🎉 转换成功！共处理 {len(sorted_rules)} 条独立域名规则，已保存至文件: {output_file}")

    except Exception as e:
        print(f"读取或转换失败，错误信息: {e}")

if __name__ == "__main__":
    convert_url_domains_to_ublock()
