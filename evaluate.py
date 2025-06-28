import requests
import json

def search_bangumi(title):
    """
    向番剧搜索API发送请求并返回结果
    
    Args:
        title (str): 要搜索的番剧标题
    
    Returns:
        str: 格式化的番剧信息字符串
    """
    url = f"https://api.timelessq.com/bangumi?title={title}"
    
    try:
        # 发送GET请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析JSON格式
        result = response.json()
        
        # 提取第一条番剧信息
        if result and 'data' in result and len(result['data']) > 0:
            bangumi_info = result['data'][0]
            
            # 提取所需字段
            title = bangumi_info.get('title', '未知标题')
            type_info = bangumi_info.get('type', '未知类型')
            lang = bangumi_info.get('lang', '未知语言')
            official_site = bangumi_info.get('officialSite', '未知出品方')
            begin = bangumi_info.get('begin', '未知上映时间')
            
            # 组合成格式化的字符串
            formatted_info = f"标题: {title}\n类型：{type_info}\n语言：{lang}\n出品方：{official_site}\n上映时间：{begin}\n完结时间：{bangumi_info.get('end', '未知')}"
            
            return formatted_info
        else:
            return "未找到相关番剧信息"
        
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"
    except json.JSONDecodeError as e:
        return f"JSON解析失败: {e}"


def search_music(keyword):
    """
    向腾讯音乐搜索API发送请求并返回结果
    
    Args:
        keyword (str): 要搜索的音乐关键词
    
    Returns:
        dict: API返回的JSON格式数据
    """
    url = f"https://api.timelessq.com/music/tencent/search?keyword={keyword}"
    
    try:
        # 发送GET请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        
        # 解析JSON格式
        result = response.json()
        
        # 打印返回的JSON格式内容
        #print("API返回的JSON内容:")
        #print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 提取第一条歌曲信息
        if result and 'data' in result and 'list' in result['data'] and len(result['data']['list']) > 0:
            song_info = result['data']['list'][0]
            
            # 提取所需字段
            songname = song_info.get('songname', '未知歌曲')
            interval = song_info.get('interval', '未知时长')
            singer_name = song_info.get('singer', [{}])[0].get('name', '未知歌手') if song_info.get('singer') else '未知歌手'
            albumname = song_info.get('albumname', '未知专辑')
            
            # 组合成通顺的句子
            sentence = f"歌曲《{songname}》由{singer_name}演唱，收录在专辑《{albumname}》中，时长{interval}秒。"
            #print(sentence)
            return sentence
        else:
            return "未找到相关歌曲"
        
        #return result
        
    except requests.exceptions.RequestException as e:
        #print(f"请求失败: {e}")
        return None
    except json.JSONDecodeError as e:
        #print(f"JSON解析失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    # 测试函数
    '''
    keyword = "周杰伦"
    result = search_music(keyword)
    print(result)
    '''

    # 测试动漫查询功能
    keyword = "火影忍者"
    result = search_bangumi(keyword)
    print(f"搜索关键词: {keyword}")
    print(f"查询结果: {result}")


