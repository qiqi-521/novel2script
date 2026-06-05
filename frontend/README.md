# Frontend

前端应用目录，负责小说输入、改编参数配置、结果预览与局部编辑交互。

## 本地开发

```powershell
npm install
npm run dev
```

开发服务默认通过 `/api` 代理到本地后端 `http://127.0.0.1:8000`，因此需要先启动 FastAPI 后端再测试生成功能。

如需连接其他后端地址，可在前端环境变量中配置：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## 可用脚本

- `npm run dev`：启动 Vite 开发服务。
- `npm run build`：执行 TypeScript 检查并构建生产包。
- `npm run preview`：本地预览生产构建结果。
