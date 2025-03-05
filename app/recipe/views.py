# 如果使用 drf-spectacular 來自動生成 API 文檔，那麼以下導入是必須的

from drf_spectacular.utils import (
    extend_schema_view,  # 用來對整個 ViewSet 自定義 schema (API 文檔)
    extend_schema,  # 用來對具體的 API 端點自定義 schema
    OpenApiParameter,  # 用來定義 API 的查詢參數
    OpenApiTypes,  # 用來定義查詢參數的類型（如整數、字符串等）
)

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication # 用於 Token 驗證
from rest_framework.permissions import IsAuthenticated  # 用於權限控制，確保只有已驗證用戶可訪問
from rest_framework.decorators import action  # 用於自定義 ViewSet 中的非標準行為（例如上傳圖片）
from rest_framework.response import Response  
from core.models import Recipe, Tag, Ingredient
from . import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication 

# 用於處理標籤或食材相關的基本操作，繼承了列表、更新、刪除等操作
class BaseAttrRecipeViewSet(mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet,
                            mixins.DestroyModelMixin):
    """重構 Class 讓 TagViewSet 跟 IngredientViewSet 繼承"""

    authentication_classes = [TokenAuthentication, ]  # 設定 Token 認證方式
    permission_classes = [IsAuthenticated, ]  # 設定權限，僅認證用戶可訪問

    def get_queryset(self):
        """
        過濾只返回當前用戶創建的數據，並根據是否分配給食譜進行進一步過濾
        """
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()  # 根據名稱排序並去重

class RecipeViewSet(viewsets.ModelViewSet):
    """處理食譜相關的 CRUD 操作"""
    serializer_class = serializers.RecipeDetailSerializer  # 默認使用詳細的序列化器
    queryset = Recipe.objects.all()  # 查詢所有食譜
    authentication_classes = [TokenAuthentication,JWTAuthentication]  # Token 認證
    permission_classes = [IsAuthenticated]  # 僅認證用戶可訪問

    def _params_to_ints(self, qs):
        """將逗號分隔的字符串轉換為整數列表，方便過濾條件使用
        input="1,2,3,4,5"
        result=[1,2,3,4,5] ->List[int]
        """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """根據當前用戶以及查詢參數過濾並檢索食譜"""
        tags = self.request.query_params.get('tags')  # 獲取查詢參數中的標籤
        ingredients = self.request.query_params.get('ingredients')  # 獲取查詢參數中的食材
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)  # 轉換標籤 ID 列表
            queryset = queryset.filter(tags__id__in=tag_ids)  # 根據標籤過濾
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)  # 轉換食材 ID 列表
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)  # 根據食材過濾

        return queryset.filter(
            user=self.request.user  # 只返回當前用戶的食譜
        ).order_by('-id').distinct()  # 根據 ID 排序並去重

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """自動將當前用戶設置為創建食譜的擁有者"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """上傳圖片功能的自定義 action"""
        recipe = self.get_object()  # 獲取當前操作的食譜對象
        serializer = self.get_serializer(recipe, data=request.data)  # 使用圖片序列化器

        if serializer.is_valid():
            serializer.save()  # 保存圖片
            return Response(serializer.data, status=status.HTTP_200_OK)  # 返回成功響應

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 返回錯誤響應

class TagViewSet(BaseAttrRecipeViewSet):
    """處理標籤的 CRUD 操作，繼承了 BaseAttrRecipeViewSet 的基礎邏輯"""
    serializer_class = serializers.TagSerializer  # 使用標籤序列化器
    queryset = Tag.objects.all()  # 查詢所有標籤

class IngredientViewSet(BaseAttrRecipeViewSet):
    serializer_class = serializers.IngredientSerializer  # 使用食材序列化器
    queryset = Ingredient.objects.all()  # 查詢所有食材
