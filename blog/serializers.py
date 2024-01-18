from rest_framework.serializers import ModelSerializer

from blog.models import News, Portfolio, Comment, CommonAuthMixin


class NewsModelSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'image', 'title', 'description']


class PortfolioModelSerializer(CommonAuthMixin, ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['image', 'link']

    def create(self, validated_data):
        user = self.authenticate_user(self.context['request'])
        print('user:', user)
        print('user_id', user.id)
        validated_data['owner'] = user
        return super().create(validated_data)


class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name']
