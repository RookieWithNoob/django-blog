from rest_framework import serializers
from .models import Article


# 创建序列化器类，回头会在视图中被调用
class ArticleModelSerializer(serializers.ModelSerializer):
    """
    创建一个ArticleModelSerializer用于序列化与反序列化。
    # """
    # url = serializers.HyperlinkedIdentityField(
    #     # view_name='article_detail',
    #     # lookup_field='id'
    # )
    author = serializers.StringRelatedField(label='作者')
    tag = serializers.StringRelatedField(label='标签')

    class Meta:
        # model 指明该序列化器处理的数据字段从模型类Article参考生成
        #
        # fields 指明该序列化器包含模型类中的哪些字段，'all'指明包含所有字段
        model = Article
        # fields = "__all__"
        fields = ("id", "title", 'views', 'author', 'attributes', 'tag', 'image_url')  # 也可指定字段