/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI API地址
  apiEndpoint: 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
  
  // API Key (从系统环境变量DASHSCOPE_API_KEY读取)
  apiKey: import.meta.env.DASHSCOPE_API_KEY || '',
  
  // 使用的模型
  model: 'qwen3.6-max-preview'
}
