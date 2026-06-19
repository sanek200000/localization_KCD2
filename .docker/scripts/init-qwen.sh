#!/bin/bash

# Функция для инициализации Qwen CLI
init_qwen_cli() {
  if [ -n "$QWEN_API_KEY" ]; then
    echo "🔑 Настройка Qwen Code CLI..."

    # Создаем/обновляем конфиг
    mkdir -p ~/.qwen-code
    cat >~/.qwen-code/config.json <<EOF
{
    "api_key": "$QWEN_API_KEY",
    "base_url": "${QWEN_BASE_URL:-https://dashscope.aliyuncs.com/compatible-mode/v1}",
    "model": "${QWEN_MODEL:-qwen-plus}",
    "timeout": 120
}
EOF

    # Проверяем установку
    if command -v qwen-code &>/dev/null; then
      echo "✅ Qwen Code CLI установлен: $(qwen-code --version)"
      echo "💡 Используйте: qwen \"ваш запрос\" или qwen --help"
    else
      echo "⚠️  qwen-code не найден в PATH"
    fi
  else
    echo "⚠️  QWEN_API_KEY не установлен. Добавьте его в .env файл."
    echo "📖 Получите ключ: https://dashscope.aliyun.com/"
  fi
}

# Запускаем инициализацию только если конфиг пустой или не существует
if [ ! -f ~/.qwen-code/config.json ] || [ ! -s ~/.qwen-code/config.json ]; then
  init_qwen_cli
fi
