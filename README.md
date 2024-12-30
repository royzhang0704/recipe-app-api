# recipe-app-api
Recipe API Project
食譜管理 API 系統。基於 Django REST Framework 開發的 RESTful API。
技術棧

Python
Django / Django REST Framework
Docker / Docker-Compose
GitHub Actions
AWS EC2
Test Driven Development
Authentication & Permissions

特點

完整的 RESTful API 設計
TDD 開發流程，確保代碼質量
Docker 容器化部署
CI/CD 自動化流程
用戶認證和權限管理
AWS 雲端服務部署

功能

User 認證系統
Recipe CRUD 操作
基於權限的訪問控制
API 文檔

本地開發設置

Clone 專案:

bashCopygit clone <your-repo-url>
cd recipe-api

啟動 Docker:

bashCopydocker-compose up

運行測試:

bashCopydocker-compose run --rm app sh -c "python manage.py test"
API 端點

/api/user/ - 用戶管理
/api/recipe/ - 食譜管理

GET: 獲取食譜列表
POST: 創建新食譜
PUT/PATCH: 更新食譜
DELETE: 刪除食譜



GitHub Actions 配置

自動運行 linting
自動運行單元測試
確保代碼質量

部署
專案使用 Docker 容器化並部署在 AWS EC2 上：

配置 AWS 設置
設置 Docker 環境
部署應用

使用的工具和服務

Docker Hub
GitHub Actions
AWS EC2

代碼質量保證

Unit Testing
Code Linting
Test Coverage
持續整合檢查
