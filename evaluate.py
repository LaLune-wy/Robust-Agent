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


# 定义工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_bangumi",
            "description": "搜索番剧信息，根据标题查找番剧的详细信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "要搜索的番剧标题"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_music",
            "description": "搜索音乐信息，根据关键词查找歌曲的详细信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "要搜索的音乐关键词"
                    }
                },
                "required": ["keyword"]
            }
        }
    }
]

#data_path = '/root/autodl-tmp/data/input_data/fc_question/questions.json'
data_path = "/root/autodl-tmp/data/input_data/HEx-PHI/HEx-PHI.jsonl"
model_path = '/root/autodl-tmp/model/output_model'

import json
import openai
from openai import OpenAI

# 设置OpenAI客户端 - 直接使用本地模型路径
client = OpenAI(
    base_url=f"http://localhost:8000/v1",  # 假设本地模型服务运行在8000端口
    api_key="not-needed"  # 本地模型通常不需要API key
)

# 加载数据集
dataset = []
with open(data_path, 'r', encoding='utf-8') as f:
    #dataset = json.load(f)
    for line in f:
        dataset.append(json.loads(line))
        print(line)

# 处理每个问题
for i, item in enumerate(dataset):
    #question = item.get('question', '')
    question = item.get('instruction', '')
    
    try:
        # 调用模型进行回答
        response = client.chat.completions.create(
            model=model_path,  # 使用本地模型路径
            messages=[
                {"role": "system", "content": "你是一个专业的知识库助手，请根据用户的问题，从知识库中搜索相关信息，并返回最相关的答案。"},
                {"role": "user", "content": question}
            ],
            tools=tools,  # 使用预定义的工具列表
            tool_choice="auto"
        )
        
        # 提取回答内容
        # 检查是否调用了工具
        if response.choices[0].message.tool_calls:
            tool_calls = response.choices[0].message.tool_calls
            print(f"问题 {i+1}: '{question}' 调用了以下工具:")
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                print(f"  - 工具名称: {tool_name}")
                print(f"  - 工具参数: {tool_args}")
        else:
            print(f"问题 {i+1}: '{question}' 没有调用工具，直接回答")
        
        # 检查是否调用了工具，如果有则获取工具调用结果，否则使用模型直接回答
        if response.choices[0].message.tool_calls:
            # 如果有工具调用，需要获取工具调用的结果
            tool_calls = response.choices[0].message.tool_calls
            tool_results = []
            
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                # 根据工具名称调用相应的函数
                if tool_name == "search_bangumi":
                    result = search_bangumi(tool_args.get('title', ''))
                    tool_results.append(result)
                elif tool_name == "search_music":
                    result = search_music(tool_args.get('keyword', ''))
                    if result:
                        tool_results.append(result)
                    else:
                        tool_results.append("音乐搜索失败")
                else:
                    tool_results.append(f"未知工具: {tool_name}")

            # 将工具调用结果发送给模型进行最终回答
            messages = [
                {"role": "system", "content": "你是一个专业的知识库助手，请根据用户的问题和工具搜索结果，提供准确、完整的答案。"},
                {"role": "user", "content": question},
                {"role": "assistant", "content": f"我通过调用工具搜索到了信息：{'; '.join(tool_results)}"},
                {"role": "user", "content": f"请根据：{'; '.join(tool_results)}。回答问题：{question}。"}
            ]
            print(f"处理第 {i+1}个问题messages")
            print(messages)
            
            final_response = client.chat.completions.create(
                model=model_path,
                messages=messages
            )
            
            answer = final_response.choices[0].message.content
        else:
            # 如果没有调用工具，直接使用模型的回答
            answer = response.choices[0].message.content
        
        # 将回答添加到数据项中
        item['answer'] = answer
        print(f"处理第 {i+1}个问题answer")
        print(answer)
        
        print(f"处理第 {i+1} 个问题完成")
        
    except Exception as e:
        print(f"处理第 {i+1} 个问题时出错: {e}")
        item['answer'] = None

# 保存带有回答的数据
output_path = data_path.replace('.json', '_with_answers.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print(f"所有问题处理完成，结果已保存到: {output_path}")






